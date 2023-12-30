import json
import os
import sys
import time
import requests
from hashlib import sha256
from typing import Any, Dict, List, Optional, Tuple
from credfind.utils import extract_inputs
from credfind.objects import Input, InputList, InputType
from playwright.sync_api import sync_playwright, TimeoutError, Page

from credgen.utils import creds_from_input
from phishflood.rabbit import RabbitConsumer
from config import general_conf

SCREENSHOT_I = 0
Actions = List[Dict[str, Any]]


def screenshot(page: Page):
    global SCREENSHOT_I
    SCREENSHOT_I += 1
    page.screenshot(path=f"samples/{SCREENSHOT_I}.png")


def hash_inputs(inputs: List[Input]) -> str:
    """Returns a unique string identifying the inputs in the website"""
    return sha256("".join([str(i) for i in inputs]).encode()).hexdigest()


def flood_page(
    page: Page, last_hash: str = ""
) -> Optional[Tuple[str, InputList, Actions]]:
    """Returns a unique string identifying the inputs in the website"""

    # Get a first screenshot
    page.wait_for_timeout(3000)
    screenshot(page)

    # Get html and extract the inputs
    html = page.content()
    res = extract_inputs(html)
    if len(res) > 0:
        fi, form, inputs = res[0]
    else:
        print("No inputs found")
        return None

    # Calculate the hash of the inputs
    input_hash = hash_inputs(inputs)
    print(f"Input hash: {input_hash}")
    if input_hash == last_hash:
        print("Already flooded this page")
        return None

    form_locator = page.locator(f"form >> nth = {form.meta_id}")

    actions = []

    # Generate the fake credentials for each form and each input
    for inp in inputs:
        FILLABLE_INPUTS = [
            InputType.TEXT,
            InputType.EMAIL,
            InputType.PASSWORD,
            InputType.NUMBER,
            InputType.TEL,
            InputType.SEARCH,
            InputType.URL,
        ]
        if inp.type_ in FILLABLE_INPUTS:
            text = creds_from_input(inp)

            # Find the inputs again and fill them
            print(f"input >> nth = {inp.meta_id}")
            try:
                input_locator = form_locator.locator(f"input >> nth = {inp.meta_id}")
                input_locator.click(timeout=100)
                input_locator.type(text)

                actions.append(
                    {
                        "action": "fill",
                        "form": form.meta_id,
                        "input": inp.meta_id,
                        "value": text,
                        "status": "success",
                    }
                )
                print(f"\t{inp} -> {text}")
            except TimeoutError:
                actions.append(
                    {
                        "action": "fill",
                        "form": form.meta_id,
                        "input": inp.meta_id,
                        "value": text,
                        "status": "failed",
                    }
                )
                print(f"Failed to find input {inp}")
        else:
            actions.append(
                {
                    "action": "ignore",
                    "form": form.meta_id,
                    "input": inp.meta_id,
                    "value": "",
                    "status": "success",
                }
            )
            print(f"\t{inp} -> Not filling this one")

    # Get a second screenshot after filling information
    screenshot(page)

    # Submit the form and continue
    form_locator.press("Enter")

    return input_hash, res, actions


def extract_inputs_from_url(url: str) -> Optional[Dict[str, Any]]:
    """Given a URL, starts a browser, visits the page, extracts the html and calls extract_inputs for that html"""
    with sync_playwright() as p:
        # Setup the browser
        browser = p.chromium.launch()
        page = browser.new_page()

        # Visit the site
        print(f"Visiting {url}")
        try:
            res = page.goto(url)
            if res is None:
                print("Failed to get response from page")
                return None
        except:
            print("Failed to visit page")
            return None
        print(f"Result: {res.status}")

        forms = []
        actions = []

        # Flood the initial page
        res = flood_page(page)
        if res is None:
            return None
        else:
            uid, inputs, acts = res
            actions += acts
            for _, f, i in inputs:
                d = f.to_dict()
                d["inputs"] = [x.to_dict() for x in i]
                forms.append(d)

        # Flood the next 5 pages too
        for _ in range(5):
            res = flood_page(page, uid)
            if res is None:
                print("No more forms to flood")
                break
            else:
                new_uid, inputs, acts = res
                actions += acts
                for _, f, i in inputs:
                    d = f.to_dict()
                    d["inputs"] = [x.to_dict() for x in i]
                    forms.append(d)

                if new_uid is None:
                    break
                else:
                    uid = new_uid

        # Get a screenshot after submitting the form
        page.wait_for_timeout(1000)
        screenshot(page)

        # Get a final screenshot after waiting for 5 seconds
        page.wait_for_timeout(5000)
        screenshot(page)

        # Generate a gif from the files
        os.system(
            'ffmpeg -y -framerate 1 -i samples/%d.png -vf "format=yuv420p" samples/output.gif'
        )
        os.system("rm -f samples/*.png")

        auth_headers = {"Authorization": f"Token {general_conf.TOKEN}"}

        phishing_id = sha256(url.encode()).hexdigest()

        # Post forms and inputs to the API
        for form in forms:
            raw_form = {
                "phishing": phishing_id,
                "meta_id": form["meta_id"],
                "html_id": form["id"],
                "html_action": form["action"],
                "html_method": form["method"],
                "html_type": form["type"],
            }
            
            print(f"Uploading form {raw_form}")
            res = requests.post(
                general_conf.API_URL + "form/",
                json=raw_form,
                headers=auth_headers,
            )
            print(f"Uploaded form: {res.status_code}, {res.text}")

            for input_ in form["inputs"]:
                print(f"Uploading input {input_}")
                res = requests.post(
                    general_conf.API_URL + "input/",
                    json={
                        "form": f"{phishing_id}-{form['meta_id']}",
                        "meta_id": input_["meta_id"],
                        "html_id": input_["id"],
                        "html_name": input_["name"],
                        "html_placeholder": input_["placeholder"],
                        "html_type": input_["type"],
                    },
                    headers=auth_headers,
                )
                print(f"Uploaded input: {res.status_code}, {res.text}")

        # Post actions to the API
        for action in actions:
            print(f"Uploading action {action}")
            res = requests.post(
                general_conf.API_URL + "action/",
                json={
                    "phishing": phishing_id,
                    "form": f"{phishing_id}-{action['form']}",
                    "input": f"{phishing_id}-{action['form']}-{action['input']}",
                    "action": action["action"],
                    "value": action["value"],
                    "status": action["status"],
                },
                headers=auth_headers,
            )
            print(f"Uploaded action: {res.status_code}, {res.text}")

        return {
            "url": url,
            "html": "...",  # page.content(),
            "forms": forms,
            "actions": actions,
        }


def rabbit_callback(body):
    global SCREENSHOT_I
    print(f"Received {body} from rabbit")
    try:
        body = json.loads(body.decode())
        url = body["url"]
        print(f"Extracting inputs from {url}")
        data = extract_inputs_from_url(body["url"])
        os.rename("samples/output.gif", f"samples/{sha256(url.encode()).hexdigest()}.gif")
        print(f"Done with {url}")
    except:
        pass
    
    # Reset screenshot counter
    SCREENSHOT_I = 0


if __name__ == "__main__":
    if sys.argv[1] == "worker":
        print("Starting worker...")

        while True:
            try:
                print("Starting rabbit consumer")
                rc = RabbitConsumer(rabbit_callback)
                rc.run()
            except:
                print("Failed to start rabbit consumer")
                time.sleep(5)
    else:
        print(f"Analyzing url {sys.argv[1]}...")
        res = extract_inputs_from_url(sys.argv[1])

        print("Saving results to sample/info.json")
        with open("samples/info.json", "w") as f:
            json.dump(res, f, indent=4)
        print("Done")

from hashlib import sha256
import json
import os
import sys
from typing import Any, Dict, Generator, List, Optional, Tuple
from credfind.utils import extract_inputs
from credfind.objects import Input, InputList, InputType
from playwright.sync_api import sync_playwright, TimeoutError, Page

from credgen.utils import creds_from_input

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

        return {
            "url": url,
            # "html": page.content(),
            "forms": forms,
            "actions": actions,
        }


if __name__ == "__main__":
    info = extract_inputs_from_url(sys.argv[1])
    with open("samples/info.json", "w") as f:
        json.dump(info, f)

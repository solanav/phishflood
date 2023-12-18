import os
import sys
from typing import List
from credfind.utils import extract_inputs
from credfind.objects import Input, InputType
from playwright.sync_api import sync_playwright

from credgen.utils import creds_from_input

def extract_inputs_from_url(url: str) -> List[Input]:
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
                return []
        except:
            print("Failed to visit page")
            return []
        print(f"Result: {res.status}")
        
        # Get a first screenshot
        page.wait_for_timeout(3000)
        page.screenshot(path="samples/1.png")
        
        # Get html and extract the inputs
        html = page.content()
        form, inputs = extract_inputs(html)
        form_locator = page.locator(f"form >> nth = {form.meta_id}")
        
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
                input_locator = form_locator.locator(f"input >> nth = {inp.meta_id}")
                # input_locator.focus()
                input_locator.click()
                input_locator.type(text)

                print(f"\t{inp} -> {text}")
            else:
                print(f"\t{inp} -> Not filling this one")
        
        # Get a second screenshot after filling information 
        page.screenshot(path="samples/2.png")
        
        # Submit the form and continue
        form_locator.press("Enter")
        
        # Get a screenshot after submitting the form
        page.wait_for_timeout(1000)
        page.screenshot(path="samples/3.png")
        
        # Get a final screenshot after waiting for 5 seconds
        page.wait_for_timeout(5000)
        page.screenshot(path="samples/4.png")
        
        # Generate a gif from the files
        os.system('ffmpeg -framerate 1 -i samples/%d.png -vf "format=yuv420p" samples/output.gif')
        
        return []
    
if __name__ == "__main__":
    inputs = extract_inputs_from_url(sys.argv[1])
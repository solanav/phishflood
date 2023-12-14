from typing import List
from credfind.utils import extract_inputs
from credfind.objects import Form, Input, InputType
from playwright.sync_api import sync_playwright

from credgen.utils import creds_from_input

def extract_inputs_from_url(url: str) -> List[Input]:
    """Given a URL, starts a browser, visits the page, extracts the html and calls extract_inputs for that html"""
    with sync_playwright() as p:
        # Setup the browser
        browser = p.chromium.launch(headless=False)
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
        page.screenshot(path="samples/01.png")
        
        # Get html and extract the inputs
        html = page.content()
        form, inputs = extract_inputs(html)
        form_locator = page.locator(f"form >> nth = {form.meta_id}")
        
        # Generate the fake credentials for each form and each input
        for inp in inputs:
            if inp.type_ != InputType.HIDDEN:
                text = creds_from_input(inp)
                
                # Find the inputs again and fill them
                input_locator = form_locator.locator(f"input >> nth = {inp.meta_id}")
                input_locator.fill(text)

                print(f"\t{inp} -> {text}")
            else:
                print(f"\t{inp} -> Not filling this one")
        
        # Get a second screenshot after filling information 
        page.screenshot(path="samples/02.png")
        
        # Submit the form and continue
        form_locator.press("Enter")
        
        # Get a first screenshot
        page.wait_for_timeout(3000)
        page.screenshot(path="samples/03.png")
        page.wait_for_timeout(3000)
        
        return []
    
if __name__ == "__main__":
    inputs = extract_inputs_from_url("https://de-02.phishinganalyzer.com/")
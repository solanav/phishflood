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
        except:
            print("Failed to visit page")
            return []
        print(f"Result: {res.status}")
        
        # Get a first screenshot
        page.wait_for_timeout(3000)
        page.screenshot(path="samples/01.png")
        
        # Get html and extract the inputs
        html = page.content()
        inputs = extract_inputs(html)
        
        # Generate the fake credentials for each form and each input
        for form, inps in inputs:
            print(f"Generating for {form}")
            for inp in inps:
                if inp.type_ != InputType.HIDDEN:
                    text = creds_from_input(inp)
                    print(f"\t{inp} -> {text}")
                else:
                    print(f"\t{inp} -> Not filling this one")
            
        return inputs
    
if __name__ == "__main__":
    inputs = extract_inputs_from_url("https://de-02.phishinganalyzer.com/")
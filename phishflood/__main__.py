from pprint import pprint
from typing import List
from credfind.utils import extract_inputs
from credfind.objects import Input
from playwright.sync_api import sync_playwright
from base64 import b64encode
from hashlib import sha256


def extract_inputs_from_url(url: str) -> List[Input]:
    """Given a URL, starts a browser, visits the page, extracts the html and calls extract_inputs for that html"""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        print(f"Visiting {url}")
        try:
            res = page.goto(url)
        except:
            print("Failed to visit page")
            return []
        print(f"Result: {res.status}")
        
        page.screenshot(path="example.png")
        
        html = page.content()
        
        # Save page content for future use
        fname = sha256(url.encode()).hexdigest()
        with open(f"pages/{fname}.html", "w") as f:
            f.write(html)
        
        inputs = extract_inputs(html)
        
        return inputs
    
if __name__ == "__main__":
    with open("urls.txt") as f:
        for url in f.read().splitlines():
            inputs = extract_inputs_from_url(url)
            pprint(inputs)
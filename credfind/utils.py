from bs4 import BeautifulSoup
from typing import List, Tuple
from credfind.objects import Form, Input


def extract_inputs(html: str) -> List[Tuple[Form, Input]]:
    """Takes a string of html and extracts all forms and inputs"""
    soup = BeautifulSoup(html, "html.parser")
    
    print("Finding all forms in the page")
    forms = soup.find_all("form")
    print(f"Found {len(forms)} forms")

    inputs = []
    for f in forms:
        form = Form.from_tag(f)
        form_inputs = [Input.from_tag(tag) for tag in f.find_all("input")]
        inputs.append((form, form_inputs))
        print(f"Found {len(form_inputs)} inputs inside form")
    
    return inputs
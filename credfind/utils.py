from bs4 import BeautifulSoup
from typing import List, Tuple
from credfind.objects import Form, Input

def extract_inputs(html: str) -> Tuple[Form, List[Input]]:
    """Given an HTML page, returns a list of inputs"""
    soup = BeautifulSoup(html, "html.parser")
    
    print("Finding all forms in the page")
    forms = soup.find_all("form")
    print(f"Found {len(forms)} forms")

    inputs = []
    for fmid, f in enumerate(forms):
        form = Form.from_tag(f, fmid)
        form_inputs = [Input.from_tag(tag, imid) for imid, tag in enumerate(f.find_all("input"))]
        inputs.append((form, form_inputs))
        print(f"Found {len(form_inputs)} inputs inside form")
    
    if len(inputs) > 1:
        return inputs[-1]    
    
    return inputs[0]
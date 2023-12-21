from bs4 import BeautifulSoup
from typing import List
from credfind.objects import Form, Input, InputList, InputType

FILLABLE_INPUTS = [
    InputType.TEXT,
    InputType.EMAIL,
    InputType.PASSWORD,
    InputType.NUMBER,
    InputType.TEL,
    InputType.SEARCH,
    InputType.URL,
]


def count_fillable_inputs(inputs: List[Input]) -> int:
    """Returns the number of fillable inputs in a list of inputs"""
    return len([i for i in inputs if i.type_ in FILLABLE_INPUTS])


def extract_inputs(html: str) -> InputList:
    """Given an HTML page, returns a list of inputs or None if nothing was found"""
    soup = BeautifulSoup(html, "html.parser")

    print("Finding all forms in the page")
    forms = soup.find_all("form")
    print(f"Found {len(forms)} forms")

    if len(forms) == 0:
        return []

    inputs = []
    for fmid, f in enumerate(forms):
        form = Form.from_tag(f, fmid)
        form_inputs = [
            Input.from_tag(tag, imid) for imid, tag in enumerate(f.find_all("input"))
        ]
        fi = count_fillable_inputs(form_inputs)
        inputs.append((fi, form, form_inputs))
        print(f"Found {len(form_inputs)} inputs inside form")

    if len(forms) == 0:
        return []
    elif len(inputs) > 1:
        inputs.sort(key=lambda x: x[0], reverse=True)

    return inputs

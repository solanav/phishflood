from credfind.utils import extract_inputs


def test_extract_inputs():
    with open("pages/bbva_generic.html", "r") as f:
        html = f.read()

    res = extract_inputs(html)
    inputs = res[0][2]

    assert len(res) == 1
    assert len(inputs) == 4

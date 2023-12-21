class TestCredfind(object):
    def test_extract_inputs(self):
        from credfind.utils import extract_inputs
        from credfind.objects import Form, Input, InputType

        with open("pages/bbva_generic.html", "r") as f:
            html = f.read()

        _, inputs = extract_inputs(html)

        assert len(inputs) == 4

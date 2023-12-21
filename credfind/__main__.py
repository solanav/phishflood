import sys

from credfind.utils import extract_inputs

if __name__ == "__main__":
    html_file = sys.argv[1]

    with open(html_file, "r") as f:
        print(f"Extracting inputs from HTML {html_file}")
        form, inputs = extract_inputs(f.read())

        for inp in inputs:
            print(inp)

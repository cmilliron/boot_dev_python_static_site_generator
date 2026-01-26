
def extract_title(markdown):
    lines_of_text = markdown.split("\n")
    for line in lines_of_text:
        if line.startswith("# "):
            return line[2:]
    raise Exception("No Header")

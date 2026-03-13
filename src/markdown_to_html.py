from block_helper_functions import markdown_to_html_node
from pathlib import Path


def extract_title(markdown):
    lines_of_text = markdown.split("\n")
    for line in lines_of_text:
        if line.startswith("# "):
            return line[2:]
    raise Exception("No Header")

def generate_page(from_path, template_path, dest_path):

    # TODO Print a message like "Generating page from from_path to dest_path using template_path".
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # TODO Read the markdown file at from_path and store the contents in a variable.
    source_content = ""
    with open(from_path, "r") as file:
        source_content = file.read()

    # TODO Read the template file at template_path and store the contents in a variable.
    template_content = ""
    with open(template_path, "r") as file:
        template_content = file.read()

    # TODO Use your markdown_to_html_node function and .to_html() method to convert the markdown file to an HTML string.
    html = markdown_to_html_node(source_content).to_html()

    # TODO Use the extract_title function to grab the title of the page.
    page_title = extract_title(source_content)

    # TODO Replace the {{ Title }} and {{ Content }} placeholders in the template with the HTML and title you generated.
    page = template_content.replace("{{ Title }}", page_title)
    page = template_content.replace("{{ Content }}", html)
    # print(page)

    # TODO Write the new full HTML page to a file at dest_path. Be sure to create any necessary directories if they don't exist.
    # source_file = Path(from_path)
    # rel_path = source_file.relative_to()
    dest_file = Path(dest_path)
    dest_file.parent.mkdir(parents=True, exist_ok=True)

    with open(dest_file, "w") as file:
        file.write(page)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    

if __name__ == "__main__":
    generate_page("content/index.md", "template.html", "public/test/test.html")
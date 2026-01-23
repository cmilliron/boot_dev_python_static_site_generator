from rich import print


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    processed_blocks = [item.strip() for item in blocks]
    cleaned_blocks = [item for item in processed_blocks if len(item) > 0]
    return cleaned_blocks


if __name__ == "__main__":
    text = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
    print(markdown_to_blocks(text))

    md = "Only one block\n\n\n"
    print(markdown_to_blocks(md))

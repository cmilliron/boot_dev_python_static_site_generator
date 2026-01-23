from rich import print
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_is_header(block):
    if block.startswith('#') or \
        block.startswith('##') or \
        block.startswith('###') or \
        block.startswith('####') or \
        block.startswith('#####') or \
        block.startswith('######'):
        return True
    else:
        return False


def block_is_code(block):
    if block.startswith("```"):
        return True
    return False


def block_is_quote(block):
    lines = block.split("\n")
    for line in lines:
        if not line.startswith(">"):
            return False
    return True


def block_is_unordered_list(block):
    lines = block.split("\n")
    for line in lines:
        if not line.startswith("-"):
            return False
    return True


def block_is_ordered_list(block):
    lines = block.split("\n")
    for i, line in enumerate(lines):
        if not line.startswith(f"{i}."):
            return False
    return True


def block_to_block_type(block):
    if block_is_header(block):
        return BlockType.HEADING
    if block_is_code(block):
        return BlockType.CODE
    if block_is_quote(block):
        return BlockType.QUOTE
    if block_is_unordered_list(block):
        return BlockType.UNORDERED_LIST
    if block_is_ordered_list(block):
        return BlockType.ORDERED_LIST 
    return BlockType.PARAGRAPH


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

from enum import Enum
from node_type_html import HTMLNode, ParentNode, LeafNode
from text_to_node import text_to_textnodes
from textnode_to_htmlnode import text_node_to_html_node
from node_type_text import TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_is_header(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
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
        if not line.startswith(f"{i+1}."):
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


def create_inline_html_nodes_from_text(text):
    # create text nodes from text
    inline_text_nodes = text_to_textnodes(text)
    html_nodes = [text_node_to_html_node(node) for node in inline_text_nodes]
    return html_nodes


def create_unordered_list_html_node(block: str):
    list_items = block.split("\n")
    print(list_items)
    processed_list_items = [ParentNode(tag="li", children=create_inline_html_nodes_from_text(item[2:])) for item in list_items]
    print(processed_list_items)
    # list_items_html_nodes = [ParentNode(tag="li", children=processed_list_items)]
    # print(list_items_html_nodes)
    html_node = ParentNode(tag="ul", children=processed_list_items)
    print(html_node)
    return html_node


def create_ordered_list_html_node(block: str):
    list_items = block.split("\n")
    processed_list_items = [ParentNode(tag="li", children=create_inline_html_nodes_from_text(item[3:])) for item in list_items]
    # list_items_html_nodes = [ParentNode(tag="li", children=processed_list_items)]
    html_node = ParentNode(tag="ol", children=processed_list_items)
    return html_node


def create_blockquote_html_node(block: str):
    process_block = " ".join(block.replace("> ", "").split("\n"))
    processed_html_node = create_inline_html_nodes_from_text(process_block)
    html_node = ParentNode(tag="blockquote", children=processed_html_node)
    return html_node


def create_code_html_node(block: str):
    # print(repr(block))
    process_block = block.strip("```").lstrip()
    # print(repr(process_block))
    text_block = TextNode(text=process_block, text_type=TextType.TEXT)
    raw_html_block = [text_node_to_html_node(text_block)]
    pre_html_block = ParentNode(tag="code", children=raw_html_block)
    html_node = ParentNode(tag="pre", children=[pre_html_block])
    return html_node


def create_paragraph_html_node(block: str):
    process_block = " ".join(block.split("\n"))
    processed_html_node = create_inline_html_nodes_from_text(process_block)
    html_node = ParentNode(tag="p", children=processed_html_node)
    return html_node


def create_heading_node(block):
    text = ""
    header = ""
    for i in range(6, 0, -1):
        header = "#"*i
        if block.startswith(header):
            text = block[i+1:]
            break
    inline_html_nodes = create_inline_html_nodes_from_text(text)
    html_content = inline_html_nodes
    html_node = ParentNode(tag=f"h{len(header)}", children=html_content)
    return html_node


def create_html_node(blocktype, content):
    match blocktype:
        case BlockType.HEADING:
            html_node = create_heading_node(content)
        case BlockType.CODE:
            html_node = create_code_html_node(content)
        case BlockType.QUOTE:
            html_node = create_blockquote_html_node(content)
        case BlockType.UNORDERED_LIST:
            html_node = create_unordered_list_html_node(content)
        case BlockType.ORDERED_LIST:
            html_node = create_ordered_list_html_node(content)
        case _:
            html_node = create_paragraph_html_node(content)
    return html_node


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        blocktype = block_to_block_type(block)
        html_node = create_html_node(blocktype, block)
        # HTMLBlock from block type
        nodes.append(html_node)
    big_div = ParentNode(tag="div", children=nodes)
    return big_div    


if __name__ == "__main__":
    md = """
- Apples
- Bananas
- Cherries
- Dates
"""
    node = markdown_to_html_node(md)
    html = node.to_html()
    print(html)
    html_expected = "<div><ul><li>Apples</li><li>Bananas</li><li>Cherries</li><li>Dates</li></ul></div>"
    print(html)


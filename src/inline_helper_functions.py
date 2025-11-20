from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if node.text.count(delimiter) % 2 == 1:
            raise Exception(f"invalid markdown: no enlcosing '{delimiter}' in '{node.text}'")

        processed_node_list = []
        split_on_delimiter = node.text.split(delimiter)
        for i, item in enumerate(split_on_delimiter):
            if len(item) > 0:
                if i % 2 == 1:
                    processed_node_list.append(TextNode(item, text_type))
                else:
                    processed_node_list.append(TextNode(item, TextType.TEXT))
        new_nodes.extend(processed_node_list)
    return new_nodes

# text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
# print(extract_markdown_images(text))
# [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]

def extract_markdown_images(text):
    r_expression = r"!\[(.*?)\]\((https:\/\/.*?\.(png|jpg|jpeg|gif))\)"
    # Expression from class: r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    raw_image_data = re.findall(r_expression, text)
    clean_images = [(image[0], image[1]) for image in raw_image_data]
    return clean_images

def extract_markdown_links(text):
    r_expression = r"(?<!!)\[(.*?)\]\((https:\/\/.*?)\)"
    # Expression from class: r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    raw_image_data = re.findall(r_expression, text)
    clean_images = [(image[0], image[1]) for image in raw_image_data]
    return clean_images


if __name__ == "__main__":
    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    print(extract_markdown_images(text))
    text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    print(extract_markdown_links(text))     

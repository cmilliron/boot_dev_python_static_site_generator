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

def process_image_node(node):
    if node.text_type != TextType.TEXT:
        return [node]
    images = extract_markdown_images(node.text)

    current_image_text = images[0][0]
    current_image_link = images[0][1]
    images_split = node.text.split(f"![{current_image_text}]({current_image_link})")
    if len(images_split) == 0:
        return [node]
    if len(images_split) == 1:
        return [TextNode(current_image_text, TextType.IMAGE, url=current_image_link)]
    if len(images_split) == 2 and images_split[0] == "":
        output = [TextNode(current_image_text, TextType.IMAGE, url=current_image_link)]
        output.extend(process_image_node(TextNode(images_split[1], TextType.TEXT)))
        return output
    if len(images_split) == 2 and images_split[1] == "":
        output = [
            TextNode(images_split[0], TextType.TEXT), 
            TextNode(current_image_text, TextType.IMAGE, url=current_image_link)
            ]
        return output
    output = [TextNode(images_split[0], TextType.TEXT), TextNode(current_image_text, TextType.IMAGE, url=current_image_link)]
    output.extend(process_image_node(TextNode(images_split[1], TextType.TEXT)))
    return output


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        processed = process_image_node(node)
        # print(processed)
        new_nodes.extend(processed)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    pass


# text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
# print(extract_markdown_images(text))
# [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]

def extract_markdown_images(text):
    # r_expression = r"!\[(.*?)\]\((https:\/\/.*?\.(png|jpg|jpeg|gif))\)"
    r_expression = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    # Expression from class: r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    raw_image_data = re.findall(r_expression, text)
    clean_images = [(image[0], image[1]) for image in raw_image_data]
    return clean_images

def extract_markdown_links(text):
    # r_expression = r"(?<!!)\[(.*?)\]\((https:\/\/.*?)\)"
    r_expression = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    # Expression from class: r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    raw_image_data = re.findall(r_expression, text)
    clean_images = [(image[0], image[1]) for image in raw_image_data]
    return clean_images


if __name__ == "__main__":
    # text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    # print(extract_markdown_images(text))
    # text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    # print(extract_markdown_links(text))   
    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    print(node)
    new_nodes = split_nodes_image([node])
    print(new_nodes)

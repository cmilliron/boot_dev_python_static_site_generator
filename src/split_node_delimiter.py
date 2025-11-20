from textnode import TextNode, TextType


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
from textnode import TextNode, TextType

# def get_text_type(delimiter):
#     match delimiter:
#         case "**":
#             return TextType.BOLD
#         case "_":
#             return TextType.ITALIC
#         case "`":
#             return TextType.CODE
#     raise ValueError(f'"{delimiter} is an invalid markdown delimiters')

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    # text_type_from_delimiter = get_text_type(delimiter)
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if node.text.count(delimiter) % 2 == 1:
            raise Exception(f"invalid markdown: no enlcosing '{delimiter}' '{node.text}'")

        processed_node_list = []
        # if node.text.startswith(delimiter):
        split_on_delimiter = node.text.split(delimiter)
        for i, item in enumerate(split_on_delimiter):
            if len(item) > 0:
                if i % 2 == 1:
                    processed_node_list.append(TextNode(item, text_type))
                else:
                    processed_node_list.append(TextNode(item, TextType.TEXT))
        # else: 
        # split_on_delimiter = node.text.split(delimiter)
        # for i, item in enumerate(split_on_delimiter):
            
        #         if i % 2 == 1:
        #             processed_node_list.append(TextNode(item, text_type))
        #         else:
        #             processed_node_list.append(TextNode(item, TextType.TEXT))
        new_nodes.extend(processed_node_list)
    return new_nodes
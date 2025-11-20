import unittest
from htmlnode import HTMLNode, LeafNode
from textnode import TextNode, TextType
from textnode_to_htmlnode import text_node_to_html_node
from inline_helper_functions import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

class TestTextToHTMLNODE(unittest.TestCase):

    def test_text(self):
        print("\nTesting creating a text node....")
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        print("Input: ", node, "\nOutput: ", html_node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        print("\nTesting creating a bold node....")
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        print("Input: ", node, "\nOutput: ", html_node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        print("\nTesting creating a italic node....")
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        print("Input: ", node, "\nOutput: ", html_node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")
    
    def test_code(self):
        print("\nTesting creating a code node....")
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        print("Input: ", node, "\nOutput: ", html_node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")
    
    def test_link(self):
        print("\nTesting creating a link node....")
        node = TextNode("Google Link", TextType.LINK, url="https://google.com")
        html_node = text_node_to_html_node(node)
        print("Input: ", node, "\nOutput: ", html_node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Google Link")
        self.assertEqual(html_node.props, {"href": "https://google.com"})

    def test_image(self):
        print("\nTesting creating a link node....")
        node = TextNode("Alt Text", TextType.IMAGE, url="https://google.com")
        html_node = text_node_to_html_node(node)
        print("Input: ", node, "\nOutput: ", html_node)
        print(html_node.to_html())
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"alt": "Alt Text", "src": "https://google.com"})
        self.assertEqual(html_node.to_html(), '<img src="https://google.com" alt="Alt Text"></img>')

    def test_image2(self):
        print("\nTesting creating a link node....")
        node = TextNode("Alt Text", TextType.IMAGE, url="https://google.com")
        html_node = text_node_to_html_node(node)
        print("Input: ", node, "\nOutput: ", html_node)
        print(html_node.to_html())
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"alt": "Alt Text", "src": "https://google.com"})
        self.assertEqual(html_node.to_html(), '<img src="https://google.com" alt="Alt Text"></img>')
    
    def test_exception(self):
        print("\nTesting exeptions....")
        with self.assertRaises(Exception):
            node = TextNode("Alt Text", "hot_pocket", url="https://google.com")
            html_node = text_node_to_html_node(node)

class TestMarkdownInlineDelimiter(unittest.TestCase):

    def test_bold_delimiter(self):
        print("\nTesting bold split delimiter....")
        nodes = [TextNode("This is text with a **bold words here** and some words here", TextType.TEXT)]
        response = split_nodes_delimiter(nodes, "**", TextType.BOLD) 
        print("Input: ", nodes, "\nOutput: ", response)
        self.assertEqual(response[0].text_type, TextType.TEXT)
        self.assertEqual(response[0].text, "This is text with a ")
        self.assertEqual(response[1].text_type, TextType.BOLD)
        self.assertEqual(response[1].text, "bold words here")
        self.assertEqual(response[2].text_type, TextType.TEXT)
        self.assertEqual(response[2].text, " and some words here")
    
    def test_code_delimiter(self):
        print("\nTesting code delimiter....")
        nodes = [TextNode("This is text with a `code goes here` and some words here", TextType.TEXT)]
        response = split_nodes_delimiter(nodes, "`", TextType.CODE) 
        print("Input: ", nodes, "\nOutput: ", response)
        self.assertEqual(response[0].text_type, TextType.TEXT)
        self.assertEqual(response[0].text, "This is text with a ")
        self.assertEqual(response[1].text_type, TextType.CODE)
        self.assertEqual(response[1].text, "code goes here")
        self.assertEqual(response[2].text_type, TextType.TEXT)
        self.assertEqual(response[2].text, " and some words here")
    
    def test_italic_delimiter(self):
        print("\nTesting italic delimiter....")
        nodes = [TextNode("This is text with a _italic words here_ and some words here", TextType.TEXT)]
        response = split_nodes_delimiter(nodes, "_", TextType.ITALIC) 
        print("Input: ", nodes, "\nOutput: ", response)
        self.assertEqual(response[0].text_type, TextType.TEXT)
        self.assertEqual(response[0].text, "This is text with a ")
        self.assertEqual(response[1].text_type, TextType.ITALIC)
        self.assertEqual(response[1].text, "italic words here")
        self.assertEqual(response[2].text_type, TextType.TEXT)
        self.assertEqual(response[2].text, " and some words here")

    def test_starts_with_delimiter(self):
        print("\nTesting starts with delimiter....")
        nodes = [TextNode("_italic words here_ and some words here", TextType.TEXT)]
        response = split_nodes_delimiter(nodes, "_", TextType.ITALIC) 
        print("Input: ", nodes, "\nOutput: ", response)
        self.assertEqual(response[0].text_type, TextType.ITALIC)
        self.assertEqual(response[0].text, "italic words here")
        self.assertEqual(response[1].text_type, TextType.TEXT)
        self.assertEqual(response[1].text, " and some words here")

    def test_multiply_nodes(self):
        print("\nTesting starts with delimiter....")
        nodes = [TextNode("This is text with a _italic words here_ and some words here", TextType.TEXT),
                 TextNode("This is text with a **bold words here** and some words here", TextType.TEXT),
                 TextNode("This is text with a `code goes here` and some words here", TextType.TEXT)
                 ]
        response = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        response = split_nodes_delimiter(response, "**", TextType.BOLD)
        response = split_nodes_delimiter(response, "`", TextType.CODE) 
        print("Input: ", nodes, "\nOutput: ", response)
        self.assertEqual(response[0].text_type, TextType.TEXT)
        self.assertEqual(response[0].text, "This is text with a ")
        self.assertEqual(response[1].text_type, TextType.ITALIC)
        self.assertEqual(response[1].text, "italic words here")
        self.assertEqual(response[2].text_type, TextType.TEXT)
        self.assertEqual(response[2].text, " and some words here")
        self.assertEqual(response[3].text_type, TextType.TEXT)
        self.assertEqual(response[3].text, "This is text with a ")
        self.assertEqual(response[4].text_type, TextType.BOLD)
        self.assertEqual(response[4].text, "bold words here")
        self.assertEqual(response[5].text_type, TextType.TEXT)
        self.assertEqual(response[5].text, " and some words here")
        self.assertEqual(response[6].text_type, TextType.TEXT)
        self.assertEqual(response[6].text, "This is text with a ")
        self.assertEqual(response[7].text_type, TextType.CODE)
        self.assertEqual(response[7].text, "code goes here")
        self.assertEqual(response[8].text_type, TextType.TEXT)
        self.assertEqual(response[8].text, " and some words here")

    # Testing Exceptions
    def test_bad_mardown_exception(self):
        print("\nTesting bad markdone exeption....")
        with self.assertRaises(Exception) as e:
            node = TextNode("This is the wrong way to **bold something in markdown", TextType.TEXT)
            response = split_nodes_delimiter([node], "**", TextType.BOLD)
        print(f"Exception: {str(e.exception)}")

class TestLinkAndImageExtraction(unittest.TestCase):    
    def test_extract_markdown_images(self):
        print("\nTesting for markdown image extraction with one image....")
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_multiple_images(self):
        print("\nTesting for markdown image extraction with one image....")
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_link(self):
        print("\nTesting for markdown link extraction with one link....")
        matches = extract_markdown_links(
            "This is text with an [Google](https://google.com)"
        )
        print(matches)
        self.assertListEqual([("Google", "https://google.com")], matches)

    def test_extract_markdown_multiple_links(self):
        print("\nTesting for multiple markdown link extraction with one link....")
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        print(matches)
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)
    

if __name__ == "__main__":
    unittest.main()
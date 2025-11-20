import unittest
from htmlnode import HTMLNode, LeafNode
from textnode import TextNode, TextType
from textnode_to_htmlnode import text_node_to_html_node

class TestLeafNode(unittest.TestCase):

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



if __name__ == "__main__":
    unittest.main()
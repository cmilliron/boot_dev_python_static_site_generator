import unittest
from htmlnode import HTMLNode, LeafNode

class TestLeafNode(unittest.TestCase):

    def test_to_html_no_value_raises(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_tag_returns_value(self):
        node = LeafNode(None, "Hello")
        self.assertEqual(node.to_html(), "Hello")

    def test_to_html_simple_tag(self):
        node = LeafNode("p", "Hello")
        self.assertEqual(node.to_html(), "<p>Hello</p>")

    def test_to_html_with_props(self):
        node = LeafNode("a", "Click", props={"href": "https://example.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://example.com">Click</a>'
        )

    def test_to_html_empty_string_value(self):
        node = LeafNode("span", "")
        self.assertEqual(node.to_html(), "<span></span>")

    def test_to_html_special_characters(self):
        node = LeafNode("p", "<b>Hi</b>")
        self.assertEqual(node.to_html(), "<p><b>Hi</b></p>")

    def test_inherits_props_to_html_behavior(self):
        node = LeafNode("div", "content", props={"id": "main"})
        self.assertIn('id="main"', node.to_html())

    def test_repr(self):
        node = LeafNode("p", "Hello", {"class": "x"})
        expected = "LeafNode(p, Hello, {'class': 'x'})"
        self.assertEqual(repr(node), expected)


if __name__ == "__main__":
    unittest.main()
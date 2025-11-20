import unittest
from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html_none(self):
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_dict(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_prop(self):
        node = HTMLNode(props={"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')
    
    def test_props_to_html_numeric_values(self):
        node = HTMLNode(props={"width": 300, "height": 200})
        self.assertEqual(node.props_to_html(), ' width="300" height="200"')

    def test_props_to_html_boolean_values(self):
        node = HTMLNode(props={"disabled": True, "checked": False})
        self.assertEqual(node.props_to_html(), ' disabled="True" checked="False"')

    def test_props_to_html_key_with_colon(self):
        node = HTMLNode(props={"aria-label": "Close"})
        self.assertEqual(node.props_to_html(), ' aria-label="Close"')

    def test_props_to_html_value_empty_string(self):
        node = HTMLNode(props={"alt": ""})
        self.assertEqual(node.props_to_html(), ' alt=""')

    def test_props_to_html_multiple_props(self):
        node = HTMLNode(props={"class": "btn", "id": "submit"})
        # Order matters because dict preserves insertion order in Python 3.7+
        self.assertEqual(node.props_to_html(), ' class="btn" id="submit"')

    def test_repr(self):
        node = HTMLNode("p", "Hello", [], {"class": "text"})
        self.assertEqual(
            repr(node),
            "HTMLNode(p, Hello, children: [], {'class': 'text'})"
        )

    def test_default_values(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_to_html_not_implemented(self):
        node = HTMLNode("p", "Hello")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_children_assignment(self):
        child = HTMLNode("span", "text")
        parent = HTMLNode("div", children=[child])
        self.assertEqual(parent.children, [child])

    def test_value_assignment(self):
        node = HTMLNode("p", "Hello")
        self.assertEqual(node.value, "Hello")
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


if __name__ == "__main__":
    unittest.main()
import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    
    def test_eq_same_url(self):
        node = TextNode("Google", TextType.LINK, "https://google.com")
        node2 = TextNode("Google", TextType.LINK, "https://google.com")
        self.assertEqual(node, node2)

    def test_not_eq_different_text(self):
        node = TextNode("Hello", TextType.TEXT)
        node2 = TextNode("Goodbye", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_type(self):
        node = TextNode("Hi", TextType.TEXT)
        node2 = TextNode("Hi", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_url(self):
        node = TextNode("Photo", TextType.IMAGE, "image1.png")
        node2 = TextNode("Photo", TextType.IMAGE, "image2.png")
        self.assertNotEqual(node, node2)

    def test_eq_with_none_url(self):
        node = TextNode("Sample", TextType.CODE, None)
        node2 = TextNode("Sample", TextType.CODE, None)
        self.assertEqual(node, node2)

    def test_repr_basic(self):
        node = TextNode("Hi", TextType.TEXT)
        self.assertEqual(repr(node), "TextNode(Hi, text, None)")

    def test_repr_with_url(self):
        node = TextNode("Link", TextType.LINK, "http://example.com")
        self.assertEqual(repr(node), "TextNode(Link, link, http://example.com)")

    def test_eq_different_objects_same_values(self):
        # confirms equality doesn't depend on object identity
        node = TextNode("X", TextType.BOLD)
        node2 = TextNode("X", TextType.BOLD)
        self.assertTrue(node == node2)

    def test_enum_value(self):
        self.assertEqual(TextType.ITALIC.value, "italic")

    # def test_type_error_comparison(self):
    #     node = TextNode("Hi", TextType.TEXT)
    #     self.assertNotEqual(node, "not a TextNode")


if __name__ == "__main__":
    unittest.main()
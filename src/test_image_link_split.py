import unittest

from textnode import TextNode, TextType
from inline_helper_functions import split_nodes_image, split_nodes_link


class TestTextNode(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        # Test 1: Simple image in the middle of text
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with an ")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[1].url, "https://i.imgur.com/zjjcJKZ.png")
        self.assertEqual(new_nodes[2].text, " and another text")

    def test_split_image_single_standalone(self):
        # Test 2: Text node is JUST the image
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[0].url, "https://i.imgur.com/zjjcJKZ.png")

    def test_split_images_multiple(self):
        # Test 3: Multiple images in sequence
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "This is text with an ")
        self.assertEqual(new_nodes[1].text, "image")
        self.assertEqual(new_nodes[2].text, " and another ")
        self.assertEqual(new_nodes[3].text, "second image")

    def test_split_link_single(self):
        # Test 4: Single link in middle of text
        node = TextNode(
            "This is text with a [link](https://www.example.com) and another text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)
        self.assertEqual(new_nodes[1].url, "https://www.example.com")

    def test_split_link_multiple(self):
        # Test 5: Multiple links
        node = TextNode(
            "Here is [link one](https://1.com) and [link two](https://2.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "Here is ")
        self.assertEqual(new_nodes[1].text, "link one")
        self.assertEqual(new_nodes[2].text, " and ")
        self.assertEqual(new_nodes[3].text, "link two")

    def test_split_link_at_end(self):
        # Test 6: Link at the very end of text
        node = TextNode(
            "Click here for [google](https://www.google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "Click here for ")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)

    def test_split_link_at_start(self):
        # Test 7: Link at the very start of text
        node = TextNode(
            "[google](https://www.google.com) is a search engine",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text_type, TextType.LINK)
        self.assertEqual(new_nodes[1].text, " is a search engine")

    def test_split_no_links(self):
        # Test 8: Text with no links should remain unchanged
        node = TextNode(
            "Just plain text with no links",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "Just plain text with no links")

    def test_non_text_node_ignored(self):
        # Test 9: Nodes that aren't TextType.TEXT should be ignored
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.BOLD, # Marked as BOLD, so image splitter should ignore it
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)

    # def test_split_mixed_syntax(self):
    #     # Test 10: Ensure image splitter does not split links and vice versa
    #     # (This verifies that regexes are strict)
    #     text = "This is a [link](url) and an ![image](img_url)"
    #     node = TextNode(text, TextType.TEXT)
        
    #     # Pass through link splitter only
    #     link_nodes = split_nodes_link([node])
    #     # Should find the link, but treat the image as plain text
    #     self.assertEqual(len(link_nodes), 2)
    #     self.assertEqual(link_nodes[0].text, "This is a ")
    #     self.assertEqual(link_nodes[1].text_type, TextType.LINK)
    #     # The image part remains part of the text in the "recursion" or remaining text 
    #     # (Wait, actually logic dictates: " and an ![image](img_url)" is the second part)
    #     # Let's verify the exact structure
    #     # [Text("This is a "), Link("link"), Text(" and an ![image](img_url)")]
    #     self.assertEqual(len(link_nodes), 3) 
    #     self.assertEqual(link_nodes[2].text, " and an ![image](img_url)")



if __name__ == "__main__":
    unittest.main()
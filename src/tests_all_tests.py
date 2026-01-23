import unittest
from htmlnode import LeafNode, ParentNode, HTMLNode
from textnode import TextNode, TextType
from textnode_to_htmlnode import text_node_to_html_node
from inline_helper_functions import split_nodes_delimiter, extract_markdown_links, extract_markdown_images, split_nodes_image, split_nodes_link
from text_to_node import text_to_textnodes
from block_helper_functions import markdown_to_blocks


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )


class TestTextNode1(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node2", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )

class TestHTMLNode2(unittest.TestCase):
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

    def test_split_image_1(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single_1(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images_1(self):
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

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )


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


class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_props_in_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild", props={"class": "links"})
        child_node = ParentNode("a", [grandchild_node], props={"href":"http://google.com", "class":"links"})
        parent_node = ParentNode("div", [child_node], props={"class": "container"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container"><a href="http://google.com" class="links"><b class="links">grandchild</b></a></div>',
        )
        
    def test_grandchild_is_none(self):
        grandchild_node = None
        child_node = ParentNode("a", [grandchild_node], props={"href":"http://google.com", "class":"links"})
        parent_node = ParentNode("div", [child_node], props={"class": "container"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container"><a href="http://google.com" class="links"></a></div>',
        )
    def test_muliple_child_nodes(self):
        grandchild_node = LeafNode("b", "grandchild", props={"class": "links"})
        child_node = ParentNode("a", [grandchild_node], props={"href":"http://google.com", "class":"links"})
        parent_node = ParentNode("div", [child_node, child_node], props={"class": "container"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container"><a href="http://google.com" class="links"><b class="links">grandchild</b></a><a href="http://google.com" class="links"><b class="links">grandchild</b></a></div>',
        )


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

class TestTextNodes(unittest.TestCase):
    def test_text_to_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text=text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    
    def test_text_to_nodes_no_image(self):
        text = "This is **text** with an _italic_ word and a `code block` and a [link](https://boot.dev) and an"
        new_nodes = text_to_textnodes(text=text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and an", TextType.TEXT),
            ],
            new_nodes,
        )


    def test_text_to_nodes_another(self):
        text = "This is **text** with an _italic_ word and a `code block` and a [link](https://boot.dev) and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
        new_nodes = text_to_textnodes(text=text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            new_nodes,
        )


    def test_text_to_nodes_another_no_link(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
        new_nodes = text_to_textnodes(text=text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            new_nodes,
        )

class TestTextDifferentNode(unittest.TestCase):
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


class TestBlockHelperFunctions(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_basic_split(self):
        # Test 1: Simple case with two distinct blocks
        md = "This is a heading\n\nThis is a paragraph."
        expected = ["This is a heading", "This is a paragraph."]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_whitespace_stripping(self):
        # Test 2: Blocks with leading/trailing spaces and tabs
        md = "   Block one with spaces   \n\n   Block two with tabs\t"
        expected = ["Block one with spaces", "Block two with tabs"]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_multiple_newlines(self):
        # Test 3: Handling more than two newlines between blocks
        md = "Block one\n\n\n\nBlock two"
        # My updated version filters empty strings, otherwise this would return ['Block one', '', 'Block two']
        expected = ["Block one", "Block two"]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_single_newline_preservation(self):
        # Test 4: Single newlines should NOT split blocks (like a list)
        md = "List item 1\nList item 2\n\nParagraph 2"
        expected = ["List item 1\nList item 2", "Paragraph 2"]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_trailing_newlines_at_eof(self):
        # Test 5: Markdown file ending with several newlines
        md = "Only one block\n\n\n"
        expected = ["Only one block"]
        self.assertEqual(markdown_to_blocks(md), expected)


if __name__ == "__main__":
    unittest.main()

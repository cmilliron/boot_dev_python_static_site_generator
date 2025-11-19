import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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


if __name__ == "__main__":
    print("Running Unit Test of ParentNode class ...")
    unittest.main()
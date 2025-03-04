import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_class_membership(self):
        childnode = LeafNode("span", "child")
        parentnode: ParentNode = ParentNode("div", [childnode])
        self.assertIsInstance(parentnode, ParentNode)

    def test_tag(self):
        childnode = LeafNode("span", "child")
        parentnode: ParentNode = ParentNode("p", [childnode])
        self.assertEqual(parentnode.tag, "p")

    def test_props(self):
        childnode = LeafNode("span", "child")
        parentnode: ParentNode = ParentNode(
            tag="div",
            children=[childnode],
            props={"href": "https://www.google.com", "target": "_blank"},
        )
        self.assertEqual(
            parentnode.props, {"href": "https://www.google.com", "target": "_blank"}
        )

    def test_to_html_child(self):
        childnode = LeafNode("span", "child")
        parentnode: ParentNode = ParentNode("div", [childnode])
        self.assertEqual(parentnode.to_html(), "<div><span>child</span></div>")

    def test_to_html_children(self):
        childnode = LeafNode("span", "child")
        childnode2 = LeafNode("b", "child2")
        parentnode: ParentNode = ParentNode("div", [childnode, childnode2])
        self.assertEqual(
            parentnode.to_html(), "<div><span>child</span><b>child2</b></div>"
        )

    def test_to_html_grandchild(self):
        grandchildnode: LeafNode = LeafNode("b", "grandchild")
        childnode: ParentNode = ParentNode("span", [grandchildnode])
        parentnode: ParentNode = ParentNode("div", [childnode])
        self.assertEqual(
            parentnode.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    _ = unittest.main()

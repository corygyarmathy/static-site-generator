import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from markdown_blocks import markdown_to_html_node


class TestHTMLNode(unittest.TestCase):
    def test_HTMLNode_defaults(self):
        htmlnode: HTMLNode = HTMLNode()
        self.assertEqual(htmlnode.tag, None)
        self.assertEqual(htmlnode.value, None)
        self.assertEqual(htmlnode.children, None)
        self.assertEqual(htmlnode.props, None)

    def test_HTMLNode_class_membership(self):
        htmlnode = HTMLNode()
        self.assertIsInstance(htmlnode, HTMLNode)

    def test_HTMLNode_tag(self):
        htmlnode: HTMLNode = HTMLNode(tag="p")
        self.assertEqual(htmlnode.tag, "p")

    def test_HTMLNode_value(self):
        htmlnode: HTMLNode = HTMLNode(value="text")
        self.assertEqual(htmlnode.value, "text")

    def test_HTMLNode_props(self):
        htmlnode: HTMLNode = HTMLNode(
            props={"href": "https://www.google.com", "target": "_blank"}
        )
        self.assertEqual(
            htmlnode.props, {"href": "https://www.google.com", "target": "_blank"}
        )

    def test_props_to_html(self):
        htmlnode: HTMLNode = HTMLNode(
            props={"href": "https://www.google.com", "target": "_blank"}
        )
        self.assertEqual(
            htmlnode.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )

    def test_HTMLNode_repr(self):
        htmlnode: HTMLNode = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            htmlnode.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

    def test_LeafNode_defaults(self):
        leafnode: LeafNode = LeafNode(None, "")
        self.assertEqual(leafnode.tag, None)
        self.assertEqual(leafnode.value, "")
        self.assertEqual(leafnode.props, None)

    def test_LeafNode_class_membership(self):
        leafnode: LeafNode = LeafNode(None, "")
        self.assertIsInstance(leafnode, LeafNode)

    def test_LeafNode_tag(self):
        leafnode: LeafNode = LeafNode("p", "")
        self.assertEqual(leafnode.tag, "p")

    def test_LeafNode_value(self):
        leafnode: LeafNode = LeafNode(tag=None, value="text")
        self.assertEqual(leafnode.value, "text")

    def test_LeafNode_props(self):
        leafnode: LeafNode = LeafNode(
            tag=None,
            value="text",
            props={"href": "https://www.google.com", "target": "_blank"},
        )
        self.assertEqual(
            leafnode.props, {"href": "https://www.google.com", "target": "_blank"}
        )

    def test_to_html_a(self):
        leafnode: LeafNode = LeafNode(
            tag="a", value="text", props={"href": "https://www.google.com"}
        )
        self.assertEqual(
            leafnode.to_html(), '<a href="https://www.google.com">text</a>'
        )

    def test_to_html_p(self):
        leafnode: LeafNode = LeafNode(tag="p", value="text")
        self.assertEqual(leafnode.to_html(), "<p>text</p>")

    def test_to_html_no_tag(self):
        leafnode: LeafNode = LeafNode(None, value="text")
        self.assertEqual(leafnode.to_html(), "text")

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

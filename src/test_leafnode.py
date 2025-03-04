import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_defaults(self):
        leafnode: LeafNode = LeafNode(None, "")
        self.assertEqual(leafnode.tag, None)
        self.assertEqual(leafnode.value, "")
        self.assertEqual(leafnode.props, None)

    def test_class_membership(self):
        leafnode: LeafNode = LeafNode(None, "")
        self.assertIsInstance(leafnode, LeafNode)

    def test_tag(self):
        leafnode: LeafNode = LeafNode("p", "")
        self.assertEqual(leafnode.tag, "p")

    def test_value(self):
        leafnode: LeafNode = LeafNode(tag=None, value="text")
        self.assertEqual(leafnode.value, "text")

    def test_props(self):
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


if __name__ == "__main__":
    _ = unittest.main()

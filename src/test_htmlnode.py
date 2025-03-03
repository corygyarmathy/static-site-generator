import unittest

from htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):
    def test_defaults(self):
        htmlnode: HTMLNode = HTMLNode()
        self.assertEqual(htmlnode.tag, None)
        self.assertEqual(htmlnode.value, None)
        self.assertEqual(htmlnode.children, None)
        self.assertEqual(htmlnode.props, None)

    def test_class_membership(self):
        htmlnode = HTMLNode()
        self.assertIsInstance(htmlnode, HTMLNode)

    def test_tag(self):
        htmlnode: HTMLNode = HTMLNode(tag="p")
        self.assertEqual(htmlnode.tag, "p")

    def test_value(self):
        htmlnode: HTMLNode = HTMLNode(value="text")
        self.assertEqual(htmlnode.value, "text")

    def test_props(self):
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
            htmlnode.props_to_html(), 'href="https://www.google.com" target="_blank"'
        )

    def test_repr(self):
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


if __name__ == "__main__":
    _ = unittest.main()

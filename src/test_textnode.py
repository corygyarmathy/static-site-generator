import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node")
        self.assertEqual(node.text, "This is a text node")

    def test_text_type_normal_value(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        self.assertEqual(node.text_type.value, "normal")

    def test_text_type_bold_value(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.text_type.value, "bold")

    def test_text_type_italic_value(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node.text_type.value, "italic")

    def test_text_type_code_value(self):
        node = TextNode("This is a text node", TextType.CODE)
        self.assertEqual(node.text_type.value, "code")

    def test_text_type_link_value(self):
        node = TextNode("This is a text node", TextType.LINK)
        self.assertEqual(node.text_type.value, "link")

    def test_text_type_image_value(self):
        node = TextNode("This is a text node", TextType.IMAGE)
        self.assertEqual(node.text_type.value, "image")

    def test_url(self):
        node = TextNode(
            "This is some anchor text", TextType.LINK, "https://www.boot.dev"
        )
        self.assertEqual(node.url, "https://www.boot.dev")

    def test_url_none(self):
        node = TextNode("This is a text node")
        self.assertEqual(node.url, None)

    def test_class_membership(self):
        node = TextNode("This is a text node", TextType.LINK, "https://boot.dev")
        self.assertIsInstance(node, TextNode)

    def test_eq(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        node2 = TextNode("This is a text node", TextType.NORMAL)
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("This is a text node")
        node2 = TextNode("This is a second text node")
        self.assertNotEqual(node, node2)

    def test_not_eq_text_type(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode(
            "This is a text node", TextType.LINK, url="https://www.boot.dev"
        )
        node2 = TextNode(
            "This is a text node", TextType.LINK, url="https://www.google.com"
        )
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode(
            "This is some anchor text", TextType.LINK, "https://www.boot.dev"
        )
        printStr = "TextNode(This is some anchor text, link, https://www.boot.dev)"
        self.assertEqual(node.__repr__(), printStr)


if __name__ == "__main__":
    _ = unittest.main()

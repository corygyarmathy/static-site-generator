import unittest

from markdown_manipulation import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
)
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node")
        self.assertEqual(node.text, "This is a text node")

    def test_text_type_text_value(self):
        node = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node.text_type.value, "text")

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
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("This is a text node")
        node2 = TextNode("This is a second text node")
        self.assertNotEqual(node, node2)

    def test_not_eq_text_type(self):
        node = TextNode("This is a text node", TextType.TEXT)
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

    def test_text_node_to_html_node_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_node_to_html_node_img(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_text_node_to_html_node_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

    def test_split_notes_delimiter_code(self):
        node = TextNode("This is text with a `markdown element` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("markdown element", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_notes_delimiter_bold(self):
        node = TextNode("This is text with a **markdown element** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("markdown element", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_notes_delimiter_bold_multiword(self):
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

    def test_split_notes_delimiter_italic(self):
        node = TextNode("This is text with a *markdown element* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("markdown element", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_notes_delimiter_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
        )

    def test_split_notes_delimiter_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        new_nodes = split_nodes_delimiter([node], "img", TextType.IMAGE)
        self.assertEqual(
            new_nodes,
            [node],
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_split_image(self):
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

    def test_split_image_single(self):
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


if __name__ == "__main__":
    _ = unittest.main()

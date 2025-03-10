from htmlnode import HTMLNode, LeafNode, ParentNode
from markdown_manipulation import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from markdown_blocks import markdown_to_blocks
from textnode import TextNode, TextType


def main():
    """Temporary scaffolding function for debugging."""
    textnode = TextNode(
        "This is some anchor text", TextType.LINK, "https://www.boot.dev"
    )
    print(textnode)
    htmlnode = HTMLNode(
        "a", "text", None, {"href": "https://www.google.com", "target": "_blank"}
    )
    print(htmlnode)

    leafnode = LeafNode("a", "text", {"href": "https://www.google.com"})
    print(leafnode.to_html())

    parentnode = ParentNode("b", [leafnode, leafnode])
    grandparentnode = ParentNode("div", [parentnode])
    print(grandparentnode.to_html())

    node = TextNode("**bold** and _italic_", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)

    img_node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    new_img_node = split_nodes_image([img_node])
    print(new_img_node.__repr__())

    link_node = TextNode(
        "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    new_link_node = split_nodes_link([link_node])
    print(new_link_node.__repr__())

    single_image_node = TextNode(
        "![image](https://www.example.COM/IMAGE.PNG)",
        TextType.TEXT,
    )
    new_single_image_nodes = split_nodes_image([single_image_node])

    text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    new_text_nodes = text_to_textnodes(text)


if __name__ == "__main__":
    _ = main()

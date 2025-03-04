from htmlnode import HTMLNode
from textnode import TextNode, TextType


def main():
    textnode = TextNode(
        "This is some anchor text", TextType.LINK, "https://www.boot.dev"
    )
    print(textnode)
    htmlnode = HTMLNode(
        "a", "text", None, {"href": "https://www.google.com", "target": "_blank"}
    )
    # print(htmlnode)

    leafnode = LeafNode("a", "text", {"href": "https://www.google.com"})
    # print(leafnode.to_html())

    parentnode = ParentNode("b", [leafnode, leafnode])
    grandparentnode = ParentNode("div", [parentnode])
    print(grandparentnode.to_html())


if __name__ == "__main__":
    _ = main()

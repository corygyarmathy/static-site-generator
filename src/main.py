from htmlnode import HTMLNode
from textnode import TextNode, TextType


def main():
    textnode = TextNode(
        "This is some anchor text", TextType.LINK, "https://www.boot.dev"
    )
    print(textnode)
    htmlnode = HTMLNode(
        "p", "text", None, {"href": "https://www.google.com", "target": "_blank"}
    )
    print(htmlnode)


if __name__ == "__main__":
    _ = main()

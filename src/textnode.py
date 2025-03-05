from enum import Enum
from typing import override
from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(
        self, text: str, text_type: TextType = TextType.TEXT, url: str | None = None
    ):
        self.text: str = text
        self.text_type: TextType = text_type
        self.url: str | None = url

    @override
    def __eq__(self, other) -> bool:
        if type(other) is TextNode:
            return (
                self.text == other.text
                and self.text_type == other.text_type
                and self.url == other.url
            )

        return False

    @override
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text_type.value)
        case TextType.LINK:
            return LeafNode(
                tag="a",
                value=text_node.text,
                props={"href": str(text_node.url)},
            )
        case TextType.IMAGE:
            return LeafNode(
                tag="img",
                value="",
                props={"src": str(text_node.url), "alt": text_node.text},
            )
        case _:
            raise ValueError("Unhandled TextType")

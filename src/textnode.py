"""Module for creating and mainipulating TextNode objects.

TextNode objects serve as an intermediary between Markdown blocks, and HTMLNode objects.
In fact the text_node_to_html_node() method is used to convert a TextNode to a HTMLNode.

Typical usage example:

text_node = TextNode("string", TextType.TEXT, None)
html_node = text_node_to_html_node(text_node)
"""

from enum import Enum
from typing import override
from htmlnode import LeafNode


class TextType(Enum):
    """Enum for the type of text, for a TextNode object."""

    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    """Object containing text, the type of text (TextType object), and an optional URL string

    TextNode objects serve as an intermediary between Markdown blocks, and HTMLNode objects.

    Attributes:
        text: A string containing the text.
        text_type: A TextType object indicating the type of text (e.g. bold, italic, text)
        url: An optional string containing the URL value if it's present (e.g. "https://www.google.com.au")
    """

    def __init__(
        self, text: str, text_type: TextType = TextType.TEXT, url: str | None = None
    ) -> None:
        """Initialises TextNode object from the text string, text type, and optional URL.

        Args:
            text: A string containing the text.
            text_type: A TextType object indicating the type of text (e.g. bold, italic, text)
            url: An optional string containing the URL value if it's present (e.g. "https://www.google.com.au")
        """

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


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    """Converts TextNode object to LeafNode (child of HTMLNode) object

    Depending on the set TextType, it constructs a LeafNode instance with the applicable tag value.

    Args:
        text_node: TextNode instance.

    Returns:
        LeafNode instance, setting the tag value according to the TextNode's TextType value.

    Raises:
        ValueError: An unhandled TextType value was sent.
    """
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

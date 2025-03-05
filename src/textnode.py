from enum import Enum
from typing import override


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

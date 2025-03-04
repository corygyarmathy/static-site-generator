from typing import LiteralString, override
from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list["HTMLNode"],
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag=tag, value=None, children=children, props=props)

    @override
    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError(f"{type(self)} must have a tag.")
        if self.children is None:
            raise ValueError(f"{type(self)} must have children.")

        childhtml: LiteralString = "".join(
            map(lambda child: child.to_html(), self.children)
        )

        return f"<{self.tag}{self.props_to_html()}>{childhtml}</{self.tag}>"

    @override
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"

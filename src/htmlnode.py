from typing import override


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        self.tag: str | None = tag
        self.value: str | None = value
        self.children: list["HTMLNode"] | None = children
        self.props: dict[str, str] | None = props

    @override
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self) -> str:
        htmlString: str = ""
        if not self.props is None:
            for k, v in self.props.items():
                htmlString += f' {k}="{v}"'
        return htmlString


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        value: str,
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag=tag, value=value, props=props)

    @override
    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("LeafNode must have a value.")

        if self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


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

        childhtml = "".join(map(lambda child: child.to_html(), self.children))

        return f"<{self.tag}{self.props_to_html()}>{childhtml}</{self.tag}>"

    @override
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"

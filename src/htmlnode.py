from typing import override


class HTMLNode:
    """Represents a 'block' or 'tag' of HTML content.

    Rarely called directly, typically used by the child classes LeafNode and ParentNode.

    Attributes:
        tag: An optional string indicating the HTML tag value
        value: An optional string indicating the value contained within the HTML tag
        children: An optional list of HTMLNode instances, containing the child HTML tags
        props: An optional dictionary of strings, containing the attributes of the HTML tag.
               For example, a link (<a> tag) might have {"href": "https://www.google.com"}
    """

    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        """Initialises HTMLNode instance from the HTML block information.

        Args:
            tag: An optional string indicating the HTML tag value
            value: An optional string indicating the value contained within the HTML tag
            children: An optional list of HTMLNode instances, containing the child HTML tags
            props: An optional dictionary of strings, containing the attributes of the HTML tag.
                For example, a link (<a> tag) might have {"href": "https://www.google.com"}
        """
        self.tag: str | None = tag
        self.value: str | None = value
        self.children: list["HTMLNode"] | None = children
        self.props: dict[str, str] | None = props

    @override
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

    def to_html(self):
        """Unimplimented method to be overridden by child classes."""
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self) -> str:
        """Converts attributes of the HTML tag to raw HTML as a string.

        Builds a HTML string from the props dictionary using the key and value pairs,
        if the props attribute is not None.

        Args:
            self: gets its values from self.props

        Returns:
            A string of HTML representing the HTML attributes in the props attribute.
        """
        htmlString: str = ""
        if not self.props is None:
            for k, v in self.props.items():
                htmlString += f' {k}="{v}"'
        return htmlString


class LeafNode(HTMLNode):
    """A LeafNode is a HTMLNode that represents a single HTML tag with no children.

    LeafNode instances typically become children of ParentNode instances.

    Attributes:
        tag: An optional string indicating the HTML tag value
        value: An optional string indicating the value contained within the HTML tag
        props: An optional dictionary of strings, containing the attributes of the HTML tag.
               For example, a link (<a> tag) might have {"href": "https://www.google.com"}
    """

    def __init__(
        self,
        tag: str | None,
        value: str,
        props: dict[str, str] | None = None,
    ) -> None:
        """Initialises LeafNode instance from the provided HTML block information.

        Args:
            tag: An optional string indicating the HTML tag value
            value: A string indicating the value contained within the HTML tag
            props: An optional dictionary of strings, containing the attributes of the HTML tag.
                For example, a link (<a> tag) might have {"href": "https://www.google.com"}
        """
        super().__init__(tag=tag, value=value, props=props)

    @override
    def to_html(self) -> str:
        """Converts self to HTML in a string format.

        Returns:
            A string of HTML from self. It includes self.props if that is not None.
        """
        if self.value is None:
            raise ValueError("LeafNode must have a value.")

        if self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    """Represents a HTML tag surrounding child HTMLNode(s).

    ParentNode instances must contain a list of children.
    These children may either be LeafNode(s) or ParentNode(s).
    While HTMLNode(s) can be used, they should not be.

    Attributes:
        tag: An optional string indicating the HTML tag value
        children: A list of HTMLNode instances, containing the child HTML tags
        value: An optional string indicating the value contained within the HTML tag
        props: An optional dictionary of strings, containing the attributes of the HTML tag.
                For example, a link (<a> tag) might have {"href": "https://www.google.com"}
    """

    def __init__(
        self,
        tag: str,
        children: list["HTMLNode"],
        props: dict[str, str] | None = None,
    ) -> None:
        """Initialises ParentNode instance from the provided HTML block information.

        Args:
            tag: An optional string indicating the HTML tag value
            children: A list of HTMLNode instances, containing the child HTML tags
            value: An optional string indicating the value contained within the HTML tag
            props: An optional dictionary of strings, containing the attributes of the HTML tag.
                   For example, a link (<a> tag) might have {"href": "https://www.google.com"}
        """
        super().__init__(tag=tag, value=None, children=children, props=props)

    @override
    def to_html(self) -> str:
        """Converts self to HTML in a string format.

        Returns:
            A string of HTML from self and children.
            It includes self.props if that is not None.

        Raises:
            ValueError: self.tag and self.children must have a value.
        """
        if self.tag is None:
            raise ValueError(f"{type(self)} must have a tag.")
        if self.children is None:
            raise ValueError(f"{type(self)} must have children.")

        childhtml: str = "".join(map(lambda child: child.to_html(), self.children))
        html = f"<{self.tag}{self.props_to_html()}>{childhtml}</{self.tag}>"

        return html

    @override
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"

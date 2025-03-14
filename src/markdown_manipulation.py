import re
from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    """Converts list of TextNode(s) into list of TextNode(s) deliminated by given str

    Builds new list of TextNode(s) with each new TextNode of TextType.TEXT split by
    and TextType set according to the given delimiter and TextType respectively.
    Enables splitting bold, italic, and code Markdown text.

    Designed to be utilised primarily through the function: text_to_textnodes()

    Args:
        old_nodes:
            A list of TextNode(s), can be any TextType.
            Expects the text of the TextNode(s) to be formatted in Markdown.

    Returns:
        A list of TextNode(s) split by the given delimiter and TextType set
        according to the supplied TextType.
    """

    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes: list[TextNode] = []
        sections: list[str] = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    """Extracts images from the given list of TextNode(s) into their own TextNode.

    Builds new list of TextNode(s) with each new TextNode of TextType.IMAGE split by
    the Markdown image links found by extract_markdown_images.

    Designed to be utilised primarily through the function: text_to_textnodes()

    Args:
        old_nodes:
            A list of TextNode(s), can be any TextType.
            Expects the text of the TextNode(s) to be formatted in Markdown.

    Returns:
        A list of TextNode(s) split by each discovered Markdown image.
    """
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        text: str = old_node.text
        img_matches: list[tuple[str, str]] = extract_markdown_images(text)
        if len(img_matches) == 0:
            new_nodes.append(old_node)
            continue
        for img_match in img_matches:
            img_text: str = img_match[0]
            img_url: str = img_match[1]
            sections: list[str] = text.split(f"![{img_text}]({img_url})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":  # Check for: image, no text
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(img_text, TextType.IMAGE, img_url))
            text = sections[1]
        if text != "":  # Check for image, no text
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    """Extracts links from the given list of TextNode(s) into their own TextNode.

    Builds new list of TextNode(s) with each new TextNode of TextType.LINK split by
    the Markdown links found by extract_markdown_links.

    Designed to be utilised primarily through the function: text_to_textnodes()

    Args:
        old_nodes:
            A list of TextNode(s), can be any TextType.
            Expects the text of the TextNode(s) to be formatted in Markdown.

    Returns:
        A list of TextNode(s) split by each discovered Markdown link.
    """
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        text: str = old_node.text
        link_matches: list[tuple[str, str]] = extract_markdown_links(text)
        if len(link_matches) == 0:
            new_nodes.append(old_node)
            continue

        for link_match in link_matches:
            link_text: str = link_match[0]
            link_url: str = link_match[1]
            sections: list[str] = text.split(f"[{link_text}]({link_url})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":  # Check for: link, no text
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            text = sections[1]
        if text != "":  # Check for link, no text
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def extract_markdown_images(markdown: str) -> list[tuple[str, str]]:
    """Converts (Markdown) string into list of tuples(s) of strings.

    tuple[0] is the alt_text of the link.
    tuple[1] is the URL to the link.

    This function is designed to be utilised primarily through the
    function: text_to_textnodes()

    Args:
        text:
            A string input, optionally holding a link in markdown format.
            If no links found, returns empty list.

    Returns:
        A list of tuples(s) containing the alt_text and URL to any links in
        markdown format in the given string input.
    """
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, markdown)
    return matches


def extract_markdown_links(markdown: str) -> list[tuple[str, str]]:
    """Converts (Markdown) string into list of tuples(s) of strings.

    tuple[0] is the alt_text of the image.
    tuple[1] is the URL to the image.

    This function is designed to be utilised primarily through the
    function: text_to_textnodes()

    Args:
        text:
            A string input, optionally holding an image link in markdown format.
            If no images found, returns empty list.

    Returns:
        A list of tuples(s) containing the alt_text and URL to any images in
        markdown format in the given string input.
    """
    pattern: str = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, markdown)
    return matches


def extract_markdown_title(markdown: str) -> str:
    """Finds the Markdown title (H1) in the string.

    Expects only one title in the string.

    Args:
        markdown:
            Markdown-formatted string.

    Returns:
        Title text, stripped of the preceeding '# ' and any
        preceeding or trailing whitespace.

    Raises:
        ValueError: Expects to find one, and only one, title.
    """

    # Find title (H1). Alt is for titles of one char.
    pattern: str = r"^# (\S.*\S|\S)\s*$"
    matches = re.search(pattern, markdown, re.MULTILINE)
    if matches is None:
        raise ValueError("No title found in the markdown provided.")
    return matches.group(1)


def markdown_to_textnodes(markdown: str) -> list[TextNode]:
    """Converts (Markdown) string into list of TextNode(s) of correct TextType.

    Runs the string through the following functions to process it:
    - split_nodes_delimiter: bold, italic, code
    - split_nodes_image: image
    - split_nodes_link: link

    The purpose of this function is to convert blocks of Markdown into TextNode(s)
    and then from there into HTMLNode(s).

    Args:
        text:
            A string input, expected to be in markdown format.
            It would still return if it was not in Markdown,
            but you would get a single TextNode of TextType TEXT.

    Returns:
        A list of TextNode(s) of correct TextType, in sequential order to how
        the text was arranged in the string input.
    """

    nodes = [TextNode(markdown, TextType.TEXT, None)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes

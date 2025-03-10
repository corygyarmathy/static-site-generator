from enum import Enum
import re

from htmlnode import HTMLNode, ParentNode
from markdown_manipulation import markdown_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    """Enum for the type of markdown block."""

    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    """Get each paragraph, sep. by whitespace, of Markdown (a block).

    Splits the given string input, expected to be in Markdown format,
    where there's two new lines (whitespace in between paragraphs).
    To be used with block_to_block_type() to get the type of Markdown
    for the given text (e.g. code, quote, heading etc.)

    Args:
        markdown:
            String expected to be in Markdown format.

    Returns:
        A list of strings, where each string is a 'block' (paragraph)
        of Markdown-formatted text.
    """

    blocks: list[str] = []
    sections: list[str] = markdown.split("\n\n")
    for section in sections:
        section: str = section.strip()
        if section == "":
            continue
        blocks.append(section)
    return blocks


def block_to_block_type(markdown: str) -> BlockType:
    """Match the Markdown 'block' (paragraph) to the type of Markdown.

    Determines if the incoming Markdown-formatted text is of type:
    Heading, Code, Quote, Unordered-List, Ordered-List, or plain-text.

    Args:
        markdown:
            String representing a 'block' (paragraph) of Markdown-formatted
            text, likely from markdown_to_blocks().

    Returns:
        BlockType:
            BlockType enum indicating the type of Markdown contained in
            the block. Used as part of converting Markdown to HTML.
    """
    if re.match(r"^#{1,6}\s.+", markdown):  # Heading
        return BlockType.HEADING
    if re.match(r"^```[\s\S]*?```$", markdown):  # Code
        return BlockType.CODE
    if re.match(r"^>([^\n]*\n>?)*", markdown):  # Blockquote
        return BlockType.QUOTE
    if re.match(r"^- (?:[^\n]*(?:\n- [^\n]*)*)", markdown):  # Unordered list
        return BlockType.ULIST
    if re.match(r"^1\. .*(?:\n(?:\d+)\. .*)*$", markdown):  # Ordered list
        return BlockType.OLIST

    return BlockType.PARAGRAPH  # Else, paragraph


def markdown_to_html_node(markdown: str) -> ParentNode:
    """Process Markdown-formatted string to HTMLNode(s) representing Markdown elements.

    Generates a ParentNode as a HTML "div" tag wrapper for HTMLNode(s) representing
    the Markdown elements in the Markdown-formatted string input.

    Args:
        markdown:
            Markdown-formatted string containing the full text to be converted.

    Returns:
        ParentNode instance as a '<div> tag wrapper, with necessary child HTMLNode(s)
        representing the Markdown elements in the string input.
    """
    blocks: list[str] = markdown_to_blocks(markdown)
    children_nodes: list[HTMLNode] = []
    for block in blocks:
        block_type: BlockType = block_to_block_type(block)
        match block_type:
            # Functions:
            # - Sanitising function: tuple: string to replace, string to replace with
            # - text_to_children(text, process_inline_markdown = True): get TextNodes, generate children
            case BlockType.PARAGRAPH:
                sanitised_block: str = block.replace("\n", " ")
                para_children_nodes: list[HTMLNode] = []
                text_nodes: list[TextNode] = markdown_to_textnodes(sanitised_block)
                for text_node in text_nodes:
                    para_children_nodes.append(text_node_to_html_node(text_node))
                block_node: ParentNode = ParentNode("p", para_children_nodes, None)
                children_nodes.append(block_node)
            case BlockType.HEADING:
                sanitised_block: str = block.replace("\n", " ")
                strip_heading: str = sanitised_block.lstrip("# ")
                para_children_nodes: list[HTMLNode] = []
                text_nodes: list[TextNode] = markdown_to_textnodes(strip_heading)
                # TODO: calculate heading_num from the first child TextNode, rather than the raw string
                #       This is to allow for a generic function to be created, and only heading specific
                #       behaviour to be present in this case.
                heading_num: int = (
                    sanitised_block.__len__() - strip_heading.__len__()
                ) - 1
                tag: str = f"h{heading_num}"
                for text_node in text_nodes:
                    para_children_nodes.append(text_node_to_html_node(text_node))
                block_node: ParentNode = ParentNode(tag, para_children_nodes, None)
                children_nodes.append(block_node)

            case BlockType.CODE:
                para_children_nodes: list[HTMLNode] = []
                # Cut first & last line using string index of '\n'
                text: str = block[block.find("\n") + 1 : block.rfind("\n") + 1]
                text_node: TextNode = TextNode(text, TextType.CODE, None)
                html_node: HTMLNode = text_node_to_html_node(text_node)
                block_node: ParentNode = ParentNode("pre", [html_node], None)
                children_nodes.append(block_node)
            case BlockType.QUOTE:
                sanitised_block: str = block.replace("\n", " ")
                sanitised_block: str = sanitised_block.replace("> ", "")
                para_children_nodes: list[HTMLNode] = []
                text_nodes: list[TextNode] = markdown_to_textnodes(sanitised_block)
                for text_node in text_nodes:
                    para_children_nodes.append(text_node_to_html_node(text_node))
                block_node: ParentNode = ParentNode(
                    "blockquote", para_children_nodes, None
                )
                children_nodes.append(block_node)
            case BlockType.ULIST:
                list_block: str = "".join(
                    f"<li>{line}</li>" for line in block.splitlines()
                )
                list_block: str = list_block.replace("<li>- ", "<li>")
                para_children_nodes: list[HTMLNode] = []
                text_nodes: list[TextNode] = markdown_to_textnodes(list_block)
                for text_node in text_nodes:
                    para_children_nodes.append(text_node_to_html_node(text_node))
                block_node: ParentNode = ParentNode("ul", para_children_nodes, None)
                children_nodes.append(block_node)
            case BlockType.OLIST:
                starting_num: int = find_olist_occurrence(block, 0)
                lines: list[str] = block.splitlines()
                list_block: str = "".join(
                    f"<li>{lines[i].lstrip(f'{starting_num + i}. ')}</li>"
                    for i in range(lines.__len__())
                )
                para_children_nodes: list[HTMLNode] = []
                text_nodes: list[TextNode] = markdown_to_textnodes(list_block)
                for text_node in text_nodes:
                    para_children_nodes.append(text_node_to_html_node(text_node))
                block_node: ParentNode = ParentNode("ol", para_children_nodes, None)
                children_nodes.append(block_node)

    parent_node: ParentNode = ParentNode(tag="div", children=children_nodes, props=None)
    return parent_node


def find_olist_occurrence(text: str, index: int = 0) -> int:
    num: int = 0
    matches: list[str] = re.findall(r"(\d+)\. ", text)
    if matches[index] is not None:
        num = int(matches[index])
    return num


# def str_replace(old_text, new_text, occurrences: int) -> str:


# def find_first_olist_number(text: str) -> int:
#     num: int = 0
#     match: re.Match[str] | None = re.search(r"(\d+)\. ", text)
#     if match is not None:
#         num = int(match.group(1))
#     return num

# def add_tag_to_lines(text: str, tag: str):
#     return "\n".join(f"{tag}{line}\{tag}" for line in text.splitlines())

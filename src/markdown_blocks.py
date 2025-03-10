from enum import Enum
import re

from htmlnode import HTMLNode, ParentNode
from markdown_manipulation import text_to_textnodes


class BlockType(Enum):
    """Enum for the type of markdown block."""

    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered list"
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
    sections = markdown.split("\n\n")
    for section in sections:
        if section == "":
            continue
        blocks.append(section.strip())
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
        match block_to_block_type(block):
            case BlockType.PARAGRAPH:
                text_nodes = text_to_textnodes(block)
            case BlockType.HEADING:
                pass
            case BlockType.CODE:
                pass
            case BlockType.QUOTE:
                pass
            case BlockType.ULIST:
                pass
            case BlockType.OLIST:
                pass

    parent_node = ParentNode(tag="div", children=children_nodes, props=None)
    return parent_node

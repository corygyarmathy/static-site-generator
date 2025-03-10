from enum import Enum
import re

from htmlnode import HTMLNode, ParentNode
from markdown_manipulation import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered list"
    OLIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks: list[str] = []
    sections = markdown.split("\n\n")
    for section in sections:
        if section == "":
            continue
        blocks.append(section.strip())
    return blocks


def block_to_block_type(markdown: str) -> BlockType:
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

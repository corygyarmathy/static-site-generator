import re
from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
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
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        text = old_node.text
        img_matches = extract_markdown_images(text)

        for img_match in img_matches:
            split_nodes = []
            img_text = f"![{img_match[0]}]({img_match[1]})"
            sections = text.split(f"![{img_match[0]}]({img_match[1]})", 1)
            # if len(img_matches[i]) > j + 1:
            #     text = sections[j]
            # if len(sections) % 2 == 0:
            #     raise ValueError("invalid markdown, formatted section not closed")
            for i in range(len(sections)):
                # if sections[i] == "":
                #     continue
                if i % 2 == 0:
                    split_nodes.append(TextNode(sections[i], TextType.TEXT))
                    text = sections[i + 1]
                else:
                    split_nodes.append(
                        TextNode(img_match[0], TextType.IMAGE, img_match[1])
                    )
            new_nodes.extend(split_nodes)
    return new_nodes
def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

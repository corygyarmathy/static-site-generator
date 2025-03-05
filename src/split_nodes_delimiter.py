from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        try:
            split_text = old_node.text.split(delimiter)
        except:
            raise SyntaxError(
                f"Function split_nodes_delimiter passed delimiter {delimiter}, not found in {old_node.text}"
            )
        count: int = 1
        if old_node.text_type == TextType.TEXT:
            for text in split_text:
                match count:
                    case 1:
                        node: TextNode = TextNode(text, TextType.TEXT)
                        count += 1
                    case 2:
                        node: TextNode = TextNode(text, text_type)
                        count += 1
                    case 3:
                        node: TextNode = TextNode(text, TextType.TEXT)
                        count = 1
                    case _:
                        raise IndexError(
                            f"count {count} is invalid in split_nodes_delimiter"
                        )
                new_nodes.append(node)
        else:
            return old_nodes
    return new_nodes

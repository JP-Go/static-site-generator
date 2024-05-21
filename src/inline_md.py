from typing import List
from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: List[TextNode], delimiter: str, text_type: TextType
):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != "text":
            new_nodes.append(node)
            continue
        splited = node.text.split(delimiter)
        if len(splited) % 2 == 0:
            raise ValueError("Invalid markdown syntax. Unclosed formatting delimiter")
        for i, text in enumerate(splited):
            if text == "":
                continue
            new_nodes.extend(
                [TextNode(text, "text") if i % 2 == 0 else TextNode(text, text_type)]
            )
    return new_nodes

""" Functions and typings for handling of markdown blocks

Constants
---------

BlockType : TypeAlias = Literal[ "paragraph", "heading", "code", "quote", "unordered_list", "ordered_list" ]
    TypeAlias representing a block in markdown. A block type can be one of 
    "paragraph", "heading", "code", "quote", "unordered_list", "ordered_list".

"""

import re
from typing import Dict, List, Literal, Sequence, TypeAlias, Callable
from htmlnode import HTMLNode, LeafNode, ParentNode
from convert import text_node_to_html_node
from inline_md import text_to_text_nodes
from textnode import TextNode

BlockType: TypeAlias = Literal[
    "paragraph", "heading", "code", "quote", "ol_list", "ul_list"
]

block_type_paragraph: BlockType = "paragraph"
""" block_type_paragraph : BlockType = "paragraph"
    Represents the paragraph block type. A paragraph is any block of text that
    is not of the other types.
"""
block_type_heading: BlockType = "heading"
""" block_type_heading: BlockType = "heading"
    Represents the heading block type. A heading is any block of text that
    starts with one to six '#' characters followed by text.
"""
block_type_code: BlockType = "code"
""" block_type_code: BlockType = "code"
    Represents the code block type. A code block is any block of text that
    starts and ends with '```' (three backticks).
"""
block_type_quote: BlockType = "quote"
""" block_type_quote: BlockType = "quote"
    Represents the quote block type. A quote block is any block of text that has
    the '>' (greater than sign) in **every** line.
"""
block_type_ordered_list: BlockType = "ol_list"
""" block_type_ordered_list: BlockType = "ordered_list"
    Represents the ordered list block type. An ordered list block is any block
    that has a number followed by a dot and a space in every line. The block
    must start with 1 (one) and increase by one every line.
"""
block_type_unordered_list: BlockType = "ul_list"
"""block_type_unordered_list: BlockType = "unordered_list"
    Represents the unordered list block type. A unordered list is any block that
    that has a '*' (start) caracther in every line, or that has a '-' (dash) caracther in
    every line.
"""


def markdown_to_blocks(markdown: str) -> List[str]:
    """separates a string representing markdown text into blocks. markdown
    blocks are separated by a sequence of two newline caracthers '\\n\\n'

    Parameters
    ----------
    markdown : str
        A string representing markdown text

    Returns
    -------
    blocks : list of str
        the strings representing markdown blocks in a list
    """
    return [block.strip() for block in re.split(r"\n{2,}", markdown)]


def block_to_block_type(block: str) -> BlockType:
    """infers the type of some markdown block based on its contents

    Parameters
    ----------
    block : str
        A string representing a block of markdown text. It can have more than
        one line

    Returns
    -------
    block_type : BlockType
        the type of block infered from the content of the block
    """
    lines = [line.strip() for line in block.split("\n")]
    if re.match(r"#{1,6}\s", block):
        return block_type_heading
    if block.startswith("```") and block.endswith("```"):
        return block_type_code
    if all(line.startswith(">") for line in lines):
        return block_type_quote
    if all(line.startswith("* ") for line in lines) or all(
        line.startswith("- ") for line in lines
    ):
        return block_type_unordered_list
    if all(line.startswith(f"{i + 1}. ") for (i, line) in enumerate(lines)):
        return block_type_ordered_list
    return block_type_paragraph


def text_nodes_to_html_children(text_nodes: Sequence[TextNode]) -> Sequence[HTMLNode]:
    html_nodes = [text_node_to_html_node(node) for node in text_nodes]
    return html_nodes


def create_text_to_html_converter(
    preprocessor: Callable[[str], List[str]],
    converter: Callable[[List[str]], HTMLNode],
):
    def html_converter(text: str) -> HTMLNode:
        lines = preprocessor(text)
        result = converter(lines)
        return result

    return html_converter


def _flattened_nodes_list(lines: List[str]) -> List[HTMLNode]:
    nodes = []
    for line in lines:
        if line.strip() == "":
            continue
        nodes.extend(text_nodes_to_html_children(text_to_text_nodes(line)))
    return nodes


def _quote_block_preprocessor(quote: str) -> List[str]:
    removed_quote_marker = [line.strip("> ").strip() for line in quote.split("\n")]
    line = " ".join(removed_quote_marker)
    return [line.strip()]


def _quote_block_converter(lines: List[str]) -> HTMLNode:
    html_nodes = _flattened_nodes_list(lines)
    return ParentNode(tag="blockquote", children=html_nodes)


quote_block_to_htmlnode = create_text_to_html_converter(
    _quote_block_preprocessor, _quote_block_converter
)
"""
converts a markdown quote into a HTML node

Parameters
----------
quote : str
    A string representing an quote block. It may have more than one line

Returns
-------
html_node : HTMLNode
    A html node representing the quote block
"""


# TODO: remove possibility of returning an empty list
def _paragraph_node_preprocessor(paragraph: str) -> List[str]:
    single_line = " ".join(
        [line.strip() for line in paragraph.split("\n") if line.strip() != ""]
    )
    return [single_line]


def _paragraph_node_conveter(lines: List[str]) -> HTMLNode:
    html_nodes = _flattened_nodes_list(lines)
    return ParentNode(tag="p", children=html_nodes)


paragraph_block_to_htmlnode = create_text_to_html_converter(
    _paragraph_node_preprocessor, _paragraph_node_conveter
)
"""
converts a markdown paragraph into a HTML node

Parameters
----------
paragraph : str
    A string representing an paragraph block. It may have more than one line

Returns
-------
html_node : HTMLNode
    A html node representing the paragraph block
"""


def _nested_nodes_list(lines: List[str]) -> List[Sequence[HTMLNode]]:
    nodes = [text_nodes_to_html_children(text_to_text_nodes(line)) for line in lines]
    return nodes


def _ol_block_preprocessor(ol: str) -> List[str]:
    return [line.strip()[3:] for line in ol.split("\n") if line.strip() != ""]


def _ol_block_converter(lines: List[str]) -> HTMLNode:
    html_nodes = _nested_nodes_list(lines)
    return ParentNode(
        tag="ol",
        children=[ParentNode(tag="li", children=nodes) for nodes in html_nodes],
    )


ol_block_to_htmlnode = create_text_to_html_converter(
    _ol_block_preprocessor, _ol_block_converter
)
"""
converts a markdown ordered list into a HTML node

Parameters
----------
ol : str
    A string representing an ordered list block. It may have more than one line

Returns
-------
html_node : HTMLNode
    A html node representing the ordered list block
"""


def _ul_block_preprocessor(ul: str) -> List[str]:
    return [line.strip()[2:] for line in ul.split("\n") if line.strip() != ""]


def _ul_block_converter(lines: List[str]) -> HTMLNode:
    html_nodes = _nested_nodes_list(lines)
    return ParentNode(
        tag="ul",
        children=[ParentNode(tag="li", children=nodes) for nodes in html_nodes],
    )


ul_block_to_htmlnode = create_text_to_html_converter(
    _ul_block_preprocessor, _ul_block_converter
)
"""
converts a markdown unordered list into a HTML node

Parameters
----------
ul : str
    A string representing an unordered list block. It may have more than one line

Returns
-------
html_node : HTMLNode
    A html node representing the unordered list block
"""


# NOTE: Using function composition here would require creating an adapter for
# the create_text_to_html_converter interface which would not be justifiable for
# only one use case.
def heading_block_to_htmlnode(heading: str) -> HTMLNode:
    """
    converts a heading block to a html node

    Parameters
    ----------
    heading : str
        A string representing a heading block. It will have only one line

    Returns
    -------
    html_node : HTMLNode
        A html node representing the heading block

    """
    heading_level = heading.count("#")
    if heading_level > 6 or heading_level < 1:
        raise ValueError("Invalid heading level")
    heading_content = heading.strip("# ")
    html_nodes = _flattened_nodes_list([heading_content])
    return ParentNode(tag="h" + str(heading_level), children=html_nodes)


def code_block_to_htmlnode(code: str) -> HTMLNode:
    """
    converts a markdown code block into a HTML node

    Parameters
    ----------
    code : str
        A string representing a code block. It may have more than one line

    Returns
    -------
    html_node : HTMLNode
        A html node representing the code block
    """
    value = "\n".join(
        line.strip() for line in code.lstrip("` \n").rstrip("` \n").split("\n")
    )
    return ParentNode(tag="pre", children=[LeafNode("code", value=value)])


_map_block_to_transformer: Dict[BlockType, Callable[[str], HTMLNode]] = {
    "paragraph": paragraph_block_to_htmlnode,
    "code": code_block_to_htmlnode,
    "ol_list": ol_block_to_htmlnode,
    "ul_list": ul_block_to_htmlnode,
    "heading": heading_block_to_htmlnode,
    "quote": quote_block_to_htmlnode,
}


def markdown_to_html_node(markdown: str) -> HTMLNode:
    """
    converts a markdown text into a HTML node

    Parameters
    ----------
    markdown : str
        A string representing a markdown text

    Returns
    -------
    html_node : HTMLNode
        A html node representing the markdown text
    """
    markdown_blocks = markdown_to_blocks(markdown)
    html_blocks = [
        _map_block_to_transformer[block_to_block_type(block)](block.strip())
        for block in markdown_blocks
    ]
    return ParentNode(tag="div", children=html_blocks)

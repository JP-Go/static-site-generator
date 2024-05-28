""" Functions and typings for handling of markdown blocks

Constants
---------

BlockType : TypeAlias = Literal[ "paragraph", "heading", "code", "quote", "unordered_list", "ordered_list" ]
    TypeAlias representing a block in markdown. A block type can be one of 
    "paragraph", "heading", "code", "quote", "unordered_list", "ordered_list".

"""

import re
from typing import List, Literal, TypeAlias

BlockType: TypeAlias = Literal[
    "paragraph", "heading", "code", "quote", "unordered_list", "ordered_list"
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

block_type_ordered_list: BlockType = "ordered_list"
""" block_type_ordered_list: BlockType = "ordered_list"
    Represents the ordered list block type. An ordered list block is any block
    that has a number followed by a dot and a space in every line. The block
    must start with 1 (one) and increase by one every line.
"""
block_type_unordered_list: BlockType = "unordered_list"
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
    return [block.strip() for block in markdown.split("\n\n")]


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
    lines = block.split("\n")
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

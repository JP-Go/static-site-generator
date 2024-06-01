import unittest
import re

from block_md import (
    code_block_to_htmlnode,
    heading_block_to_htmlnode,
    markdown_to_blocks,
    block_type_paragraph,
    block_type_ordered_list,
    block_type_unordered_list,
    block_type_quote,
    block_type_code,
    block_type_heading,
    block_to_block_type,
    markdown_to_html_node,
    ol_block_to_htmlnode,
    ul_block_to_htmlnode,
    paragraph_block_to_htmlnode,
    quote_block_to_htmlnode,
)
from htmlnode import LeafNode, ParentNode


class TestMarkdownToBlocks(unittest.TestCase):

    def test_separate_blocks(self):
        input = """
            # This is a heading

            This is a paragraph of text. It has some **bold** and *italic* words inside of it.

            * This is a list item
            * This is another list item
        """
        expected_count = 3

        self.assertEqual(len(markdown_to_blocks(input)), expected_count)

    def test_separate_blocks_len(self):
        input = """
            # This is a heading

            This is a paragraph of text. It has some **bold**
            and *italic* words inside of it.

            * This is a list item
            * This is another list item
        """
        result = markdown_to_blocks(input)
        self.assertTrue(all([re.match(r"^\s+", s) is None for s in result]))
        self.assertTrue(all([re.match(r"\s+$", s) is None for s in result]))

    def test_separate_block(self):
        input = """
            # This is a heading
        """
        expected_count = 1

        self.assertEqual(len(markdown_to_blocks(input)), expected_count)

    def test_strip_spaces(self):
        input = """
            # This is a heading      
        """
        expected_count = 1

        result = markdown_to_blocks(input)
        self.assertEqual(len(result), expected_count)
        self.assertTrue(all([re.match(r"^\s+", s) is None for s in result]))
        self.assertTrue(all([re.match(r"\s+$", s) is None for s in result]))


class TestBlockToBlockType(unittest.TestCase):

    def test_heading_block(self):
        for i in range(1, 7):
            self.assertEqual(
                block_type_heading, block_to_block_type("#" * i + f" heading {i}")
            )

    def test_quote_block(self):
        input = ">some quote\n>someone said someday"
        self.assertEqual(block_type_quote, block_to_block_type(input))

    def test_unordered_list_block(self):
        input = "* some item\n* some other item."
        self.assertEqual(block_type_unordered_list, block_to_block_type(input))

    def test_ordered_list_block(self):
        input = "1. some item\n2. some other item."
        self.assertEqual(block_type_ordered_list, block_to_block_type(input))

    def test_code_block(self):
        input = "``` some='python'\n print(some)```"
        self.assertEqual(block_type_code, block_to_block_type(input))

    def test_paragraph_block(self):
        input = "A paragraph, with\n multiple lines"
        self.assertEqual(block_type_paragraph, block_to_block_type(input))

    def test_paragraph_block_that_looks_like_code_block(self):
        input = "``` some code unfinished"
        self.assertEqual(block_type_paragraph, block_to_block_type(input))

    def test_paragraph_block_that_looks_like_unordered_list(self):
        input = "*some list that is not done right"
        self.assertEqual(block_type_paragraph, block_to_block_type(input))

    def test_paragraph_block_that_looks_like_ordered_list(self):
        input = "1.some list that is not done right"
        self.assertEqual(block_type_paragraph, block_to_block_type(input))

    def test_paragraph_block_that_looks_like_heading(self):
        input = "#some heading with no space"
        self.assertEqual(block_type_paragraph, block_to_block_type(input))


class TestQuoteBlockToHTMLNode(unittest.TestCase):

    def test_basic_quote(self):
        input = """
> A quote with some meaninfull text
> That was said by someone i don't know
"""
        expected = ParentNode(
            tag="blockquote",
            children=[
                LeafNode(
                    tag=None,
                    value="A quote with some meaninfull text That was said by someone i don't know",
                ),
            ],
        )
        result = quote_block_to_htmlnode(input)
        self.assertEqual(expected, result)

    def test_quote_with_bolded_text(self):
        input = """
        > A quote with some **meaninfull** text
        > That was said by someone i don't know
        """
        expected = ParentNode(
            tag="blockquote",
            children=[
                LeafNode(tag=None, value="A quote with some "),
                LeafNode(tag="b", value="meaninfull"),
                LeafNode(tag=None, value=" text That was said by someone i don't know"),
            ],
        )
        result = quote_block_to_htmlnode(input)
        self.assertEqual(expected, result)

    def test_quote_with_misc_text(self):
        input = """
        > A quote with some **meaninfull** text
        > That was said by *someone* i don't know
        > And it has `some code in it`.
        """
        expected = ParentNode(
            tag="blockquote",
            children=[
                LeafNode(tag=None, value="A quote with some "),
                LeafNode(tag="b", value="meaninfull"),
                LeafNode(tag=None, value=" text That was said by "),
                LeafNode(tag="i", value="someone"),
                LeafNode(tag=None, value=" i don't know And it has "),
                LeafNode(tag="code", value="some code in it"),
                LeafNode(tag=None, value="."),
            ],
        )
        result = quote_block_to_htmlnode(input)
        self.assertEqual(expected, result)


class TestCodeBlockToHTML(unittest.TestCase):
    def test_basic_code(self):
        input = """
        ```
        console.log("this is javascript")
        ```
        """
        expected = ParentNode(
            tag="pre",
            children=[LeafNode(tag="code", value='console.log("this is javascript")')],
        )
        result = code_block_to_htmlnode(input)
        self.assertEqual(expected, result)

    def test_multiline_code(self):
        input = """
        ```
        const c = "some constant"
        console.log(c)
        ```
        """
        expected = ParentNode(
            tag="pre",
            children=[
                LeafNode(tag="code", value='const c = "some constant"\nconsole.log(c)')
            ],
        )
        result = code_block_to_htmlnode(input)
        self.assertEqual(expected, result)


class TestHeadingBlockToHTML(unittest.TestCase):

    def test_heading_basic(self):
        for i in range(1, 7):
            input = "#" * (i) + " Some heading"
            expected = ParentNode(
                tag=f"h{i}", children=[LeafNode(tag=None, value="Some heading")]
            )
            result = heading_block_to_htmlnode(input)
            self.assertEqual(expected, result)

    def test_heading_misc(self):
        for i in range(1, 7):
            input = "#" * (i) + " Some **bolded** heading"
            expected = ParentNode(
                tag=f"h{i}",
                children=[
                    LeafNode(tag=None, value="Some "),
                    LeafNode(tag="b", value="bolded"),
                    LeafNode(tag=None, value=" heading"),
                ],
            )
            result = heading_block_to_htmlnode(input)
            self.assertEqual(expected, result)


class TestParagraphBlockToHTML(unittest.TestCase):
    def test_basic_paragraph(self):
        input = """
        Some paragraph that talks about
        markdown code as a form of communication
        between members of a developer team.
        """
        expected = ParentNode(
            tag="p",
            children=[
                LeafNode(
                    tag=None,
                    value="Some paragraph that talks about markdown code as a form of communication between members of a developer team.",
                )
            ],
        )
        result = paragraph_block_to_htmlnode(input)
        self.assertEqual(expected, result)

    def test_paragraph_with_inline_md(self):
        input = """
        Some paragraph that **talks about**
        markdown code as a *form of* communication
        between `members` of a developer team.
        Here's an image: ![image](https://picsum.photo/200).
        """
        children = [
            LeafNode(tag=None, value="Some paragraph that "),
            LeafNode(tag="b", value="talks about"),
            LeafNode(tag=None, value=" markdown code as a "),
            LeafNode(tag="i", value="form of"),
            LeafNode(tag=None, value=" communication between "),
            LeafNode(tag="code", value="members"),
            LeafNode(tag=None, value=" of a developer team. Here's an image: "),
            LeafNode(
                tag="img",
                value="",
                props={"src": "https://picsum.photo/200", "alt": "image"},
            ),
            LeafNode(tag=None, value="."),
        ]
        expected = ParentNode(tag="p", children=children)
        result = paragraph_block_to_htmlnode(input)
        self.assertEqual(expected, result)


class TestOLBlockToHTMLNode(unittest.TestCase):
    def test_basic_ol(self):
        input = """
        1. list item one
        2. list item two
        3. list item three
        """

        children = [
            ParentNode(tag="li", children=[LeafNode(tag=None, value="list item one")]),
            ParentNode(tag="li", children=[LeafNode(tag=None, value="list item two")]),
            ParentNode(
                tag="li", children=[LeafNode(tag=None, value="list item three")]
            ),
        ]
        expected = ParentNode(tag="ol", children=children)
        result = ol_block_to_htmlnode(input)
        self.assertEqual(expected, result)

    def test_ol_with_inline_md(self):
        input = """
        1. list **item** one
        2. list item *two*
        3. `list` item three
        """

        children = [
            ParentNode(
                tag="li",
                children=[
                    LeafNode(tag=None, value="list "),
                    LeafNode(tag="b", value="item"),
                    LeafNode(tag=None, value=" one"),
                ],
            ),
            ParentNode(
                tag="li",
                children=[
                    LeafNode(tag=None, value="list item "),
                    LeafNode(tag="i", value="two"),
                ],
            ),
            ParentNode(
                tag="li",
                children=[
                    LeafNode(tag="code", value="list"),
                    LeafNode(tag=None, value=" item three"),
                ],
            ),
        ]
        expected = ParentNode(tag="ol", children=children)
        result = ol_block_to_htmlnode(input)
        self.assertEqual(expected, result)


class TestULBlockToHTMLNode(unittest.TestCase):
    def test_basic_ol(self):
        input = """
        * list item one
        * list item two
        * list item three
        """

        children = [
            ParentNode(tag="li", children=[LeafNode(tag=None, value="list item one")]),
            ParentNode(tag="li", children=[LeafNode(tag=None, value="list item two")]),
            ParentNode(
                tag="li", children=[LeafNode(tag=None, value="list item three")]
            ),
        ]
        expected = ParentNode(tag="ul", children=children)
        result = ul_block_to_htmlnode(input)
        self.assertEqual(expected, result)

    def test_ul_with_inline_md(self):
        input = """
        - list **item** one
        - list item *two*
        - `list` item three
        """

        children = [
            ParentNode(
                tag="li",
                children=[
                    LeafNode(tag=None, value="list "),
                    LeafNode(tag="b", value="item"),
                    LeafNode(tag=None, value=" one"),
                ],
            ),
            ParentNode(
                tag="li",
                children=[
                    LeafNode(tag=None, value="list item "),
                    LeafNode(tag="i", value="two"),
                ],
            ),
            ParentNode(
                tag="li",
                children=[
                    LeafNode(tag="code", value="list"),
                    LeafNode(tag=None, value=" item three"),
                ],
            ),
        ]
        expected = ParentNode(tag="ul", children=children)
        result = ul_block_to_htmlnode(input)
        self.assertEqual(expected, result)


class TestMarkdownToHTML(unittest.TestCase):
    def test_basic_md(self):
        input = """
        # A simple markdown document

        I have a paragraph and a list:

        * item 1
        * item 2

        And a code block as well

        ```
        print("hello, world")
        ```
        """
        expected = ParentNode(
            tag="div",
            children=[
                ParentNode(
                    tag="h1",
                    children=[LeafNode(tag=None, value="A simple markdown document")],
                ),
                ParentNode(
                    tag="p",
                    children=[
                        LeafNode(tag=None, value="I have a paragraph and a list:")
                    ],
                ),
                ParentNode(
                    tag="ul",
                    children=[
                        ParentNode(
                            tag="li", children=[LeafNode(tag=None, value="item 1")]
                        ),
                        ParentNode(
                            tag="li", children=[LeafNode(tag=None, value="item 2")]
                        ),
                    ],
                ),
                ParentNode(
                    tag="p",
                    children=[LeafNode(tag=None, value="And a code block as well")],
                ),
                ParentNode(
                    tag="pre",
                    children=[LeafNode(tag="code", value='print("hello, world")')],
                ),
            ],
        )
        result = markdown_to_html_node(input)
        self.assertEqual(expected, result)

    def test_markdown_with_inline_md(self):
        input = """
        # A simple markdown document

        I have a **paragraph** and a list:

        * item 1
        * item 2

        And a `code block` as well

        ```
        print("hello, world")
        ```
        """
        expected = ParentNode(
            tag="div",
            children=[
                ParentNode(
                    tag="h1",
                    children=[LeafNode(tag=None, value="A simple markdown document")],
                ),
                ParentNode(
                    tag="p",
                    children=[
                        LeafNode(tag=None, value="I have a "),
                        LeafNode(tag="b", value="paragraph"),
                        LeafNode(tag=None, value=" and a list:"),
                    ],
                ),
                ParentNode(
                    tag="ul",
                    children=[
                        ParentNode(
                            tag="li", children=[LeafNode(tag=None, value="item 1")]
                        ),
                        ParentNode(
                            tag="li", children=[LeafNode(tag=None, value="item 2")]
                        ),
                    ],
                ),
                ParentNode(
                    tag="p",
                    children=[
                        LeafNode(tag=None, value="And a "),
                        LeafNode(tag="code", value="code block"),
                        LeafNode(tag=None, value=" as well"),
                    ],
                ),
                ParentNode(
                    tag="pre",
                    children=[LeafNode(tag="code", value='print("hello, world")')],
                ),
            ],
        )
        result = markdown_to_html_node(input)
        self.assertEqual(expected, result)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
            html,
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
            html,
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
            html,
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
            html,
        )


if __name__ == "__main__":
    unittest.main()

import unittest
import re

from block_md import (
    markdown_to_blocks,
    block_type_paragraph,
    block_type_ordered_list,
    block_type_unordered_list,
    block_type_quote,
    block_type_code,
    block_type_heading,
    block_to_block_type,
)


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


if __name__ == "__main__":
    unittest.main()

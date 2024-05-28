import unittest
import re

from block_md import markdown_to_blocks


class TestBlockMD(unittest.TestCase):

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


if __name__ == "__main__":
    unittest.main()

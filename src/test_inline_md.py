import unittest
from inline_md import split_nodes_delimiter
from textnode import TextNode


class TestSplitNodes(unittest.TestCase):

    def test_code_split(self):
        node = TextNode("This is text with a `code block` word", "text")
        new_nodes = split_nodes_delimiter([node], "`", "code")
        result = [
            TextNode("This is text with a ", "text"),
            TextNode("code block", "code"),
            TextNode(" word", "text"),
        ]
        self.assertSequenceEqual(new_nodes, result)

    def test_bold_split(self):
        node = TextNode("This is text with a **bold block** word", "text")
        new_nodes = split_nodes_delimiter([node], "**", "bold")
        result = [
            TextNode("This is text with a ", "text"),
            TextNode("bold block", "bold"),
            TextNode(" word", "text"),
        ]
        self.assertSequenceEqual(new_nodes, result)

    def test_italic_split(self):
        node = TextNode("This is text with a *italic block* word", "text")
        new_nodes = split_nodes_delimiter([node], "*", "italic")
        result = [
            TextNode("This is text with a ", "text"),
            TextNode("italic block", "italic"),
            TextNode(" word", "text"),
        ]
        self.assertSequenceEqual(new_nodes, result)

    def test_multiple_italic_split(self):
        node = TextNode(
            "This is text with a *italic block* word. And another one here: *This one* right",
            "text",
        )
        new_nodes = split_nodes_delimiter([node], "*", "italic")
        result = [
            TextNode("This is text with a ", "text"),
            TextNode("italic block", "italic"),
            TextNode(" word. And another one here: ", "text"),
            TextNode("This one", "italic"),
            TextNode(" right", "text"),
        ]
        self.assertSequenceEqual(new_nodes, result)

    def test_multiple_italic_and_bold(self):
        node = TextNode(
            "This is text with a *italic block* word. And this one is bolded **This one**",
            "text",
        )
        new_nodes = split_nodes_delimiter([node], "**", "bold")
        new_nodes = split_nodes_delimiter([*new_nodes], "*", "italic")
        result = [
            TextNode("This is text with a ", "text"),
            TextNode("italic block", "italic"),
            TextNode(" word. And this one is bolded ", "text"),
            TextNode("This one", "bold"),
        ]
        self.assertSequenceEqual(new_nodes, result)

    def test_raise_if_unbalanced_delimiter(self):
        node = TextNode(
            "I'm umbalanced on purpose `code starts but does not end", "text"
        )
        self.assertRaisesRegex(
            ValueError,
            "Invalid markdown syntax. Unclosed formatting delimiter",
            lambda: split_nodes_delimiter([node], "`", "code"),
        )


if __name__ == "__main__":
    unittest.main()

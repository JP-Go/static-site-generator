import unittest
from inline_md import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
)
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


class TestExtractImages(unittest.TestCase):
    def test_extracts_one_image(self):
        input = "Some image here: ![image](https://here.com)"
        expected = [("image", "https://here.com")]
        self.assertEqual(extract_markdown_images(input), expected)

    def test_extracts_more_than_one_image(self):
        input = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        expected = [
            (
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            (
                "another",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
            ),
        ]
        self.assertEqual(extract_markdown_images(input), expected)

    def test_extracts_no_image(self):
        input = "There is no image in this"
        expected = []
        self.assertEqual(extract_markdown_images(input), expected)

    def test_does_not_match_links(self):
        input = (
            "There is no image in this but there is a link [here](https://google.com)"
        )
        expected = []
        self.assertEqual(extract_markdown_images(input), expected)


class TestExtractLinks(unittest.TestCase):
    def test_extracts_one_link(self):
        input = "Some link here: [link](https://here.com)"
        expected = [("link", "https://here.com")]
        self.assertEqual(extract_markdown_links(input), expected)

    def test_extracts_more_than_one_link(self):
        input = "This is text with an [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and [another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        expected = [
            (
                "link",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            (
                "another",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
            ),
        ]
        self.assertEqual(extract_markdown_links(input), expected)

    def test_extracts_no_link(self):
        input = "There is no link in this"
        expected = []
        self.assertEqual(extract_markdown_links(input), expected)

    def test_does_not_extract_images(self):
        input = "There is no link in this but theres an image ![here](https://some-image-here)"
        expected = []
        self.assertEqual(extract_markdown_links(input), expected)


class TestSplitImages(unittest.TestCase):

    def test_multiple_images(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            "text",
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", "text"),
            TextNode(
                "image",
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and another ", "text"),
            TextNode(
                "second image",
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
            ),
        ]
        self.assertEqual(expected, new_nodes)

    def test_one_image(self):
        node = TextNode(
            (
                "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)"
                " and no other image"
            ),
            "text",
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", "text"),
            TextNode(
                "image",
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and no other image", "text"),
        ]
        self.assertEqual(expected, new_nodes)

    def test_one_image_and_link(self):
        node = TextNode(
            (
                "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)"
                " and no other image but a link [link](https://google.com)"
            ),
            "text",
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", "text"),
            TextNode(
                "image",
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(
                " and no other image but a link [link](https://google.com)", "text"
            ),
        ]
        self.assertEqual(expected, new_nodes)

    def test_no_image_and_link(self):
        node = TextNode(
            ("This is text with no image" " and a link [link](https://google.com)"),
            "text",
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode(
                "This is text with no image and a link [link](https://google.com)",
                "text",
            ),
        ]
        self.assertEqual(expected, new_nodes)

    def test_just_text(self):
        node = TextNode(
            ("This is text with no image and no links"),
            "text",
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode(
                "This is text with no image and no links",
                "text",
            ),
        ]
        self.assertEqual(expected, new_nodes)


class TestSplitLinks(unittest.TestCase):
    def test_multiple_links(self):
        node = TextNode(
            "This is text with an [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another [second link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            "text",
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with an ", "text"),
            TextNode(
                "link",
                "link",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and another ", "text"),
            TextNode(
                "second link",
                "link",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
            ),
        ]
        self.assertEqual(expected, new_nodes)

    def test_one_link(self):
        node = TextNode(
            (
                "This is text with an [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)"
                " and no other link"
            ),
            "text",
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with an ", "text"),
            TextNode(
                "link",
                "link",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and no other link", "text"),
        ]
        self.assertEqual(expected, new_nodes)

    def test_one_image_and_link(self):
        node = TextNode(
            (
                "This is text with an [link1](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)"
                " and an image ![link2](https://google.com)"
            ),
            "text",
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with an ", "text"),
            TextNode(
                "link1",
                "link",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and an image ![link2](https://google.com)", "text"),
        ]
        self.assertEqual(expected, new_nodes)

    def test_no_link_and_an_image(self):
        node = TextNode(
            ("This is text with no link and an image ![like this](https://google.com)"),
            "text",
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode(
                "This is text with no link and an image ![like this](https://google.com)",
                "text",
            ),
        ]
        self.assertEqual(expected, new_nodes)

    def test_just_text(self):
        node = TextNode(
            "This is text with no image and no links",
            "text",
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode(
                "This is text with no image and no links",
                "text",
            ),
        ]
        self.assertEqual(expected, new_nodes)


if __name__ == "__main__":
    unittest.main()

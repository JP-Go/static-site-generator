import unittest
from convert import text_node_to_html_node
from textnode import TextNode
from htmlnode import LeafNode


class TestConvert(unittest.TestCase):

    def test_node_text(self):
        input = TextNode("text node", "text")
        expected = LeafNode(None, "text node")
        result = text_node_to_html_node(input)
        self.assertEqual(result, expected)

    def test_node_bold(self):
        input = TextNode("bold node", "bold")
        expected = LeafNode("b", "bold node")
        result = text_node_to_html_node(input)
        self.assertEqual(result, expected)

    def test_node_italic(self):
        input = TextNode("italic node", "italic")
        expected = LeafNode("i", "italic node")
        result = text_node_to_html_node(input)
        self.assertEqual(result, expected)

    def test_node_code(self):
        input = TextNode("code node", "code")
        expected = LeafNode("code", "code node")
        result = text_node_to_html_node(input)
        self.assertEqual(result, expected)

    def test_node_link(self):
        input = TextNode("link somewhere", "link", "https://google.com")
        expected = LeafNode("a", "link somewhere", props={"href": "https://google.com"})
        result = text_node_to_html_node(input)
        self.assertEqual(result, expected)

    def test_node_image(self):
        input = TextNode("some image", "image", "https://google.com")
        expected = LeafNode(
            "img", "", props={"src": "https://google.com", "alt": "some image"}
        )
        result = text_node_to_html_node(input)
        self.assertEqual(result, expected)

    def test_raises_link_missing_url(self):
        input = TextNode("link somewhere", "link")
        self.assertRaisesRegex(
            ValueError,
            "Link without a url",
            lambda: text_node_to_html_node(input),
        )

    def test_raises_image_missing_url(self):
        input = TextNode("some image", "image")
        self.assertRaisesRegex(
            ValueError,
            "Image without a url",
            lambda: text_node_to_html_node(input),
        )

    def test_raises_invalid_type(self):
        input = TextNode("text node", "invalid")  # type: ignore on purpose
        self.assertRaisesRegex(
            ValueError,
            "Invalid text node type",
            lambda: text_node_to_html_node(input),
        )

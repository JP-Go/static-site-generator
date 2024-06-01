import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html_with_none(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_empty_dict(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_dict(self):
        node = HTMLNode(props={"class": "test"})
        self.assertEqual(node.props_to_html(), 'class="test"')

    def test_props_to_html_with_multiple_attrs(self):
        node = HTMLNode(
            props={
                "class": "test",
                "contenteditable": "yes",
                "dir": "ltr",
            }
        )
        self.assertEqual(
            node.props_to_html(), 'class="test" contenteditable="yes" dir="ltr"'
        )

    def test_props_to_html_duplicate_props(self):
        node = HTMLNode(
            props={
                "class": "test",
                "class": "test2",
                "contenteditable": "yes",
                "contenteditable": "no",
                "dir": "rtl",
                "dir": "ltr",
            }
        )
        self.assertEqual(
            node.props_to_html(), 'class="test2" contenteditable="no" dir="ltr"'
        )


class TestLeafNode(unittest.TestCase):

    def test_to_html_raises_if_no_value(self):
        leaf = LeafNode("p")
        self.assertRaises(
            ValueError,
            lambda: leaf.to_html(),
        )

    def test_to_html_p_tag(self):
        leaf = LeafNode("p", "some content")
        expected = "<p>some content</p>"
        self.assertEqual(
            leaf.to_html(),
            expected,
            "Did not render the correct html"
            + f"\n expected {expected}\n got {leaf.to_html()}",
        )

    def test_to_html_p_tag_with_props(self):
        leaf = LeafNode("p", "some content", {"class": "text"})
        expected = '<p class="text">some content</p>'
        self.assertEqual(
            leaf.to_html(),
            expected,
            "Did not render the correct html"
            + f"\n expected {expected}\n got {leaf.to_html()}",
        )

    def test_to_html_no_tag(self):
        leaf = LeafNode(value="some content")
        expected = "some content"
        self.assertEqual(
            leaf.to_html(),
            expected,
            "Did not render the correct html"
            + f"\n expected {expected}\n got {leaf.to_html()}",
        )

    def test_to_html_no_tag_ignore_props(self):
        leaf = LeafNode(None, "some content", {"class": "text"})
        expected = "some content"
        self.assertEqual(
            leaf.to_html(),
            expected,
            "Did not render the correct html"
            + f"\n expected {expected}\n got {leaf.to_html()}",
        )


class TestParentNode(unittest.TestCase):
    def test_raises_if_no_tag(self):
        parent = ParentNode(None, [LeafNode("i", "italic")])
        self.assertRaisesRegex(ValueError, "must have a tag", lambda: parent.to_html())

    def test_raises_if_no_children_no_list(self):
        parent = ParentNode(
            "p",
        )
        self.assertRaisesRegex(
            ValueError, "must have at least one child", lambda: parent.to_html()
        )

    def test_one_child(self):
        parent = ParentNode("p", [LeafNode("i", "Italic text")])
        expected = "<p><i>Italic text</i></p>"
        self.assertEqual(
            parent.to_html(),
            expected,
        )

    def test_one_child_no_tag_in_child(self):
        parent = ParentNode("p", [LeafNode(None, "some text")])
        expected = "<p>some text</p>"
        self.assertEqual(
            parent.to_html(),
            expected,
        )

    def test_multiple_leaf_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        node.to_html()
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(
            node.to_html(),
            expected,
        )

    def test_single_parent_node_as_child(self):
        parent = ParentNode(
            "p",
            [
                ParentNode(
                    "li",
                    [
                        LeafNode(None, "some text"),
                        LeafNode("i", "italic text"),
                        LeafNode("b", "bold text"),
                    ],
                )
            ],
        )
        expected = "<p><li>some text<i>italic text</i><b>bold text</b></li></p>"
        self.assertEqual(
            parent.to_html(),
            expected,
        )

    def test_single_parent_node_as_child_with_props(self):
        parent = ParentNode(
            "p",
            [
                ParentNode(
                    "li",
                    [
                        LeafNode(None, "some text"),
                        LeafNode("i", "italic text"),
                        LeafNode("b", "bold text"),
                    ],
                )
            ],
            {"class": "paragraph"},
        )
        expected = '<p class="paragraph"><li>some text<i>italic text</i><b>bold text</b></li></p>'
        self.assertEqual(
            parent.to_html(),
            expected,
        )

    def test_multipe_parent_node_as_children(self):
        parent = ParentNode(
            "p",
            [
                ParentNode(
                    "li",
                    [
                        LeafNode(None, "some text"),
                    ],
                ),
                ParentNode(
                    "li",
                    [
                        LeafNode("i", "italic text"),
                        LeafNode("b", "bold text"),
                    ],
                ),
            ],
        )
        expected = (
            "<p><li>some text</li><li><i>italic text</i><b>bold text</b></li></p>"
        )
        self.assertEqual(
            parent.to_html(),
            expected,
        )

    def test_mixed_leaf_and_parent_nodes(self):
        parent = ParentNode(
            "ul",
            [
                ParentNode(
                    "li",
                    [
                        LeafNode(None, "some text"),
                    ],
                    {"class": "item"},
                ),
                ParentNode(
                    "li",
                    [ParentNode("b", [LeafNode(None, "bold text")])],
                    {"class": "item"},
                ),
                LeafNode("li", "item text", {"class": "item"}),
            ],
            {"class": "list"},
        )
        expected = (
            '<ul class="list">'
            '<li class="item">some text</li>'
            '<li class="item"><b>bold text</b></li>'
            '<li class="item">item text</li></ul>'
        )
        self.assertEqual(
            parent.to_html(),
            expected,
        )


if __name__ == "__main__":
    unittest.main()

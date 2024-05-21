from textnode import TextNode
from htmlnode import LeafNode


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case "text":
            return LeafNode(tag=None, value=text_node.text)
        case "bold":
            return LeafNode(tag="b", value=text_node.text)
        case "italic":
            return LeafNode(tag="i", value=text_node.text)
        case "code":
            return LeafNode(tag="code", value=text_node.text)
        case "link":
            if text_node.url is None:
                raise ValueError("Link without a url")
            return LeafNode(
                tag="a", value=text_node.text, props={"href": text_node.url}
            )
        case "image":
            if text_node.url is None:
                raise ValueError("Image without a url")
            return LeafNode(
                tag="img", value="", props={"src": text_node.url, "alt": text_node.text}
            )
        case _:
            raise ValueError("Invalid text node type")

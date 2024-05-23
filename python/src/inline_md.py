import re
from typing import Callable, List, Tuple, TypeVar
from textnode import TextNode, TextType


T = TypeVar("T")


# INFO: This may be too much abstraction for only two cases of reuse. This
# implementation is just showcasing a way to use function composition to
# extract the list of nodes from a string and use recursion to aggregate them.
def create_nodes_splitter(
    extractor: Callable[[str], List[T]],
    aggregator: Callable[[str, List[T]], List[TextNode]],
):

    def split_nodes(nodes: List[TextNode]) -> List[TextNode]:
        new_nodes: List[TextNode] = []
        for node in nodes:
            if node.text_type != "text":
                new_nodes.append(node)
                continue
            items = extractor(node.text)
            has_items = len(items) > 0
            if not has_items:
                new_nodes.append(node)
                continue
            new_nodes.extend(aggregator(node.text, items))

        return new_nodes

    return split_nodes


# INFO: Again, this may be too much abstraction for little reuse. This
# implementation is just showcasing a way to use function composition
# and recursion
def create_aggregator(
    sep_constructor: Callable[[T], str], node_constructor: Callable[[T], TextNode]
):

    def aggregate(text: str, aggregates: List[T]) -> List[TextNode]:
        if text == "":
            return []
        if len(aggregates) == 0:
            return [TextNode(text, "text")]
        agg = aggregates[0]
        sep = sep_constructor(agg)
        [text_before, text_after] = text.split(sep, 1)

        nodes = [TextNode(text_before, "text"), node_constructor(agg)]
        nodes.extend(aggregate(text_after, aggregates[1:]))

        return nodes

    return aggregate


def img_info_to_sep(img_info: Tuple[str, str]) -> str:
    return f"![{img_info[0]}]({img_info[1]})"


def img_info_to_text_node(img_info: Tuple[str, str]) -> TextNode:
    return TextNode(img_info[0], "image", img_info[1])


def link_info_to_sep(link_info: Tuple[str, str]) -> str:
    return f"[{link_info[0]}]({link_info[1]})"


def link_info_to_text_node(link_info: Tuple[str, str]) -> TextNode:
    return TextNode(link_info[0], "link", link_info[1])


aggregate_split_images = create_aggregator(img_info_to_sep, img_info_to_text_node)
aggregate_split_links = create_aggregator(link_info_to_sep, link_info_to_text_node)


def extract_markdown_images(text: str) -> List[Tuple[str, str]]:
    pattern = re.compile(r"!\[(.+?)\]\((.+?)\)")
    return re.findall(pattern, text)


def extract_markdown_links(text: str) -> List[Tuple[str, str]]:
    pattern = re.compile(r"(?<!\!)\[(.+?)\]\((.+?)\)")
    return re.findall(pattern, text)


def split_nodes_delimiter(
    old_nodes: List[TextNode], delimiter: str, text_type: TextType
):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != "text":
            new_nodes.append(node)
            continue
        splited = node.text.split(delimiter)
        if len(splited) % 2 == 0:
            raise ValueError("Invalid markdown syntax. Unclosed formatting delimiter")
        for i, text in enumerate(splited):
            if text == "":
                continue
            new_nodes.extend(
                [TextNode(text, "text") if i % 2 == 0 else TextNode(text, text_type)]
            )
    return new_nodes


split_nodes_image = create_nodes_splitter(
    extract_markdown_images, aggregate_split_images
)
split_nodes_link = create_nodes_splitter(extract_markdown_links, aggregate_split_links)

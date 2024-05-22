from typing import Dict, List, Optional


class HTMLNode:
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: Optional[List["HTMLNode"]] = None,
        props: Optional[Dict[str, str]] = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        return " ".join([f'{prop}="{value}"' for (prop, value) in self.props.items()])

    # dummy implementation just to pass static typing
    def to_html(self) -> str:
        raise NotImplementedError("Subclasses should implement this method")

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other) -> bool:
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )


class LeafNode(HTMLNode):

    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        props: Optional[Dict[str, str]] = None,
    ):

        super().__init__(tag=tag, value=value, props=props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("Leaf node should have a value")
        if self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{' '+self.props_to_html() if self.props is not None else ''}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: Optional[str] = None,
        children: Optional[List[HTMLNode]] = None,
        props: Optional[Dict[str, str]] = None,
    ):
        super().__init__(tag=tag, children=children, props=props, value=None)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("Parent node must have a tag")
        if self.children is None or len(self.children) == 0:
            raise ValueError("Parent node must have at least one child")

        inner_html = ""
        for child in self.children:
            inner_html += child.to_html()
        return (
            f"<{self.tag}{' '+self.props_to_html() if self.props is not None else ''}>{inner_html}"
            f"</{self.tag}>"
        )

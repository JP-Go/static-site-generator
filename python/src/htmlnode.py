""" 
The representations for HTML nodes. An HTMLNode, in
this context is either one the two specialized classes that inherit from it: 
a ParentNode or a LeafNode. A LeafNode is a HTML node without any child nodes. 
In contrast, the ParentNode is a node that has at least one HTMLNode as child.
A ParentNode may have one or more instances of ParentNode as children.
"""

from typing import Dict, Optional, Sequence


class HTMLNode:
    r"""Represents a node in a HTML document.

    Attributes
    ----------

    tag : str, optional
        The HTML tag that this node represents.

    value : str, optional
        The HTML content that this node holds.

    children : list of HTMLNode, optional
        A list of this node's children.

    props : dict of str to str, optional
        A dictionary of this node's html properties.

    Methods
    -------
    props_to_html()
        Joins the properties of the HTML node into a string with html valid
        properties declaration.


    """

    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: Optional[Sequence["HTMLNode"]] = None,
        props: Optional[Dict[str, str]] = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def props_to_html(self) -> str:
        """Joins the properties of the HTML node into a string with html valid
        properties declaration.

        Returns
        -------
        joined_props : str
            a string of properties
        """
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
    """A leaf node is a HTMLNode that has no children

    Attributes
    ----------
    tag : str, optional
        The HTML tag that this node represents.

    value : str, optional
        the value the html node holds

    props : dict of str to str, optional
        A dictionary of this node's html properties.

    Methods
    -------
    to_html()
        gives the html representation of this leaf node
    """

    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        props: Optional[Dict[str, str]] = None,
    ):

        super().__init__(tag=tag, value=value, props=props, children=None)

    def to_html(self) -> str:
        """Returns the html representation of the node. It will fail if the
        node has no value. If the node has no tag, the value of the node is
        returned, ignoring props. Otherwise it returns a valid html tag.

        Returns
        -------
        html_tag : str
            valid html content

        Raises
        -------
        ValueError
            if tag is None
        """
        if self.value is None:
            raise ValueError("Leaf node should have a value")
        if self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{' '+self.props_to_html() if self.props is not None else ''}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.children}, {self.props})"


class ParentNode(HTMLNode):
    """A parent node is a HTMLNode that has at least one child

    Attributes
    ----------
    tag : str, optional
        The HTML tag that this node represents.

    children : list of HTMLNode, optional
        A list of this node's children.

    props : dict of str to str, optional
        A dictionary of this node's html properties.

    Methods
    -------
    to_html()
        gives the html representation of this parent node
    """

    def __init__(
        self,
        tag: Optional[str] = None,
        children: Optional[Sequence[HTMLNode]] = None,
        props: Optional[Dict[str, str]] = None,
    ):
        super().__init__(tag=tag, children=children, props=props, value=None)

    def to_html(self) -> str:
        """Returns the html representation of the node. It will fail if the
        node has no tag. Otherwise it returns valid html text.

        Returns
        -------
        html : str
            valid html content

        Raises
        -------
        ValueError
            if tag is None or children is None or len(children) == 0
        """
        if self.tag is None:
            raise ValueError("Parent node must have a tag")
        if self.children is None:
            raise ValueError("Parent node must have at least one child")

        inner_html = ""
        for child in self.children:
            if child.children is not None and len(child.children) == 0:
                continue
            inner_html += child.to_html()
        return (
            f"<{self.tag}{' '+self.props_to_html() if self.props is not None else ''}>{inner_html}"
            f"</{self.tag}>"
        )

    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, {self.value}, {self.children}, {self.props})"

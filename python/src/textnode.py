from typing import Literal, Optional


TextType = Literal["text", "bold", "italic", "code", "link", "image"]


class TextNode:
    def __init__(
        self,
        text: str,
        text_type: TextType,
        url: Optional[str] = None,
    ):
        self.text = text
        self.text_type: TextType = text_type
        self.url = url

    def __eq__(self, value) -> bool:
        return (
            self.text == value.text
            and self.text_type == value.text_type
            and self.url == value.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

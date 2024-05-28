#[derive(PartialEq, Debug)]
pub enum TextType<'a> {
    Text,
    Link(&'a str),
    Image(&'a str),
    Bold,
    Italic,
    Code,
}

#[derive(PartialEq, Debug)]
pub struct TextNode<'a> {
    text: &'a str,
    text_type: TextType<'a>,
}

impl<'a> TextNode<'a> {
    pub fn new(text: &'a str, text_type: &str, url: Option<&'a str>) -> Result<Self, &'static str> {
        let text_type = match text_type {
            "text" => TextType::Text,
            "bold" => TextType::Bold,
            "italic" => TextType::Italic,
            "code" => TextType::Code,
            "link" => url.map(TextType::Link).ok_or("Missing link url")?,
            "image" => url.map(TextType::Image).ok_or("Missing image url")?,
            _ => Err("invalid text type")?,
        };
        if text.is_empty() {
            return Err("Text can not be empty");
        }
        Ok(Self { text_type, text })
    }

    pub fn text(self: Self) -> &'a str {
        self.text
    }
    pub fn text_type(self: Self) -> TextType<'a> {
        self.text_type
    }
}

#[test]
fn construct_text() {
    let result = TextNode::new("Some text", "text", None);
    assert!(result.is_ok());
    assert_eq!(
        result.ok().unwrap(),
        TextNode {
            text: "Some text",
            text_type: TextType::Text
        }
    )
}

#[test]
fn construct_bold() {
    let result = TextNode::new("Some text", "bold", None);
    assert!(result.is_ok());
    assert_eq!(
        result.ok().unwrap(),
        TextNode {
            text: "Some text",
            text_type: TextType::Bold
        }
    )
}

#[test]
fn construct_italic() {
    let result = TextNode::new("Some text", "italic", None);
    assert!(result.is_ok());
    assert_eq!(
        result.ok().unwrap(),
        TextNode {
            text: "Some text",
            text_type: TextType::Italic
        }
    )
}

#[test]
fn construct_code() {
    let result = TextNode::new("Some code", "code", None);
    assert!(result.is_ok());
    assert_eq!(
        result.ok().unwrap(),
        TextNode {
            text: "Some code",
            text_type: TextType::Code
        }
    )
}

#[test]
fn construct_image() {
    let result = TextNode::new("An image", "image", Some("https://google.com"));
    assert!(result.is_ok());
    assert_eq!(
        result.ok().unwrap(),
        TextNode {
            text: "An image",
            text_type: TextType::Image("https://google.com")
        }
    )
}

#[test]
fn construct_link() {
    let result = TextNode::new("A link", "link", Some("https://google.com"));
    assert!(result.is_ok());
    assert_eq!(
        result.ok().unwrap(),
        TextNode {
            text: "A link",
            text_type: TextType::Link("https://google.com")
        }
    )
}

#[test]
fn fail_construct_link() {
    let result = TextNode::new("A link", "link", None);
    assert!(result.is_err_and(|err| { err == "Missing link url" }));
}

#[test]
fn fail_construct_image() {
    let result = TextNode::new("An image", "image", None);
    assert!(result.is_err_and(|err| { err == "Missing image url" }));
}

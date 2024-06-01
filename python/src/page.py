import os
import pathlib
from block_md import markdown_to_blocks, markdown_to_html_node


def extract_title(markdown: str) -> str:
    first_block = markdown_to_blocks(markdown)[0]
    if not first_block.count("# ") == 1:
        raise ValueError("Missing title")
    return first_block[2:]


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    if not os.path.exists(from_path):
        raise FileNotFoundError(f"{from_path} does not exist")
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"{template_path} does not exist")

    template_handle = open(template_path, "r")
    template = template_handle.read()
    template_handle.close()

    from_handle = open(from_path, "r")
    content = from_handle.read()
    title = extract_title(content)
    from_contents = content
    from_handle.close()

    template = template.replace("{{ Title }}", title)
    template = template.replace(
        "{{ Content }}", markdown_to_html_node(from_contents).to_html()
    )

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    dest_handle = open(dest_path, "w")
    dest_handle.write(template)


def generate_pages_recursive(content_dir: str, template_path: str, dest_dir: str):
    content_base = pathlib.Path(content_dir)
    dest_base = pathlib.Path(dest_dir)
    for file in os.listdir(content_dir):
        prev_path = pathlib.Path(content_base, file)
        if os.path.isfile(prev_path):
            new_path = dest_base / (file.removesuffix(".md") + ".html")
            generate_page(str(prev_path), template_path, str(new_path))
        else:
            generate_pages_recursive(
                str(content_base / file), template_path, str(dest_base / file)
            )
    return

from page import generate_pages_recursive
from tree import copy_file_tree


def main():
    copy_file_tree("./static", "./public")
    generate_pages_recursive("./content", "./template.html", "public")


main()

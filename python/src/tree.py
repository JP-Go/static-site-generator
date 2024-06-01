import os
import shutil
from typing import Set


def copy_file_tree(source_path: str, dest_path: str):
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"Path {source_path} does not exist")
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
    os.makedirs(dest_path)
    contents_to_copy = get_files(source_path)
    for file in contents_to_copy:
        relative_path = file.removeprefix(source_path)
        new_path = dest_path + relative_path
        if not os.path.exists(os.path.dirname(new_path)):
            os.makedirs(os.path.dirname(new_path))
        shutil.copy(file, new_path)


def get_files(path: str, tree: Set = set()) -> set[str]:
    contents = os.listdir(path)
    for content in contents:
        fullpath = os.path.join(path, content)
        if os.path.isfile(fullpath):
            tree.add(fullpath)
        else:
            tree.update(get_files(fullpath))
    return tree

from node_type_text import TextNode, TextType
import shutil, os
from pathlib import Path


def reset_public_folder():
    home_dir = Path.cwd()
    public_folder = home_dir / "public"
    if public_folder.exists():
        shutil.rmtree(public_folder)
    Path.mkdir(home_dir / "public")


def copy_static_folder_to_public(dir: Path):
    # directory_list = os.listdir(dir)
    for item in dir.iterdir():
        if os.path.isdir(item):
            print("dir ", item.relative_to(Path.cwd()))
            Path.mkdir(Path.cwd() / 'public' / item.relative_to(Path.cwd() / "static"))
            copy_static_folder_to_public(item)
        else:
            shutil.copy(item, Path.cwd() / "public" / item.relative_to(Path.cwd() / "static").parent)
            print("copyed file", item.relative_to(Path.cwd() / "static"))
        

def main():
    home_dir = Path.cwd()
    static = home_dir / "static"
    reset_public_folder()
    copy_static_folder_to_public(static)


if __name__ == "__main__":
    main()

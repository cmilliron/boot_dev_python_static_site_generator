from node_type_text import TextNode, TextType
import shutil, os, sys
from pathlib import Path
from markdown_to_html import generate_pages_recursive


def reset_public_folder(public_folder):
    if public_folder.exists():
        shutil.rmtree(public_folder)
    public_folder.parent.mkdir(parents=True, exist_ok=True)
    Path.mkdir(public_folder)


def copy_static_folder_to_public(dir: Path, dest_path: Path):
    # directory_list = os.listdir(dir)
    for item in dir.iterdir():
        if os.path.isdir(item):
            # print("dir ", item.relative_to(Path.cwd()))
            Path.mkdir(dest_path / item.relative_to(dir))
            copy_static_folder_to_public(item, dest_path / item.relative_to(dir))
        else:
            shutil.copy(item, dest_path / item.relative_to(dir).parent)
            # print("copyed file", item.relative_to(dir))
        

def main():
    # home_dir = Path.cwd()
    static = Path("static")
    source_base_path = Path('content')
    destination_path = Path("docs") 
    add_on = ""
    if len(sys.argv) > 1:
        add_on = sys.argv[1]
        destination_path = destination_path / add_on
    # destination_base_path = root_path / add_on_path
    reset_public_folder(destination_path)
 
    copy_static_folder_to_public(static, destination_path)
    generate_pages_recursive(source_base_path, "template.html", destination_path, add_on)
    
    
    
    


if __name__ == "__main__":
    main()

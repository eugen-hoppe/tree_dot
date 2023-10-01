import os
import shutil
from zipfile import ZipFile


def delete_folder_recursive(path):
    if os.path.exists(path) and os.path.isdir(path):
        shutil.rmtree(path)


def copy_files_and_folder(src_folder, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    for item in os.listdir(src_folder):
        source_item = os.path.join(src_folder, item)
        dest_item = os.path.join(dest_folder, item)
        if os.path.isdir(source_item):
            shutil.copytree(source_item, dest_item)
        else:
            shutil.copy2(source_item, dest_item)


def create_zip(source_folder, zip_name):
    with ZipFile(zip_name, "w") as zf:
        for foldername, subfolders, filenames in os.walk(source_folder):
            for filename in filenames:
                filepath = os.path.join(foldername, filename)
                zf.write(filepath, os.path.relpath(filepath, source_folder))


def main():
    src_folder = "tree_dot"
    dest_folder = "installation/trdt"
    single_file = "dot.py"
    zip_name = "trdt.zip"
    final_dest = "installation"
    copy_files_and_folder(src_folder, os.path.join(dest_folder, "tree_dot"))
    with open(os.path.join(dest_folder, '.gitignore'), 'w') as f:
        f.write("*\n")
    shutil.copy2(single_file, dest_folder)
    delete_folder_recursive(os.path.join(dest_folder, "tree_dot", "__pycache__"))

    create_zip(dest_folder, zip_name)
    shutil.move(zip_name, os.path.join(final_dest, zip_name))
    delete_folder_recursive(os.path.join(dest_folder))


if __name__ == "__main__":
    main()

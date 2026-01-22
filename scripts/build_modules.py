import json
import os.path
import pathlib
import zipfile

MODULES_PATH = "src/module/modules"
TARGET_PATH = "modules"

def main():
    modules = os.listdir(MODULES_PATH)
    for module_name in modules:
        module_directory = pathlib.Path(f"{MODULES_PATH}/{module_name}")
        name, class_name, file = load_module_entry(module_directory.joinpath("module.json"))
        file = module_directory.joinpath(file)
        if not module_directory.is_dir():
            continue
        if file.exists():
            archive_path = os.path.join(TARGET_PATH, f"{name}.module")
            create_archive(module_directory, archive_path)
        print(f"successfully created module {module_name}")

def create_archive(directory, output):
    with zipfile.ZipFile(output, "w") as zip_file:
        for root, dirs, files in os.walk(directory):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                arcname = os.path.relpath(dir_path, directory) + "/"
                zip_file.writestr(arcname, "")

            for file_name in files:
                file_path = os.path.join(root, file_name)
                arcname = os.path.relpath(file_path, directory)
                zip_file.write(file_path, arcname)


def load_module_entry(path: pathlib.Path):
    with open(path) as file:
        data = json.load(file)
    name = data['name']
    class_name = data['class']
    file = data['file']
    return name, class_name, file

if __name__ == '__main__':
    main()

import os.path
import pathlib
import shutil
import subprocess
import sys

MODULES_PATH = "src/module/modules"
TARGET_PATH = "modules"
BUILD_PATH = "build_modules"

def main():
    clean_build_directory()
    modules = os.listdir(MODULES_PATH)
    for module_name in modules:
        module_directory = pathlib.Path(f"{MODULES_PATH}/{module_name}")
        module_py = module_directory.joinpath(f"{module_name}.py")
        if not module_directory.is_dir():
            continue
        if module_py.exists():
            compile_module(module_directory, module_py)
        print(f"successfully compiled module {module_name}")
        move_compiled_modules()

def clean_build_directory():
    if os.path.exists(BUILD_PATH):
        shutil.rmtree(BUILD_PATH)

def compile_module(module_directory, module_py):
    flags = list()
    py_files = module_directory.glob("**/*.py")
    for py_file in py_files:
        flags.append(f"--follow-import-to={py_file.stem}")
    args = [
        sys.executable,
        "-m",
        "nuitka",
        "--module",
        f"--output-dir={BUILD_PATH}",
        str(module_py)
    ]
    args.extend(flags)
    process = subprocess.run(args)
    if process.returncode == -1:
        raise Exception(process.stderr)

def move_compiled_modules():
    found = list(pathlib.Path(BUILD_PATH).glob(f"*.{determine_module_extension()}"))
    if len(found) > 1:
        raise Exception(f"multiple shared libraries found: {found}")
    target_file = pathlib.Path(TARGET_PATH).joinpath(found[0].name)
    if target_file.exists():
        os.remove(target_file)
    shutil.move(found[0], TARGET_PATH)

def determine_module_extension():
    if os.name == "posix":
        return "so"
    if os.name == "nt":
        return "pyd"
    return None

if __name__ == '__main__':
    main()

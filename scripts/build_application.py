
import os
import shutil
import subprocess
import sys


BUILD_PATH = "build"
SRC_PATH = "src/main.py"
APP_NAME = "JustForYou"

def main():
    clean_build_directory()
    compile()

def clean_build_directory():
    if os.path.exists(BUILD_PATH):
        shutil.rmtree(BUILD_PATH)

def compile():
    args = [
        sys.executable,
        "-m",
        "nuitka",
        "--standalone",
        "--onefile",
        "--follow-imports",
        "--assume-yes-for-downloads",
        "--enable-plugin=pyqt6",
        f"--output-dir={BUILD_PATH}",
        f"--output-filename={APP_NAME}",
        SRC_PATH
    ]
    process = subprocess.run(args)
    if process.returncode == -1:
        raise Exception(process.stderr)

if __name__ == '__main__':
    main()
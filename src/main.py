import pathlib
import sys
from PyQt6.QtWidgets import QApplication
from src.module.module_manager import ModuleManager
from src.window.window import Window


def main():
    app = QApplication(sys.argv)
    window = Window()

    module_manager = ModuleManager()
    module_manager.set_directory(pathlib.Path("modules"))
    module_manager.load()

    window.show()

    app.exec()
    pass

if __name__ == '__main__':
    main()
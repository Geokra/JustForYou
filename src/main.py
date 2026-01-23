import pathlib
import sys
from PyQt6.QtWidgets import QApplication
from manager.module_manager import ModuleManager
from window.window import Window
import module

def main():
    app = QApplication(sys.argv)
    window = Window()

    module_manager = ModuleManager(False)
    if module_manager.debug:
        module_manager.set_directory(pathlib.Path("src/modules"))
    else:
        module_manager.set_directory(pathlib.Path("modules"))
    module_manager.load()
    module_manager.enable()

    window.set_modules(module_manager.modules)
    window.setup()
    window.show()

    app.exec()

    module_manager.disable()

if __name__ == '__main__':
    main()
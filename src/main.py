import pathlib
import sys
from PyQt6.QtWidgets import QApplication
import history
from manager.module_manager import ModuleManager
import settings
from window.window import Window

def main():
    app = QApplication(sys.argv)
    window = Window()
    settings.settings.load()

    module_manager = ModuleManager(True)
    if module_manager.debug:
        module_manager.set_directory(pathlib.Path("src/modules"))
    else:
        module_manager.set_directory(pathlib.Path("modules"))
    module_manager.load()
    module_manager.enable()

    window.set_modules(module_manager.modules)
    window.setup()
    window.show()
    history.history.load()

    app.exec()

    module_manager.disable()
    settings.settings.save()
    history.history.save()

if __name__ == '__main__':
    main()



from PyQt6.QtCore import QFile, QIODeviceBase, QTextStream, Qt
from PyQt6.QtWidgets import QHBoxLayout, QMainWindow, QStackedWidget, QVBoxLayout, QWidget

class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.modules = dict()

        self.setWindowTitle("JustForYou")
        self.resize(1920, 1080)
        self.load_stylesheet()

    def setup(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        main_layout = QHBoxLayout(self.central_widget)

        # left section
        self.left_section = QWidget(self)
        self.left_layout = QVBoxLayout(self.left_section)
        self.left_section.setObjectName("left_section")
        self.left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # right section
        self.right_section = QWidget(self)
        self.stacked_widget = QStackedWidget(self)
        self.right_section.setObjectName("right_section")

        for module in self.modules.values():
            button = module.button
            button.clicked.connect(lambda _, w=module.widget: self.stacked_widget.setCurrentWidget(w))
            self.left_layout.addWidget(button)

        main_layout.addWidget(self.left_section)

        for module in self.modules.values():
            self.stacked_widget.addWidget(module.widget)

        self.right_section_layout = QVBoxLayout(self.right_section)
        self.right_section_layout.addWidget(self.stacked_widget)

        main_layout.addWidget(self.right_section)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
    def set_modules(self, modules: dict):
        self.modules = modules

    def load_stylesheet(self):
        file = QFile("styles/main.qss")
        if file.open(QIODeviceBase.OpenModeFlag.ReadOnly | QIODeviceBase.OpenModeFlag.Text):
            stylesheet = QTextStream(file).readAll()
            self.setStyleSheet(stylesheet)
        else:
            print("unable to load stylesheet")

    
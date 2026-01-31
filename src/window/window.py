
from PyQt6.QtCore import QFile, QIODeviceBase, QTextStream, Qt
from PyQt6.QtWidgets import QApplication, QFrame, QHBoxLayout, QMainWindow, QPushButton, QStackedWidget, QTextEdit, QVBoxLayout, QWidget

import history
import settings

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

        main_layout = QVBoxLayout(self.central_widget)

        top_layout = QHBoxLayout()

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

        for module in self.modules.values():
            self.stacked_widget.addWidget(module.widget)

        self.right_section_layout = QVBoxLayout(self.right_section)
        self.right_section_layout.addWidget(self.stacked_widget)

        top_layout.addWidget(self.left_section)
        top_layout.addWidget(self.right_section)
        
        bottom_layout = QHBoxLayout()

        # left bottom section
        self.left_bottom_section = QWidget(self)
        self.left_bottom_layout = QVBoxLayout(self.left_bottom_section)
        self.left_bottom_section.setObjectName("left_bottom_section")

        settings_button = QPushButton("Settings")
        self.left_bottom_layout.addWidget(settings_button)
        self.left_bottom_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)

        settings.settings.setup_ui()
        self.stacked_widget.addWidget(settings.settings.widget)
        settings_button.clicked.connect(lambda _, w=settings.settings.widget: self.stacked_widget.setCurrentWidget(w))

        self.right_bottom_section = QWidget(self)
        self.right_bottom_section.setObjectName("right_bottom_section")
        self.right_bottom_layout = QVBoxLayout(self.right_bottom_section)
        self.right_bottom_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        history_text_edit = QTextEdit()
        for line in history.history.lines:
            history_text_edit.append(line)
        history_text_edit.setReadOnly(True)
        history_text_edit.setFrameShape(QFrame.Shape.NoFrame)

        self.right_bottom_layout.addWidget(history_text_edit)

        bottom_layout.addWidget(self.left_bottom_section)
        bottom_layout.addWidget(self.right_bottom_section)

        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)
        main_layout.setSpacing(0)
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

    
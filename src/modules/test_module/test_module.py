from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget
from module import Module

class TestModule(Module):

    def on_enable(self):
        print("enable")
        self.button = QPushButton("Test Module")
        self.widget = QWidget()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Ansicht 1"))
        self.widget.setLayout(layout)
    
    def on_disable(self):
        print("disable")

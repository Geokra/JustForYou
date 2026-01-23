from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget
from module import Module

class TestModule2(Module):

    def on_enable(self):
        print("enable")
        self.button = QPushButton("Test Module 2")
        self.widget = QWidget()
        
        # Layout for View 1
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Ansicht 2"))
        self.widget.setLayout(layout)

    def on_disable(self):
        print("disable")

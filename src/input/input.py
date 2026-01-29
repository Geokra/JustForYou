import os
import sys
from pynput.keyboard import Controller, Key

from PyQt6.QtCore import QFile, QIODeviceBase, QTextStream
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout,
    QPushButton, QGroupBox, QLineEdit
)


class EingabeWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.load_stylesheet()

        self.setWindowTitle("Eingabe")
        self.setFixedSize(320, 420)

        group = QGroupBox("Eingabe")
        grid = QGridLayout(group)

        grid.setSpacing(12)
        grid.setContentsMargins(15, 20, 15, 15)

        self.lineedit = QLineEdit()
        self.lineedit.setFixedHeight(40)
        grid.addWidget(self.lineedit, 0, 0, 1, 3)

        buttons = [
            "1", "2", "3",
            "4", "5", "6",
            "7", "8", "9",
            "<--", "0", "Del"
        ]

        for i, text in enumerate(buttons):
            btn = QPushButton(text)
            btn.setFixedSize(80, 60)
            btn.clicked.connect(lambda _, t=text: self.on_button_click(t))

            row = (i // 3) + 1
            col = i % 3
            grid.addWidget(btn, row, col)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.addWidget(group)

        self.setLayout(layout)

    def load_stylesheet(self):
        file = QFile("../../styles/input.qss")
        if file.open(QIODeviceBase.OpenModeFlag.ReadOnly | QIODeviceBase.OpenModeFlag.Text):
            stylesheet = QTextStream(file).readAll()
            self.setStyleSheet(stylesheet)

    def on_button_click(self, text):
        keyboard = Controller()
        match text:
            case "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9":
                keyboard.press(text)
                keyboard.release(text)
            case "<--":
                keyboard.press(Key.backspace)
                keyboard.release(Key.backspace)
            case "Del":
                keyboard.press(Key.delete)
                keyboard.release(Key.delete)


def main():
    app = QApplication(sys.argv)
    window = EingabeWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

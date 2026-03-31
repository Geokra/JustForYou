import typing
from PyQt6 import QtGui
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtCore import QLocale, Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QGridLayout, QLineEdit, QPushButton


class NumPad(QWidget):
    def __init__(self, target: QLineEdit):
        super().__init__()
        self.target = target
        self.setWindowFlags(Qt.WindowType.Popup)

        layout = QGridLayout(self)

        nums = [
            "7","8","9",
            "4","5","6",
            "1","2","3",
            "0",".", "±",
            "⌫"
        ]

        for i, text in enumerate(nums):
            btn = QPushButton(text)
            btn.clicked.connect(lambda _, t=text: self.press(t))
            layout.addWidget(btn, i // 3, i % 3)

    def press(self, t):
        if t == "±":
            text = self.target.text()
            if text.startswith("-"):
                self.target.setText(text[1:])
            elif text:
                self.target.setText("-" + text)
        if t == "⌫":
            self.target.backspace()
        elif t == ".":
            if "." not in self.target.text():
                self.target.insert(t)
        else:
            self.target.insert(t)


class ClickableLineEdit(QLineEdit):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        validator = QDoubleValidator()
        self.setValidator(validator)

        # connect signal to slot
        self.clicked.connect(self.open_numpad)
    

    def mousePressEvent(self, a0: typing.Optional[QtGui.QMouseEvent]) -> None:
        self.clicked.emit()

        return super().mousePressEvent(a0)

    def open_numpad(self):

        pad = NumPad(self)

        # show under the field
        pos = self.mapToGlobal(self.rect().bottomLeft())
        pad.move(pos)
        pad.show()



from PyQt6.QtWidgets import QFrame, QTextEdit

class History:

    def setup(self):
        self.history_text_edit = QTextEdit()
        self.history_text_edit.setReadOnly(True)
        self.history_text_edit.setFrameShape(QFrame.Shape.NoFrame)

    def update(self, element):
        self.history_text_edit.append(element)

    def clear(self):
        self.history_text_edit.clear()

history = History()
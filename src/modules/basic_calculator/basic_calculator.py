from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLineEdit, QPushButton, QWidget, QGroupBox, QVBoxLayout, QGridLayout, QLabel, QSizePolicy
from module import Module
import history
import helper

class BasicCalculator(Module):

    def on_enable(self):
        self.button = QPushButton("Grundrechner")
        self.widget = QWidget()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(12)

        options_group = QGroupBox()
        options_layout = QVBoxLayout(options_group)

        self.input_term = QLineEdit()
        self.input_term.setPlaceholderText("Eingabe...")
        self.input_term.returnPressed.connect(self.on_calc)
        self.output_label = QLabel()

        # Calculator button grid
        calc_grid = QGridLayout()
        calc_grid.setSpacing(4)

        buttons = [
            ("(", 0, 0), (")", 0, 1), ("**", 0, 2), ("C", 0, 3),
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
            ("0", 4, 0), (".", 4, 1), ("\u232b", 4, 2), ("+", 4, 3),
        ]

        for text, row, col in buttons:
            btn = QPushButton(text)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            btn.setMinimumHeight(50)
            btn.setObjectName("calc_btn")
            if text == "C":
                btn.setObjectName("calc_btn_clear")
                btn.clicked.connect(self.on_clear)
            elif text == "\u232b":
                btn.setObjectName("calc_btn_backspace")
                btn.clicked.connect(self.on_backspace)
            else:
                btn.clicked.connect(lambda _, t=text: self.on_button(t))
            calc_grid.addWidget(btn, row, col)

        equals_btn = QPushButton("=")
        equals_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        equals_btn.setMinimumHeight(50)
        equals_btn.setObjectName("calc_btn_equals")
        equals_btn.clicked.connect(self.on_calc)
        calc_grid.addWidget(equals_btn, 5, 0, 1, 4)

        options_layout.addWidget(self.input_term)
        options_layout.addLayout(calc_grid)
        options_layout.addWidget(self.output_label)

        layout.addWidget(options_group)

        self.widget.setLayout(layout)

    def on_button(self, text):
        self.input_term.insert(text)
        self.input_term.setFocus()

    def on_clear(self):
        self.input_term.clear()
        self.output_label.clear()
        self.input_term.setFocus()

    def on_backspace(self):
        self.input_term.backspace()
        self.input_term.setFocus()

    def on_calc(self):
        try:
            result = helper.calculate(self.input_term.text())
            self.output_label.setText("Ergebnis: " + str(result))
            history.history.update(str(result))
        except ValueError as e:
            self.output_label.setText("Error: " + str(e))

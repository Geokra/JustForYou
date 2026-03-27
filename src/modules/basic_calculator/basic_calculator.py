from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLineEdit, QPushButton, QWidget, QGroupBox,
    QVBoxLayout, QLabel, QGridLayout
)
from module import Module
import history
import helper2

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
        self.output_label = QLabel()

        self.calc_button = QPushButton("=")
        self.calc_button.clicked.connect(self.on_calc)

        grid = QGridLayout()

        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('.', 3, 1), ('(', 3, 2), (')', 3, 3),
            ('+', 4, 0)
        ]

        for text, row, col in buttons:
            btn = QPushButton(text)
            btn.clicked.connect(lambda checked, t=text: self.add_to_input(t))
            grid.addWidget(btn, row, col)

        grid.addWidget(self.calc_button, 4, 1, 1, 3)

        clear_btn = QPushButton("C")
        clear_btn.clicked.connect(self.clear_input)
        grid.addWidget(clear_btn, 5, 0, 1, 4)

        options_layout.addWidget(self.input_term)
        options_layout.addLayout(grid)
        options_layout.addWidget(self.output_label)

        layout.addWidget(options_group)
        self.widget.setLayout(layout)

    def add_to_input(self, value):
        current = self.input_term.text()
        self.input_term.setText(current + value)

    def clear_input(self):
        self.input_term.clear()
        self.output_label.clear()

    def on_calc(self):
        try:
            result = helper2.calculate(self.input_term.text())
            self.output_label.setText("Ergebnis: " + str(result))
            history.history.update(str(result))
        except ValueError as e:
            self.output_label.setText("Error: " + str(e))
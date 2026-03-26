"""Nebenrechner-Dialog: kann aus jedem Modul aufgerufen werden.
Ergebnis ist uebernehmbar als Parameterwert."""

import sys
import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog, QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QVBoxLayout
)

# Ensure basic_calculator helper is importable
_bc_path = os.path.join(os.path.dirname(__file__), "modules", "basic_calculator")
if _bc_path not in sys.path:
    sys.path.insert(0, _bc_path)

from calc_helper import calculate


class SideCalculatorDialog(QDialog):
    """Nebenrechner-Dialog mit Taschenrechner-Buttons.
    Nach Berechnung kann das Ergebnis uebernommen werden."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nebenrechner")
        self.setMinimumSize(340, 420)
        self._result_value: float | None = None

        layout = QVBoxLayout(self)
        layout.setSpacing(8)

        # Input
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Ausdruck eingeben...")
        self.input_field.returnPressed.connect(self._on_calc)
        layout.addWidget(self.input_field)

        # Calculator grid
        grid = QGridLayout()
        grid.setSpacing(4)

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
            btn.setMinimumHeight(45)
            btn.setObjectName("calc_btn")
            if text == "C":
                btn.setObjectName("calc_btn_clear")
                btn.clicked.connect(self._on_clear)
            elif text == "\u232b":
                btn.setObjectName("calc_btn_backspace")
                btn.clicked.connect(self._on_backspace)
            else:
                btn.clicked.connect(lambda _, t=text: self._on_button(t))
            grid.addWidget(btn, row, col)

        equals_btn = QPushButton("=")
        equals_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        equals_btn.setMinimumHeight(45)
        equals_btn.setObjectName("calc_btn_equals")
        equals_btn.clicked.connect(self._on_calc)
        grid.addWidget(equals_btn, 5, 0, 1, 4)

        layout.addLayout(grid)

        # Result
        self.result_label = QLabel()
        self.result_label.setObjectName("result_label")
        layout.addWidget(self.result_label)

        self.error_label = QLabel()
        self.error_label.setObjectName("error_label")
        layout.addWidget(self.error_label)

        # Action buttons
        btn_row = QHBoxLayout()
        self.take_btn = QPushButton("Ergebnis übernehmen")
        self.take_btn.setEnabled(False)
        self.take_btn.clicked.connect(self.accept)
        btn_row.addWidget(self.take_btn)

        cancel_btn = QPushButton("Schließen")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)

        layout.addLayout(btn_row)

    def _on_button(self, text: str):
        self.input_field.insert(text)
        self.input_field.setFocus()

    def _on_clear(self):
        self.input_field.clear()
        self.result_label.clear()
        self.error_label.clear()
        self._result_value = None
        self.take_btn.setEnabled(False)
        self.input_field.setFocus()

    def _on_backspace(self):
        self.input_field.backspace()
        self.input_field.setFocus()

    def _on_calc(self):
        self.error_label.clear()
        self.result_label.clear()
        self._result_value = None
        self.take_btn.setEnabled(False)

        try:
            expression = self.input_field.text()
            result = calculate(expression)
            self._result_value = result
            self.result_label.setText(f"Ergebnis: {result}")
            self.take_btn.setEnabled(True)

            import history
            history.history.update(f"NR: {expression} = {result}")
        except ValueError as e:
            self.error_label.setText(f"Fehler: {e}")

    def get_result(self) -> float | None:
        return self._result_value

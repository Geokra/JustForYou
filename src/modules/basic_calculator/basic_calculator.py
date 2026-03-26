from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLineEdit, QPushButton, QWidget, QGroupBox, QVBoxLayout, QLabel
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
        self.output_label = QLabel()

        self.calc_button = QPushButton("Berechnen")
        self.calc_button.clicked.connect(self.on_calc)

        options_layout.addWidget(self.input_term)
        options_layout.addWidget(self.calc_button)
        options_layout.addWidget(self.output_label)

        layout.addWidget(options_group)

        self.widget.setLayout(layout)
    
    def on_calc(self):
        try: 
            result = helper.calculate(self.input_term.text())
            self.output_label.setText(("Ergebnis: " + str(result)))
            history.history.update(str(result))
        except ValueError as e:
            self.output_label.setText(("Error: " + str(e)))

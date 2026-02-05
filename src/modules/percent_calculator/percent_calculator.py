from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QComboBox, QFormLayout, QGroupBox, QLabel, QPushButton, QSpinBox, QVBoxLayout, QWidget
from module import Module

class PercentCalculator(Module):

    def on_enable(self):
        print("enable")
        self.button = QPushButton("Prozent Rechner")
        self.widget = QWidget()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(12)

        options_group = QGroupBox()


        # --- Storage calculation group ---
        storage_group = QGroupBox("Prozentberechnung")
        storage_layout = QVBoxLayout(storage_group)

        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignTop)


        storage_layout.addLayout(form_layout)



        self.calculate_button = QPushButton("Berechnen")
        #self.calculate_button.clicked.connect(self.on_calculate_storage)
        storage_layout.addWidget(self.calculate_button)

        self.output_result = QLabel("Ergebnis: –")
        self.output_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.output_result.setStyleSheet("font-weight: bold;")
        storage_layout.addWidget(self.output_result)

        layout.addWidget(options_group)
        layout.addWidget(storage_group)


        self.widget.setLayout(layout)

    def on_disable(self):
        print("disable")
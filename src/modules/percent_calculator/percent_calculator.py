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
        options_layout = QVBoxLayout(options_group)



        # --- Storage calculation group ---
        storage_group = QGroupBox("Speicherberechnung")
        storage_layout = QVBoxLayout(storage_group)

        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignTop)


        self.input_width = QSpinBox()
        self.input_width.setRange(1, 10000)

        self.input_height = QSpinBox()
        self.input_height.setRange(1, 10000)

        self.input_color_depth = QSpinBox()
        self.input_color_depth.setRange(1, 64)

        self.input_frames = QSpinBox()
        self.input_frames.setRange(1, 100000)

        self.unit = QComboBox()
        self.unit.addItems(["BIT", "BYTE", "KIB", "MIB", "GIB", "TIB"])

        form_layout.addRow("Breite (px):", self.input_width)
        form_layout.addRow("Höhe (px):", self.input_height)
        form_layout.addRow("Farbtiefe (Bit):", self.input_color_depth)
        form_layout.addRow("Frames:", self.input_frames)
        form_layout.addRow("Ergebnis Einheit:", self.unit)

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
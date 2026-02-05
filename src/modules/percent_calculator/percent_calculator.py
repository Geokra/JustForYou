from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QComboBox, QFormLayout, QGroupBox, QLabel, QPushButton, QDoubleSpinBox, QVBoxLayout, QWidget
from module import Module

class PercentCalculator(Module):

    def on_enable(self):
        print("enable")
        self.button = QPushButton("Prozent Rechner")
        self.widget = QWidget()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(12)

        # --- Storage calculation group ---
        storage_group = QGroupBox("Prozentberechnung")
        storage_layout = QVBoxLayout(storage_group)

        # 1. Add the Selection ComboBox at the top of the group
        self.calc_mode_combo = QComboBox()
        self.calc_mode_combo.addItems(["Prozentwert Dazu Rechnen",
                                       "Prozentwert Abziehen",
                                       "Prozentwert von einem Wert ausrechnen",
                                       "Prozentsatz von Werten ausrechnen",
                                       "Bruttopreis ausrechnen",
                                       "Nettopreis ausrechnen"])
        storage_layout.addWidget(self.calc_mode_combo)

        # 2. This is your existing Form Layout for shared or specific inputs
        self.form_layout = QFormLayout()
        self.form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)

        # Example Input: Always visible
        self.input_base = QDoubleSpinBox()
        self.input_base.setRange(0, float('inf'))
        self.form_layout.addRow("Grundwert:", self.input_base)

        # 3. Create a specific widget for "Prozentwert" inputs
        self.wert_container = QWidget()
        wert_layout = QFormLayout(self.wert_container)
        wert_layout.setContentsMargins(0, 0, 0, 0)  # Remove double margins
        self.input_percent = QDoubleSpinBox()
        wert_layout.addRow("Prozentsatz (%):", self.input_percent)

        # 4. Create a specific widget for "Prozentfuß" inputs
        self.fuss_container = QWidget()
        fuss_layout = QFormLayout(self.fuss_container)
        fuss_layout.setContentsMargins(0, 0, 0, 0)
        self.input_part = QDoubleSpinBox()
        fuss_layout.addRow("Prozentwert (Anteil):", self.input_part)

        # Add both containers to the form_layout
        self.form_layout.addRow(self.wert_container)
        self.form_layout.addRow(self.fuss_container)

        #form_layout = QFormLayout()
        #form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        #form_layout.setFormAlignment(Qt.AlignmentFlag.AlignTop)


        storage_layout.addLayout(self.form_layout)



        self.calculate_button = QPushButton("Berechnen")
        #self.calculate_button.clicked.connect(self.on_calculate_storage)
        storage_layout.addWidget(self.calculate_button)

        self.output_result = QLabel("Ergebnis: –")
        self.output_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.output_result.setStyleSheet("font-weight: bold;")
        storage_layout.addWidget(self.output_result)

        layout.addWidget(storage_group)


        self.widget.setLayout(layout)

    def on_disable(self):
        print("disable")
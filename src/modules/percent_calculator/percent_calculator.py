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

        self.input_base = QDoubleSpinBox()
        self.input_base.setRange(0, float('inf'))
        self.form_layout.addRow("Grundwert:", self.input_base)

        # ===========================================================================

        # 1. Create a specific widget for "Prozent dazu Rechnen" inputs
        self.prozentwert_dazu_container = QWidget()
        wert_layout = QFormLayout(self.prozentwert_dazu_container)
        wert_layout.setContentsMargins(0, 0, 0, 0)  # Remove double margins
        self.input_percent = QDoubleSpinBox()
        wert_layout.addRow("Prozentsatz (%):", self.input_percent)

        # ===========================================================================

        # 2. Create a specific widget for "Prozent Abziehen" inputs
        self.prozentwert_abziehen_container = QWidget()
        wert_layout = QFormLayout(self.prozentwert_abziehen_container)
        wert_layout.setContentsMargins(0, 0, 0, 0)
        self.input_part = QDoubleSpinBox()
        wert_layout.addRow("Prozentwert (%):", self.input_part)

        # ===========================================================================

        # 3. Create a specific widget for "Prozent von einem Wert ausrechnen" inputs
        self.prozentwert_davon_container = QWidget()
        wert_layout = QFormLayout(self.prozentwert_davon_container)
        wert_layout.setContentsMargins(0, 0, 0, 0)
        self.input_part = QDoubleSpinBox()
        wert_layout.addRow("Prozentwert (%):", self.input_part)

        # ===========================================================================

        # 4. Create a specific widget for "Prozentsatz ausrechnen von 2 Werten" inputs
        self.prozentwert_satz_container = QWidget()
        wert_layout = QFormLayout(self.prozentwert_satz_container)
        wert_layout.setContentsMargins(0, 0, 0, 0)
        self.input_part = QDoubleSpinBox()
        self.input_part.setRange(0, float('inf'))
        wert_layout.addRow("Grundwert 2:", self.input_part)


        # ===========================================================================

        # 5. Create a specific widget for "Bruttowert ausrechnen" inputs
        self.prozentwert_brutto_container = QWidget()
        wert_layout = QFormLayout(self.prozentwert_brutto_container)
        wert_layout.setContentsMargins(0, 0, 0, 0)
        self.input_part = QDoubleSpinBox()

        # ===========================================================================

        # 6. Create a specific widget for "Nettowert ausrechnen" inputs
        self.prozentwert_netto_container = QWidget()
        wert_layout = QFormLayout(self.prozentwert_netto_container)
        wert_layout.setContentsMargins(0, 0, 0, 0)
        self.input_part = QDoubleSpinBox()


        # Add both containers to the form_layout
        self.form_layout.addRow(self.prozentwert_dazu_container)
        self.form_layout.addRow(self.prozentwert_abziehen_container)
        self.form_layout.addRow(self.prozentwert_davon_container)
        self.form_layout.addRow(self.prozentwert_satz_container)
        self.form_layout.addRow(self.prozentwert_brutto_container)
        self.form_layout.addRow(self.prozentwert_netto_container)

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

        # --- Logic ---
        # Connect the switcher
        self.calc_mode_combo.currentTextChanged.connect(self.update_sub_ui)
        # Set initial state
        self.update_sub_ui(self.calc_mode_combo.currentText())

    def update_sub_ui(self, text):
        # Toggle visibility based on selection
        self.prozentwert_dazu_container.setVisible(text == "Prozentwert Dazu Rechnen")
        self.prozentwert_abziehen_container.setVisible(text == "Prozentwert Abziehen")
        self.prozentwert_davon_container.setVisible(text == "Prozentwert von einem Wert ausrechnen")
        self.prozentwert_satz_container.setVisible(text == "Prozentsatz von Werten ausrechnen")
        self.prozentwert_brutto_container.setVisible(text == "Bruttopreis ausrechnen")
        self.prozentwert_netto_container.setVisible(text == "Nettopreis ausrechnen")

    def on_disable(self):
        print("disable")
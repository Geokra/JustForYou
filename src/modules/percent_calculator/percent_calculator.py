from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QComboBox, QFormLayout, QGroupBox, QLabel,
                             QPushButton, QDoubleSpinBox, QVBoxLayout, QWidget)
from module import Module

# Assuming your helper functions are in calculations.py
from calculations import (Unit, calculate_percentage_dazu, calculate_percentage_weg,
                          calculate_percentage_davon, calculate_percentage_satz,
                          calculate_percentage_mwst_brutto, calculate_percentage_mwst_netto)


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

        # 1. Selection ComboBox
        self.calc_mode_combo = QComboBox()
        self.mode_map = {
            "Prozentwert Dazu Rechnen": Unit.dazu,
            "Prozentwert Abziehen": Unit.weg,
            "Prozentwert von einem Wert ausrechnen": Unit.davon,
            "Prozentsatz von Werten ausrechnen": Unit.satz,
            "Bruttopreis ausrechnen": Unit.brutto,
            "Nettopreis ausrechnen": Unit.netto
        }
        self.calc_mode_combo.addItems(self.mode_map.keys())
        storage_layout.addWidget(self.calc_mode_combo)

        # 2. Form Layout for Inputs
        self.form_layout = QFormLayout()
        self.form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)

        # Base Input (Grundwert) - Used by all
        self.input_base = QDoubleSpinBox()
        self.input_base.setRange(0, float('inf'))
        self.input_base.setDecimals(2)
        self.form_layout.addRow("Grundwert:", self.input_base)

        # --- Dynamic Input Container ---
        # Used for Dazu, Abziehen, and Davon (Percentage or Wert 2)
        self.container_dynamic = QWidget()
        dynamic_layout = QFormLayout(self.container_dynamic)
        dynamic_layout.setContentsMargins(0, 0, 0, 0)

        self.label_dynamic = QLabel("Prozent (%):")
        self.input_dynamic = QDoubleSpinBox()
        self.input_dynamic.setRange(0, float('inf'))
        self.input_dynamic.setDecimals(2)
        dynamic_layout.addRow(self.label_dynamic, self.input_dynamic)

        # --- Comparison Container ---
        # Used only for "Prozentsatz von Werten ausrechnen"
        self.container_satz = QWidget()
        satz_layout = QFormLayout(self.container_satz)
        satz_layout.setContentsMargins(0, 0, 0, 0)

        self.input_compare = QDoubleSpinBox()
        self.input_compare.setRange(0, float('inf'))
        self.input_compare.setDecimals(2)
        satz_layout.addRow("Vergleichswert:", self.input_compare)

        # Add containers to the main form
        self.form_layout.addRow(self.container_dynamic)
        self.form_layout.addRow(self.container_satz)

        storage_layout.addLayout(self.form_layout)

        # --- Action & Output ---
        self.calculate_button = QPushButton("Berechnen")
        self.calculate_button.clicked.connect(self.on_calculate_storage)
        storage_layout.addWidget(self.calculate_button)

        self.output_result = QLabel("Ergebnis: –")
        self.output_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.output_result.setStyleSheet("font-weight: bold; font-size: 14px; color: #2ecc71;")
        storage_layout.addWidget(self.output_result)

        layout.addWidget(storage_group)
        self.widget.setLayout(layout)

        # --- Initialization ---
        self.calc_mode_combo.currentTextChanged.connect(self.update_sub_ui)
        self.update_sub_ui(self.calc_mode_combo.currentText())

    def update_sub_ui(self, text):
        mode = self.mode_map.get(text)

        # Toggle Visibility
        self.container_dynamic.setVisible(mode in [Unit.dazu, Unit.weg, Unit.davon])
        self.container_satz.setVisible(mode == Unit.satz)

        # Dynamic Label Text
        if text == "Prozentwert von einem Wert ausrechnen":
            self.label_dynamic.setText("Wert 2:")
        else:
            self.label_dynamic.setText("Prozent (%):")

    def on_calculate_storage(self):
        text = self.calc_mode_combo.currentText()
        mode = self.mode_map.get(text)

        val_base = self.input_base.value()
        val_dyn = self.input_dynamic.value()
        val_comp = self.input_compare.value()

        result = 0.0

        try:
            if mode == Unit.dazu:
                result = calculate_percentage_dazu(val_base, val_dyn)
            elif mode == Unit.weg:
                result = calculate_percentage_weg(val_base, val_dyn)
            elif mode == Unit.davon:
                result = calculate_percentage_davon(val_base, val_dyn)
            elif mode == Unit.satz:
                if val_comp != 0:
                    result = calculate_percentage_satz(val_base, val_comp)
                else:
                    self.output_result.setText("Fehler: Division durch 0")
                    return
            elif mode == Unit.brutto:
                result = calculate_percentage_mwst_brutto(val_base)
            elif mode == Unit.netto:
                result = calculate_percentage_mwst_netto(val_base)

            self.output_result.setText(f"Ergebnis: {result:,.2f}")
        except Exception as e:
            self.output_result.setText(f"Fehler: {str(e)}")

    def on_disable(self):
        print("disable")
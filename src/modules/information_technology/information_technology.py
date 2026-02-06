from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QComboBox, QDoubleSpinBox, QFormLayout, QGroupBox, QLabel, QPushButton, QSpinBox, QStackedWidget, QTextEdit, QVBoxLayout, QWidget
from module import Module
import helper
import history

class InformationTechnology(Module):

    def on_enable(self):
        self.button = QPushButton("Informationstechnik")
        self.widget = QWidget()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(12)

        options_group = QGroupBox()
        options_layout = QVBoxLayout(options_group)

        storage_calculation_button = QPushButton("Speicherberechnung")
        options_layout.addWidget(storage_calculation_button)
        
        base_calculation_button = QPushButton("Zahlensystemberechnung")
        options_layout.addWidget(base_calculation_button)

        data_conversion_button = QPushButton("Datenmengenumrechnung")
        options_layout.addWidget(data_conversion_button)

        self.stacked_widget = QStackedWidget()
        self.setup_ui_calculate_storage()
        self.setup_ui_base_calculation()
        self.setup_ui_data_conversion()
        self.stacked_widget.addWidget(self.storage_group)
        self.stacked_widget.addWidget(self.base_group)
        self.stacked_widget.addWidget(self.data_conversion_group)

        storage_calculation_button.clicked.connect(self.switch_to_storage)
        base_calculation_button.clicked.connect(self.switch_to_base)
        data_conversion_button.clicked.connect(self.switch_to_data_conversion)

        layout.addWidget(options_group)
        layout.addWidget(self.stacked_widget)

        self.widget.setLayout(layout)
    
    def on_disable(self):
        pass

    def switch_to_storage(self):
        self.stacked_widget.setCurrentWidget(self.storage_group)

    def switch_to_base(self):
        self.stacked_widget.setCurrentWidget(self.base_group)
        
    def switch_to_data_conversion(self):
        self.stacked_widget.setCurrentWidget(self.data_conversion_group)

    def on_calculate_storage(self):
        result = helper.calculate_storage(
                self.input_width.value(),
                self.input_height.value(),
                self.input_color_depth.value(),
                self.input_frames.value()
        )
        
        target_unit = helper.Unit[self.unit.currentText()]
        result = helper.convert_to_unit(result, helper.Unit.BIT, target_unit)
        history.history.update(f"{result} {target_unit.name}")

    def on_calculate_base(self):
        text = self.number.toPlainText().strip()
        from_base_text = self.base_from.currentText().upper()
        to_base_text = self.base_to.currentText().upper()

        from_base = helper.Base[from_base_text]
        to_base = helper.Base[to_base_text]

        try:
            result = helper.convert_number(text, from_base, to_base)
            self.error.setText("")
            history.history.update(result)
        except ValueError:
            self.error.setText("Ungültige Eingabe")

    def on_convert_data(self):
        value = self.data_value.value()
        from_unit = self.data_from.currentText()
        to_unit = self.data_to.currentText()

        try:
            result = helper.convert_data_units(value, from_unit, to_unit)
            
            if result == int(result):
                result_text = f"{int(result)} {to_unit}"
            else:
                result_text = f"{result:.6f} {to_unit}"
            
            self.data_error.setText("")
            history.history.update(result_text)
            
        except Exception as e:
            self.data_error.setText(f"Fehler bei der Umrechnung: {str(e)}")
        


    def setup_ui_calculate_storage(self):
        self.storage_group = QGroupBox("Speicherberechnung")
        storage_layout = QVBoxLayout(self.storage_group)

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

        calculate_button = QPushButton("Berechnen")
        calculate_button.clicked.connect(self.on_calculate_storage)
        
        storage_layout.addLayout(form_layout)
        storage_layout.addWidget(calculate_button)


    def setup_ui_base_calculation(self):
        self.base_group = QGroupBox("Zahlensystemberechnung")
        base_layout = QVBoxLayout(self.base_group)

        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignTop)

        self.base_from = QComboBox()
        self.base_from.addItems(["decimal", "binary", "ternary", "octal"])

        self.base_to = QComboBox()
        self.base_to.addItems(["decimal", "binary", "ternary", "octal"])

        self.number = QTextEdit()
        self.number.setPlaceholderText("Geben Sie hier die Zahl ein")

        form_layout.addRow("Von Zahlensystem:", self.base_from)
        form_layout.addRow("Zu Zahlensystem:", self.base_to)
        form_layout.addRow("Zahl:", self.number)

        base_layout.addLayout(form_layout)

        self.error = QLabel()
        base_layout.addWidget(self.error)

        calculate_button = QPushButton("Umrechnen")
        calculate_button.clicked.connect(self.on_calculate_base)
        base_layout.addWidget(calculate_button)

    def setup_ui_data_conversion(self):
        self.data_conversion_group = QGroupBox("Datenmengenumrechnung")
        data_layout = QVBoxLayout(self.data_conversion_group)

        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignTop)

        self.data_value = QDoubleSpinBox()
        self.data_value.setRange(0.000001, 999999999.0)
        self.data_value.setDecimals(6)
        self.data_value.setValue(1.0)

        self.data_from = QComboBox()
        self.data_from.addItems(["B", "KiB", "MiB", "GiB", "TiB", "KB", "MB", "GB", "TB"])

        self.data_to = QComboBox()
        self.data_to.addItems(["B", "KiB", "MiB", "GiB", "TiB", "KB", "MB", "GB", "TB"])

        form_layout.addRow("Wert:", self.data_value)
        form_layout.addRow("Von Einheit:", self.data_from)
        form_layout.addRow("Zu Einheit:", self.data_to)

        data_layout.addLayout(form_layout)

        self.data_error = QLabel()
        self.data_error.setStyleSheet("color: red;")
        data_layout.addWidget(self.data_error)

        info_label = QLabel(
            "Binärpräfixe (KiB, MiB, GiB, TiB) verwenden Basis 1024\n"
            "Dezimalpräfixe (KB, MB, GB, TB) verwenden Basis 1000"
        )
        info_label.setStyleSheet("color: gray; font-size: 9pt;")
        data_layout.addWidget(info_label)

        convert_button = QPushButton("Umrechnen")
        convert_button.clicked.connect(self.on_convert_data)
        data_layout.addWidget(convert_button)

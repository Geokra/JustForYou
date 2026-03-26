
import json
import os
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontDatabase
from PyQt6.QtWidgets import QColorDialog, QComboBox, QFormLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QScrollArea, QSlider, QVBoxLayout, QWidget



SETTINGS_FILE = "settings.json"

DEFAULTS = {
    "primary_color":    "#4CAF50",
    "hover_color":      "#45a049",
    "bg_left":          "#2C2C2C",
    "bg_right":         "#f4f4f4",
    "text_color":       "#333333",
    "button_text_color":"#ffffff",
    "font_family":      "Arial",
    "font_size":        16,
}


def _color_button(color: str) -> QPushButton:
    btn = QPushButton()
    btn.setFixedSize(80, 32)
    btn.setStyleSheet(
        f"background-color: {color}; border: 1px solid #888; border-radius: 4px;"
    )
    return btn


class Settings:

    def __init__(self):
        self.window = None
        self.widget: QWidget | None = None
        self._values: dict = dict(DEFAULTS)
        self._color_btns: dict[str, QPushButton] = {}
        self._font_combo: QComboBox | None = None
        self._size_slider: QSlider | None = None
        self._size_label: QLabel | None = None
        self.load()


    def load(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    stored = json.load(f)
                self._values.update({k: stored[k] for k in DEFAULTS if k in stored})
            except Exception as e:
                print(f"Settings load error: {e}")

    def save(self):
        try:
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(self._values, f, indent=2)
        except Exception as e:
            print(f"Settings save error: {e}")

    
    def build_stylesheet(self) -> str:
        v = self._values
        return f"""
#left_section {{
    background-color: {v['bg_left']};
    padding: 10px;
    min-width: 200px;
}}

#left_bottom_section {{
    background-color: {v['bg_left']};
    padding: 10px;
    min-width: 200px;
    max-width: 200px;
}}

#right_section {{
    background-color: {v['bg_right']};
    border-radius: 10px;
    padding: 20px;
}}

QPushButton {{
    background-color: {v['primary_color']};
    color: {v['button_text_color']};
    padding: 15px;
    border-radius: 5px;
    font-size: {v['font_size']}px;
    font-family: "{v['font_family']}";
    margin: 5px;
}}

QPushButton:hover {{
    background-color: {v['hover_color']};
}}

QStackedWidget {{
    background-color: {v['bg_right']};
}}

QLabel {{
    font-size: {v['font_size'] + 4}px;
    font-weight: bold;
    color: {v['text_color']};
    margin: 20px;
    font-family: "{v['font_family']}";
}}
"""


    def apply(self):
        """Push the current stylesheet to the main window."""
        if self.window:
            self.window.setStyleSheet(self.build_stylesheet())


    def setup_ui(self):
        self.widget = QWidget()
        self.widget.setObjectName("settings_widget")

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(scroll.Shape.NoFrame)

        inner = QWidget()
        outer_layout = QVBoxLayout(inner)
        outer_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        outer_layout.setSpacing(16)
        outer_layout.setContentsMargins(20, 20, 20, 20)

        outer_layout.addWidget(QLabel("Einstellungen"))

        color_group = QGroupBox("Farben")
        color_form = QFormLayout(color_group)
        color_form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        color_form.setSpacing(10)

        color_fields = [
            ("primary_color",     "Primärfarbe (Button)"),
            ("hover_color",       "Hover-Farbe"),
            ("bg_left",           "Hintergrund links"),
            ("bg_right",          "Hintergrund rechts"),
            ("text_color",        "Textfarbe"),
            ("button_text_color", "Button-Textfarbe"),
        ]

        for key, label in color_fields:
            btn = _color_button(self._values[key])
            hex_edit = QLineEdit(self._values[key])
            hex_edit.setFixedWidth(90)

            def _make_picker(k, b, h):
                def pick():
                    from PyQt6.QtGui import QColor
                    c = QColorDialog.getColor(
                        QColor(self._values[k]), self.widget, f"Farbe wählen – {k}"
                    )
                    if c.isValid():
                        hex_val = c.name()
                        self._values[k] = hex_val
                        b.setStyleSheet(
                            f"background-color: {hex_val}; border: 1px solid #888; border-radius: 4px;"
                        )
                        h.setText(hex_val)
                        self.apply()
                return pick

            def _make_hex_changed(k, b):
                def changed(text):
                    if len(text) == 7 and text.startswith("#"):
                        self._values[k] = text
                        b.setStyleSheet(
                            f"background-color: {text}; border: 1px solid #888; border-radius: 4px;"
                        )
                        self.apply()
                return changed

            btn.clicked.connect(_make_picker(key, btn, hex_edit))
            hex_edit.textChanged.connect(_make_hex_changed(key, btn))
            self._color_btns[key] = btn

            row = QWidget()
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.addWidget(btn)
            row_layout.addWidget(hex_edit)
            row_layout.addStretch()

            color_form.addRow(label, row)

        outer_layout.addWidget(color_group)

        font_group = QGroupBox("Schrift")
        font_layout = QFormLayout(font_group)
        font_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        font_layout.setSpacing(10)

        self._font_combo = QComboBox()
        families = sorted(QFontDatabase.families())
        self._font_combo.addItems(families)
        if self._values["font_family"] in families:
            self._font_combo.setCurrentText(self._values["font_family"])
        self._font_combo.currentTextChanged.connect(self._on_font_changed)
        font_layout.addRow("Schriftart", self._font_combo)

        size_row = QWidget()
        size_row_layout = QHBoxLayout(size_row)
        size_row_layout.setContentsMargins(0, 0, 0, 0)

        self._size_slider = QSlider(Qt.Orientation.Horizontal)
        self._size_slider.setRange(10, 32)
        self._size_slider.setValue(self._values["font_size"])
        self._size_slider.setFixedWidth(180)

        self._size_label = QLabel(f"{self._values['font_size']} px")
        self._size_label.setFixedWidth(50)

        self._size_slider.valueChanged.connect(self._on_size_changed)
        size_row_layout.addWidget(self._size_slider)
        size_row_layout.addWidget(self._size_label)
        size_row_layout.addStretch()
        font_layout.addRow("Schriftgröße", size_row)

        outer_layout.addWidget(font_group)

        btn_row = QHBoxLayout()

        save_btn = QPushButton("Speichern")
        save_btn.clicked.connect(self._on_save)

        reset_btn = QPushButton("Zurücksetzen")
        reset_btn.clicked.connect(self._on_reset)

        btn_row.addWidget(save_btn)
        btn_row.addWidget(reset_btn)
        btn_row.addStretch()
        outer_layout.addLayout(btn_row)

        scroll.setWidget(inner)

        root_layout = QVBoxLayout(self.widget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.addWidget(scroll)

    def _on_font_changed(self, family: str):
        self._values["font_family"] = family
        self.apply()

    def _on_size_changed(self, value: int):
        self._values["font_size"] = value
        if self._size_label:
            self._size_label.setText(f"{value} px")
        self.apply()

    def _on_save(self):
        self.save()
        print("Settings gespeichert.")

    def _on_reset(self):
        self._values = dict(DEFAULTS)
        # refresh color buttons
        for key, btn in self._color_btns.items():
            btn.setStyleSheet(
                f"background-color: {DEFAULTS[key]}; border: 1px solid #888; border-radius: 4px;"
            )
        if self._font_combo:
            self._font_combo.setCurrentText(DEFAULTS["font_family"])
        if self._size_slider:
            self._size_slider.setValue(DEFAULTS["font_size"])
        self.apply()

    def set_window(self, window):
        self.window = window
        self.apply()     

settings = Settings()
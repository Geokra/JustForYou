
import json
import os
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontDatabase
from PyQt6.QtWidgets import QColorDialog, QComboBox, QFormLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QScrollArea, QSlider, QVBoxLayout, QWidget



SETTINGS_FILE = "settings.json"

DEFAULTS = {
    "primary_color":    "#4CAF50",
    "hover_color":      "#45a049",
    "bg_left":          "#1E1E2E",
    "bg_right":         "#FAFAFA",
    "text_color":       "#2D2D2D",
    "button_text_color":"#ffffff",
    "font_family":      "Arial",
    "font_size":        16,
}

_QSS_TEMPLATE = """
/* ===== Global ===== */
QWidget {{
    font-family: "{font_family}";
    font-size: {font_size}px;
    color: {text_color};
}}

/* ===== Layout Sections ===== */
#left_section {{
    background-color: {bg_left};
    padding: 10px;
    min-width: 200px;
}}

#left_bottom_section {{
    background-color: {bg_left};
    padding: 10px;
    min-width: 200px;
    max-width: 200px;
}}

#right_section {{
    background-color: {bg_right};
    border-radius: 10px;
    padding: 20px;
}}

#right_bottom_section {{
    background-color: {bg_right};
    border-top: 1px solid #E0E0E0;
    padding: 12px;
}}

QStackedWidget {{
    background-color: {bg_right};
}}

/* ===== Sidebar Buttons ===== */
#left_section QPushButton,
#left_bottom_section QPushButton {{
    background: transparent;
    color: #B0B0B0;
    border: none;
    text-align: left;
    padding: 12px 16px;
    border-radius: 6px;
    font-size: {font_size_sidebar}px;
    font-family: "{font_family}";
    margin: 2px 0px;
}}

#left_section QPushButton:hover,
#left_bottom_section QPushButton:hover {{
    background: rgba(255, 255, 255, 0.08);
    color: #FFFFFF;
}}

#left_section QPushButton:pressed,
#left_bottom_section QPushButton:pressed {{
    background: rgba(255, 255, 255, 0.12);
}}

/* ===== Content Area Buttons ===== */
#right_section QPushButton {{
    background-color: {primary_color};
    color: {button_text_color};
    padding: 10px 24px;
    border-radius: 6px;
    border: none;
    font-size: {font_size}px;
    font-family: "{font_family}";
    font-weight: 600;
    margin: 4px 2px;
}}

#right_section QPushButton:hover {{
    background-color: {hover_color};
}}

#right_section QPushButton:pressed {{
    background-color: {pressed_color};
}}

#right_section QPushButton:disabled {{
    background-color: #BDBDBD;
    color: #757575;
}}

/* ===== Tab Buttons ===== */
#tab_btn {{
    background: transparent;
    border: none;
    border-bottom: 3px solid transparent;
    padding: 10px 16px;
    color: #757575;
    font-weight: 600;
    font-family: "{font_family}";
    border-radius: 0px;
    margin: 0px;
}}

#tab_btn:checked {{
    border-bottom-color: {primary_color};
    color: {text_color};
}}

#tab_btn:hover:!checked {{
    color: {text_color};
    border-bottom-color: #E0E0E0;
}}

/* ===== Calculator Buttons ===== */
#calc_btn, #calc_btn_clear, #calc_btn_backspace, #calc_btn_equals {{
    font-size: 18px;
    font-weight: bold;
    padding: 10px;
    border-radius: 8px;
    min-width: 60px;
    border: 1px solid #4A4A5A;
}}

#calc_btn {{
    background-color: #3A3A4A;
    color: white;
}}

#calc_btn:hover {{
    background-color: #4A4A5A;
}}

#calc_btn:pressed {{
    background-color: #2A2A3A;
}}

#calc_btn_clear {{
    background-color: #E53935;
    color: white;
    border-color: #C62828;
}}

#calc_btn_clear:hover {{
    background-color: #C62828;
}}

#calc_btn_backspace {{
    background-color: #F57C00;
    color: white;
    border-color: #E65100;
}}

#calc_btn_backspace:hover {{
    background-color: #E65100;
}}

#calc_btn_equals {{
    background-color: {primary_color};
    color: white;
    font-size: 20px;
    border-color: {hover_color};
}}

#calc_btn_equals:hover {{
    background-color: {hover_color};
}}

/* ===== QGroupBox ===== */
QGroupBox {{
    background: #FFFFFF;
    border: 1px solid #E0E0E0;
    border-radius: 8px;
    margin-top: 8px;
    padding: 16px 12px 12px 12px;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 4px 12px;
    color: {text_color};
    font-weight: bold;
    font-size: {font_size}px;
    font-family: "{font_family}";
}}

/* ===== QLabel ===== */
QLabel {{
    font-size: {font_size}px;
    color: {text_color};
    margin: 4px;
    font-family: "{font_family}";
    background: transparent;
}}

#result_label {{
    font-weight: 600;
    color: #2E7D32;
    font-size: {font_size_result}px;
    margin: 4px 0px;
}}

#error_label {{
    color: #D32F2F;
    font-weight: normal;
    font-size: {font_size_small}px;
}}

#info_label {{
    color: #757575;
    font-size: {font_size_info}px;
    font-weight: normal;
}}

#section_title {{
    font-size: {font_size_section}px;
    font-weight: 600;
    margin: 12px 0px 4px 0px;
    color: {text_color};
}}

/* ===== QLineEdit ===== */
QLineEdit {{
    background: #FFFFFF;
    border: 1px solid #E0E0E0;
    border-radius: 6px;
    padding: 8px 12px;
    color: {text_color};
    font-family: "{font_family}";
    font-size: {font_size}px;
    selection-background-color: {primary_color};
    selection-color: #FFFFFF;
}}

QLineEdit:focus {{
    border-color: {primary_color};
}}

QLineEdit:disabled {{
    background: #F5F5F5;
    color: #BDBDBD;
}}

/* ===== QSpinBox / QDoubleSpinBox ===== */
QSpinBox, QDoubleSpinBox {{
    background: #FFFFFF;
    border: 1px solid #E0E0E0;
    border-radius: 6px;
    padding: 6px 8px;
    color: {text_color};
    font-family: "{font_family}";
    font-size: {font_size}px;
    min-height: 20px;
}}

QSpinBox:focus, QDoubleSpinBox:focus {{
    border-color: {primary_color};
}}

QSpinBox::up-button, QDoubleSpinBox::up-button {{
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 24px;
    border-left: 1px solid #E0E0E0;
    border-bottom: 1px solid #E0E0E0;
    border-top-right-radius: 6px;
    background: #FAFAFA;
}}

QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover {{
    background: #F0F0F0;
}}

QSpinBox::down-button, QDoubleSpinBox::down-button {{
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    width: 24px;
    border-left: 1px solid #E0E0E0;
    border-bottom-right-radius: 6px;
    background: #FAFAFA;
}}

QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {{
    background: #F0F0F0;
}}

QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {{
    width: 0px;
    height: 0px;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-bottom: 5px solid #757575;
}}

QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {{
    width: 0px;
    height: 0px;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #757575;
}}

/* ===== QComboBox ===== */
QComboBox {{
    background: #FFFFFF;
    border: 1px solid #E0E0E0;
    border-radius: 6px;
    padding: 8px 12px;
    color: {text_color};
    font-family: "{font_family}";
    font-size: {font_size}px;
    min-height: 20px;
}}

QComboBox:focus {{
    border-color: {primary_color};
}}

QComboBox::drop-down {{
    border-left: 1px solid #E0E0E0;
    width: 30px;
    border-top-right-radius: 6px;
    border-bottom-right-radius: 6px;
    background: #FAFAFA;
}}

QComboBox::down-arrow {{
    width: 0px;
    height: 0px;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #757575;
}}

QComboBox QAbstractItemView {{
    background: #FFFFFF;
    border: 1px solid #E0E0E0;
    border-radius: 4px;
    selection-background-color: #E8F5E9;
    selection-color: {text_color};
    padding: 4px;
}}

/* ===== QTextEdit ===== */
QTextEdit {{
    background: #FFFFFF;
    border: 1px solid #E0E0E0;
    border-radius: 6px;
    padding: 8px;
    color: {text_color};
    font-family: "{font_family}";
    font-size: {font_size}px;
}}

QTextEdit:focus {{
    border-color: {primary_color};
}}

#history_text_edit {{
    font-family: monospace;
    border: 1px solid #E0E0E0;
    border-radius: 6px;
    padding: 8px;
    background: #FFFFFF;
}}

/* ===== QListWidget ===== */
QListWidget {{
    background: #FFFFFF;
    border: 1px solid #E0E0E0;
    border-radius: 6px;
    padding: 4px;
}}

QListWidget::item {{
    padding: 6px 8px;
    border-bottom: 1px solid #F0F0F0;
}}

QListWidget::item:selected {{
    background: #E8F5E9;
    color: {text_color};
}}

QListWidget::item:hover {{
    background: #F5F5F5;
}}

/* ===== QSlider ===== */
QSlider::groove:horizontal {{
    height: 6px;
    background: #E0E0E0;
    border-radius: 3px;
}}

QSlider::handle:horizontal {{
    background: {primary_color};
    width: 18px;
    height: 18px;
    margin: -6px 0;
    border-radius: 9px;
}}

QSlider::handle:horizontal:hover {{
    background: {hover_color};
}}

QSlider::sub-page:horizontal {{
    background: {primary_color};
    border-radius: 3px;
}}

/* ===== QScrollArea ===== */
QScrollArea {{
    background: transparent;
    border: none;
}}

QScrollBar:vertical {{
    width: 8px;
    background: transparent;
}}

QScrollBar::handle:vertical {{
    background: #C0C0C0;
    border-radius: 4px;
    min-height: 20px;
}}

QScrollBar::handle:vertical:hover {{
    background: #A0A0A0;
}}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar:horizontal {{
    height: 8px;
    background: transparent;
}}

QScrollBar::handle:horizontal {{
    background: #C0C0C0;
    border-radius: 4px;
    min-width: 20px;
}}

QScrollBar::handle:horizontal:hover {{
    background: #A0A0A0;
}}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {{
    width: 0px;
}}

/* ===== QFrame HLine ===== */
QFrame[frameShape="4"] {{
    color: #E0E0E0;
    max-height: 1px;
}}

/* ===== QFormLayout Labels inside GroupBox ===== */
QGroupBox QLabel {{
    font-weight: normal;
    margin: 0px;
    font-size: {font_size}px;
    font-family: "{font_family}";
}}
"""


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
        fs = v['font_size']
        # Derive a darker shade for pressed state from primary_color
        pressed = v.get('hover_color', '#388E3C')
        return _QSS_TEMPLATE.format(
            primary_color=v['primary_color'],
            hover_color=v['hover_color'],
            pressed_color=pressed,
            bg_left=v['bg_left'],
            bg_right=v['bg_right'],
            text_color=v['text_color'],
            button_text_color=v['button_text_color'],
            font_family=v['font_family'],
            font_size=fs,
            font_size_sidebar=max(fs - 1, 12),
            font_size_result=fs + 1,
            font_size_small=max(fs - 1, 11),
            font_size_info=max(fs - 2, 11),
            font_size_section=fs + 2,
        )


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

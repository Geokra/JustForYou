
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox, QFormLayout, QGroupBox, QHBoxLayout,
    QLabel, QListWidget, QPushButton, QVBoxLayout, QWidget
)
from module import Module
import history


GRADE_SYSTEMS = {
    "1–6 (Noten)": {
        "type": "noten",
        "values": [1, 2, 3, 4, 5, 6],
        "labels": ["1", "2", "3", "4", "5", "6"],
        "best": 1,
        "worst": 6,
    },
    "1–15 (Punkte)": {
        "type": "punkte",
        "values": list(range(1, 16)),
        "labels": [str(i) for i in range(1, 16)],
        "best": 15,
        "worst": 1,
    },
}


def grade_recommendation(avg: float, system: dict) -> str:
    """Return the Zeugnisnote recommendation for a given average."""
    if system["type"] == "noten":
        rec = max(1, min(6, round(avg)))
        labels = {1: "1 (Sehr gut)", 2: "2 (Gut)", 3: "3 (Befriedigend)",
                  4: "4 (Ausreichend)", 5: "5 (Mangelhaft)", 6: "6 (Ungenügend)"}
        return labels[rec]
    else:
        rec = max(1, min(15, round(avg)))
        if rec >= 13:
            letter = "1"
        elif rec >= 10:
            letter = "2"
        elif rec >= 7:
            letter = "3"
        elif rec >= 4:
            letter = "4"
        elif rec >= 2:
            letter = "5"
        else:
            letter = "6"
        return f"{rec} Punkte (Note {letter})"


class Schule(Module):

    def on_enable(self):
        self.button = QPushButton("Schule")
        self.widget = QWidget()

        self._grades: list[float] = list()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(12)

        system_group = QGroupBox("Notensystem")
        system_layout = QHBoxLayout(system_group)
        system_layout.addWidget(QLabel("System:"))
        self.system_combo = QComboBox()
        self.system_combo.addItems(list(GRADE_SYSTEMS.keys()))
        self.system_combo.currentTextChanged.connect(self._on_system_changed)
        system_layout.addWidget(self.system_combo)
        layout.addWidget(system_group)

        input_group = QGroupBox("Note eingeben")
        input_layout = QHBoxLayout(input_group)

        self.grade_input = QComboBox()
        self._populate_grade_input()
        input_layout.addWidget(self.grade_input)

        add_button = QPushButton("Hinzufügen")
        add_button.clicked.connect(self._on_add_grade)
        input_layout.addWidget(add_button)

        remove_button = QPushButton("Letzte entfernen")
        remove_button.clicked.connect(self._on_remove_last)
        input_layout.addWidget(remove_button)

        reset_button = QPushButton("Zurücksetzen")
        reset_button.clicked.connect(self._on_reset)
        input_layout.addWidget(reset_button)

        layout.addWidget(input_group)

        list_group = QGroupBox("Eingegebene Noten")
        list_layout = QVBoxLayout(list_group)
        self.grade_list = QListWidget()
        self.grade_list.setFixedHeight(120)
        list_layout.addWidget(self.grade_list)
        layout.addWidget(list_group)

        result_group = QGroupBox("Ergebnis")
        result_layout = QFormLayout(result_group)
        result_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)

        self.lbl_count = QLabel("–")
        self.lbl_avg = QLabel("–")
        self.lbl_recommendation = QLabel("–")

        result_layout.addRow("Anzahl Noten:", self.lbl_count)
        result_layout.addRow("Notendurchschnitt:", self.lbl_avg)
        result_layout.addRow("Zeugnisnotenempfehlung:", self.lbl_recommendation)

        layout.addWidget(result_group)

        self.widget.setLayout(layout)

    def on_disable(self):
        pass

    def _current_system(self) -> dict:
        return GRADE_SYSTEMS[self.system_combo.currentText()]

    def _populate_grade_input(self):
        self.grade_input.clear()
        sys = self._current_system()
        self.grade_input.addItems(sys["labels"])

    def _on_system_changed(self):
        self._grades.clear()
        self.grade_list.clear()
        self._populate_grade_input()
        self._update_results()

    def _on_add_grade(self):
        sys = self._current_system()
        idx = self.grade_input.currentIndex()
        value = float(sys["values"][idx])
        self._grades.append(value)
        self.grade_list.addItem(f"Note: {sys['labels'][idx]}")
        self._update_results()

    def _on_remove_last(self):
        if self._grades:
            self._grades.pop()
            self.grade_list.takeItem(self.grade_list.count() - 1)
            self._update_results()

    def _on_reset(self):
        self._grades.clear()
        self.grade_list.clear()
        self._update_results()

    def _update_results(self):
        n = len(self._grades)
        if n == 0:
            self.lbl_count.setText("–")
            self.lbl_avg.setText("–")
            self.lbl_recommendation.setText("–")
            return

        avg = sum(self._grades) / n
        sys = self._current_system()
        rec = grade_recommendation(avg, sys)

        self.lbl_count.setText(str(n))
        self.lbl_avg.setText(f"{avg:.2f}")
        self.lbl_recommendation.setText(rec)

        history.history.update(
            f"Schule | {n} Noten | Ø {avg:.2f} | Empfehlung: {rec}"
        )
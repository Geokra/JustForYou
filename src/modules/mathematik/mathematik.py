from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox, QDoubleSpinBox, QFormLayout, QGroupBox, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSpinBox, QStackedWidget,
    QVBoxLayout, QWidget
)

from module import Module
from modules.mathematik.math_helper import factorial, sqrt, decimal_to_fraction, simplify_fraction
import history


class Mathematik(Module):

    def on_enable(self):
        self.button = QPushButton("Mathematik")
        self.widget = QWidget()

        layout = QVBoxLayout(self.widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        header = QGroupBox()
        tab_layout = QHBoxLayout(header)

        self.tab_functions = QPushButton("Funktionen")
        self.tab_primes = QPushButton("Primzahlen")
        self.tab_fractions = QPushButton("Bruchrechnung")

        for b in (self.tab_functions, self.tab_primes, self.tab_fractions):
            b.setCheckable(True)
            b.setAutoExclusive(True)
            tab_layout.addWidget(b)

        layout.addWidget(header)

        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        self.stack.addWidget(self._build_functions_page())
        self.stack.addWidget(self._build_primes_page())
        self.stack.addWidget(self._build_fractions_page())

        self.tab_functions.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.tab_primes.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.tab_fractions.clicked.connect(lambda: self.stack.setCurrentIndex(2))

        self.tab_functions.setChecked(True)

    def on_disable(self):
        pass

    def _build_functions_page(self) -> QWidget:
        page = QWidget()
        outer = QVBoxLayout(page)
        outer.setAlignment(Qt.AlignmentFlag.AlignTop)

        group = QGroupBox("Mathematische Funktionen")
        group_layout = QVBoxLayout(group)

        self.func_combo = QComboBox()
        self.func_combo.addItems(["Fakultät", "Quadratwurzel", "Potenz"])
        self.func_combo.currentTextChanged.connect(self._on_func_changed)
        group_layout.addWidget(self.func_combo)

        form = QFormLayout()

        self.func_label_a = QLabel("")

        self.func_input_int = QSpinBox()
        self.func_input_int.setRange(0, 1_000_000)

        self.func_input_float = QDoubleSpinBox()
        self.func_input_float.setRange(-1e9, 1e9)
        self.func_input_float.setDecimals(10)

        form.addRow(self.func_label_a, self.func_input_int)
        form.addRow("", self.func_input_float)

        self.func_input_b = QDoubleSpinBox()
        self.func_input_b.setRange(-1e9, 1e9)
        self.func_input_b.setDecimals(10)

        self.func_label_b = QLabel("Exponent:")
        form.addRow(self.func_label_b, self.func_input_b)

        group_layout.addLayout(form)

        calc_btn = QPushButton("Berechnen")
        calc_btn.clicked.connect(self._calc_function)
        group_layout.addWidget(calc_btn)

        self.func_result = QLabel()
        self.func_result.setWordWrap(True)
        self.func_result.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.func_result.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        group_layout.addWidget(self.func_result)

        self.func_error = QLabel()
        group_layout.addWidget(self.func_error)

        outer.addWidget(group)

        self._on_func_changed(self.func_combo.currentText())
        return page

    def _on_func_changed(self, text: str):
        is_potenz = text == "Potenz"
        is_fakultaet = text == "Fakultät"

        self.func_input_b.setVisible(is_potenz)
        self.func_label_b.setVisible(is_potenz)

        if is_fakultaet:
            self.func_label_a.setText("n (≥ 0):")
            self.func_input_int.show()
            self.func_input_float.hide()
        elif text == "Quadratwurzel":
            self.func_label_a.setText("Zahl (≥ 0):")
            self.func_input_int.hide()
            self.func_input_float.show()
        else:
            self.func_label_a.setText("Basis:")
            self.func_input_int.hide()
            self.func_input_float.show()

    def _format_result(self, value: float) -> str:
        if value == int(value) and abs(value) < 1e15:
            return str(int(value))
        return f"{value:.10g}"

    def _calc_function(self):
        self.func_error.clear()
        self.func_result.clear()

        mode = self.func_combo.currentText()

        try:
            if mode == "Fakultät":
                a = self.func_input_int.value()
                result = factorial(a)
                self.func_result.setText(f"Ergebnis: {result}")
                history.history.update(f"{a}! = {result}")

            elif mode == "Quadratwurzel":
                a = self.func_input_float.value()
                if a < 0:
                    self.func_result.setText("Zahl darf nicht negativ sein")
                else:
                    result = sqrt(a)
                    self.func_result.setText(f"Ergebnis: {self._format_result(result)}")
                    history.history.update(f"√{self._format_result(a)} = {self._format_result(result)}")

            elif mode == "Potenz":
                a = self.func_input_float.value()
                b = self.func_input_b.value()
                result = a ** b
                self.func_result.setText(f"Ergebnis: {self._format_result(result)}")
                history.history.update(
                    f"{self._format_result(a)}^{self._format_result(b)} = {self._format_result(result)}"
                )

        except OverflowError:
            self.func_error.setText("Fehler: Ergebnis zu groß")


    def _build_primes_page(self) -> QWidget:
        page = QWidget()
        outer = QVBoxLayout(page)

        group = QGroupBox("Primzahlen zwischen Grenzwerten")
        group_layout = QVBoxLayout(group)

        form = QFormLayout()

        self.prime_from = QSpinBox()
        self.prime_from.setRange(2, 1_000_000)

        self.prime_to = QSpinBox()
        self.prime_to.setRange(2, 1_000_000)
        self.prime_to.setValue(100)

        form.addRow("Untergrenze:", self.prime_from)
        form.addRow("Obergrenze:", self.prime_to)

        group_layout.addLayout(form)

        btn = QPushButton("Primzahlen finden")
        btn.clicked.connect(self._calc_primes)
        group_layout.addWidget(btn)

        self.prime_count = QLabel()
        self.prime_result = QLabel()
        self.prime_result.setWordWrap(True)
        self.prime_error = QLabel()

        group_layout.addWidget(self.prime_count)
        group_layout.addWidget(self.prime_result)
        group_layout.addWidget(self.prime_error)

        outer.addWidget(group)
        return page

    def _is_prime(self, n: int) -> bool:
        if n < 2:
            return False
        if n < 4:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    def _calc_primes(self):
        self.prime_error.clear()
        self.prime_count.clear()
        self.prime_result.clear()

        lo = self.prime_from.value()
        hi = self.prime_to.value()

        if lo > hi:
            self.prime_error.setText("Fehler: Untergrenze muss ≤ Obergrenze sein")
            return

        primes = [n for n in range(lo, hi + 1) if self._is_prime(n)]
        self.prime_count.setText(f"Anzahl: {len(primes)}")
        self.prime_result.setText(", ".join(map(str, primes)))

        history.history.update(f"Primzahlen [{lo}–{hi}]: {len(primes)} gefunden")


    def _build_fractions_page(self) -> QWidget:
        page = QWidget()
        outer = QVBoxLayout(page)

        group = QGroupBox("Bruch → Dezimal")
        layout = QVBoxLayout(group)

        form = QFormLayout()

        self.frac_numerator = QSpinBox()
        self.frac_denominator = QSpinBox()
        self.frac_denominator.setRange(1, 1_000_000)

        form.addRow("Zähler:", self.frac_numerator)
        form.addRow("Nenner:", self.frac_denominator)

        layout.addLayout(form)

        btn = QPushButton("Umwandeln")
        btn.clicked.connect(self._fraction_to_decimal)
        layout.addWidget(btn)

        self.frac_result = QLabel()
        self.frac_error = QLabel()

        layout.addWidget(self.frac_result)
        layout.addWidget(self.frac_error)

        outer.addWidget(group)
        return page

    def _fraction_to_decimal(self):
        self.frac_error.clear()
        self.frac_result.clear()

        try:
            num = self.frac_numerator.value()
            den = self.frac_denominator.value()

            result = num / den
            n, d = simplify_fraction(num, den)

            self.frac_result.setText(f"Ergebnis: {self._format_result(result)}")
            history.history.update(f"{n}/{d} = {self._format_result(result)}")

        except ValueError as e:
            self.frac_error.setText(f"Fehler: {e}")
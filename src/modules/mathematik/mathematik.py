import math
from fractions import Fraction

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox, QDoubleSpinBox, QFormLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSpinBox, QStackedWidget,
    QVBoxLayout, QWidget
)
from module import Module
import history


class Mathematik(Module):

    def on_enable(self):
        self.button = QPushButton("Mathematik")
        self.widget = QWidget()

        layout = QVBoxLayout(self.widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(12)

        # Tab header
        header = QGroupBox()
        tab_layout = QHBoxLayout(header)

        self.tab_functions = QPushButton("Funktionen")
        self.tab_primes = QPushButton("Primzahlen")
        self.tab_fractions = QPushButton("Bruchrechnung")

        for b in (self.tab_functions, self.tab_primes, self.tab_fractions):
            b.setCheckable(True)
            b.setAutoExclusive(True)
            b.setObjectName("tab_btn")
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
        self.stack.setCurrentIndex(0)

    def on_disable(self):
        pass

    # ── Page 1: Fakultät, Quadratwurzel, Potenz ──

    def _build_functions_page(self) -> QWidget:
        page = QWidget()
        outer = QVBoxLayout(page)
        outer.setAlignment(Qt.AlignmentFlag.AlignTop)
        outer.setSpacing(12)

        # Function selector
        group = QGroupBox("Mathematische Funktionen")
        group_layout = QVBoxLayout(group)

        self.func_combo = QComboBox()
        self.func_combo.addItems(["Fakultät", "Quadratwurzel", "Potenz"])
        self.func_combo.currentTextChanged.connect(self._on_func_changed)
        group_layout.addWidget(self.func_combo)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)

        self.func_input_a = QLineEdit()
        self.func_input_a.setPlaceholderText("Zahl eingeben...")
        self.func_label_a = QLabel("n:")
        form.addRow(self.func_label_a, self.func_input_a)

        self.func_input_b_container = QWidget()
        b_layout = QFormLayout(self.func_input_b_container)
        b_layout.setContentsMargins(0, 0, 0, 0)
        self.func_input_b = QLineEdit()
        self.func_input_b.setPlaceholderText("Exponent eingeben...")
        self.func_label_b = QLabel("Exponent:")
        b_layout.addRow(self.func_label_b, self.func_input_b)
        form.addRow(self.func_input_b_container)

        group_layout.addLayout(form)

        calc_btn = QPushButton("Berechnen")
        calc_btn.clicked.connect(self._calc_function)
        group_layout.addWidget(calc_btn)

        self.func_result = QLabel()
        self.func_result.setObjectName("result_label")
        group_layout.addWidget(self.func_result)

        self.func_error = QLabel()
        self.func_error.setObjectName("error_label")
        group_layout.addWidget(self.func_error)

        outer.addWidget(group)
        self._on_func_changed(self.func_combo.currentText())
        return page

    def _on_func_changed(self, text: str):
        is_potenz = text == "Potenz"
        is_fakultaet = text == "Fakultät"
        self.func_input_b_container.setVisible(is_potenz)

        if is_fakultaet:
            self.func_label_a.setText("n (≥ 0, ganzzahlig):")
            self.func_input_a.setPlaceholderText("Ganzzahl eingeben...")
        elif text == "Quadratwurzel":
            self.func_label_a.setText("Zahl (≥ 0):")
            self.func_input_a.setPlaceholderText("Zahl eingeben...")
        else:
            self.func_label_a.setText("Basis:")
            self.func_input_a.setPlaceholderText("Basis eingeben...")

    def _parse_rational(self, text: str) -> float:
        text = text.strip().replace(",", ".")
        if "/" in text:
            parts = text.split("/")
            if len(parts) != 2:
                raise ValueError("Ungültiger Bruch")
            return float(parts[0]) / float(parts[1])
        return float(text)

    def _format_result(self, value: float) -> str:
        if value == int(value) and abs(value) < 1e15:
            return str(int(value))
        return f"{value:.10g}"

    def _calc_function(self):
        self.func_error.clear()
        self.func_result.clear()
        mode = self.func_combo.currentText()

        try:
            a = self._parse_rational(self.func_input_a.text())

            if mode == "Fakultät":
                if a < 0 or a != int(a):
                    raise ValueError("n muss eine nicht-negative Ganzzahl sein")
                result = math.factorial(int(a))
                self.func_result.setText(f"Ergebnis: {result}")
                history.history.update(f"{int(a)}! = {result}")

            elif mode == "Quadratwurzel":
                if a < 0:
                    raise ValueError("Zahl darf nicht negativ sein")
                result = math.sqrt(a)
                self.func_result.setText(f"Ergebnis: {self._format_result(result)}")
                history.history.update(f"√{self._format_result(a)} = {self._format_result(result)}")

            elif mode == "Potenz":
                b = self._parse_rational(self.func_input_b.text())
                result = a ** b
                self.func_result.setText(f"Ergebnis: {self._format_result(result)}")
                history.history.update(
                    f"{self._format_result(a)}^{self._format_result(b)} = {self._format_result(result)}"
                )

        except ValueError as e:
            self.func_error.setText(f"Fehler: {e}")
        except OverflowError:
            self.func_error.setText("Fehler: Ergebnis zu groß")

    # ── Page 2: Primzahlen zwischen Grenzwerten ──

    def _build_primes_page(self) -> QWidget:
        page = QWidget()
        outer = QVBoxLayout(page)
        outer.setAlignment(Qt.AlignmentFlag.AlignTop)
        outer.setSpacing(12)

        group = QGroupBox("Primzahlen zwischen Grenzwerten")
        group_layout = QVBoxLayout(group)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)

        self.prime_from = QSpinBox()
        self.prime_from.setRange(2, 1_000_000)
        self.prime_from.setValue(2)
        form.addRow("Untergrenze:", self.prime_from)

        self.prime_to = QSpinBox()
        self.prime_to.setRange(2, 1_000_000)
        self.prime_to.setValue(100)
        form.addRow("Obergrenze:", self.prime_to)

        group_layout.addLayout(form)

        calc_btn = QPushButton("Primzahlen finden")
        calc_btn.clicked.connect(self._calc_primes)
        group_layout.addWidget(calc_btn)

        self.prime_count = QLabel()
        self.prime_count.setObjectName("result_label")
        group_layout.addWidget(self.prime_count)

        self.prime_result = QLabel()
        self.prime_result.setWordWrap(True)
        group_layout.addWidget(self.prime_result)

        self.prime_error = QLabel()
        self.prime_error.setObjectName("error_label")
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
        self.prime_result.setText(", ".join(str(p) for p in primes))
        history.history.update(f"Primzahlen [{lo}–{hi}]: {len(primes)} gefunden")

    # ── Page 3: Bruch ↔ Dezimalbruch ──

    def _build_fractions_page(self) -> QWidget:
        page = QWidget()
        outer = QVBoxLayout(page)
        outer.setAlignment(Qt.AlignmentFlag.AlignTop)
        outer.setSpacing(12)

        # Dezimal → Bruch
        dec_group = QGroupBox("Dezimalbruch → Gemeiner Bruch")
        dec_layout = QVBoxLayout(dec_group)

        form1 = QFormLayout()
        form1.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        self.dec_input = QLineEdit()
        self.dec_input.setPlaceholderText("z.B. 0,75 oder 0.75")
        form1.addRow("Dezimalzahl:", self.dec_input)
        dec_layout.addLayout(form1)

        dec_btn = QPushButton("Umwandeln")
        dec_btn.clicked.connect(self._decimal_to_fraction)
        dec_layout.addWidget(dec_btn)

        self.dec_result = QLabel()
        self.dec_result.setObjectName("result_label")
        dec_layout.addWidget(self.dec_result)

        self.dec_error = QLabel()
        self.dec_error.setObjectName("error_label")
        dec_layout.addWidget(self.dec_error)

        outer.addWidget(dec_group)

        # Bruch → Dezimal
        frac_group = QGroupBox("Gemeiner Bruch → Dezimalbruch")
        frac_layout = QVBoxLayout(frac_group)

        form2 = QFormLayout()
        form2.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        self.frac_numerator = QLineEdit()
        self.frac_numerator.setPlaceholderText("Zähler")
        form2.addRow("Zähler:", self.frac_numerator)

        self.frac_denominator = QLineEdit()
        self.frac_denominator.setPlaceholderText("Nenner")
        form2.addRow("Nenner:", self.frac_denominator)

        frac_layout.addLayout(form2)

        frac_btn = QPushButton("Umwandeln")
        frac_btn.clicked.connect(self._fraction_to_decimal)
        frac_layout.addWidget(frac_btn)

        self.frac_result = QLabel()
        self.frac_result.setObjectName("result_label")
        frac_layout.addWidget(self.frac_result)

        self.frac_error = QLabel()
        self.frac_error.setObjectName("error_label")
        frac_layout.addWidget(self.frac_error)

        outer.addWidget(frac_group)
        return page

    def _decimal_to_fraction(self):
        self.dec_error.clear()
        self.dec_result.clear()

        try:
            text = self.dec_input.text().strip().replace(",", ".")
            if not text:
                raise ValueError("Bitte eine Dezimalzahl eingeben")
            frac = Fraction(text).limit_denominator()
            self.dec_result.setText(f"Ergebnis: {frac.numerator}/{frac.denominator}")
            history.history.update(f"{text} = {frac.numerator}/{frac.denominator}")
        except (ValueError, ZeroDivisionError) as e:
            self.dec_error.setText(f"Fehler: {e}")

    def _fraction_to_decimal(self):
        self.frac_error.clear()
        self.frac_result.clear()

        try:
            num_text = self.frac_numerator.text().strip().replace(",", ".")
            den_text = self.frac_denominator.text().strip().replace(",", ".")

            if not num_text or not den_text:
                raise ValueError("Bitte Zähler und Nenner eingeben")

            numerator = float(num_text)
            denominator = float(den_text)

            if denominator == 0:
                raise ValueError("Nenner darf nicht 0 sein")

            result = numerator / denominator
            frac = Fraction(numerator).limit_denominator() / Fraction(denominator).limit_denominator()
            frac = frac.limit_denominator()

            self.frac_result.setText(f"Ergebnis: {self._format_result(result)}")
            history.history.update(f"{frac.numerator}/{frac.denominator} = {self._format_result(result)}")
        except ValueError as e:
            self.frac_error.setText(f"Fehler: {e}")

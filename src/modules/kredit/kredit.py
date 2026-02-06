from PyQt6.QtWidgets import (
    QWidget, QPushButton, QGroupBox, QHBoxLayout, QVBoxLayout, QStackedWidget,
    QLabel, QLineEdit, QGridLayout, QFrame, QSizePolicy, QSpacerItem
)
from PyQt6.QtCore import Qt, QDateTime
from module import Module
import history


class Kredit(Module):
    def on_enable(self):
        self.button = QPushButton("Kredit")
        self.widget = QWidget()

        self.pb_einmal = QPushButton("Einmalig")
        self.pb_laufzeit = QPushButton("Nach Laufzeit")
        self.pb_raten = QPushButton("Nach Raten")

        for b in (self.pb_einmal, self.pb_laufzeit, self.pb_raten):
            b.setCheckable(True)
            b.setAutoExclusive(True)

        main_layout = QVBoxLayout(self.widget)

        header_group = QGroupBox()
        tab_layout = QHBoxLayout(header_group)
        tab_layout.addWidget(self.pb_einmal)
        tab_layout.addWidget(self.pb_laufzeit)
        tab_layout.addWidget(self.pb_raten)
        main_layout.addWidget(header_group)

        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack, 1)

        self.page_einmal = self.build_page_einmal()
        self.page_laufzeit = self.build_page_laufzeit()
        self.page_raten = self.build_page_raten()

        self.stack.addWidget(self.page_einmal)
        self.stack.addWidget(self.page_laufzeit)
        self.stack.addWidget(self.page_raten)

        self.pb_einmal.clicked.connect(lambda: self.set_tab(0))
        self.pb_laufzeit.clicked.connect(lambda: self.set_tab(1))
        self.pb_raten.clicked.connect(lambda: self.set_tab(2))

        self.pb_einmal.setChecked(True)
        self.set_tab(0)

    def set_tab(self, index: int):
        self.stack.setCurrentIndex(index)

    def hline(self) -> QFrame:
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        return line

    def mk_label(self, text: str) -> QLabel:
        lb = QLabel(text)
        lb.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        lb.setMinimumHeight(32)
        lb.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        lb.setStyleSheet("margin: 0px;")
        return lb

    def mk_unit_label(self, text: str) -> QLabel:
        lb = QLabel(text)
        lb.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        lb.setMinimumHeight(32)
        lb.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        lb.setStyleSheet("margin: 0px;")
        return lb

    def mk_input(self) -> QLineEdit:
        le = QLineEdit()
        le.setFixedHeight(32)
        le.setMinimumWidth(180)
        le.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        return le

    def field_with_suffix(self, suffix: str):
        w = QWidget()
        lay = QHBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        le = self.mk_input()
        suf = self.mk_unit_label(suffix)
        suf.setMinimumWidth(suf.sizeHint().width())

        lay.addWidget(le, 1, alignment=Qt.AlignmentFlag.AlignVCenter)
        lay.addWidget(suf, 0, alignment=Qt.AlignmentFlag.AlignVCenter)
        return w, le

    def grid_one_per_row(self) -> QGridLayout:
        grid = QGridLayout()
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(12)
        grid.setColumnStretch(0, 0)
        grid.setColumnStretch(1, 1)
        grid.setContentsMargins(0, 0, 0, 0)
        return grid

    def add_one_field(self, grid: QGridLayout, row: int, label: str, w: QWidget):
        grid.addWidget(self.mk_label(label), row, 0, alignment=Qt.AlignmentFlag.AlignVCenter)
        grid.addWidget(w, row, 1, alignment=Qt.AlignmentFlag.AlignVCenter)

    def to_float(self, s: str) -> float:
        if s is None:
            raise ValueError("Leerer Wert")
        s = s.strip()
        if not s:
            raise ValueError("Leerer Wert")
        s = s.replace(" ", "")
        s = s.replace(".", "").replace(",", ".")
        return float(s)

    def to_int(self, s: str) -> int:
        v = self.to_float(s)
        iv = int(round(v))
        if abs(v - iv) > 1e-9:
            raise ValueError("Ganzzahl erwartet")
        return iv

    def eur(self, value: float) -> str:
        value = round(value + 1e-12, 2)
        s = f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return f"{s} €"

    def eur_value_only(self, value: float) -> str:
        value = round(value + 1e-12, 2)
        return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def monthly_rate(self, zinssatz_pa_percent: float) -> float:
        return (zinssatz_pa_percent / 100.0) / 12.0

    def einmalig(self, kreditbetrag: float, zinssatz_pa_percent: float, laufzeit_monate: int):
        i = self.monthly_rate(zinssatz_pa_percent)
        n = laufzeit_monate
        fv = kreditbetrag * ((1.0 + i) ** n)
        zinsen = fv - kreditbetrag
        return fv, zinsen

    def rate_bei_laufzeit(self, kreditbetrag: float, zinssatz_pa_percent: float,
                          laufzeit_monate: int, schlussrate: float):
        i = self.monthly_rate(zinssatz_pa_percent)
        n = laufzeit_monate

        if n <= 0:
            raise ValueError("Laufzeit muss > 0 sein")
        if schlussrate < 0:
            raise ValueError("Schlussrate darf nicht negativ sein")
        if schlussrate > kreditbetrag:
            raise ValueError("Schlussrate darf nicht größer als Kreditbetrag sein")

        if i == 0.0:
            rate = (kreditbetrag - schlussrate) / n
        else:
            disc = (1.0 + i) ** n
            pv_balloon = schlussrate / disc
            numerator = (kreditbetrag - pv_balloon) * i
            denom = 1.0 - (1.0 / disc)
            if denom == 0.0:
                raise ValueError("Ungültige Parameter")
            rate = numerator / denom

        gesamtzahlung = rate * n + schlussrate
        zinsen = gesamtzahlung - kreditbetrag
        return rate, gesamtzahlung, zinsen

    def laufzeit_bei_rate(self, kreditbetrag: float, zinssatz_pa_percent: float,
                          rate: float, schlussrate: float, max_months: int = 1200):
        i = self.monthly_rate(zinssatz_pa_percent)

        if rate <= 0:
            raise ValueError("Rate muss > 0 sein")
        if schlussrate < 0:
            raise ValueError("Schlussrate darf nicht negativ sein")
        if schlussrate > kreditbetrag:
            raise ValueError("Schlussrate darf nicht größer als Kreditbetrag sein")

        if i == 0.0:
            rest = kreditbetrag - schlussrate
            if rest < 0:
                raise ValueError("Schlussrate darf nicht größer als Kreditbetrag sein")
            n = int(rest / rate)
            if abs(rest - (n * rate)) > 1e-12:
                n += 1
            if n <= 0:
                n = 1
            gesamtzahlung = rate * n + schlussrate
            zinsen = gesamtzahlung - kreditbetrag
            return n, gesamtzahlung, zinsen

        if (rate / i) < kreditbetrag - 1e-9:
            raise ValueError("Rate zu klein für diesen Kredit/Zins")

        def pv_for_months(n: int) -> float:
            pv = 0.0
            base = 1.0 + i
            for t in range(1, n + 1):
                pv += rate / (base ** t)
            pv += schlussrate / (base ** n)
            return pv

        lo, hi = 1, max_months
        while lo < hi:
            mid = (lo + hi) // 2
            if pv_for_months(mid) >= kreditbetrag:
                hi = mid
            else:
                lo = mid + 1

        n = lo
        gesamtzahlung = rate * n + schlussrate
        zinsen = gesamtzahlung - kreditbetrag
        return n, gesamtzahlung, zinsen

    def _history_update(self, result: str, unit_name: str):
        ts = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm")
        target_unit = type("Unit", (), {"name": unit_name})()
        history.history.update(f"[{ts}] {result} {target_unit.name}")

    def _mk_result_label(self, text: str) -> QLabel:
        lb = QLabel(text)
        lb.setStyleSheet("margin: 0px;")
        return lb

    def build_page_einmal(self) -> QWidget:
        page = QWidget()
        outer = QVBoxLayout(page)

        self.e1_title = QLabel("Kredit mit einmaliger Rückzahlung")
        outer.addWidget(self.e1_title)
        outer.addWidget(self.hline())

        grid = self.grid_one_per_row()

        w_k, self.e1_kreditbetrag = self.field_with_suffix("€")
        w_p, self.e1_zinssatz = self.field_with_suffix("% p.a.")
        w_n, self.e1_laufzeit = self.field_with_suffix("Monate")

        self.add_one_field(grid, 0, "Kreditbetrag:", w_k)
        self.add_one_field(grid, 1, "Zinssatz:", w_p)
        self.add_one_field(grid, 2, "Laufzeit:", w_n)

        outer.addLayout(grid)

        self.e1_res_title = QLabel("Ergebnis")
        self.e1_res_title.setStyleSheet("margin: 0px;")
        outer.addWidget(self.e1_res_title)

        self.e1_out_rueckzahlung = self._mk_result_label("Rückzahlung gesamt: —")
        self.e1_out_zinsen = self._mk_result_label("Zinsen gesamt: —")
        outer.addWidget(self.e1_out_rueckzahlung)
        outer.addWidget(self.e1_out_zinsen)

        outer.addStretch(1)

        self.e1_btn = QPushButton("Berechnen")
        self.e1_btn.clicked.connect(self.calc_einmal)
        outer.addWidget(self.e1_btn, alignment=Qt.AlignmentFlag.AlignRight)
        return page

    def calc_einmal(self):
        try:
            k = self.to_float(self.e1_kreditbetrag.text())
            p = self.to_float(self.e1_zinssatz.text())
            n = self.to_int(self.e1_laufzeit.text())

            if k <= 0:
                raise ValueError("Kreditbetrag muss > 0 sein")
            if p < 0:
                raise ValueError("Zinssatz darf nicht negativ sein")
            if n <= 0:
                raise ValueError("Laufzeit muss > 0 sein")

            rueckzahlung, zinsen = self.einmalig(k, p, n)
            r_text = f"Rückzahlung gesamt: {self.eur(rueckzahlung)}"
            z_text = f"Zinsen gesamt: {self.eur(zinsen)}"

            self.e1_out_rueckzahlung.setText(r_text)
            self.e1_out_zinsen.setText(z_text)

            self._history_update(f"Rückzahlung gesamt: {self.eur_value_only(rueckzahlung)}", "EUR")
            self._history_update(f"Zinsen gesamt: {self.eur_value_only(zinsen)}", "EUR")
        except Exception as e:
            self.e1_out_rueckzahlung.setText("Rückzahlung gesamt: —")
            self.e1_out_zinsen.setText(f"Fehler: {e}")

    def build_page_laufzeit(self) -> QWidget:
        page = QWidget()
        outer = QVBoxLayout(page)

        self.l1_title = QLabel("Ratenkredit – Vorgabe der Laufzeit")
        outer.addWidget(self.l1_title)
        outer.addWidget(self.hline())

        grid = self.grid_one_per_row()

        w_k, self.l1_kreditbetrag = self.field_with_suffix("€")
        w_p, self.l1_zinssatz = self.field_with_suffix("% p.a.")
        w_n, self.l1_laufzeit = self.field_with_suffix("Monate")
        w_s, self.l1_schlussrate = self.field_with_suffix("€")

        self.add_one_field(grid, 0, "Kreditbetrag:", w_k)
        self.add_one_field(grid, 1, "Zinssatz:", w_p)
        self.add_one_field(grid, 2, "Laufzeit:", w_n)
        self.add_one_field(grid, 3, "Schlussrate:", w_s)

        outer.addLayout(grid)

        self.l1_res_title = QLabel("Ergebnis")
        self.l1_res_title.setStyleSheet("margin: 0px;")
        outer.addWidget(self.l1_res_title)

        self.l1_out_rate = self._mk_result_label("Ratenhöhe: —")
        self.l1_out_gesamt = self._mk_result_label("Gesamtzahlung: —")
        self.l1_out_zinsen = self._mk_result_label("Zinsen gesamt: —")
        outer.addWidget(self.l1_out_rate)
        outer.addWidget(self.l1_out_gesamt)
        outer.addWidget(self.l1_out_zinsen)

        outer.addStretch(1)

        self.l1_btn = QPushButton("Berechnen")
        self.l1_btn.clicked.connect(self.calc_laufzeit)
        outer.addWidget(self.l1_btn, alignment=Qt.AlignmentFlag.AlignRight)
        return page

    def calc_laufzeit(self):
        try:
            k = self.to_float(self.l1_kreditbetrag.text())
            p = self.to_float(self.l1_zinssatz.text())
            n = self.to_int(self.l1_laufzeit.text())
            s_txt = self.l1_schlussrate.text().strip()
            s = self.to_float(s_txt) if s_txt else 0.0

            if k <= 0:
                raise ValueError("Kreditbetrag muss > 0 sein")
            if p < 0:
                raise ValueError("Zinssatz darf nicht negativ sein")
            if n <= 0:
                raise ValueError("Laufzeit muss > 0 sein")

            rate, gesamt, zinsen = self.rate_bei_laufzeit(k, p, n, s)
            r_text = f"Ratenhöhe: {self.eur(rate)}"
            g_text = f"Gesamtzahlung: {self.eur(gesamt)}"
            z_text = f"Zinsen gesamt: {self.eur(zinsen)}"

            self.l1_out_rate.setText(r_text)
            self.l1_out_gesamt.setText(g_text)
            self.l1_out_zinsen.setText(z_text)

            self._history_update(f"Ratenhöhe: {self.eur_value_only(rate)}", "EUR")
            self._history_update(f"Gesamtzahlung: {self.eur_value_only(gesamt)}", "EUR")
            self._history_update(f"Zinsen gesamt: {self.eur_value_only(zinsen)}", "EUR")
        except Exception as e:
            self.l1_out_rate.setText("Ratenhöhe: —")
            self.l1_out_gesamt.setText("Gesamtzahlung: —")
            self.l1_out_zinsen.setText(f"Fehler: {e}")

    def build_page_raten(self) -> QWidget:
        page = QWidget()
        outer = QVBoxLayout(page)

        self.r1_title = QLabel("Ratenkredit – Vorgabe der Ratenhöhe")
        outer.addWidget(self.r1_title)
        outer.addWidget(self.hline())

        grid = self.grid_one_per_row()

        w_k, self.r1_kreditbetrag = self.field_with_suffix("€")
        w_p, self.r1_zinssatz = self.field_with_suffix("% p.a.")
        w_r, self.r1_rate = self.field_with_suffix("€")
        w_s, self.r1_schlussrate = self.field_with_suffix("€")

        self.add_one_field(grid, 0, "Kreditbetrag:", w_k)
        self.add_one_field(grid, 1, "Zinssatz:", w_p)
        self.add_one_field(grid, 2, "Ratenhöhe:", w_r)
        self.add_one_field(grid, 3, "Schlussrate:", w_s)

        outer.addLayout(grid)

        self.r1_res_title = QLabel("Ergebnis")
        self.r1_res_title.setStyleSheet("margin: 0px;")
        outer.addWidget(self.r1_res_title)

        self.r1_out_laufzeit = self._mk_result_label("Laufzeit (Monate): —")
        self.r1_out_gesamt = self._mk_result_label("Gesamtzahlung: —")
        self.r1_out_zinsen = self._mk_result_label("Zinsen gesamt: —")
        outer.addWidget(self.r1_out_laufzeit)
        outer.addWidget(self.r1_out_gesamt)
        outer.addWidget(self.r1_out_zinsen)

        outer.addStretch(1)

        self.r1_btn = QPushButton("Berechnen")
        self.r1_btn.clicked.connect(self.calc_raten)
        outer.addWidget(self.r1_btn, alignment=Qt.AlignmentFlag.AlignRight)
        return page

    def calc_raten(self):
        try:
            k = self.to_float(self.r1_kreditbetrag.text())
            p = self.to_float(self.r1_zinssatz.text())
            rate = self.to_float(self.r1_rate.text())
            s_txt = self.r1_schlussrate.text().strip()
            s = self.to_float(s_txt) if s_txt else 0.0

            if k <= 0:
                raise ValueError("Kreditbetrag muss > 0 sein")
            if p < 0:
                raise ValueError("Zinssatz darf nicht negativ sein")
            if rate <= 0:
                raise ValueError("Ratenhöhe muss > 0 sein")

            n, gesamt, zinsen = self.laufzeit_bei_rate(k, p, rate, s)
            l_text = f"Laufzeit (Monate): {n}"
            g_text = f"Gesamtzahlung: {self.eur(gesamt)}"
            z_text = f"Zinsen gesamt: {self.eur(zinsen)}"

            self.r1_out_laufzeit.setText(l_text)
            self.r1_out_gesamt.setText(g_text)
            self.r1_out_zinsen.setText(z_text)

            self._history_update(f"Laufzeit: {n}", "Monate")
            self._history_update(f"Gesamtzahlung: {self.eur_value_only(gesamt)}", "EUR")
            self._history_update(f"Zinsen gesamt: {self.eur_value_only(zinsen)}", "EUR")
        except Exception as e:
            self.r1_out_laufzeit.setText("Laufzeit (Monate): —")
            self.r1_out_gesamt.setText("Gesamtzahlung: —")
            self.r1_out_zinsen.setText(f"Fehler: {e}")

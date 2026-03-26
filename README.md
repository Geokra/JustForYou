# JustForYou

Ein modularer Taschenrechner mit grafischer Oberfläche, entwickelt mit Python und PyQt6.

## Features

### Taschenrechner
- Grundrechenarten (+, -, *, /)
- Potenzrechnung und Klammerunterstützung
- Eigener Expression-Parser mit korrekter Operatorrangfolge

### Prozentrechnung
- Prozentwert dazu rechnen / abziehen
- Prozentwert und Prozentsatz berechnen
- Brutto-/Nettopreisberechnung (19% MwSt.)

### Mathematik
- **Fakultät** (n!) -- eigene iterative Implementierung
- **Quadratwurzel** -- Heron-Verfahren (Newton-Iteration)
- **Potenzfunktion** -- Exponentiation by Squaring, rationale Exponenten via eigener ln/exp-Reihe
- **Primzahlen** zwischen zwei Grenzwerten finden (bis 1.000.000)
- **Bruchrechnung** -- Dezimal zu Bruch und umgekehrt, automatisches Kürzen via euklidischem Algorithmus

### Informationstechnik
- Speicherberechnung (Breite x Höhe x Farbtiefe x Frames)
- Zahlensysteme umrechnen (Binär, Oktal, Ternär, Dezimal)
- Dateneinheiten umrechnen (Binär- und Dezimalpräfixe)

### Kreditrechner
- Einmalrückzahlung, Ratentilgung, feste Monatsrate
- Zinsberechnung und Laufzeitermittlung
- Ausgabe in Euro-Format (1.234,56 EUR)

### Notenverwaltung
- Notensysteme 1--6 (Schulnoten) und 1--15 (Punkte)
- Durchschnittsberechnung und Zeugnisempfehlung

## Architektur

```
src/
├── main.py                          # Einstiegspunkt
├── module.py                        # Abstrakte Basisklasse für Module
├── history.py                       # Verlaufssystem
├── settings.py                      # Einstellungen (Farben, Schriftart)
├── manager/
│   └── module_manager.py            # Dynamischer Modullader
├── window/
│   └── window.py                    # Hauptfenster
└── modules/
    ├── basic_calculator/            # Taschenrechner
    ├── percent_calculator/          # Prozentrechnung
    ├── mathematik/                  # Mathematische Funktionen
    ├── information_technology/      # IT-Berechnungen
    ├── kredit/                      # Kreditrechner
    └── schule/                      # Notenverwaltung
styles/
└── main.qss                         # Stylesheet
```

Module werden dynamisch aus `src/modules/` geladen. Jedes Modul definiert eine `module.json` mit Name, Klasse und Einstiegsdatei.

## Installation

```bash
# Repository klonen
git clone https://github.com/Geokra/JustForYou.git
cd JustForYou

# Virtuelle Umgebung erstellen und aktivieren
python -m venv .venv
source .venv/bin/activate

# Abhängigkeiten installieren
pip install -r requirements.txt
```

## Starten

```bash
python src/main.py
```

## Einstellungen

Über den Button "Einstellungen" im Hauptfenster konfigurierbar:

- **Farben** -- Primärfarbe, Hover, Hintergrund, Text
- **Schriftart** -- Familie und Größe (10--32 px)

Einstellungen werden in `settings.json` gespeichert.

## Technische Details

- Keine externen Mathematik-Bibliotheken -- alle Berechnungen (Fakultät, Wurzel, Logarithmus, Exponentialfunktion) sind eigenständig implementiert
- Singleton-Pattern für Module
- Modulares Plugin-System mit ZIP-Archiv-Unterstützung für Distribution

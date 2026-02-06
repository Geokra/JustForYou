## Projekt: WINDOWS-Rechnermodul „JustForYou"

---

## 1 Projektbeschreibung

### Projektziel
Ziel des Projekts ist die Entwicklung einer modularisierten, unter WINDOWS lauffähigen Rechner-Software („JustForYou“), die aus einer Basisanwendung und bis zu drei kundenindividuell auswählbaren Branchenmodulen besteht. Die Module werden als Laufzeitbibliotheken realisiert und ermöglichen eine geführte, sequentielle Eingabe von Parametern sowie eine vollständige Protokollierung aller Berechnungen. Die Software soll wartungsfrei ausgeliefert werden und den Qualitätsanforderungen nach DIN ISO 21500, DIN ISO 9241 sowie relevanten Softwarequalitätsnormen entsprechen.

### Projektorganisation
- **Auftraggeber (AG):** Kleinstweich Deutschland GmbH (KWD)
- **Projektleiter (PL):** Georg Krauße – verantwortlich für Projektplanung, Termine, Kosten, Risikomanagement und Qualitätssicherung
- **Product Owner (PO):** Jamie Löhnert – verantwortlich für fachliche Anforderungen, Priorisierung der Funktionen, Kundenkontakt und Abnahmen
- **Projektteam:** 
  - Alexander Schwarz – Entwicklung Basisrechner, mathematische Funktionen, Modultests
  - Jonas Kipper – Entwicklung GUI, Eingabemodul, Integration der Branchenmodule

### Schnittstellen zu anderen Projekten
Es bestehen keine direkten Schnittstellen zu Parallelprojekten. Abhängigkeiten ergeben sich lediglich aus der Nutzung betrieblicher Infrastruktur und vorgegebener Entwicklungswerkzeuge (Microsoft-Umfeld).

### Beteiligte Lieferanten
- Microsoft AG (Entwicklungswerkzeuge, Betriebssystem)
- Open-Source-Komponenten (Freeware), sofern durch den AG genehmigt

### Rahmenbedingungen zu Terminen und Aufwand
- **Projektlaufzeit:** 7 Projektwochen
- **Kostenrahmen:** max. 30.000 € Personalkosten
- **Vorgehensmodell:** agil gemäß DIN ISO 21500
- **Dokumentenablage:** Closed-Shop über LernSax

---

## 2 Projektorganisation

### 2.1 Aufbauorganisation

#### Beteiligte Personen und Verantwortlichkeiten
- **Georg Krauße (Projektleiter):** Gesamtkoordination, Projektcontrolling, Qualitätssicherung, Risikomanagement, Pflege des Projektplans
- **Jamie Löhnert (Product Owner):** Abstimmung mit dem Kunden, Pflege des Product Backlogs, fachliche Abnahmen, Verantwortung für Black-Box-Tests
- **Alexander Schwarz:** Implementierung der Rechen- und Branchenmodule, Erstellung von Testlisten, technische Dokumentation
- **Jonas Kipper:** Implementierung der grafischen Benutzeroberfläche, Eingabemodul, GUI-Prototyping, Integration und Usability-Tests

#### Einbindung der Qualitätssicherung
- Qualitätssicherung ist integraler Bestandteil aller Projektphasen
- QS-Maßnahmen werden im Projektplan und Projekttagebuch dokumentiert
- Berücksichtigung von Datenschutz- und Datensicherheitsvorgaben

#### Mittel und Ressourcen für QM
- **Werkzeuge:** Python, IDE, Microsoft Office, UML-Tools
- **Zeit:** QS-Aufgaben in jedem Sprint eingeplant
- **Dokumente:** Projektplan, Pflichtenheft, Testlisten, QM-Plan

### 2.2 Berichtswesen

- **Arten von Berichten:**
  - Projekttagebuch (täglich)
  - Statusberichte (wöchentlich)
  - Meilensteinprotokolle
- **Auslöser:** Sprintende, Kundenmeetings, Abweichungen
- **Inhalte:** Fortschritt, Risiken, Qualität, Entscheidungen
- **Informationswege:** Projektteam ↔ PL ↔ PO ↔ Kunde

---

## 3 Qualitätsforderungen

### 3.1 Kundenanforderungen

- Einhaltung von DIN ISO 21500 (Projektmanagement)
- Softwareergonomie gemäß DIN ISO 9241
- Modulare Architektur mit Laufzeitbibliotheken
- Zwangsgeführte Benutzereingaben
- Vollständige und korrekte Ergebnisprotokollierung
- GUI-Prototyp muss vom AG freigegeben werden

### 3.2 Innerbetriebliche Anforderungen

- Programmiersprache Python
- Einheitliche Code-Konventionen
- Proprietäre Implementierung der Rechenfunktionen
- Nutzung genehmigter Werkzeuge (Microsoft-Umfeld)
- Vollständige Projektdokumentation

### 3.3 Projektbezogene Qualitätsziele

- **Funktionalität:** 100 % Umsetzung der freigegebenen Anforderungen
- **Zuverlässigkeit:** fehlerfreie Berechnungen gemäß Spezifikation
- **Benutzbarkeit:** ergonomische, konsistente GUI
- **Wartbarkeit:** klare Modul- und Schnittstellenstruktur
- **Prozessqualität:** termingerechte Meilensteinerreichung

---

## 4 Projektrisiken (Fehler-Einfluss-Analyse)

| Risiko | Ursache | Auswirkung | Gegenmaßnahme |
|------|--------|------------|---------------|
| Unklare Anforderungen | späte Präzisierungen | Nacharbeit | regelmäßige Abstimmungen |
| Zeitüberschreitung | zu hoher Implementierungsaufwand | Terminverzug | Sprintplanung, Priorisierung |
| Qualitätsmängel | fehlende Tests | Nachbesserungen | Testpläne, Reviews |
| Tool-Probleme | ungeeignete Werkzeuge | Effizienzverlust | Abstimmung mit AG |
| Personalausfall | Krankheit | Verzögerung | Wissensdokumentation |

---

## 5 Qualitätsmaßnahmeplan

### 5.1 Konstruktive Maßnahmen

#### 5.1.1 Problemmanagement
- Zentrale Erfassung von Problemen im Projekttagebuch
- Ursachenanalyse im Team
- Ableitung und Dokumentation von Korrekturmaßnahmen

#### 5.1.2 Vorgehensmodell
- Agiles Vorgehen (inkrementell, sprintbasiert)
- Abweichungen werden mit dem AG abgestimmt

#### 5.1.3 Fortbildung
- Kurze interne Schulungen zu Python, GUI-Framework, UML
- Selbststudium anhand bereitgestellter Materialien

#### 5.1.4 Technologie und technische Auslegung
- Objektorientierte Analyse und Design
- Klare Modul- und Schnittstellendefinition
- GUI-Prototyping vor Implementierung

### 5.2 Analytische Maßnahmen

#### 5.2.1 Statische Maßnahmen
- Reviews von Pflichtenheft, Klassendiagrammen und Code
- Meilensteine: GUI-Prototyp, Inkrement, Projektabschluss

#### 5.2.2 Dynamische Maßnahmen
- Black-Box-Tests für alle Module
- Testlisten mit prüfbaren Beispieldaten
- Tests vor jeder Meilensteinabnahme

#### 5.2.3 Lieferantenkontrolle
- Prüfung eingesetzter Frameworks und Tools auf AG-Freigabe

#### 5.2.4 Kundenkontakt
- Regelmäßige Meilensteinberatungen
- Präsentation von Zwischenergebnissen
- Dokumentierte Abnahmen durch den AG
# Mindrift

**Find your flow. Own your focus.**

Mindrift ist eine minimalistische Desktop-Anwendung zur Produktivitätssteigerung, entwickelt mit Python. Sie hilft dir dabei, Aufgaben zu organisieren, konzentrierte Arbeitssitzungen zu verwalten, Notizen zu speichern und deine Produktivität zu verfolgen – alles in einer übersichtlichen Oberfläche.

## Funktionen

- **Dashboard** – Behalte deine Produktivität im Überblick.
- **Aufgabenverwaltung** – Erstelle, erledige und lösche Aufgaben.
- **Pomodoro-Timer** – Konzentrierte Arbeitssitzungen sowie kurze und lange Pausen.
- **Notizen** – Erstelle, bearbeite und verwalte deine persönlichen Notizen.
- **Statistiken** – Verfolge erledigte Aufgaben und deine gesamte Fokuszeit.
- **Einstellungen** – Passe die Timer-Dauer und das Erscheinungsbild an.
- **Lokale Datenbank** – Speichere Aufgaben, Notizen, Sitzungen und Einstellungen mit SQLite.
- **Dark UI** – Minimalistisches Design mit Fokus auf Übersichtlichkeit.

## Verwendete Technologien

- Python
- CustomTkinter
- SQLite
- Matplotlib
- Pillow
- PyInstaller

## Projektstruktur

```text
Mindrift/
│
├── main.py
├── config.py
├── database.py
├── requirements.txt
├── build_exe.bat
│
├── data/
│
└── ui/
    ├── __init__.py
    ├── sidebar.py
    ├── dashboard.py
    ├── tasks.py
    ├── timer.py
    ├── notes.py
    ├── statistics.py
    └── settings.py
```

## Installation und Start

### Voraussetzungen

- Python 3.11 oder neuer
- pip

### Installation

1. Repository klonen:

```bash
git clone https://github.com/DEIN-BENUTZERNAME/mindrift.git
```

2. In das Projektverzeichnis wechseln:

```bash
cd mindrift
```

3. Abhängigkeiten installieren:

```bash
py -m pip install -r requirements.txt
```

4. Mindrift starten:

```bash
py main.py
```

## Datenspeicherung

Mindrift verwendet SQLite zur lokalen Speicherung deiner Daten.

Gespeichert werden:

- Aufgaben und deren Status
- Persönliche Notizen
- Fokus-Sitzungen
- Anwendungseinstellungen

Alle Daten werden lokal gespeichert. Ein Online-Konto ist nicht erforderlich.

## Windows-Version erstellen

Mit PyInstaller kann Mindrift als eigenständige Windows-Anwendung erstellt werden.

Führe dazu folgende Datei aus:

```bash
build_exe.bat
```

Die fertige EXE-Datei wird im Verzeichnis `dist/` erstellt.

## Roadmap

- [x] Grundstruktur der Desktop-Anwendung
- [x] SQLite-Datenbankintegration
- [x] Aufgabenverwaltung
- [x] Pomodoro-Timer
- [x] Notizenverwaltung
- [x] Produktivitätsstatistiken
- [x] Anwendungseinstellungen
- [ ] Erweiterte Dashboard-Analysen
- [ ] Verbesserte Diagramme und Visualisierungen
- [ ] Weitere Anpassungsmöglichkeiten

---

**Mindrift – Find your flow. Own your focus.**

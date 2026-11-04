# Fokuswerk

**Find your flow. Own your focus.**

Fokuswerk ist eine minimalistische Desktop-Anwendung zur Produktivitätssteigerung, entwickelt mit Python. Sie hilft dir dabei, Aufgaben zu organisieren, konzentrierte Arbeitssitzungen zu verwalten, Notizen zu speichern und deine Produktivität zu verfolgen – alles in einer übersichtlichen Oberfläche.

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
Fokuswerk/
│
├── main.py
├── config.py
├── database.py
├── requirements.txt
├── build_exe.bat
├── start_fokuswerk.bat
├── Fokuswerk.spec
├── test_database.py
│
├── data/          (wird automatisch angelegt, nicht in Git)
├── tests/
│   └── test_timer_logic.py
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
git clone https://github.com/y-zaitsev/fokuswerk.git
```

2. In das Projektverzeichnis wechseln:

```bash
cd fokuswerk
```

3. Abhängigkeiten installieren:

```bash
py -m pip install -r requirements.txt
```

4. Fokuswerk starten:

```bash
py main.py
```

## Datenspeicherung

Fokuswerk verwendet SQLite zur lokalen Speicherung deiner Daten.

Gespeichert werden:

- Aufgaben und deren Status
- Persönliche Notizen
- Fokus-Sitzungen
- Anwendungseinstellungen

Alle Daten werden lokal gespeichert. Ein Online-Konto ist nicht erforderlich.

Speicherort der Datenbank (`fokuswerk.db`):

- Start über `py main.py`: Ordner `data/` im Projektverzeichnis
- Windows-EXE: `%APPDATA%\Fokuswerk\` (bleibt auch nach einem Update der EXE erhalten)

Wer vorher die Version „Mindrift“ benutzt hat: Eine vorhandene `data/mindrift.db` wird beim ersten Start automatisch übernommen.

## Tests

```bash
py -m unittest -v
```

Die Tests nutzen temporäre Datenbanken und verändern deine echten Daten nicht.

## Windows-Version erstellen

Mit PyInstaller kann Fokuswerk als eigenständige Windows-Anwendung erstellt werden.

Führe dazu folgende Datei aus:

```bash
build_exe.bat
```

Die fertige EXE-Datei wird im Verzeichnis `dist/` erstellt. Bitte nicht in Git committen, sondern als Datei unter *Releases* auf GitHub hochladen.

## Roadmap

- [x] Grundstruktur der Desktop-Anwendung
- [x] SQLite-Datenbankintegration
- [x] Aufgabenverwaltung
- [x] Pomodoro-Timer
- [x] Notizenverwaltung
- [x] Produktivitätsstatistiken
- [x] Anwendungseinstellungen
- [x] Timer: Seitenwechsel setzt den Countdown nicht mehr zurück, genaue Zeitmessung
- [x] Daten bleiben in der EXE erhalten (`%APPDATA%`)
- [ ] Aufgaben bearbeiten, Priorität, Fälligkeit, Suche und Filter
- [ ] Timer: automatischer Wechsel, lange Pause nach 4 Sitzungen
- [ ] Notizen: Inhalt bearbeiten, Autosave, Suche
- [ ] Helles Theme
- [ ] Erweiterte Dashboard-Analysen
- [ ] Verbesserte Diagramme und Visualisierungen
- [ ] Weitere Anpassungsmöglichkeiten

---

**Fokuswerk – Find your flow. Own your focus.**

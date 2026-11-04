# Fokuswerk

**Find your flow. Own your focus.**

Fokuswerk ist eine minimalistische Desktop-Anwendung zur Produktivitätssteigerung, entwickelt mit Python. Sie hilft dir dabei, Aufgaben zu organisieren, konzentrierte Arbeitssitzungen zu verwalten, Notizen zu speichern und deine Produktivität zu verfolgen – alles in einer übersichtlichen Oberfläche.

## Funktionen

### Dashboard

- Übersicht über die eigene Produktivität.
- Dynamische Aufgabenstatistiken aus der SQLite-Datenbank.
- Anzeige erledigter Aufgaben und des gesamten Fortschritts.
- Erfassung der Fokuszeit.
- Anzeige der zuletzt erstellten Aufgaben.
- Aufgaben direkt im Dashboard als erledigt markieren.
- Schnellzugriff auf den Focus Timer.

### Aufgabenverwaltung

- Aufgaben erstellen und verwalten.
- Aufgabenbeschreibungen und Prioritäten festlegen.
- Fälligkeitsdaten hinzufügen.
- Zwischen offenen und erledigten Aufgaben unterscheiden.
- Aufgaben lokal in der Datenbank speichern.

### Focus Timer

- Pomodoro-basierter Fokus-Timer.
- Verschiedene Modi: Fokuszeit, kurze Pause und lange Pause.
- Timer starten, pausieren, fortsetzen und zurücksetzen.
- Fokus-Sitzungen in der Datenbank speichern.
- Unvollständige Sitzungen beim Pausieren, Zurücksetzen, Wechseln des Modus oder Schließen der Anwendung speichern.
- Sitzungsdauer sekundengenau erfassen.

### Notizen

- Notizen erstellen und verwalten.
- Bestehende Notizen bearbeiten.
- Notizen lokal in der Datenbank speichern.

### Statistiken

- Anzahl erledigter Aufgaben anzeigen.
- Gesamte Fokuszeit erfassen.
- Abgeschlossene Fokus-Sitzungen zählen.
- Gesamtzahl aller gespeicherten Fokus-Sitzungen anzeigen, einschließlich unterbrochener Sitzungen.

### Einstellungen

- Anwendungseinstellungen verwalten.
- Einstellungen dauerhaft in SQLite speichern.

## Verwendete Technologien

| Technologie   | Verwendung                   |
| ------------- | ---------------------------- |
| Python 3.11+  | Anwendungslogik              |
| CustomTkinter | Grafische Benutzeroberfläche |
| SQLite        | Lokale Datenbank             |
| Matplotlib    | Datenvisualisierung          |
| Pillow        | Bildverarbeitung             |
| PyInstaller   | Erstellung der Windows-EXE   |

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

## Installation

### 1. Repository klonen

```bash
git clone https://github.com/y-zaitsev/fokuswerk.git
```

### 2. Virtuelle Umgebung erstellen

```bash
cd fokuswerk
```

### 4. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

4. Fokuswerk starten:

```bash
python main.py
```

## Windows-EXE erstellen

Mindrift kann mit PyInstaller als eigenständige Windows-Anwendung erstellt werden.

Dazu das Build-Skript ausführen:

```powershell
cmd /c build_exe.bat
```

Nach erfolgreichem Build befindet sich die ausführbare Datei unter:

```text
dist/Mindrift.exe
```

## Datenspeicherung

Fokuswerk verwendet SQLite zur lokalen Speicherung deiner Daten.

Gespeichert werden:

- Aufgaben
- Notizen
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

Die fertige EXE-Datei wird im Verzeichnis `dist/` erstellt. Bitte nicht in Git committen, sondern als Datei unter _Releases_ auf GitHub hochladen.

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

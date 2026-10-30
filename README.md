# Mindrift

**Find your flow. Own your focus.**

Mindrift ist eine Desktop-Produktivitätsanwendung, die mit Python entwickelt wurde. Sie hilft dabei, Aufgaben zu organisieren, konzentrierte Arbeitsphasen zu verwalten, Notizen zu erstellen und die eigene Produktivität im Blick zu behalten.

Die Anwendung bietet eine minimalistische Benutzeroberfläche im Dark Mode mit violetten Akzenten. Alle Daten werden lokal gespeichert.

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

| Technologie | Verwendung |
|---|---|
| Python 3.11+ | Anwendungslogik |
| CustomTkinter | Grafische Benutzeroberfläche |
| SQLite | Lokale Datenbank |
| Matplotlib | Datenvisualisierung |
| Pillow | Bildverarbeitung |
| PyInstaller | Erstellung der Windows-EXE |

## Projektstruktur

```text
Mindrift/
├── main.py
├── config.py
├── database.py
├── requirements.txt
├── build_exe.bat
├── README.md
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
git clone <repository-url>
cd Mindrift
```

### 2. Virtuelle Umgebung erstellen

```bash
python -m venv .venv
```

### 3. Virtuelle Umgebung aktivieren

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 5. Mindrift starten

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

Mindrift verwendet SQLite zur lokalen Speicherung aller Anwendungsdaten.

Die Datenbank wird beim Start der Anwendung automatisch initialisiert.

Gespeichert werden:
- Aufgaben
- Notizen
- Fokus-Sitzungen
- Anwendungseinstellungen

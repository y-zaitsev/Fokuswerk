"""Zentrale Konfiguration für Fokuswerk."""
import os
import sys
from pathlib import Path

APP_NAME = "Fokuswerk"
APP_VERSION = "0.2.0"
APP_TAGLINE = "Find your flow. Own your focus."

WINDOW_SIZE = "1200x750"
MIN_WINDOW_SIZE = (900, 600)

DB_FILENAME = "fokuswerk.db"
LEGACY_DB_FILENAME = "mindrift.db"  # alter Name, wird beim ersten Start übernommen


def get_data_dir() -> Path:
    """Ordner für die Datenbank.

    * Normaler Start (py main.py): ./data neben dem Quellcode.
    * Als .exe (PyInstaller): %APPDATA%/Fokuswerk. Der Ordner neben dem Code
      liegt bei --onefile in einem temporären Verzeichnis, das beim Beenden
      gelöscht wird – dort würden alle Daten verloren gehen.
    """
    if getattr(sys, "frozen", False):
        base = Path(os.environ.get("APPDATA") or Path.home() / ".local" / "share")
        path = base / APP_NAME
    else:
        path = Path(__file__).resolve().parent / "data"
    path.mkdir(parents=True, exist_ok=True)
    return path


COLORS = {
    "background": "#101114",
    "sidebar": "#15161A",
    "card": "#1B1D23",
    "card_alt": "#22242B",
    "accent": "#8B7CFF",
    "accent_hover": "#7666EA",
    "text": "#F5F5F7",
    "muted": "#92949F",
    "success": "#55C99A",
    "warning": "#F0B85A",
    "danger": "#EF6B73",
    "border": "#2B2D35",
}

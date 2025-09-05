from pathlib import Path

## Hier werden alle Presets hinzugefügt, ganz einfach dega

# Basis-Pfad
BASE_DIR = Path(__file__).resolve().parents[1]

# Tabellen-Verzeichnis
TABLES_DIR = BASE_DIR / "tabellen"

# Verfügbare Presets: Name -> CSV-Datei
PRESET_SOURCES = {
    "AVG Köln": TABLES_DIR / "AVG Köln.csv",
}

# Standard-Preset
DEFAULT_PRESET = "AVG Köln"

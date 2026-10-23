from pathlib import Path
from PySide6.QtCore import QStandardPaths

APP_DIR = Path(QStandardPaths.writableLocation(QStandardPaths.AppDataLocation))
APP_DIR.mkdir(parents=True, exist_ok=True)

PROFILE_DIR = APP_DIR / "profile"
PROFILE_DIR.mkdir(parents=True, exist_ok=True)

BACKGROUND_DIR = APP_DIR / "backgrounds"
BACKGROUND_DIR.mkdir(parents=True, exist_ok=True)

DATA_DIR = APP_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

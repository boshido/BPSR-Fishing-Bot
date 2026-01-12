import sys
from pathlib import Path

def get_package_root():
    if getattr(sys, 'frozen', False):
        base_path = Path(sys._MEIPASS)
        return base_path / "src" / "fishbot"
    else:
        return Path(__file__).resolve().parent.parent

PACKAGE_ROOT = get_package_root()
ASSETS_PATH = PACKAGE_ROOT / "assets"
TEMPLATES_PATH = ASSETS_PATH / "templates"
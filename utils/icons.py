import configparser
from pathlib import Path

from PyQt6.QtGui import QIcon


def resolve_icon_theme(theme: str) -> str:
    if theme != "auto":
        return theme

    for path in [
        Path.home() / ".config/gtk-4.0/settings.ini",
        Path.home() / ".config/gtk-3.0/settings.ini",
    ]:
        cfg = configparser.ConfigParser()
        _ = cfg.read(path)

        name = cfg.get("Settings", "gtk-icon-theme-name", fallback=None)

        if name:
            return name

    return "hicolor"


def find_app_icon(name: str, theme: str) -> QIcon:
    if "/" in name:
        return QIcon(name)

    for base in [Path.home() / ".local/share/icons", Path("/usr/share/icons")]:
        for size in (256, 128, 64, 48):
            for ext in ("svg", "png"):
                path = base / theme / "apps" / str(size) / f"{name}.{ext}"
                if path.exists():
                    return QIcon(str(path))

    return QIcon.fromTheme(name)

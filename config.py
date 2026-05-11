import json
from pathlib import Path
from typing import TypedDict, Self, cast


class Settings(TypedDict):
    test_mode: bool
    scan_pattern: str
    theme: str


class ScanPaths(TypedDict):
    default: list[str]
    test: str


class ConfigFile(TypedDict, total=False):
    settings: Settings
    scan_paths: ScanPaths


class Config:
    def __init__(self, settings: Settings, scan_paths: ScanPaths) -> None:
        self.settings: Settings = settings
        self.scan_paths: ScanPaths = scan_paths

    DEFAULT_SETTINGS: Settings = {"test_mode": False, "scan_pattern": "*.desktop*", "theme": "auto"}

    DEFAULT_SCAN_PATHS: ScanPaths = {
        "default": ["/usr/share/applications", "~/.local/share/applications"],
        "test": "./config.json",
    }

    @classmethod
    def load(
        cls,
        path: str | Path = "./config.json",
    ) -> Self:
        with open(path, encoding="utf-8") as f:
            raw = cast(ConfigFile, json.load(f))
        return cls(
            settings=cast(Settings, cast(object, {**cls.DEFAULT_SETTINGS, **raw.get("settings", {})})),
            scan_paths=cast(ScanPaths, cast(object, {**cls.DEFAULT_SCAN_PATHS, **raw.get("scan_paths", {})})),
        )

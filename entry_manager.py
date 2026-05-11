from collections.abc import Iterable
from itertools import chain
from pathlib import Path
from config import Config
from desktop_entry import DesktopEntry


class EntryManager:
    def __init__(self, config: Config) -> None:

        self.test_mode: bool = config.settings["test_mode"]
        self.scan_pattern: str = config.settings["scan_pattern"]
        self.default_paths: list[str] = config.scan_paths["default"]
        self.test_path: str = config.scan_paths["test"]

        self.files: list[DesktopEntry] = self._scan_fs(
            self.test_mode, self.scan_pattern, self.default_paths, self.test_path
        )

    @staticmethod
    def _scan_fs(test_mode: bool, patt: str, default_paths: list[str], test_path: str) -> list[DesktopEntry]:

        files: Iterable[Path]

        if test_mode:
            files = Path(test_path).glob(patt)
        else:
            files = chain.from_iterable(Path(p).glob(patt) for p in default_paths)

        result: dict[str, DesktopEntry] = {}

        for file in files:
            result[file.name] = DesktopEntry(str(file))

        return list(result.values())

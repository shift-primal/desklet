from pathlib import Path
from itertools import chain
from desktop_entry import DesktopEntry


class EntryManager:
    def __init__(self):
        self.files: list[DesktopEntry] = self._scan_fs()

    @staticmethod
    def _scan_fs():
        rootPath = "/usr/share/applications"
        localPath = Path.home() / ".local/share/applications"
        patt = "*.desktop"

        rootFiles = Path(rootPath).glob(patt)
        localFiles = Path(localPath).glob(patt)

        result: dict[str, DesktopEntry] = {}

        for file in chain(rootFiles, localFiles):
            result[file.name] = DesktopEntry(str(file))

        return list(result.values())

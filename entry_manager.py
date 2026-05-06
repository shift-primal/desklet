from pathlib import Path
from itertools import chain
from desktop_entry import DesktopEntry


class EntryManager:
    def __init__(self, testmode: bool = False):
        self.files: list[DesktopEntry] = self._scan_fs(testmode)

    @staticmethod
    def _scan_fs(testmode: bool):
        rootPath = "/usr/share/applications"
        localPath = Path.home() / ".local/share/applications"
        testPath = "./testfiles"
        patt = "*.desktop"

        if testmode:
            files = Path(testPath).glob(patt)
        else:
            files = chain(Path(rootPath).glob(patt), Path(localPath).glob(patt))

        result: dict[str, DesktopEntry] = {}

        for file in files:
            result[file.name] = DesktopEntry(str(file))

        return list(result.values())

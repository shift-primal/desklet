from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QSplitter

from config import Config
from entry_manager import EntryManager
from widgets.entry_editor import EntryEditor
from widgets.entry_list import EntryList


class MainWindow(QMainWindow):
    def __init__(self, config: Config) -> None:
        super().__init__()

        self.entry_manager: EntryManager = EntryManager(config)
        self.entry_list: EntryList = EntryList(self.entry_manager, config)
        self.entry_editor: EntryEditor = EntryEditor()

        self.splitter: QSplitter = self._make_splitter()

        self.setup_ui()

    def setup_ui(self) -> None:
        self.setWindowTitle("Desklet")

        self.setCentralWidget(self.splitter)

        self.splitter.setSizes([800, 500])
        self.splitter.setContentsMargins(30, 30, 30, 30)

    def _make_splitter(self) -> QSplitter:

        splitter: QSplitter = QSplitter(Qt.Orientation.Horizontal)

        _ = self.entry_editor.entry_changed.connect(self.entry_list.refresh)
        _ = self.entry_list.entry_selected.connect(self.entry_editor.update_entry)

        splitter.addWidget(self.entry_list)
        splitter.addWidget(self.entry_editor)

        return splitter

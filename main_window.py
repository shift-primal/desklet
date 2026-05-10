from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow,
    QSplitter,
)

from entry_editor import EntryEditor
from entry_list import EntryList
from entry_manager import EntryManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.entry_manager: EntryManager = EntryManager(testmode=True)
        self.entry_list: EntryList = EntryList(self.entry_manager)
        self.editor_widget: EntryEditor = EntryEditor()

        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Desklet")

        splitter: QSplitter = QSplitter(Qt.Orientation.Horizontal)

        splitter.addWidget(self.entry_list)
        _ = self.entry_list.entry_selected.connect(self.editor_widget.update_entry)
        splitter.addWidget(self.editor_widget)

        self.setCentralWidget(splitter)

        splitter.setSizes([800, 500])
        splitter.setContentsMargins(30, 30, 30, 30)

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QSplitter,
)

from entry_editor import EntryEditor
from entry_manager import EntryManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.entry_manager: EntryManager = EntryManager()
        self.list_widget: QListWidget = QListWidget()
        self.editor_widget: EntryEditor = EntryEditor()

        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Desklet")

        splitter: QSplitter = QSplitter(Qt.Orientation.Horizontal)

        splitter.addWidget(self.list_widget)
        _ = self.list_widget.currentItemChanged.connect(  # pyright: ignore[reportUnknownMemberType]
            self.on_entry_selected
        )
        splitter.addWidget(self.editor_widget)

        self.setCentralWidget(splitter)

        splitter.setSizes([800, 500])  # pyright: ignore[reportUnknownMemberType]

        self.populate_list()

    def populate_list(self):
        for f in self.entry_manager.files:
            self.list_widget.addItem(f.name)

    def on_entry_selected(self, _item: QListWidgetItem | None):
        self.editor_widget.update_entry(
            self.entry_manager.files[self.list_widget.currentRow()]
        )

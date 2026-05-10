from PyQt6.QtCore import QPoint, QSize, Qt, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QMenu, QWidget

from desktop_entry import DesktopEntry
from entry_manager import EntryManager


class EntryList(QListWidget):
    entry_selected: pyqtSignal = pyqtSignal(DesktopEntry)

    def __init__(self, entry_manager: EntryManager):
        super().__init__()
        self.entry_manager: EntryManager = entry_manager
        self.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        _ = self.currentItemChanged.connect(self._on_item_changed)
        _ = self.customContextMenuRequested.connect(self._show_context_menu)
        self.populate_list()

    def _make_item_widget(self, file: DesktopEntry) -> QWidget:
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(4, 2, 4, 2)

        icon_label = QLabel()
        fallback = QIcon("/usr/share/icons/breeze/actions/16/error.svg")
        if file.icon:
            icon = QIcon(file.icon) if "/" in file.icon else QIcon.fromTheme(file.icon, fallback)
        else:
            icon = fallback
        icon_label.setPixmap(icon.pixmap(24, 24))

        name_label = QLabel(file.name)
        name_label.setStyleSheet("font-size: 16px;")

        eye_label = QLabel()
        eye_name = "view-hidden" if file.hidden else "view-visible"
        eye_icon = QIcon.fromTheme(eye_name, QIcon(f"/usr/share/icons/breeze/actions/16/{eye_name}.svg"))
        eye_label.setPixmap(eye_icon.pixmap(16, 16))

        layout.addWidget(icon_label)
        layout.addWidget(name_label)
        layout.addStretch()
        layout.addWidget(eye_label)

        return widget

    def _make_list_item(self) -> QListWidgetItem:
        item = QListWidgetItem()
        item.setSizeHint(QSize(0, 36))
        return item

    def populate_list(self):
        for f in self.entry_manager.files:
            item = self._make_list_item()
            self.addItem(item)
            self.setItemWidget(item, self._make_item_widget(f))

    def refresh(self):
        self.clear()
        self.populate_list()

    def _show_context_menu(self, pos: QPoint):
        rows = [i.row() for i in self.selectedIndexes()]
        if not rows:
            return

        menu = QMenu(self)
        hide_action = menu.addAction("Hide selected")
        unhide_action = menu.addAction("Unhide selected")

        triggered = menu.exec(self.mapToGlobal(pos))
        if triggered == hide_action:
            for row in rows:
                self.entry_manager.files[row].set_field("hidden", True)
            self.refresh()
        elif triggered == unhide_action:
            for row in rows:
                self.entry_manager.files[row].set_field("hidden", False)
            self.refresh()

    def _on_item_changed(self, _item: QListWidgetItem | None):
        row = self.currentRow()
        if row >= 0:
            self.entry_selected.emit(self.entry_manager.files[row])

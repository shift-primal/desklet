from PyQt6.QtCore import QPoint, QSize, Qt, pyqtSignal
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QMenu, QWidget

from config import Config
from desktop_entry import DesktopEntry
from entry_manager import EntryManager
from utils.icons import find_app_icon


class EntryList(QListWidget):
    entry_selected: pyqtSignal = pyqtSignal(DesktopEntry)

    def __init__(self, entry_manager: EntryManager, config: Config) -> None:
        super().__init__()

        self.entry_manager: EntryManager = entry_manager

        self.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        _ = self.currentItemChanged.connect(self._on_item_changed)
        _ = self.customContextMenuRequested.connect(self._show_context_menu)

        self.populate_list()

    def _make_item_widget(self, file: DesktopEntry) -> QWidget:
        widget: QWidget = QWidget()
        layout: QHBoxLayout = QHBoxLayout(widget)
        layout.setContentsMargins(4, 2, 4, 2)

        icon_label: QLabel = QLabel()

        icon: QIcon

        if file.icon and QIcon.hasThemeIcon(file.icon):
            icon = find_app_icon(file.icon, QIcon.themeName())
        else:
            icon = QIcon.fromTheme("error")

        icon_label.setPixmap(icon.pixmap(24, 24))

        name_label: QLabel = QLabel(file.name)
        name_label.setStyleSheet("font-size: 16px;")

        eye_text = "X" if file.hidden else "O"
        eye_label: QLabel = QLabel(eye_text)

        layout.addWidget(icon_label)
        layout.addWidget(name_label)
        layout.addStretch()
        layout.addWidget(eye_label)

        return widget

    def _make_list_item(self) -> QListWidgetItem:
        item: QListWidgetItem = QListWidgetItem()
        item.setSizeHint(QSize(0, 36))

        return item

    def _show_context_menu(self, pos: QPoint) -> None:
        rows: list[int] = [i.row() for i in self.selectedIndexes()]

        if not rows:
            return

        menu: QMenu = QMenu(self)

        hide_action: QAction | None = menu.addAction("Hide selected")
        unhide_action: QAction | None = menu.addAction("Unhide selected")

        triggered: QAction | None = menu.exec(self.mapToGlobal(pos))

        if triggered == hide_action:
            for row in rows:
                self.entry_manager.files[row].set_field("hidden", True)
                self.refresh()
        elif triggered == unhide_action:
            for row in rows:
                self.entry_manager.files[row].set_field("hidden", False)
                self.refresh()

    def populate_list(self) -> None:
        for f in self.entry_manager.files:
            item = self._make_list_item()
            self.addItem(item)
            self.setItemWidget(item, self._make_item_widget(f))

    def refresh(self) -> None:
        self.clear()
        self.populate_list()

    def _on_item_changed(self, _item: QListWidgetItem | None) -> None:
        row: int = self.currentRow()
        if row >= 0:
            self.entry_selected.emit(self.entry_manager.files[row])

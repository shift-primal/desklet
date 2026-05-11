from functools import partial
from typing import Callable
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QCheckBox, QFormLayout, QLabel, QLayoutItem, QLineEdit, QVBoxLayout, QWidget

from desktop_entry import DesktopEntry


class EntryEditor(QWidget):
    entry_changed: pyqtSignal = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()

        self.title_label: QLabel = self._make_title_label()
        self.form: QFormLayout = QFormLayout()
        self.box_layout: QVBoxLayout = self._make_box_layout()

        self.setLayout(self.box_layout)

    ENTRIES: dict[str, dict[str, str]] = {
        "name": {"label": "Name", "type": "line"},
        "comment": {"label": "Comment", "type": "line"},
        "executable": {"label": "Executable", "type": "line"},
        "terminal": {"label": "Terminal", "type": "checkbox"},
        "hidden": {"label": "Hidden", "type": "checkbox"},
    }

    def _make_box_layout(self) -> QVBoxLayout:
        box_layout: QVBoxLayout = QVBoxLayout()

        box_layout.addWidget(self.title_label)
        box_layout.addLayout(self.form)
        box_layout.setSpacing(10)
        box_layout.addStretch()

        return box_layout

    def _make_title_label(self) -> QLabel:
        title_label: QLabel = QLabel()
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        return title_label

    def _make_line_edit(self, text: str | None, callback: Callable[[str], None]) -> QLineEdit:
        line_edit = QLineEdit()
        line_edit.setText(text or "")

        def _on_text(value: str) -> None:
            callback(value)
            self.entry_changed.emit()

        _ = line_edit.textChanged.connect(_on_text)

        return line_edit

    def _make_checkbox(self, active: bool, callback: Callable[[bool], None]) -> QCheckBox:
        checkbox = QCheckBox()
        checkbox.setChecked(active)

        def _on_state(state: int) -> None:
            callback(bool(state))
            self.entry_changed.emit()

        _ = checkbox.stateChanged.connect(_on_state)

        return checkbox

    def update_entry(self, entry: DesktopEntry) -> None:
        self.title_label.setText(entry.name)

        self.clear_entries()

        row_entries: list[tuple[str, QWidget]] = []

        for k, v in self.ENTRIES.items():
            entry_key = getattr(entry, k)  # pyright: ignore[reportAny]
            entry_callback = partial(entry.set_field, k)
            entry_label = v["label"]
            widget_type = v["type"]

            if widget_type == "line":
                widget = self._make_line_edit(entry_key, entry_callback)  # pyright: ignore[reportAny]
            else:
                widget = self._make_checkbox(entry_key, entry_callback)  # pyright: ignore[reportAny]

            row_entries.append((entry_label, widget))

        for l, w in row_entries:
            self.form.addRow(l, w)

    def clear_entries(self) -> None:
        while self.form.count():
            child: QLayoutItem | None = self.form.takeAt(0)

            if child:
                widget: QWidget | None = child.widget()
                if widget:
                    widget.deleteLater()

from collections.abc import Callable
from functools import partial
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFormLayout,
    QLineEdit,
    QVBoxLayout,
    QWidget,
    QCheckBox,
    QLabel,
)

from desktop_entry import DesktopEntry


class EntryEditor(QWidget):
    def __init__(self):
        super().__init__()

        self.entries: dict[str, dict[str, str]] = {
            "name": {"label": "Name", "type": "line"},
            "comment": {"label": "Comment", "type": "line"},
            "executable": {"label": "Executable", "type": "line"},
            "terminal": {"label": "Terminal", "type": "checkbox"},
            "hidden": {"label": "Hidden", "type": "checkbox"},
        }

        self.box_layout: QVBoxLayout = QVBoxLayout()
        self.title_label: QLabel = QLabel()

        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.form: QFormLayout = QFormLayout()

        self.box_layout.addWidget(self.title_label)
        self.box_layout.addLayout(self.form)
        self.box_layout.setSpacing(10)
        self.box_layout.addStretch()

        self.setLayout(self.box_layout)

    def _make_line_edit(self, text: str | None, callback: Callable[[str], None]) -> QLineEdit:
        line_edit = QLineEdit()
        line_edit.setText(text or "")
        _ = line_edit.textChanged.connect(callback)

        return line_edit

    def _make_checkbox(self, active: bool, callback: Callable[[bool], None]) -> QCheckBox:
        checkbox = QCheckBox()
        checkbox.setChecked(active)
        _ = checkbox.stateChanged.connect(lambda state: callback(bool(state)))

        return checkbox

    def update_entry(self, entry: DesktopEntry):
        self.title_label.setText(entry.name)
        self.clear_entries()

        row_entries: list[tuple[str, QWidget]] = []

        for k, v in self.entries.items():
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

    def clear_entries(self):
        while self.form.count():
            child = self.form.takeAt(0)

            if child:
                widget = child.widget()
                if widget:
                    widget.deleteLater()

from collections.abc import Callable
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

entries = {
    "name": {"label": "Name", "type": "line"},
    "comment": {"label": "Comment", "type": "line"},
    "executable": {"label": "Executable", "type": "line"},
    "terminal": {"label": "Terminal", "type": "checkbox"},
    "hidden": {"label": "Hidden", "type": "checkbox"},
}


class EntryEditor(QWidget):
    def __init__(self):
        super().__init__()

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
        _ = checkbox.stateChanged.connect(lambda state: callback(bool()))

        return checkbox

    def _add_rows(self, rowElements: list[tuple[str, QWidget]]):
        for l, w in rowElements:
            self.form.addRow(l, w)

    def update_entry(self, entry: DesktopEntry):
        self.title_label.setText(entry.name)
        self.clear_entries()

        line_name = self._make_line_edit(entry.name, entry.set_name)
        line_comment = self._make_line_edit(entry.comment, entry.set_comment)
        line_executable = self._make_line_edit(entry.executable, entry.set_executable)
        checkbox_terminal = self._make_checkbox(entry.terminal, entry.set_terminal)
        checkbox_hidden = self._make_checkbox(entry.hidden, entry.set_hidden)

        rowElements = []

        self.form.addRow("Name", line_name)
        self.form.addRow("Comment", line_comment)
        self.form.addRow("Exec", line_executable)
        self.form.addRow("Terminal", checkbox_terminal)
        self.form.addRow("Hidden", checkbox_hidden)

    def clear_entries(self):
        while self.form.count():
            child = self.form.takeAt(0)

            if child:
                widget = child.widget()
                if widget:
                    widget.deleteLater()

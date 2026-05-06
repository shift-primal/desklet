from PyQt6.QtWidgets import QFormLayout, QLineEdit, QWidget, QCheckBox

from desktop_entry import DesktopEntry


class EntryEditor(QWidget):
    def __init__(self):
        super().__init__()

        self.form_layout: QFormLayout = QFormLayout()
        self.setLayout(self.form_layout)

    def update_entry(self, entry: DesktopEntry):
        self.clear_layout()

        checkbox = QCheckBox()
        checkbox.setChecked(entry.hidden)

        line_edit = QLineEdit()
        line_edit.setText(entry.name)

        self.form_layout.addRow(entry.name, line_edit)
        self.form_layout.addRow("Hidden", checkbox)

    def clear_layout(self):
        while self.form_layout.count():
            child = self.form_layout.takeAt(0)

            if child:
                widget = child.widget()
                if widget:
                    widget.deleteLater()

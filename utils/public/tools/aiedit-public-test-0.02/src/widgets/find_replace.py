from PyQt5.QtWidgets import (
    QDialog, QDialogButtonBox, QGridLayout, QVBoxLayout,
    QLabel, QLineEdit, QComboBox, QCheckBox,
)
from widgets.attribute_editor import KNOWN_ATTRS


class FindReplaceDialog(QDialog):

    def __init__(self, parent, files):
        super().__init__(parent)
        self._files = files
        self.setWindowTitle("Find & Replace in Attributes")
        self.setMinimumWidth(420)

        layout = QVBoxLayout(self)

        # Form
        form = QGridLayout()

        form.addWidget(QLabel("Attribute key:"), 0, 0)
        self._key_combo = QComboBox()
        self._key_combo.addItems(list(KNOWN_ATTRS.keys()) + ["(custom)"])
        self._key_combo.setEditable(True)
        form.addWidget(self._key_combo, 0, 1)

        form.addWidget(QLabel("Find value:"), 1, 0)
        self._find_edit = QLineEdit()
        form.addWidget(self._find_edit, 1, 1)

        form.addWidget(QLabel("Replace with:"), 2, 0)
        self._replace_edit = QLineEdit()
        form.addWidget(self._replace_edit, 2, 1)

        layout.addLayout(form)

        self._scope_all = QCheckBox("Apply to ALL loaded files")
        self._scope_all.setChecked(True)
        layout.addWidget(self._scope_all)

        self._result_label = QLabel("")
        self._result_label.setStyleSheet("color: #27ae60;")
        layout.addWidget(self._result_label)

        # Buttons
        btns = QDialogButtonBox()
        apply_btn = btns.addButton("Apply", QDialogButtonBox.AcceptRole)
        btns.addButton("Close", QDialogButtonBox.RejectRole)
        apply_btn.clicked.connect(self._apply)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

    def _apply(self):
        key       = self._key_combo.currentText().strip()
        find_val  = self._find_edit.text().strip()
        repl_val  = self._replace_edit.text().strip()

        if not key or not find_val:
            return

        count = 0
        for fname, fd in self._files.items():
            for entity in fd['entities']:
                for block in entity['blocks']:
                    if block['type'] != 'attributes':
                        continue
                    for kv in block['kvs']:
                        if kv['key'] == key and kv['value'] == find_val:
                            kv['value'] = repl_val
                            count += 1
                            fd['modified'] = True

        self._result_label.setText(f"Replaced {count} occurrence(s).")

        # Notify the main window to refresh its visual indicators
        if hasattr(self.parent(), 'refresh_modified_indicators'):
            self.parent().refresh_modified_indicators()

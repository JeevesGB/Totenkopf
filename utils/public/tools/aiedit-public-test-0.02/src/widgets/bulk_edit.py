from PyQt5.QtWidgets import (
    QDialog, QDialogButtonBox, QGridLayout, QVBoxLayout,
    QLabel, QLineEdit, QComboBox, QCheckBox,
)
from widgets.attribute_editor import KNOWN_ATTRS


class BulkEditDialog(QDialog):
    def __init__(self, parent, files):
        super().__init__(parent)
        self._files = files
        self.setWindowTitle("Bulk Set Attribute — All Entities")
        self.setMinimumWidth(380)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(
            "Set an attribute value across ALL entities in ALL loaded files that have it:"
        ))

        # Form
        form = QGridLayout()

        form.addWidget(QLabel("Attribute key:"), 0, 0)
        self._key_combo = QComboBox()
        self._key_combo.addItems(list(KNOWN_ATTRS.keys()) + ["(custom)"])
        self._key_combo.setEditable(True)
        form.addWidget(self._key_combo, 0, 1)

        form.addWidget(QLabel("New value:"), 1, 0)
        self._val_edit = QLineEdit()
        form.addWidget(self._val_edit, 1, 1)

        layout.addLayout(form)

        self._only_existing = QCheckBox("Only update entities that already have this attribute")
        self._only_existing.setChecked(True)
        layout.addWidget(self._only_existing)

        self._result_label = QLabel("")
        self._result_label.setStyleSheet("color: #27ae60;")
        layout.addWidget(self._result_label)

        # Buttons
        btns = QDialogButtonBox()
        apply_btn = btns.addButton("Apply to All", QDialogButtonBox.AcceptRole)
        btns.addButton("Close", QDialogButtonBox.RejectRole)
        apply_btn.clicked.connect(self._apply)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

    def _apply(self):
        key          = self._key_combo.currentText().strip()
        new_val      = self._val_edit.text().strip()
        only_existing = self._only_existing.isChecked()

        if not key or not new_val:
            return

        count = 0
        for fname, fd in self._files.items():
            for entity in fd['entities']:
                for block in entity['blocks']:
                    if block['type'] != 'attributes':
                        continue

                    matched = False
                    for kv in block['kvs']:
                        if kv['key'] == key:
                            kv['value'] = new_val
                            count += 1
                            matched = True
                            fd['modified'] = True

                    if not matched and not only_existing:
                        block['kvs'].append({'key': key, 'value': new_val, 'comment': ''})
                        count += 1
                        fd['modified'] = True

        self._result_label.setText(f"Updated {count} attribute(s) across all files.")

        if hasattr(self.parent(), 'refresh_modified_indicators'):
            self.parent().refresh_modified_indicators()

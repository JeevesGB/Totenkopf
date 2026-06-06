import json
import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton,
    QLineEdit, QSpinBox, QDoubleSpinBox, QInputDialog,
)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont


# Load attribute metadata from JSON at import time so the widget has no
# hard-coded data.  Falls back to an empty dict if the file is missing.
_ATTRS_JSON = os.path.join(os.path.dirname(__file__), '..', 'config', 'known_attrs.json')

def _load_known_attrs():
    try:
        with open(_ATTRS_JSON, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

KNOWN_ATTRS = _load_known_attrs()


class AttributeEditor(QWidget):
    """
    Displays the kvs from an entity's attributes block as editable fields.
    Emits `changed` whenever any value is modified.
    """

    changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._kvs = []
        self._widgets = {}

        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(6)

        title = QLabel("Attributes")
        title.setFont(QFont("Segoe UI", 11, QFont.Bold))
        root.addWidget(title)

        self._grid_widget = QWidget()
        self._grid = QGridLayout(self._grid_widget)
        self._grid.setSpacing(6)
        self._grid.setColumnStretch(1, 1)
        root.addWidget(self._grid_widget)

        self._add_btn = QPushButton("+ Add attribute")
        self._add_btn.clicked.connect(self._on_add)
        root.addWidget(self._add_btn)

        self._empty_label = QLabel("No attributes block found for this entity.")
        self._empty_label.setStyleSheet("color: #888; font-style: italic;")
        root.addWidget(self._empty_label)

        root.addStretch()

    # ── Public ────────────────────────────────────────────────────────────────

    def load(self, kvs):
        """Replace the current attribute list with a new set of KV dicts."""
        self._kvs = [dict(kv) for kv in kvs]
        self._widgets = {}
        self._rebuild()

    def get_kvs(self):
        """Return the current list of KV dicts."""
        return self._kvs

    # ── Internal ──────────────────────────────────────────────────────────────

    def _rebuild(self):
        # Remove all existing widgets from the grid
        while self._grid.count():
            item = self._grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self._empty_label.setVisible(len(self._kvs) == 0)

        for row, kv in enumerate(self._kvs):
            key  = kv['key']
            info = KNOWN_ATTRS.get(key, {})
            label_text = info.get('label', key)
            val_type   = info.get('type', 'str')
            tooltip    = f"{key}  —  {info.get('description', '')}"

            # Label column
            lbl = QLabel(label_text)
            lbl.setToolTip(tooltip)
            lbl.setFixedWidth(130)

            # Input widget column
            w = self._make_input(key, kv['value'], val_type)

            # Small raw-key reminder
            key_lbl = QLabel(f'<span style="color:#666;font-size:10px">{key}</span>')

            # Delete button
            del_btn = QPushButton("✕")
            del_btn.setFixedSize(22, 22)
            del_btn.setStyleSheet(
                "QPushButton { border: none; color: #888; }"
                "QPushButton:hover { color: #c0392b; }"
            )
            del_btn.clicked.connect(lambda _, k=key: self._on_delete(k))

            self._grid.addWidget(lbl,     row, 0)
            self._grid.addWidget(w,       row, 1)
            self._grid.addWidget(key_lbl, row, 2)
            self._grid.addWidget(del_btn, row, 3)
            self._widgets[key] = w

    def _make_input(self, key, value, val_type):
        """Create the right input widget for the attribute type."""
        if val_type == 'int':
            w = QSpinBox()
            w.setRange(0, 9_999_999)
            try:
                w.setValue(int(float(value)))
            except (ValueError, TypeError):
                w.setValue(0)
            w.valueChanged.connect(lambda v, k=key: self._on_change(k, str(v)))

        elif val_type == 'float':
            w = QDoubleSpinBox()
            w.setRange(0.0, 9_999.0)
            w.setDecimals(2)
            w.setSingleStep(0.05)
            try:
                w.setValue(float(value))
            except (ValueError, TypeError):
                w.setValue(0.0)
            w.valueChanged.connect(lambda v, k=key: self._on_change(k, f'{v:.1f}'))

        else:
            w = QLineEdit(value)
            w.textChanged.connect(lambda v, k=key: self._on_change(k, v))

        return w

    def _on_change(self, key, value):
        for kv in self._kvs:
            if kv['key'] == key:
                kv['value'] = value
                break
        self.changed.emit()

    def _on_delete(self, key):
        self._kvs = [kv for kv in self._kvs if kv['key'] != key]
        self._rebuild()
        self.changed.emit()

    def _on_add(self):
        existing = {kv['key'] for kv in self._kvs}
        available_keys = [k for k in KNOWN_ATTRS if k not in existing]

        if not available_keys:
            # All known attrs present — ask for a custom key
            self._add_custom()
            return

        items = [f"{k}  ({KNOWN_ATTRS[k]['label']})" for k in available_keys] + ["Custom..."]
        chosen, ok = QInputDialog.getItem(self, "Add Attribute", "Choose attribute:", items, 0, False)
        if not ok:
            return

        if chosen == "Custom...":
            self._add_custom()
        else:
            key = chosen.split()[0]
            default = '0' if KNOWN_ATTRS[key]['type'] == 'int' else '0.0'
            self._kvs.append({'key': key, 'value': default, 'comment': ''})
            self._rebuild()
            self.changed.emit()

    def _add_custom(self):
        key, ok = QInputDialog.getText(self, "Add Attribute", "Attribute key:")
        if not (ok and key.strip()):
            return
        val, ok2 = QInputDialog.getText(self, "Add Attribute", f"Value for '{key}':")
        if ok2:
            self._kvs.append({'key': key.strip(), 'value': val.strip(), 'comment': ''})
            self._rebuild()
            self.changed.emit()

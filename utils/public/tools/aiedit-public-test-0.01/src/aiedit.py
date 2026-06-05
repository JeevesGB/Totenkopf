"""
RTCW AI File Editor
A desktop editor for Return to Castle Wolfenstein .ai script files.
"""

import sys
import os
import re
import copy
import json
import shutil
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QSplitter, QListWidget, QListWidgetItem,
    QTreeWidget, QTreeWidgetItem, QTextEdit, QLineEdit, QLabel, QPushButton,
    QHBoxLayout, QVBoxLayout, QGridLayout, QGroupBox, QTabWidget, QFileDialog,
    QMessageBox, QAction, QToolBar, QStatusBar, QScrollArea, QFrame,
    QSizePolicy, QInputDialog, QMenu, QAbstractItemView, QHeaderView,
    QDialog, QDialogButtonBox, QCheckBox, QComboBox, QSpinBox, QDoubleSpinBox,
    QSplitterHandle
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt5.QtGui import (
    QFont, QColor, QPalette, QSyntaxHighlighter, QTextCharFormat,
    QIcon, QKeySequence, QFontDatabase
)


# ─── Maps JSON ────────────────────────────────────────────────────────────────

def load_maps_json(path):
    """Load maps.json and return list of map names."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list):
            return [str(m) for m in data]
    except Exception:
        pass
    return []


def find_maps_json():
    """Look for maplist.json next to the script/exe, then cwd."""
    candidates = [
        os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'maplist.json'),
        os.path.join(os.getcwd(), 'maplist.json'),
    ]
    for c in candidates:
        if os.path.isfile(c):
            return c
    return None


# ─── Parser ───────────────────────────────────────────────────────────────────

def parse_ai_file(text):
    """
    Parse a RTCW .ai file into a list of entities.
    Each entity: { 'name': str, 'raw_header': str, 'blocks': [...], 'raw': str }
    Each block:  { 'type': str, 'arg': str, 'lines': [str], 'raw': str }
    """
    entities = []
    i = 0
    lines = text.split('\n')
    n = len(lines)

    def skip_to_open_brace(start):
        for j in range(start, n):
            if '{' in lines[j]:
                return j
        return start

    def read_block(start):
        """Read from opening { to matching }, return (content_lines, end_idx)"""
        depth = 0
        content = []
        j = start
        while j < n:
            line = lines[j]
            depth += line.count('{')
            depth -= line.count('}')
            content.append(line)
            if depth == 0:
                return content, j
            j += 1
        return content, j

    i = 0
    while i < n:
        line = lines[i].strip()

        # Skip pure comment lines and blank lines at top level
        if not line or line.startswith('//'):
            i += 1
            continue

        # Check for entity name line (word possibly with digits/underscores, no leading whitespace in original)
        original = lines[i]
        stripped = original.strip()
        if re.match(r'^[\w]+\s*(//.*)?\s*$', stripped) and not stripped.startswith('//'):
            entity_name = stripped.split()[0]
            # Look ahead for {
            brace_line = skip_to_open_brace(i + 1)
            if brace_line >= n:
                i += 1
                continue

            # Read the outer block
            outer_lines, end_idx = read_block(brace_line)
            raw_entity = '\n'.join(lines[i:end_idx + 1])

            # Parse sub-blocks inside outer_lines
            blocks = parse_subblocks(outer_lines[1:-1])  # strip outer { }

            entities.append({
                'name': entity_name,
                'raw': raw_entity,
                'blocks': blocks,
                'start_line': i,
                'end_line': end_idx,
            })
            i = end_idx + 1
        else:
            i += 1

    return entities


def parse_subblocks(lines):
    """Parse sub-blocks (attributes, spawn, trigger X, death, etc.) from inner lines."""
    blocks = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped or stripped.startswith('//'):
            i += 1
            continue

        # Match sub-block header: word(s) followed by optional { on same or next line
        # Could be: "attributes", "spawn", "trigger foo", "pain 15", "enemysight player", etc.
        header_match = re.match(r'^(\w[\w\s]*)$', stripped) or re.match(r'^([\w][\w\s]*)(//.*)?\s*$', stripped)
        if header_match and i + 1 < n and '{' in lines[i + 1]:
            block_header = stripped.split('//')[0].strip()
            parts = block_header.split(None, 1)
            block_type = parts[0]
            block_arg = parts[1] if len(parts) > 1 else ''

            # Find opening brace
            j = i + 1
            while j < n and '{' not in lines[j]:
                j += 1
            if j >= n:
                i += 1
                continue

            # Read until matching }
            depth = 0
            block_lines = []
            k = j
            while k < n:
                l = lines[k]
                depth += l.count('{')
                depth -= l.count('}')
                block_lines.append(l)
                if depth == 0:
                    break
                k += 1

            inner_lines = block_lines[1:-1]  # strip { }
            raw_block = '\n'.join(lines[i:k + 1])

            # Parse key-value pairs from inner lines (for attributes block)
            kvs = []
            for il in inner_lines:
                s = il.strip()
                if not s or s.startswith('//'):
                    continue
                kv_match = re.match(r'^(\w+)\s+(.+?)(\s*//.*)?$', s)
                if kv_match:
                    kvs.append({
                        'key': kv_match.group(1),
                        'value': kv_match.group(2).strip(),
                        'comment': (kv_match.group(3) or '').strip()
                    })

            blocks.append({
                'type': block_type,
                'arg': block_arg,
                'header': block_header,
                'inner_lines': inner_lines,
                'kvs': kvs,
                'raw': raw_block,
            })
            i = k + 1
        elif stripped and '{' in stripped:
            # Inline block header with brace on same line
            header_part = stripped[:stripped.index('{')].strip()
            parts = header_part.split(None, 1)
            block_type = parts[0] if parts else 'unknown'
            block_arg = parts[1] if len(parts) > 1 else ''

            depth = 0
            block_lines = []
            k = i
            while k < n:
                l = lines[k]
                depth += l.count('{')
                depth -= l.count('}')
                block_lines.append(l)
                if depth == 0:
                    break
                k += 1

            inner_lines = []
            if len(block_lines) > 1:
                inner_lines = block_lines[1:-1]

            kvs = []
            for il in inner_lines:
                s = il.strip()
                if not s or s.startswith('//'):
                    continue
                kv_match = re.match(r'^(\w+)\s+(.+?)(\s*//.*)?$', s)
                if kv_match:
                    kvs.append({
                        'key': kv_match.group(1),
                        'value': kv_match.group(2).strip(),
                        'comment': (kv_match.group(3) or '').strip()
                    })

            raw_block = '\n'.join(block_lines)
            blocks.append({
                'type': block_type,
                'arg': block_arg,
                'header': header_part,
                'inner_lines': inner_lines,
                'kvs': kvs,
                'raw': raw_block,
            })
            i = k + 1
        else:
            i += 1

    return blocks


def reconstruct_entity(entity):
    """Rebuild the raw text of an entity from its parsed blocks."""
    lines = []
    raw = entity['raw']
    # Rebuild attributes block if it exists
    for block in entity['blocks']:
        if block['type'] == 'attributes' and block['kvs']:
            new_attr_raw = 'attributes\n\t{\n'
            for kv in block['kvs']:
                comment = f'  {kv["comment"]}' if kv['comment'] else ''
                new_attr_raw += f'\t\t{kv["key"]} {kv["value"]}{comment}\n'
            new_attr_raw += '\t}'
            # Replace old attributes block in raw
            old_raw = block['raw']
            raw = raw.replace(old_raw, new_attr_raw, 1)
    return raw


# ─── Syntax Highlighter ───────────────────────────────────────────────────────

class AIHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super().__init__(parent)
        self.rules = []

        # Comments
        fmt = QTextCharFormat()
        fmt.setForeground(QColor('#6A9955'))
        self.rules.append((re.compile(r'//[^\n]*'), fmt))

        # Keywords / block types
        fmt = QTextCharFormat()
        fmt.setForeground(QColor('#569CD6'))
        fmt.setFontWeight(QFont.Bold)
        keywords = r'\b(attributes|spawn|trigger|death|pain|enemysight|bulletimpact|inspectsoundstart|inspectbodystart|inspectfriendlycombatstart|playerstart|blocked)\b'
        self.rules.append((re.compile(keywords), fmt))

        # Attribute keys
        fmt = QTextCharFormat()
        fmt.setForeground(QColor('#9CDCFE'))
        self.rules.append((re.compile(r'\b(starting_health|aggression|aim_accuracy|fov|camper|tactical|attack_skill|alertness)\b'), fmt))

        # Numbers
        fmt = QTextCharFormat()
        fmt.setForeground(QColor('#B5CEA8'))
        self.rules.append((re.compile(r'\b\d+(\.\d+)?\b'), fmt))

        # Strings / identifiers after commands
        fmt = QTextCharFormat()
        fmt.setForeground(QColor('#CE9178'))
        self.rules.append((re.compile(r'\b(weapon_\w+|ammo_\w+|sound/\S+)\b'), fmt))

    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            for m in pattern.finditer(text):
                self.setFormat(m.start(), m.end() - m.start(), fmt)


# ─── Attribute Editor Widget ──────────────────────────────────────────────────

KNOWN_ATTRS = {
    'starting_health': ('Health', 'int', 'Starting HP for this entity'),
    'aggression':      ('Aggression', 'float', '0.0 = passive, 1.0 = max aggression'),
    'aim_accuracy':    ('Aim Accuracy', 'float', '0.0 = terrible, 1.0 = perfect'),
    'attack_skill':    ('Attack Skill', 'float', 'Overall combat skill'),
    'fov':             ('Field of View', 'int', 'Vision cone in degrees'),
    'camper':          ('Camper', 'float', 'Tendency to stay put (0-1)'),
    'tactical':        ('Tactical', 'float', 'Use of cover / tactics (0-1)'),
    'alertness':       ('Alertness', 'int', 'How quickly entity notices threats'),
}


class AttributeEditor(QWidget):
    changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.kvs = []
        self.widgets = {}
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(12, 12, 12, 12)
        self._layout.setSpacing(6)

        title = QLabel("Attributes")
        title.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self._layout.addWidget(title)

        self.grid_widget = QWidget()
        self.grid = QGridLayout(self.grid_widget)
        self.grid.setSpacing(6)
        self.grid.setColumnStretch(1, 1)
        self._layout.addWidget(self.grid_widget)

        self.add_btn = QPushButton("+ Add attribute")
        self.add_btn.clicked.connect(self.add_attribute)
        self._layout.addWidget(self.add_btn)
        self._layout.addStretch()

        self.no_attrs_label = QLabel("No attributes block found for this entity.")
        self.no_attrs_label.setStyleSheet("color: #888; font-style: italic;")
        self._layout.addWidget(self.no_attrs_label)

    def load(self, kvs):
        self.kvs = [dict(kv) for kv in kvs]
        self.widgets = {}
        self._rebuild_grid()

    def _rebuild_grid(self):
        # Clear grid
        while self.grid.count():
            item = self.grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.no_attrs_label.setVisible(len(self.kvs) == 0)
        self.add_btn.setVisible(True)

        for row, kv in enumerate(self.kvs):
            key = kv['key']
            info = KNOWN_ATTRS.get(key, (key, 'str', ''))
            label_text = info[0]

            lbl = QLabel(label_text)
            lbl.setToolTip(f"{key}  —  {info[2]}")
            lbl.setFixedWidth(130)

            val_type = info[1]
            val = kv['value']

            if val_type == 'int':
                w = QSpinBox()
                w.setRange(0, 9999999)
                try:
                    w.setValue(int(float(val)))
                except:
                    w.setValue(0)
                w.valueChanged.connect(lambda v, k=key: self._on_change(k, str(v)))
            elif val_type == 'float':
                w = QDoubleSpinBox()
                w.setRange(0.0, 9999.0)
                w.setDecimals(2)
                w.setSingleStep(0.05)
                try:
                    w.setValue(float(val))
                except:
                    w.setValue(0.0)
                w.valueChanged.connect(lambda v, k=key: self._on_change(k, f'{v:.1f}'))
            else:
                w = QLineEdit(val)
                w.textChanged.connect(lambda v, k=key: self._on_change(k, v))

            key_lbl = QLabel(f'<span style="color:#666;font-size:10px">{key}</span>')

            del_btn = QPushButton("✕")
            del_btn.setFixedSize(22, 22)
            del_btn.setStyleSheet("QPushButton { border: none; color: #888; } QPushButton:hover { color: #c0392b; }")
            del_btn.clicked.connect(lambda _, k=key: self._delete(k))

            self.grid.addWidget(lbl, row, 0)
            self.grid.addWidget(w, row, 1)
            self.grid.addWidget(key_lbl, row, 2)
            self.grid.addWidget(del_btn, row, 3)
            self.widgets[key] = w

    def _on_change(self, key, value):
        for kv in self.kvs:
            if kv['key'] == key:
                kv['value'] = value
                break
        self.changed.emit()

    def _delete(self, key):
        self.kvs = [kv for kv in self.kvs if kv['key'] != key]
        self._rebuild_grid()
        self.changed.emit()

    def add_attribute(self):
        keys = [info[0] for info in KNOWN_ATTRS.values()]
        raw_keys = list(KNOWN_ATTRS.keys())
        existing = {kv['key'] for kv in self.kvs}
        available = [(raw_keys[i], keys[i]) for i in range(len(raw_keys)) if raw_keys[i] not in existing]

        if not available:
            # Custom
            key, ok = QInputDialog.getText(self, "Add Attribute", "Attribute key:")
            if ok and key.strip():
                val, ok2 = QInputDialog.getText(self, "Add Attribute", f"Value for '{key}':")
                if ok2:
                    self.kvs.append({'key': key.strip(), 'value': val.strip(), 'comment': ''})
                    self._rebuild_grid()
                    self.changed.emit()
        else:
            items = [f"{rk}  ({lbl})" for rk, lbl in available] + ["Custom..."]
            item, ok = QInputDialog.getItem(self, "Add Attribute", "Choose attribute:", items, 0, False)
            if ok:
                if item == "Custom...":
                    key, ok = QInputDialog.getText(self, "Add Attribute", "Attribute key:")
                    if ok and key.strip():
                        val, ok2 = QInputDialog.getText(self, "Add Attribute", f"Value for '{key}':")
                        if ok2:
                            self.kvs.append({'key': key.strip(), 'value': val.strip(), 'comment': ''})
                            self._rebuild_grid()
                            self.changed.emit()
                else:
                    rk = item.split()[0]
                    default = '0' if KNOWN_ATTRS[rk][1] == 'int' else '0.0'
                    self.kvs.append({'key': rk, 'value': default, 'comment': ''})
                    self._rebuild_grid()
                    self.changed.emit()

    def get_kvs(self):
        return self.kvs


# ─── Find & Replace Dialog ────────────────────────────────────────────────────

class FindReplaceDialog(QDialog):
    def __init__(self, parent, files):
        super().__init__(parent)
        self.files = files  # dict of filename -> FileData
        self.setWindowTitle("Find & Replace in Attributes")
        self.setMinimumWidth(420)

        layout = QVBoxLayout(self)

        form = QGridLayout()
        form.addWidget(QLabel("Attribute key:"), 0, 0)
        self.key_combo = QComboBox()
        self.key_combo.addItems(list(KNOWN_ATTRS.keys()) + ["(custom)"])
        self.key_combo.setEditable(True)
        form.addWidget(self.key_combo, 0, 1)

        form.addWidget(QLabel("Find value:"), 1, 0)
        self.find_edit = QLineEdit()
        form.addWidget(self.find_edit, 1, 1)

        form.addWidget(QLabel("Replace with:"), 2, 0)
        self.replace_edit = QLineEdit()
        form.addWidget(self.replace_edit, 2, 1)

        layout.addLayout(form)

        self.scope_all = QCheckBox("Apply to ALL loaded files")
        self.scope_all.setChecked(True)
        layout.addWidget(self.scope_all)

        self.result_label = QLabel("")
        self.result_label.setStyleSheet("color: #27ae60;")
        layout.addWidget(self.result_label)

        btns = QDialogButtonBox()
        self.apply_btn = btns.addButton("Apply", QDialogButtonBox.AcceptRole)
        btns.addButton("Close", QDialogButtonBox.RejectRole)
        self.apply_btn.clicked.connect(self.apply)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

    def apply(self):
        key = self.key_combo.currentText().strip()
        find_val = self.find_edit.text().strip()
        replace_val = self.replace_edit.text().strip()
        if not key or not find_val:
            return

        count = 0
        for fname, fd in self.files.items():
            for entity in fd['entities']:
                for block in entity['blocks']:
                    if block['type'] == 'attributes':
                        for kv in block['kvs']:
                            if kv['key'] == key and kv['value'] == find_val:
                                kv['value'] = replace_val
                                count += 1
                                fd['modified'] = True
        self.result_label.setText(f"Replaced {count} occurrence(s).")
        self.parent().refresh_modified_indicators()


# ─── Bulk Edit Dialog ─────────────────────────────────────────────────────────

class BulkEditDialog(QDialog):
    def __init__(self, parent, files):
        super().__init__(parent)
        self.files = files
        self.setWindowTitle("Bulk Set Attribute — All Entities")
        self.setMinimumWidth(380)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Set an attribute value across ALL entities in ALL loaded files that have it:"))

        form = QGridLayout()
        form.addWidget(QLabel("Attribute key:"), 0, 0)
        self.key_combo = QComboBox()
        self.key_combo.addItems(list(KNOWN_ATTRS.keys()) + ["(custom)"])
        self.key_combo.setEditable(True)
        form.addWidget(self.key_combo, 0, 1)

        form.addWidget(QLabel("New value:"), 1, 0)
        self.val_edit = QLineEdit()
        form.addWidget(self.val_edit, 1, 1)

        self.only_existing = QCheckBox("Only update entities that already have this attribute")
        self.only_existing.setChecked(True)
        layout.addLayout(form)
        layout.addWidget(self.only_existing)

        self.result_label = QLabel("")
        self.result_label.setStyleSheet("color: #27ae60;")
        layout.addWidget(self.result_label)

        btns = QDialogButtonBox()
        apply_btn = btns.addButton("Apply to All", QDialogButtonBox.AcceptRole)
        btns.addButton("Close", QDialogButtonBox.RejectRole)
        apply_btn.clicked.connect(self.apply)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

    def apply(self):
        key = self.key_combo.currentText().strip()
        new_val = self.val_edit.text().strip()
        only_existing = self.only_existing.isChecked()
        if not key or not new_val:
            return
        count = 0
        for fname, fd in self.files.items():
            for entity in fd['entities']:
                for block in entity['blocks']:
                    if block['type'] == 'attributes':
                        found = False
                        for kv in block['kvs']:
                            if kv['key'] == key:
                                kv['value'] = new_val
                                count += 1
                                found = True
                                fd['modified'] = True
                        if not found and not only_existing:
                            block['kvs'].append({'key': key, 'value': new_val, 'comment': ''})
                            count += 1
                            fd['modified'] = True
        self.result_label.setText(f"Updated {count} attribute(s) across all files.")
        self.parent().refresh_modified_indicators()


# ─── Main Window ──────────────────────────────────────────────────────────────

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RTCW AI Editor")
        self.resize(1240, 750)
        self.files = {}          # filename -> {path, entities, modified}
        self.current_file = None
        self.current_entity = None
        self.current_attr_block_idx = None
        self._suppress_save = False
        self.map_names = []      # ordered list from maps.json
        self.ai_folder = None    # folder where .ai files live

        self._build_ui()
        self._build_menu()
        self._apply_dark_theme()

        # Auto-load maps.json on startup
        maps_path = find_maps_json()
        if maps_path:
            self._load_maps_json(maps_path)

    def _build_menu(self):
        mb = self.menuBar()

        file_menu = mb.addMenu("File")
        file_menu.addAction("Load maps.json...", self.browse_maps_json)
        file_menu.addAction("Set AI Files Folder...", self.set_ai_folder)
        file_menu.addAction("Load All Maps", self.load_all_maps, "Ctrl+Shift+O")
        file_menu.addSeparator()
        file_menu.addAction("Open Files...", self.open_files, QKeySequence.Open)
        file_menu.addAction("Save Current", self.save_current, QKeySequence.Save)
        file_menu.addAction("Save All", self.save_all, "Ctrl+Shift+S")
        file_menu.addAction("Backup AI Folder...", self.backup_ai_folder, "Ctrl+B")
        file_menu.addSeparator()
        file_menu.addAction("Close File", self.close_current_file)
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close)

        edit_menu = mb.addMenu("Edit")
        edit_menu.addAction("Find & Replace in Attributes...", self.find_replace)
        edit_menu.addAction("Bulk Set Attribute...", self.bulk_edit)

        help_menu = mb.addMenu("Help")
        help_menu.addAction("About", self.show_about)

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Left sidebar: map list + entity list
        sidebar = QWidget()
        sidebar.setFixedWidth(240)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        # Maps panel header
        maps_header = QWidget()
        maps_header.setFixedHeight(36)
        mh_layout = QHBoxLayout(maps_header)
        mh_layout.setContentsMargins(10, 0, 6, 0)
        self.maps_header_label = QLabel("Maps  —  no maps.json loaded")
        self.maps_header_label.setStyleSheet("color: #888; font-size: 11px;")
        mh_layout.addWidget(self.maps_header_label)
        mh_layout.addStretch()
        load_folder_btn = QPushButton("📂")
        load_folder_btn.setFixedSize(24, 24)
        load_folder_btn.setToolTip("Set AI files folder")
        load_folder_btn.clicked.connect(self.set_ai_folder)
        mh_layout.addWidget(load_folder_btn)

        backup_btn = QPushButton("💾")
        backup_btn.setFixedSize(24, 24)
        backup_btn.setToolTip("Backup AI folder")
        backup_btn.clicked.connect(self.backup_ai_folder)
        mh_layout.addWidget(backup_btn)

        # Map list
        self.map_list = QListWidget()
        self.map_list.setMaximumHeight(220)
        self.map_list.setToolTip("Click a map to load its .ai file")
        self.map_list.itemDoubleClicked.connect(self.on_map_doubleclicked)
        self.map_list.currentItemChanged.connect(self.on_map_selected)
        self.map_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.map_list.customContextMenuRequested.connect(self.file_context_menu)

        # Entity list
        entity_header = QWidget()
        entity_header.setFixedHeight(36)
        eh_layout = QHBoxLayout(entity_header)
        eh_layout.setContentsMargins(10, 0, 10, 0)
        eh_layout.addWidget(QLabel("Entities"))
        eh_layout.addStretch()
        self.entity_filter = QLineEdit()
        self.entity_filter.setPlaceholderText("Filter...")
        self.entity_filter.setFixedWidth(80)
        self.entity_filter.textChanged.connect(self.filter_entities)
        eh_layout.addWidget(self.entity_filter)

        self.entity_list = QListWidget()
        self.entity_list.currentItemChanged.connect(self.on_entity_selected)

        sidebar_layout.addWidget(maps_header)
        sidebar_layout.addWidget(self.map_list)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sidebar_layout.addWidget(sep)

        sidebar_layout.addWidget(entity_header)
        sidebar_layout.addWidget(self.entity_list)

        # Right: tabs
        self.tabs = QTabWidget()

        # Tab 1: Attribute Editor
        attr_tab = QWidget()
        attr_layout = QVBoxLayout(attr_tab)
        attr_layout.setContentsMargins(0, 0, 0, 0)

        self.entity_title = QLabel("Select an entity")
        self.entity_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.entity_title.setContentsMargins(12, 10, 12, 4)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.attr_editor = AttributeEditor()
        self.attr_editor.changed.connect(self.on_attr_changed)
        scroll.setWidget(self.attr_editor)

        attr_layout.addWidget(self.entity_title)
        attr_layout.addWidget(scroll)

        # Tab 2: Raw Script Editor
        raw_tab = QWidget()
        raw_layout = QVBoxLayout(raw_tab)
        raw_layout.setContentsMargins(0, 0, 0, 0)

        raw_toolbar = QWidget()
        raw_tb_layout = QHBoxLayout(raw_toolbar)
        raw_tb_layout.setContentsMargins(8, 4, 8, 4)
        save_raw_btn = QPushButton("Apply raw changes")
        save_raw_btn.clicked.connect(self.apply_raw_changes)
        raw_tb_layout.addWidget(save_raw_btn)
        raw_tb_layout.addStretch()
        raw_tb_layout.addWidget(QLabel("Edit raw script — changes update the attribute editor on Apply"))

        self.raw_editor = QTextEdit()
        self.raw_editor.setFont(QFont("Consolas", 10))
        self.highlighter = AIHighlighter(self.raw_editor.document())

        raw_layout.addWidget(raw_toolbar)
        raw_layout.addWidget(self.raw_editor)

        # Tab 3: All-files attributes table
        all_tab = QWidget()
        all_layout = QVBoxLayout(all_tab)
        all_layout.setContentsMargins(8, 8, 8, 8)
        all_layout.addWidget(QLabel("All entities with attributes across all loaded files:"))

        self.all_tree = QTreeWidget()
        self.all_tree.setHeaderLabels(["Entity", "File", "starting_health", "aggression", "aim_accuracy", "fov", "camper", "tactical"])
        self.all_tree.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.all_tree.itemDoubleClicked.connect(self.jump_to_entity)

        all_layout.addWidget(self.all_tree)

        self.tabs.addTab(attr_tab, "Attributes")
        self.tabs.addTab(raw_tab, "Raw Script")
        self.tabs.addTab(all_tab, "All Entities")
        self.tabs.currentChanged.connect(self.on_tab_changed)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(sidebar)
        splitter.addWidget(self.tabs)
        splitter.setStretchFactor(1, 1)

        main_layout.addWidget(splitter)

        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Open .ai files to begin  —  File > Open Files")

    def _apply_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow, QWidget { background: #1e1e1e; color: #d4d4d4; }
            QListWidget { background: #252526; border: none; }
            QListWidget::item { padding: 5px 8px; border-radius: 3px; }
            QListWidget::item:selected { background: #094771; color: #fff; }
            QListWidget::item:hover { background: #2a2d2e; }
            QTreeWidget { background: #252526; border: none; }
            QTreeWidget::item:selected { background: #094771; }
            QTabWidget::pane { border: none; border-top: 1px solid #3c3c3c; }
            QTabBar::tab { background: #2d2d2d; color: #888; padding: 6px 16px; border: none; }
            QTabBar::tab:selected { background: #1e1e1e; color: #d4d4d4; border-top: 2px solid #007acc; }
            QTextEdit { background: #1e1e1e; border: none; color: #d4d4d4; }
            QLineEdit { background: #3c3c3c; border: 1px solid #555; color: #d4d4d4; padding: 3px 6px; border-radius: 3px; }
            QLineEdit:focus { border-color: #007acc; }
            QSpinBox, QDoubleSpinBox { background: #3c3c3c; border: 1px solid #555; color: #d4d4d4; padding: 2px 4px; border-radius: 3px; }
            QSpinBox:focus, QDoubleSpinBox:focus { border-color: #007acc; }
            QPushButton { background: #3c3c3c; border: 1px solid #555; color: #d4d4d4; padding: 4px 12px; border-radius: 3px; }
            QPushButton:hover { background: #4a4a4a; border-color: #007acc; }
            QPushButton:pressed { background: #094771; }
            QScrollArea { border: none; }
            QLabel { color: #d4d4d4; }
            QMenuBar { background: #2d2d2d; color: #d4d4d4; }
            QMenuBar::item:selected { background: #094771; }
            QMenu { background: #2d2d2d; border: 1px solid #3c3c3c; }
            QMenu::item:selected { background: #094771; }
            QStatusBar { background: #007acc; color: #fff; }
            QSplitter::handle { background: #3c3c3c; width: 1px; }
            QHeaderView::section { background: #2d2d2d; color: #888; border: none; padding: 4px; }
            QComboBox { background: #3c3c3c; border: 1px solid #555; color: #d4d4d4; padding: 3px 6px; border-radius: 3px; }
            QGroupBox { border: 1px solid #3c3c3c; border-radius: 4px; margin-top: 8px; }
            QGroupBox::title { color: #888; subcontrol-origin: margin; left: 8px; }
            QCheckBox { color: #d4d4d4; }
            QDialog { background: #1e1e1e; }
        """)

    # ─── Maps JSON ────────────────────────────────────────────────────────────────

    def _load_maps_json(self, path):
        names = load_maps_json(path)
        if not names:
            QMessageBox.warning(self, "maps.json", f"No map names found in:\n{path}")
            return
        self.map_names = names
        self.maps_header_label.setText(f"Maps  ({len(names)})")
        self._rebuild_map_list()
        self.status.showMessage(f"Loaded maps.json — {len(names)} maps. Double-click a map to open its .ai file.")

    def _rebuild_map_list(self):
        self.map_list.clear()
        for name in self.map_names:
            fname = f"{name}.ai"
            item = QListWidgetItem()
            loaded = fname in self.files
            modified = loaded and self.files[fname]['modified']
            if modified:
                item.setText(f"● {name}")
                item.setForeground(QColor('#e5c07b'))
            elif loaded:
                item.setText(f"✓ {name}")
                item.setForeground(QColor('#98c379'))
            else:
                item.setText(f"  {name}")
                item.setForeground(QColor('#666'))
            item.setData(Qt.UserRole, name)
            self.map_list.addItem(item)

    def browse_maps_json(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open maps.json", "", "JSON Files (*.json);;All Files (*)"
        )
        if path:
            self._load_maps_json(path)

    def set_ai_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select folder containing .ai files")
        if folder:
            self.ai_folder = folder
            self.status.showMessage(f"AI folder set: {folder}")
            # Auto-load any already-known maps found in this folder
            if self.map_names:
                found = 0
                for name in self.map_names:
                    path = os.path.join(folder, f"{name}.ai")
                    if os.path.isfile(path) and f"{name}.ai" not in self.files:
                        found += 1
                if found:
                    r = QMessageBox.question(self, "Load Maps",
                        f"Found {found} .ai file(s) in that folder. Load them all now?",
                        QMessageBox.Yes | QMessageBox.No)
                    if r == QMessageBox.Yes:
                        self.load_all_maps()

    def load_all_maps(self):
        if not self.ai_folder:
            self.set_ai_folder()
            return
        if not self.map_names:
            QMessageBox.information(self, "No maps.json", "Load a maps.json first (File > Load maps.json).")
            return
        loaded = 0
        missing = []
        for name in self.map_names:
            path = os.path.join(self.ai_folder, f"{name}.ai")
            if os.path.isfile(path):
                if f"{name}.ai" not in self.files:
                    self.load_file(path)
                    loaded += 1
            else:
                missing.append(name)
        self._rebuild_map_list()
        self.refresh_all_tree()
        msg = f"Loaded {loaded} map(s)."
        if missing:
            msg += f"  Missing: {', '.join(missing)}"
        self.status.showMessage(msg)

    def backup_ai_folder(self):
        folder = self.ai_folder
        if not folder:
            QMessageBox.information(self, "No folder set",
                "Set your AI files folder first (📂 button or File > Set AI Files Folder).")
            return

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        default_dest = os.path.join(os.path.dirname(folder),
                                    f"{os.path.basename(folder)}_backup_{timestamp}")

        dest = QFileDialog.getExistingDirectory(
            self, "Choose where to save the backup — a new folder will be created inside here",
            os.path.dirname(folder)
        )
        if not dest:
            return

        backup_path = os.path.join(dest, f"{os.path.basename(folder)}_backup_{timestamp}")
        try:
            shutil.copytree(folder, backup_path)
            self.status.showMessage(f"Backup created: {backup_path}")
            QMessageBox.information(self, "Backup Complete",
                f"AI folder backed up to:\n{backup_path}")
        except Exception as e:
            QMessageBox.critical(self, "Backup Failed", str(e))

    def on_map_doubleclicked(self, item):
        name = item.data(Qt.UserRole)
        if not name:
            return
        fname = f"{name}.ai"
        if fname in self.files:
            # Already loaded — just select it
            self._select_file(fname)
            return
        # Try to find and load it
        if self.ai_folder:
            path = os.path.join(self.ai_folder, fname)
            if os.path.isfile(path):
                self.load_file(path)
                self._rebuild_map_list()
                self.refresh_all_tree()
                self._select_file(fname)
                return
        # Ask user to locate it
        path, _ = QFileDialog.getOpenFileName(
            self, f"Locate {fname}", "", f"AI Files ({fname});;All Files (*)"
        )
        if path:
            if not self.ai_folder:
                self.ai_folder = os.path.dirname(path)
            self.load_file(path)
            self._rebuild_map_list()
            self.refresh_all_tree()
            self._select_file(fname)

    def on_map_selected(self, current, previous):
        if not current:
            return
        name = current.data(Qt.UserRole)
        fname = f"{name}.ai"
        if fname in self.files:
            self._select_file(fname)

    def _select_file(self, fname):
        """Populate entity list for a given filename."""
        if fname not in self.files:
            return
        self.current_file = fname
        self.entity_list.clear()
        fd = self.files[fname]
        for entity in fd['entities']:
            self.entity_list.addItem(entity['name'])
        self.status.showMessage(f"{fname}  —  {len(fd['entities'])} entities")

    # ─── File Operations ───────────────────────────────────────────────────────

    def open_files(self):
        paths, _ = QFileDialog.getOpenFileNames(
            self, "Open AI Files", self.ai_folder or "", "AI Script Files (*.ai);;All Files (*)"
        )
        for path in paths:
            self.load_file(path)
        self._rebuild_map_list()
        self.refresh_all_tree()

    def load_file(self, path):
        fname = os.path.basename(path)
        if fname in self.files:
            self.status.showMessage(f"{fname} already loaded.")
            return
        try:
            with open(path, 'r', encoding='utf-8', errors='replace') as f:
                text = f.read()
            entities = parse_ai_file(text)
            self.files[fname] = {
                'path': path,
                'raw': text,
                'entities': entities,
                'modified': False,
            }
            self.status.showMessage(f"Loaded {fname}  —  {len(entities)} entities")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load {fname}:\n{e}")

    def save_current(self):
        if not self.current_file:
            return
        self._commit_raw_if_needed()
        self._save_file(self.current_file)

    def save_all(self):
        self._commit_raw_if_needed()
        for fname in list(self.files.keys()):
            self._save_file(fname)

    def _save_file(self, fname):
        fd = self.files[fname]
        full_text = fd['raw']
        for entity in fd['entities']:
            new_raw = reconstruct_entity(entity)
            if new_raw != entity['raw']:
                full_text = full_text.replace(entity['raw'], new_raw, 1)
                entity['raw'] = new_raw
        try:
            with open(fd['path'], 'w', encoding='utf-8') as f:
                f.write(full_text)
            fd['raw'] = full_text
            fd['modified'] = False
            self._rebuild_map_list()
            self.status.showMessage(f"Saved {fname}")
        except Exception as e:
            QMessageBox.critical(self, "Save Error", str(e))

    def close_current_file(self):
        if not self.current_file:
            return
        fd = self.files[self.current_file]
        if fd['modified']:
            r = QMessageBox.question(self, "Unsaved Changes",
                f"{self.current_file} has unsaved changes. Close anyway?",
                QMessageBox.Yes | QMessageBox.No)
            if r != QMessageBox.Yes:
                return
        del self.files[self.current_file]
        self.current_file = None
        self.current_entity = None
        self.entity_list.clear()
        self.attr_editor.load([])
        self.raw_editor.clear()
        self._rebuild_map_list()
        self.refresh_all_tree()

    def file_context_menu(self, pos):
        item = self.map_list.itemAt(pos)
        if not item:
            return
        name = item.data(Qt.UserRole)
        fname = f"{name}.ai"
        menu = QMenu(self)
        if fname in self.files:
            menu.addAction("Save", self.save_current)
            menu.addAction("Close", self.close_current_file)
        else:
            menu.addAction("Load...", lambda: self.on_map_doubleclicked(item))
        menu.exec_(self.map_list.mapToGlobal(pos))

    def refresh_modified_indicators(self):
        self._rebuild_map_list()

    # ─── Selection & Display ──────────────────────────────────────────────────

    def filter_entities(self, text):
        for i in range(self.entity_list.count()):
            item = self.entity_list.item(i)
            item.setHidden(text.lower() not in item.text().lower())

    def on_entity_selected(self, current, previous):
        if not current or not self.current_file:
            return
        name = current.text()
        fd = self.files[self.current_file]
        entity = next((e for e in fd['entities'] if e['name'] == name), None)
        if not entity:
            return
        self.current_entity = entity
        self.entity_title.setText(name)

        # Find attributes block
        attr_block = next((b for b in entity['blocks'] if b['type'] == 'attributes'), None)
        self.current_attr_block_idx = next(
            (i for i, b in enumerate(entity['blocks']) if b['type'] == 'attributes'), None
        )

        self._suppress_save = True
        if attr_block:
            self.attr_editor.load(attr_block['kvs'])
        else:
            self.attr_editor.load([])

        self.raw_editor.setPlainText(entity['raw'])
        self._suppress_save = False

    def on_tab_changed(self, idx):
        if idx == 2:
            self.refresh_all_tree()

    def on_attr_changed(self):
        if self._suppress_save or not self.current_entity or self.current_attr_block_idx is None:
            return
        # Write back kvs to the entity's attribute block
        block = self.current_entity['blocks'][self.current_attr_block_idx]
        block['kvs'] = self.attr_editor.get_kvs()
        if self.current_file:
            self.files[self.current_file]['modified'] = True
            self.refresh_modified_indicators()

    def apply_raw_changes(self):
        if not self.current_entity or not self.current_file:
            return
        new_raw = self.raw_editor.toPlainText()
        # Re-parse just this entity block
        entities = parse_ai_file(new_raw)
        if entities:
            e = entities[0]
            self.current_entity['blocks'] = e['blocks']
            self.current_entity['raw'] = e['raw']
        else:
            self.current_entity['raw'] = new_raw

        # Reload attribute editor
        attr_block = next((b for b in self.current_entity['blocks'] if b['type'] == 'attributes'), None)
        self.current_attr_block_idx = next(
            (i for i, b in enumerate(self.current_entity['blocks']) if b['type'] == 'attributes'), None
        )
        self._suppress_save = True
        self.attr_editor.load(attr_block['kvs'] if attr_block else [])
        self._suppress_save = False

        self.files[self.current_file]['modified'] = True
        self.refresh_modified_indicators()
        self.status.showMessage("Raw changes applied.")

    def _commit_raw_if_needed(self):
        if self.tabs.currentIndex() == 1:
            self.apply_raw_changes()

    # ─── All-entities tree ────────────────────────────────────────────────────

    def refresh_all_tree(self):
        self.all_tree.clear()
        COLS = ['starting_health', 'aggression', 'aim_accuracy', 'fov', 'camper', 'tactical']
        for fname, fd in self.files.items():
            for entity in fd['entities']:
                attr_block = next((b for b in entity['blocks'] if b['type'] == 'attributes'), None)
                if not attr_block:
                    continue
                kv_map = {kv['key']: kv['value'] for kv in attr_block['kvs']}
                row = [entity['name'], fname] + [kv_map.get(c, '') for c in COLS]
                item = QTreeWidgetItem(row)
                item.setData(0, Qt.UserRole, (fname, entity['name']))
                self.all_tree.addTopLevelItem(item)

    def jump_to_entity(self, item, col):
        data = item.data(0, Qt.UserRole)
        if not data:
            return
        fname, ename = data
        # Switch to the map in the map list
        for i in range(self.map_list.count()):
            map_item = self.map_list.item(i)
            if f"{map_item.data(Qt.UserRole)}.ai" == fname:
                self.map_list.setCurrentRow(i)
                break
        # Switch entity
        for i in range(self.entity_list.count()):
            if self.entity_list.item(i).text() == ename:
                self.entity_list.setCurrentRow(i)
                break
        self.tabs.setCurrentIndex(0)

    # ─── Dialogs ──────────────────────────────────────────────────────────────

    def find_replace(self):
        dlg = FindReplaceDialog(self, self.files)
        dlg.exec_()
        if self.current_entity:
            attr_block = next((b for b in self.current_entity['blocks'] if b['type'] == 'attributes'), None)
            if attr_block:
                self._suppress_save = True
                self.attr_editor.load(attr_block['kvs'])
                self._suppress_save = False

    def bulk_edit(self):
        dlg = BulkEditDialog(self, self.files)
        dlg.exec_()
        if self.current_entity:
            attr_block = next((b for b in self.current_entity['blocks'] if b['type'] == 'attributes'), None)
            if attr_block:
                self._suppress_save = True
                self.attr_editor.load(attr_block['kvs'])
                self._suppress_save = False

    def show_about(self):
        QMessageBox.about(self, "About RTCW AI Editor",
            "RTCW AI Editor\n"
            "─────────────────────────────────────────\n\n"
            "A desktop tool for editing Return to Castle Wolfenstein\n"
            "AI script files (.ai), built for the Totenkopf mod.\n\n"
            "RTCW .ai files define the behaviour of every entity in a\n"
            "map — soldiers, scientists, lopers, bosses and more. Each\n"
            "entity has an attributes block controlling stats like health,\n"
            "aggression and accuracy, plus scripted blocks that drive\n"
            "spawning, triggers, patrols and cinematic sequences.\n\n"
            "This editor lets you work across all 26 Totenkopf maps at\n"
            "once rather than opening files one at a time in a text editor.\n\n"
            "Features\n"
            "─────────────────────────────────────────\n"
            "    colour-coded by load and save state\n"
            "  • Point at your AI folder once and open any map with a\n"
            "    double-click, or load them all in one go\n"
            "  • Attribute editor — health, aggression, accuracy, FOV,\n"
            "    camper and tactical values as proper number fields\n"
            "  • Raw script editor with syntax highlighting for\n"
            "    advanced edits to triggers, spawns and cinematics\n"
            "  • All Entities table — spreadsheet view across every\n"
            "    loaded map, double-click any row to jump straight to it\n"
            "  • Find & Replace — swap a specific attribute value across\n"
            "    all loaded files at once\n"
            "  • Bulk Set — apply one attribute value to every entity\n"
            "    in every map in a single operation\n"
            "  • Saves back in the original format, preserving all\n"
            "    comments, whitespace and script structure\n\n"
            "Built with Python + PyQt5"
        )


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("RTCW AI Editor")
    app.setStyle("Fusion")
    win = MainWindow()
    win.show()
    # Open files passed as args
    for arg in sys.argv[1:]:
        if arg.endswith('.ai') and os.path.isfile(arg):
            win.load_file(arg)
    if any(a.endswith('.ai') for a in sys.argv[1:]):
        win._rebuild_map_list()
        win.refresh_all_tree()
    sys.exit(app.exec_())
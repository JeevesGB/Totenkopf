import os
import shutil
import webbrowser
from datetime import datetime

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QDockWidget, QListWidget, QListWidgetItem,
    QTreeWidget, QTreeWidgetItem, QTextEdit, QLineEdit, QLabel, QPushButton,
    QHBoxLayout, QVBoxLayout, QTabWidget, QFileDialog, QMessageBox,
    QStatusBar, QScrollArea, QHeaderView, QMenu, QDialog, QDialogButtonBox,
)
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QFont, QColor, QKeySequence

from parser import parse_ai_file, reconstruct_entity
from highlighter import AIHighlighter
from widgets.attribute_editor import AttributeEditor
from widgets.find_replace import FindReplaceDialog
from widgets.bulk_edit import BulkEditDialog
from utils.maps import load_maps_json, find_maps_json


# Columns shown in the All Entities tab (must match known_attrs.json keys)
_ALL_COLS = ['starting_health', 'aggression', 'aim_accuracy', 'fov', 'camper', 'tactical']


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RTCW AI Editor")
        self.resize(1240, 750)

        self._files = {}
        self._current_file = None
        self._current_entity = None
        self._current_attr_idx = None
        self._suppress_save = False
        self._map_names = []
        self._ai_folder = None

        self._build_ui()
        self._build_menu()
        self._load_stylesheet()
        self._restore_layout()

        # Auto-locate and load maps.json on startup
        maps_path = find_maps_json()
        if maps_path:
            self._load_maps_json(maps_path)

    # ── Stylesheet ────────────────────────────────────────────────────────────

    def _load_stylesheet(self):
        qss_path = os.path.join(os.path.dirname(__file__), 'config', 'newice.qss')
        try:
            with open(qss_path, 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            pass

    # ── Layout persistence ────────────────────────────────────────────────────

    def _restore_layout(self):
        settings = QSettings("JeevesGB", "RTCWAIEditor")
        geometry = settings.value("geometry")
        state    = settings.value("windowState")
        if geometry:
            self.restoreGeometry(geometry)
        if state:
            self.restoreState(state)

    def _save_layout(self):
        settings = QSettings("JeevesGB", "RTCWAIEditor")
        settings.setValue("geometry",    self.saveGeometry())
        settings.setValue("windowState", self.saveState())

    def _reset_layout(self):
        self.addDockWidget(Qt.LeftDockWidgetArea, self._maps_dock)
        self.addDockWidget(Qt.LeftDockWidgetArea, self._entities_dock)
        self.splitDockWidget(self._maps_dock, self._entities_dock, Qt.Vertical)
        self._maps_dock.show()
        self._entities_dock.show()
        self.resize(1240, 750)

    def closeEvent(self, event):
        self._save_layout()
        super().closeEvent(event)

    # ── Menu ──────────────────────────────────────────────────────────────────

    def _build_menu(self):
        mb = self.menuBar()

        file_menu = mb.addMenu("File")
        file_menu.addAction("Load maps.json…",       self.browse_maps_json)
        file_menu.addAction("Set AI Files Folder…",  self.set_ai_folder)
        file_menu.addAction("Load All Maps",         self.load_all_maps,    "Ctrl+Shift+O")
        file_menu.addSeparator()
        file_menu.addAction("Open Files…",           self.open_files,       QKeySequence.Open)
        file_menu.addAction("Save Current",          self.save_current,     QKeySequence.Save)
        file_menu.addAction("Save All",              self.save_all,         "Ctrl+Shift+S")
        file_menu.addAction("Backup AI Folder…",     self.backup_ai_folder, "Ctrl+B")
        file_menu.addSeparator()
        file_menu.addAction("Close File",            self.close_current_file)
        file_menu.addSeparator()
        file_menu.addAction("Exit",                  self.close)

        edit_menu = mb.addMenu("Edit")
        edit_menu.addAction("Find & Replace in Attributes…", self.find_replace)
        edit_menu.addAction("Bulk Set Attribute…",           self.bulk_edit)

        view_menu = mb.addMenu("View")
        view_menu.addAction("Show Maps Panel",     lambda: self._maps_dock.show())
        view_menu.addAction("Show Entities Panel", lambda: self._entities_dock.show())
        view_menu.addSeparator()
        view_menu.addAction("Save Layout", self._save_layout)
        view_menu.addAction("Reset Layout",        self._reset_layout)

        help_menu = mb.addMenu("Help")
        help_menu.addAction("About", self.show_about)

    # ── UI Layout ─────────────────────────────────────────────────────────────

    def _build_ui(self):
        # Central widget is the tab area
        self.setCentralWidget(self._build_tabs())

        # ── Maps dock ──
        self._map_list = QListWidget()
        self._map_list.setToolTip("Double-click a map to load its .ai file")
        self._map_list.itemDoubleClicked.connect(self._on_map_doubleclicked)
        self._map_list.currentItemChanged.connect(self._on_map_selected)
        self._map_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self._map_list.customContextMenuRequested.connect(self._map_context_menu)

        maps_widget = QWidget()
        maps_layout = QVBoxLayout(maps_widget)
        maps_layout.setContentsMargins(0, 0, 0, 0)
        maps_layout.setSpacing(0)
        maps_layout.addWidget(self._build_maps_header())
        maps_layout.addWidget(self._map_list)

        self._maps_dock = QDockWidget("Maps", self)
        self._maps_dock.setObjectName("MapsDock")        # required for saveState/restoreState
        self._maps_dock.setWidget(maps_widget)
        self._maps_dock.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.addDockWidget(Qt.LeftDockWidgetArea, self._maps_dock)

        # ── Entities dock ──
        self._entity_list = QListWidget()
        self._entity_list.currentItemChanged.connect(self._on_entity_selected)

        entities_widget = QWidget()
        entities_layout = QVBoxLayout(entities_widget)
        entities_layout.setContentsMargins(0, 0, 0, 0)
        entities_layout.setSpacing(0)
        entities_layout.addWidget(self._build_entities_header())
        entities_layout.addWidget(self._entity_list)

        self._entities_dock = QDockWidget("Entities", self)
        self._entities_dock.setObjectName("EntitiesDock")  # required for saveState/restoreState
        self._entities_dock.setWidget(entities_widget)
        self._entities_dock.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.addDockWidget(Qt.LeftDockWidgetArea, self._entities_dock)

        # Stack Maps above Entities by default
        self.splitDockWidget(self._maps_dock, self._entities_dock, Qt.Vertical)

        self._status = QStatusBar()
        self.setStatusBar(self._status)
        self._status.showMessage("Open .ai files to begin  —  File > Open Files")

    def _build_maps_header(self):
        header = QWidget()
        header.setFixedHeight(36)
        layout = QHBoxLayout(header)
        layout.setContentsMargins(10, 0, 6, 0)

        self._maps_header_label = QLabel("Maps  —  no maps.json loaded")
        self._maps_header_label.setStyleSheet("color: #888; font-size: 11px;")
        layout.addWidget(self._maps_header_label)
        layout.addStretch()

        folder_btn = QPushButton("📂")
        folder_btn.setFixedSize(24, 24)
        folder_btn.setToolTip("Set AI files folder")
        folder_btn.clicked.connect(self.set_ai_folder)
        layout.addWidget(folder_btn)

        backup_btn = QPushButton("💾")
        backup_btn.setFixedSize(24, 24)
        backup_btn.setToolTip("Backup AI folder")
        backup_btn.clicked.connect(self.backup_ai_folder)
        layout.addWidget(backup_btn)

        return header

    def _build_entities_header(self):
        header = QWidget()
        header.setFixedHeight(36)
        layout = QHBoxLayout(header)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.addWidget(QLabel("Entities"))
        layout.addStretch()

        self._entity_filter = QLineEdit()
        self._entity_filter.setPlaceholderText("Filter…")
        self._entity_filter.setFixedWidth(80)
        self._entity_filter.textChanged.connect(self._filter_entities)
        layout.addWidget(self._entity_filter)

        return header

    def _build_tabs(self):
        self._tabs = QTabWidget()
        self._tabs.addTab(self._build_attr_tab(),  "Attributes")
        self._tabs.addTab(self._build_raw_tab(),   "Raw Script")
        self._tabs.addTab(self._build_all_tab(),   "All Entities")
        self._tabs.currentChanged.connect(self._on_tab_changed)
        return self._tabs

    def _build_attr_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)

        self._entity_title = QLabel("Select an entity")
        self._entity_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self._entity_title.setContentsMargins(12, 10, 12, 4)
        layout.addWidget(self._entity_title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self._attr_editor = AttributeEditor()
        self._attr_editor.changed.connect(self._on_attr_changed)
        scroll.setWidget(self._attr_editor)
        layout.addWidget(scroll)
        return tab

    def _build_raw_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)

        toolbar = QWidget()
        tb_layout = QHBoxLayout(toolbar)
        tb_layout.setContentsMargins(8, 4, 8, 4)

        apply_btn = QPushButton("Apply raw changes")
        apply_btn.clicked.connect(self._apply_raw_changes)
        tb_layout.addWidget(apply_btn)
        tb_layout.addStretch()
        tb_layout.addWidget(QLabel("Edit raw script — changes update the attribute editor on Apply"))

        self._raw_editor = QTextEdit()
        self._raw_editor.setFont(QFont("Consolas", 10))
        self._highlighter = AIHighlighter(self._raw_editor.document())

        layout.addWidget(toolbar)
        layout.addWidget(self._raw_editor)
        return tab

    def _build_all_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.addWidget(QLabel("All entities with attributes across all loaded files:"))

        self._all_tree = QTreeWidget()
        self._all_tree.setHeaderLabels(
            ["Entity", "File"] + [c.replace('_', ' ').title() for c in _ALL_COLS]
        )
        self._all_tree.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self._all_tree.itemDoubleClicked.connect(self._jump_to_entity)
        layout.addWidget(self._all_tree)
        return tab

    # ── maps.json ─────────────────────────────────────────────────────────────

    def _load_maps_json(self, path):
        names = load_maps_json(path)
        if not names:
            QMessageBox.warning(self, "maps.json", f"No map names found in:\n{path}")
            return
        self._map_names = names
        self._maps_header_label.setText(f"Maps  ({len(names)})")
        self._rebuild_map_list()
        self._status.showMessage(
            f"Loaded maps.json — {len(names)} maps. Double-click a map to open its .ai file."
        )

    def browse_maps_json(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open maps.json", "", "JSON Files (*.json);;All Files (*)"
        )
        if path:
            self._load_maps_json(path)

    def _rebuild_map_list(self):
        self._map_list.clear()
        for name in self._map_names:
            fname    = f"{name}.ai"
            loaded   = fname in self._files
            modified = loaded and self._files[fname]['modified']

            item = QListWidgetItem()
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
            self._map_list.addItem(item)

    # ── AI folder ─────────────────────────────────────────────────────────────

    def set_ai_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Select folder containing .ai files"
        )
        if not folder:
            return
        self._ai_folder = folder
        self._status.showMessage(f"AI folder set: {folder}")

        if not self._map_names:
            return
        unloaded = [
            name for name in self._map_names
            if f"{name}.ai" not in self._files
            and os.path.isfile(os.path.join(folder, f"{name}.ai"))
        ]
        if unloaded:
            r = QMessageBox.question(
                self, "Load Maps",
                f"Found {len(unloaded)} .ai file(s) in that folder. Load them all now?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if r == QMessageBox.Yes:
                self.load_all_maps()

    def load_all_maps(self):
        if not self._ai_folder:
            self.set_ai_folder()
            return
        if not self._map_names:
            QMessageBox.information(
                self, "No maps.json", "Load a maps.json first (File > Load maps.json)."
            )
            return

        loaded  = 0
        missing = []
        for name in self._map_names:
            path = os.path.join(self._ai_folder, f"{name}.ai")
            if os.path.isfile(path):
                if f"{name}.ai" not in self._files:
                    self._load_file(path)
                    loaded += 1
            else:
                missing.append(name)

        self._rebuild_map_list()
        self._refresh_all_tree()

        msg = f"Loaded {loaded} map(s)."
        if missing:
            msg += f"  Missing: {', '.join(missing)}"
        self._status.showMessage(msg)

    def backup_ai_folder(self):
        if not self._ai_folder:
            QMessageBox.information(
                self, "No folder set",
                "Set your AI files folder first (📂 button or File > Set AI Files Folder)."
            )
            return

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        dest = QFileDialog.getExistingDirectory(
            self,
            "Choose where to save the backup — a new folder will be created inside here",
            os.path.dirname(self._ai_folder),
        )
        if not dest:
            return

        backup_path = os.path.join(
            dest, f"{os.path.basename(self._ai_folder)}_backup_{timestamp}"
        )
        try:
            shutil.copytree(self._ai_folder, backup_path)
            self._status.showMessage(f"Backup created: {backup_path}")
            QMessageBox.information(
                self, "Backup Complete", f"AI folder backed up to:\n{backup_path}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Backup Failed", str(e))

    # ── Map list events ───────────────────────────────────────────────────────

    def _on_map_doubleclicked(self, item):
        name  = item.data(Qt.UserRole)
        fname = f"{name}.ai"

        if fname in self._files:
            self._select_file(fname)
            return

        if self._ai_folder:
            path = os.path.join(self._ai_folder, fname)
            if os.path.isfile(path):
                self._load_file(path)
                self._rebuild_map_list()
                self._refresh_all_tree()
                self._select_file(fname)
                return

        path, _ = QFileDialog.getOpenFileName(
            self, f"Locate {fname}", "", f"AI Files ({fname});;All Files (*)"
        )
        if path:
            if not self._ai_folder:
                self._ai_folder = os.path.dirname(path)
            self._load_file(path)
            self._rebuild_map_list()
            self._refresh_all_tree()
            self._select_file(fname)

    def _on_map_selected(self, current, previous):
        if not current:
            return
        fname = f"{current.data(Qt.UserRole)}.ai"
        if fname in self._files:
            self._select_file(fname)

    def _select_file(self, fname):
        if fname not in self._files:
            return
        self._current_file = fname
        self._entity_list.clear()
        fd = self._files[fname]
        for entity in fd['entities']:
            self._entity_list.addItem(entity['name'])
        self._status.showMessage(f"{fname}  —  {len(fd['entities'])} entities")

    def _map_context_menu(self, pos):
        item = self._map_list.itemAt(pos)
        if not item:
            return
        name  = item.data(Qt.UserRole)
        fname = f"{name}.ai"
        menu  = QMenu(self)
        if fname in self._files:
            menu.addAction("Save",  self.save_current)
            menu.addAction("Close", self.close_current_file)
        else:
            menu.addAction("Load…", lambda: self._on_map_doubleclicked(item))
        menu.exec_(self._map_list.mapToGlobal(pos))

    # ── File I/O ──────────────────────────────────────────────────────────────

    def open_files(self):
        paths, _ = QFileDialog.getOpenFileNames(
            self, "Open AI Files",
            self._ai_folder or "",
            "AI Script Files (*.ai);;All Files (*)",
        )
        for path in paths:
            self._load_file(path)
        self._rebuild_map_list()
        self._refresh_all_tree()

    def _load_file(self, path):
        fname = os.path.basename(path)
        if fname in self._files:
            self._status.showMessage(f"{fname} already loaded.")
            return
        try:
            with open(path, 'r', encoding='utf-8', errors='replace') as f:
                text = f.read()
            entities = parse_ai_file(text)
            self._files[fname] = {
                'path':     path,
                'raw':      text,
                'entities': entities,
                'modified': False,
            }
            self._status.showMessage(f"Loaded {fname}  —  {len(entities)} entities")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load {fname}:\n{e}")

    def save_current(self):
        if not self._current_file:
            return
        self._commit_raw_if_needed()
        self._save_file(self._current_file)

    def save_all(self):
        self._commit_raw_if_needed()
        for fname in list(self._files.keys()):
            self._save_file(fname)

    def _save_file(self, fname):
        fd        = self._files[fname]
        full_text = fd['raw']

        for entity in fd['entities']:
            new_raw = reconstruct_entity(entity)
            if new_raw != entity['raw']:
                full_text     = full_text.replace(entity['raw'], new_raw, 1)
                entity['raw'] = new_raw

        try:
            with open(fd['path'], 'w', encoding='utf-8') as f:
                f.write(full_text)
            fd['raw']      = full_text
            fd['modified'] = False
            self._rebuild_map_list()
            self._status.showMessage(f"Saved {fname}")
        except Exception as e:
            QMessageBox.critical(self, "Save Error", str(e))

    def close_current_file(self):
        if not self._current_file:
            return
        fd = self._files[self._current_file]
        if fd['modified']:
            r = QMessageBox.question(
                self, "Unsaved Changes",
                f"{self._current_file} has unsaved changes. Close anyway?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if r != QMessageBox.Yes:
                return

        del self._files[self._current_file]
        self._current_file   = None
        self._current_entity = None
        self._entity_list.clear()
        self._attr_editor.load([])
        self._raw_editor.clear()
        self._rebuild_map_list()
        self._refresh_all_tree()

    def refresh_modified_indicators(self):
        self._rebuild_map_list()

    # ── Entity selection ──────────────────────────────────────────────────────

    def _filter_entities(self, text):
        for i in range(self._entity_list.count()):
            item = self._entity_list.item(i)
            item.setHidden(text.lower() not in item.text().lower())

    def _on_entity_selected(self, current, previous):
        if not current or not self._current_file:
            return
        name   = current.text()
        fd     = self._files[self._current_file]
        entity = next((e for e in fd['entities'] if e['name'] == name), None)
        if not entity:
            return

        self._current_entity   = entity
        self._entity_title.setText(name)

        attr_block = next((b for b in entity['blocks'] if b['type'] == 'attributes'), None)
        self._current_attr_idx = next(
            (i for i, b in enumerate(entity['blocks']) if b['type'] == 'attributes'), None
        )

        self._suppress_save = True
        self._attr_editor.load(attr_block['kvs'] if attr_block else [])
        self._raw_editor.setPlainText(entity['raw'])
        self._suppress_save = False

    def _on_tab_changed(self, idx):
        if idx == 2:
            self._refresh_all_tree()

    def _on_attr_changed(self):
        if self._suppress_save or not self._current_entity or self._current_attr_idx is None:
            return
        block = self._current_entity['blocks'][self._current_attr_idx]
        block['kvs'] = self._attr_editor.get_kvs()
        if self._current_file:
            self._files[self._current_file]['modified'] = True
            self._rebuild_map_list()

    def _apply_raw_changes(self):
        if not self._current_entity or not self._current_file:
            return
        new_raw  = self._raw_editor.toPlainText()
        entities = parse_ai_file(new_raw)
        if entities:
            e = entities[0]
            self._current_entity['blocks'] = e['blocks']
            self._current_entity['raw']    = e['raw']
        else:
            self._current_entity['raw'] = new_raw

        attr_block = next(
            (b for b in self._current_entity['blocks'] if b['type'] == 'attributes'), None
        )
        self._current_attr_idx = next(
            (i for i, b in enumerate(self._current_entity['blocks']) if b['type'] == 'attributes'),
            None,
        )

        self._suppress_save = True
        self._attr_editor.load(attr_block['kvs'] if attr_block else [])
        self._suppress_save = False

        self._files[self._current_file]['modified'] = True
        self._rebuild_map_list()
        self._status.showMessage("Raw changes applied.")

    def _commit_raw_if_needed(self):
        if self._tabs.currentIndex() == 1:
            self._apply_raw_changes()

    # ── All Entities tab ──────────────────────────────────────────────────────

    def _refresh_all_tree(self):
        self._all_tree.clear()
        for fname, fd in self._files.items():
            for entity in fd['entities']:
                attr_block = next(
                    (b for b in entity['blocks'] if b['type'] == 'attributes'), None
                )
                if not attr_block:
                    continue
                kv_map = {kv['key']: kv['value'] for kv in attr_block['kvs']}
                row    = [entity['name'], fname] + [kv_map.get(c, '') for c in _ALL_COLS]
                item   = QTreeWidgetItem(row)
                item.setData(0, Qt.UserRole, (fname, entity['name']))
                self._all_tree.addTopLevelItem(item)

    def _jump_to_entity(self, item, col):
        data = item.data(0, Qt.UserRole)
        if not data:
            return
        fname, ename = data

        for i in range(self._map_list.count()):
            map_item = self._map_list.item(i)
            if f"{map_item.data(Qt.UserRole)}.ai" == fname:
                self._map_list.setCurrentRow(i)
                break
        for i in range(self._entity_list.count()):
            if self._entity_list.item(i).text() == ename:
                self._entity_list.setCurrentRow(i)
                break
        self._tabs.setCurrentIndex(0)

    # ── Dialogs ───────────────────────────────────────────────────────────────

    def find_replace(self):
        dlg = FindReplaceDialog(self, self._files)
        dlg.exec_()
        self._reload_current_attr_editor()

    def bulk_edit(self):
        dlg = BulkEditDialog(self, self._files)
        dlg.exec_()
        self._reload_current_attr_editor()

    def _reload_current_attr_editor(self):
        if not self._current_entity:
            return
        attr_block = next(
            (b for b in self._current_entity['blocks'] if b['type'] == 'attributes'), None
        )
        if attr_block:
            self._suppress_save = True
            self._attr_editor.load(attr_block['kvs'])
            self._suppress_save = False

    def show_about(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("About RTCW AI Editor")
        dlg.setWindowFlags(dlg.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        dlg.setFixedWidth(420)

        layout = QVBoxLayout(dlg)
        layout.setSpacing(10)

        text = QLabel(
            "RTCW AI Editor\n"
            "─────────────────────────────────────────\n\n"
            "A desktop tool for editing Return to Castle Wolfenstein\n"
            "AI script files (.ai), built for the Totenkopf mod.\n\n"
            "Features\n"
            "─────────────────────────────────────────\n"
            "  • Map list colour-coded by load and save state\n\n"
            "  • Point at your AI folder once and open any map with a\n"
            "    double-click, or load them all in one go\n\n"
            "  • Attribute editor with proper number fields\n\n"
            "  • Raw script editor with syntax highlighting\n\n"
            "  • All Entities table — spreadsheet view across every\n"
            "    loaded map, double-click any row to jump straight to it\n\n"
            "  • Find & Replace across all loaded files at once\n\n"
            "  • Bulk Set — apply one attribute value to every entity\n\n"
            "  • Saves in the original format, preserving comments\n\n"
            "  • Dockable panels — drag Maps and Entities anywhere\n\n"
            "JeevesGB 2026"
        )
        text.setWordWrap(True)
        layout.addWidget(text)

        btn_row = QHBoxLayout()

        github_btn = QPushButton("View on GitHub")
        github_btn.clicked.connect(
            lambda: webbrowser.open("https://github.com/JeevesGB")
        )
        btn_row.addWidget(github_btn)
        btn_row.addStretch()

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dlg.accept)
        btn_row.addWidget(close_btn)

        layout.addLayout(btn_row)
        dlg.exec_()
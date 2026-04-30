import sys
import json
import os
import time
import subprocess
import webbrowser
import shutil
from datetime import datetime
import platformdirs
if sys.platform == "win32":
    import winreg
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFileDialog, QInputDialog, QFrame, 
    QScrollArea, QGridLayout, QMenu, QDialog, QListWidget, QMessageBox,
    QLineEdit, QComboBox, QFormLayout, QStatusBar, QSystemTrayIcon,
    QDoubleSpinBox, QCheckBox
)
from PySide6.QtCore import Qt, Signal, QMimeData, QThread, QByteArray
from PySide6.QtGui import QAction, QDrag, QPixmap, QIcon, QKeySequence, QShortcut

USER_DATA_DIR = platformdirs.user_data_dir("Nexus", "FarazKayanHaque")
os.makedirs(USER_DATA_DIR, exist_ok=True)
WORKFLOWS_FILE = os.path.join(USER_DATA_DIR, "workflows.json")
SETTINGS_FILE = os.path.join(USER_DATA_DIR, "settings.json")

STYLESHEET = """
QMainWindow { background-color: #121212; }
QWidget { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; color: #E0E0E0; font-size: 14px; }
QScrollArea, QScrollArea > QWidget > QWidget { background-color: #121212; border: none; }
QScrollBar:vertical { background: transparent; width: 10px; margin: 0; }
QScrollBar::handle:vertical { background: #333333; min-height: 20px; border-radius: 5px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
QLabel#Title { font-size: 28px; font-weight: 700; color: #FFFFFF; }
QFrame#WorkflowCard { background-color: #2A2A2A; border-radius: 12px; }
QFrame#WorkflowCard:hover { background-color: #353535; }
QLabel#CardTitle { font-size: 16px; font-weight: 600; color: #FFFFFF; }
QLabel#CardSubtext { font-size: 12px; color: #888888; }
QPushButton#MenuButton { background-color: transparent; color: #A0A0A0; font-size: 18px; font-weight: bold; border: none; padding: 0px; border-radius: 4px; }
QPushButton#MenuButton:hover { color: #FFFFFF; background-color: rgba(255, 255, 255, 0.1); }
QPushButton#AddCard { background-color: transparent; border: 2px dashed #404040; border-radius: 12px; font-size: 16px; font-weight: 600; color: #A0A0A0; }
QPushButton#AddCard:hover { border-color: #4F46E5; background-color: rgba(79, 70, 229, 0.05); color: #4F46E5; }
QPushButton#AddCard:pressed { background-color: rgba(79, 70, 229, 0.1); }
QDialog { background-color: #1A1A1A; border-radius: 8px; }
QDialog QLabel#ModalTitle { font-size: 20px; font-weight: 700; color: #FFFFFF; }
QLineEdit { background-color: #121212; border: 1px solid #333333; border-radius: 6px; padding: 10px; color: white; }
QLineEdit:focus { border: 1px solid #4F46E5; }
QListWidget { background-color: #121212; border: 1px solid #333333; border-radius: 6px; padding: 6px; outline: none; }
QListWidget::item { padding: 8px; border-radius: 4px; margin-bottom: 2px; }
QListWidget::item:selected { background-color: #2A2A2A; color: #FFFFFF; }
QPushButton { background-color: #2A2A2A; border: 1px solid #3A3A3A; border-radius: 6px; padding: 8px 16px; font-weight: 500; color: #FFFFFF; }
QPushButton:hover { background-color: #353535; border: 1px solid #4A4A4A; }
QPushButton:pressed { background-color: #1A1A1A; }
QPushButton#AccentButton { background-color: #4F46E5; border: none; color: white; font-weight: bold; padding: 10px 20px; border-radius: 6px; }
QPushButton#AccentButton:hover { background-color: #4338CA; }
QMenu { background-color: #2A2A2A; border: 1px solid #3A3A3A; border-radius: 6px; padding: 4px; }
QMenu::item { padding: 6px 24px 6px 12px; border-radius: 4px; color: #E0E0E0; }
QMenu::item:selected { background-color: #4F46E5; color: white; }
QComboBox { background-color: #121212; border: 1px solid #333333; border-radius: 6px; padding: 8px; color: white; }
QStatusBar { background-color: #121212; color: #888888; border-top: 1px solid #222222; }
"""

LIGHT_STYLESHEET = """
QMainWindow { background-color: #F3F4F6; }
QWidget { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; color: #1F2937; font-size: 14px; }
QScrollArea, QScrollArea > QWidget > QWidget { background-color: #F3F4F6; border: none; }
QScrollBar:vertical { background: transparent; width: 10px; margin: 0; }
QScrollBar::handle:vertical { background: #CBD5E1; min-height: 20px; border-radius: 5px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
QLabel#Title { font-size: 28px; font-weight: 700; color: #111827; }
QFrame#WorkflowCard { background-color: #FFFFFF; border-radius: 12px; border: 1px solid #E5E7EB; }
QFrame#WorkflowCard:hover { background-color: #F9FAFB; border-color: #D1D5DB; }
QLabel#CardTitle { font-size: 16px; font-weight: 600; color: #111827; }
QLabel#CardSubtext { font-size: 12px; color: #6B7280; }
QPushButton#MenuButton { background-color: transparent; color: #6B7280; font-size: 18px; font-weight: bold; border: none; padding: 0px; border-radius: 4px; }
QPushButton#MenuButton:hover { color: #111827; background-color: rgba(0, 0, 0, 0.05); }
QPushButton#AddCard { background-color: transparent; border: 2px dashed #D1D5DB; border-radius: 12px; font-size: 16px; font-weight: 600; color: #6B7280; }
QPushButton#AddCard:hover { border-color: #4F46E5; background-color: rgba(79, 70, 229, 0.05); color: #4F46E5; }
QPushButton#AddCard:pressed { background-color: rgba(79, 70, 229, 0.1); }
QDialog { background-color: #FFFFFF; border-radius: 8px; }
QDialog QLabel#ModalTitle { font-size: 20px; font-weight: 700; color: #111827; }
QLineEdit { background-color: #FFFFFF; border: 1px solid #D1D5DB; border-radius: 6px; padding: 10px; color: #1F2937; }
QLineEdit:focus { border: 1px solid #4F46E5; }
QListWidget { background-color: #FFFFFF; border: 1px solid #D1D5DB; border-radius: 6px; padding: 6px; outline: none; }
QListWidget::item { padding: 8px; border-radius: 4px; margin-bottom: 2px; color: #1F2937; }
QListWidget::item:selected { background-color: #F3F4F6; color: #111827; }
QPushButton { background-color: #FFFFFF; border: 1px solid #D1D5DB; border-radius: 6px; padding: 8px 16px; font-weight: 500; color: #1F2937; }
QPushButton:hover { background-color: #F9FAFB; border: 1px solid #9CA3AF; }
QPushButton:pressed { background-color: #E5E7EB; }
QPushButton#AccentButton { background-color: #4F46E5; border: none; color: white; font-weight: bold; padding: 10px 20px; border-radius: 6px; }
QPushButton#AccentButton:hover { background-color: #4338CA; }
QMenu { background-color: #FFFFFF; border: 1px solid #D1D5DB; border-radius: 6px; padding: 4px; }
QMenu::item { padding: 6px 24px 6px 12px; border-radius: 4px; color: #1F2937; }
QMenu::item:selected { background-color: #4F46E5; color: white; }
QComboBox { background-color: #FFFFFF; border: 1px solid #D1D5DB; border-radius: 6px; padding: 8px; color: #1F2937; }
QStatusBar { background-color: #F3F4F6; color: #6B7280; border-top: 1px solid #E5E7EB; }
"""

class SettingsDialog(QDialog):
    def __init__(self, parent=None, current_theme="Dark", startup_enabled=False, launch_delay=1.5):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.resize(400, 400)
        self.setModal(True)
        self.current_theme = current_theme
        self.startup_enabled = startup_enabled
        self.launch_delay = launch_delay
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        
        title_lbl = QLabel(self.windowTitle())
        title_lbl.setObjectName("ModalTitle")
        layout.addWidget(title_lbl)
        layout.addSpacing(10)
        
        form_layout = QFormLayout()
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light", "System Default"])
        self.theme_combo.setCurrentText(self.current_theme)
        
        theme_lbl = QLabel("Theme:")
        theme_lbl.setStyleSheet("font-weight: bold;")
        form_layout.addRow(theme_lbl, self.theme_combo)

        self.delay_spin = QDoubleSpinBox()
        self.delay_spin.setRange(0.5, 5.0)
        self.delay_spin.setSingleStep(0.5)
        self.delay_spin.setSuffix(" sec")
        self.delay_spin.setValue(self.launch_delay)
        
        delay_lbl = QLabel("Launch delay:")
        delay_lbl.setStyleSheet("font-weight: bold;")
        form_layout.addRow(delay_lbl, self.delay_spin)

        if sys.platform == "win32":
            self.startup_cb = QCheckBox()
            self.startup_cb.setChecked(self.startup_enabled)
            startup_lbl = QLabel("Run on startup:")
            startup_lbl.setStyleSheet("font-weight: bold;")
            form_layout.addRow(startup_lbl, self.startup_cb)

        layout.addLayout(form_layout)
        
        layout.addSpacing(10)
        
        manage_data_lbl = QLabel("Manage Data")
        manage_data_lbl.setStyleSheet("font-weight: bold; font-size: 16px; margin-top: 10px;")
        layout.addWidget(manage_data_lbl)

        data_layout = QHBoxLayout()
        btn_export = QPushButton("📤 Export")
        btn_export.clicked.connect(self.export_data)
        btn_import = QPushButton("📥 Import")
        btn_import.clicked.connect(self.import_data)
        data_layout.addWidget(btn_export)
        data_layout.addWidget(btn_import)
        data_layout.addStretch()
        layout.addLayout(data_layout)

        layout.addSpacing(20)
        
        about_title = QLabel("About App")
        about_title.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(about_title)
        
        about_desc = QLabel("Nexus Workflow Manager\n\nCreate, organize, and execute all your apps and sites in one go!\n\nCreator: Faraz Kayan Haque")
        about_desc.setWordWrap(True)
        about_desc.setStyleSheet("color: #888888; margin-top: 5px;")
        layout.addWidget(about_desc)
        
        layout.addStretch()
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_cancel = QPushButton("Cancel")
        btn_cancel.clicked.connect(self.reject)
        btn_save = QPushButton("Save Settings")
        btn_save.setObjectName("AccentButton")
        btn_save.clicked.connect(self.accept)
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_save)
        
        layout.addLayout(btn_layout)
        
    def export_data(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export Workflows", "nexus_workflows.json", "JSON Files (*.json)")
        if path:
            self.parent().export_workflows(path)

    def import_data(self):
        path, _ = QFileDialog.getOpenFileName(self, "Import Workflows", "", "JSON Files (*.json)")
        if path:
            self.parent().import_workflows(path)
            self.accept()

    def get_data(self):
        startup = self.startup_cb.isChecked() if hasattr(self, 'startup_cb') else False
        return self.theme_combo.currentText(), startup, self.delay_spin.value()

class WorkflowExecutor(QThread):
    finished_all = Signal(list)

    def __init__(self, urls, apps, launch_delay=1.5, parent=None):
        super().__init__(parent)
        self.urls = urls
        self.apps = apps
        self.launch_delay = launch_delay
        self.errors = []

    def run(self):
        for i, url in enumerate(self.urls):
            try:
                webbrowser.open(url)
            except Exception as e:
                self.errors.append(f"<b>Failed to open URL:</b> {url}<br/><i>{e}</i>")
            
            if i < len(self.urls) - 1 or len(self.apps) > 0:
                time.sleep(self.launch_delay)

        for app_path in self.apps:
            try:
                if sys.platform == "win32": os.startfile(app_path)
                elif sys.platform == "darwin": subprocess.Popen(["open", app_path])
                else: subprocess.Popen(["xdg-open", app_path])
            except Exception as e:
                app_name = os.path.basename(app_path)
                self.errors.append(f"<b>Failed to launch app:</b> {app_name}<br/><i>{e}</i><br/>Path: {app_path}")
                
        self.finished_all.emit(self.errors)

class WorkflowDialog(QDialog):
    def __init__(self, parent=None, workflow_name="", description="", color="Default", apps=None, urls=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Workflow" if workflow_name else "Create Workflow")
        self.resize(500, 650)
        self.setModal(True)
        
        self.workflow_name = workflow_name
        self.description = description
        self.color = color
        self.apps = apps[:] if apps else []
        self.urls = urls[:] if urls else []
        
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        title_lbl = QLabel(self.windowTitle())
        title_lbl.setObjectName("ModalTitle")
        layout.addWidget(title_lbl)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Workflow Name")
        self.name_input.setText(self.workflow_name)
        layout.addWidget(self.name_input)
        
        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("Description (Optional)")
        self.desc_input.setText(self.description)
        layout.addWidget(self.desc_input)

        color_layout = QFormLayout()
        self.color_combo = QComboBox()
        self.color_combo.addItems(["Default", "Blue", "Purple", "Green", "Red", "Orange"])
        self.color_combo.setCurrentText(self.color)
        color_lbl = QLabel("Tag Color:")
        color_lbl.setStyleSheet("font-weight: bold; color: #888888;")
        color_layout.addRow(color_lbl, self.color_combo)
        layout.addLayout(color_layout)
        
        apps_lbl = QLabel("APPLICATIONS")
        apps_lbl.setStyleSheet("font-size: 12px; font-weight: bold; color: #888888; margin-top: 10px;")
        layout.addWidget(apps_lbl)
        
        self.apps_list = QListWidget()
        for app in self.apps: self.apps_list.addItem(app)
        layout.addWidget(self.apps_list)
        
        apps_btn_layout = QHBoxLayout()
        btn_add_app = QPushButton("Add App")
        btn_add_app.clicked.connect(self.add_app)
        btn_remove_app = QPushButton("Remove")
        btn_remove_app.clicked.connect(self.remove_app)
        apps_btn_layout.addWidget(btn_add_app)
        apps_btn_layout.addWidget(btn_remove_app)
        apps_btn_layout.addStretch()
        layout.addLayout(apps_btn_layout)
        
        urls_lbl = QLabel("WEBSITES")
        urls_lbl.setStyleSheet("font-size: 12px; font-weight: bold; color: #888888; margin-top: 10px;")
        layout.addWidget(urls_lbl)
        
        self.urls_list = QListWidget()
        for url in self.urls: self.urls_list.addItem(url)
        layout.addWidget(self.urls_list)
        
        urls_btn_layout = QHBoxLayout()
        btn_add_url = QPushButton("Add URL")
        btn_add_url.clicked.connect(self.add_url)
        btn_remove_url = QPushButton("Remove")
        btn_remove_url.clicked.connect(self.remove_url)
        urls_btn_layout.addWidget(btn_add_url)
        urls_btn_layout.addWidget(btn_remove_url)
        urls_btn_layout.addStretch()
        layout.addLayout(urls_btn_layout)
        
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        btn_cancel = QPushButton("Cancel")
        btn_cancel.clicked.connect(self.reject)
        self.btn_save = QPushButton("Save Workflow")
        self.btn_save.setObjectName("AccentButton")
        self.btn_save.clicked.connect(self.accept)
        bottom_layout.addWidget(btn_cancel)
        bottom_layout.addWidget(self.btn_save)
        
        layout.addLayout(bottom_layout)
        
    def add_app(self):
        filters = "Executables (*.exe *.app *.sh *.bat);;All Files (*)"
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Application", "", filters)
        if file_path and file_path not in self.apps:
            self.apps.append(file_path)
            self.apps_list.addItem(file_path)

    def remove_app(self):
        selected = self.apps_list.selectedItems()
        if selected:
            row = self.apps_list.row(selected[0])
            self.apps_list.takeItem(row)
            self.apps.pop(row)

    def add_url(self):
        url, ok = QInputDialog.getText(self, "Add URL", "Enter website URL:")
        if ok and url:
            url = url.strip()
            if not url: return
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "https://" + url
            if url not in self.urls:
                self.urls.append(url)
                self.urls_list.addItem(url)

    def remove_url(self):
        selected = self.urls_list.selectedItems()
        if selected:
            row = self.urls_list.row(selected[0])
            self.urls_list.takeItem(row)
            self.urls.pop(row)
            
    def get_data(self):
        return self.name_input.text().strip(), self.desc_input.text().strip(), self.color_combo.currentText(), self.apps, self.urls

class WorkflowCard(QFrame):
    clicked = Signal(str)
    reordered = Signal(str, str) # source_name, target_name

    def __init__(self, w_name, w_data, parent=None):
        super().__init__(parent)
        self.w_name = w_name
        self.w_data = w_data
        self.setObjectName("WorkflowCard")
        self.setFixedSize(280, 120)
        self.setCursor(Qt.PointingHandCursor)
        self.setAcceptDrops(True)
        self.drag_start_pos = None
        self._did_drag = False

        color_map = {
            "Blue": "#3B82F6", "Purple": "#8B5CF6", "Green": "#10B981", 
            "Red": "#EF4444", "Orange": "#F59E0B"
        }
        color_name = w_data.get("color", "Default")
        border_color = color_map.get(color_name, "transparent")
        
        if border_color != "transparent":
            self.setStyleSheet(f"QFrame#WorkflowCard {{ border-left: 4px solid {border_color}; }}")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 20, 10, 20)
        layout.setSpacing(10)
        
        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)
        title = QLabel(w_name)
        title.setObjectName("CardTitle")
        title.setWordWrap(True)
        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        title.setAttribute(Qt.WA_TransparentForMouseEvents)
        
        title_layout.addWidget(title)
        
        desc_text = w_data.get("description", "")
        if desc_text:
            desc = QLabel(desc_text)
            desc.setStyleSheet("color: #888888; font-size: 13px;")
            desc.setWordWrap(True)
            desc.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            desc.setAttribute(Qt.WA_TransparentForMouseEvents)
            title_layout.addWidget(desc)

        last_run = w_data.get("last_run")
        if last_run:
            try:
                lr_dt = datetime.fromisoformat(last_run)
                delta = (datetime.now() - lr_dt).days
                if delta == 0:
                    lr_str = "Last run: Today"
                elif delta == 1:
                    lr_str = "Last run: Yesterday"
                else:
                    lr_str = f"Last run: {delta} days ago"
                lr_lbl = QLabel(lr_str)
                lr_lbl.setObjectName("CardSubtext")
                lr_lbl.setAttribute(Qt.WA_TransparentForMouseEvents)
                title_layout.addWidget(lr_lbl)
            except ValueError:
                pass

        title_layout.addStretch()

        layout.addLayout(title_layout, 1)
        
        # Check for missing apps
        apps = w_data.get("apps", [])
        missing = any(not os.path.exists(app) for app in apps)
        if missing:
            warning_lbl = QLabel("!", self)
            warning_lbl.setFixedSize(20, 20)
            warning_lbl.setStyleSheet("background-color: #F59E0B; color: white; border-radius: 10px; font-weight: bold; font-size: 14px;")
            warning_lbl.setAlignment(Qt.AlignCenter)
            warning_lbl.setToolTip("One or more app paths are missing.")
            warning_lbl.move(self.width() - 25, self.height() - 25)

        self.menu_btn = QPushButton("⋮")
        self.menu_btn.setObjectName("MenuButton")
        self.menu_btn.setFixedSize(30, 30)
        self.menu_btn.setCursor(Qt.PointingHandCursor)
        
        # Menu attached later by main window
        layout.addWidget(self.menu_btn, 0, Qt.AlignTop)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_pos = event.pos()
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if not self._did_drag:
                self.clicked.emit(self.w_name)
            self._did_drag = False
            event.accept()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if self.drag_start_pos is None:
            return
        if (event.pos() - self.drag_start_pos).manhattanLength() < QApplication.startDragDistance():
            return
        
        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(self.w_name)
        drag.setMimeData(mime_data)
        pixmap = self.grab()
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())
        
        self._did_drag = True
        drag.exec(Qt.MoveAction)
        self.drag_start_pos = None

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            source_name = event.mimeData().text()
            if source_name != self.w_name:
                event.acceptProposedAction()
                self.setStyleSheet(f"QFrame#WorkflowCard {{ background-color: #4F46E5; border: 2px solid white; }}")

    def dragLeaveEvent(self, event):
        color_map = {
            "Blue": "#3B82F6", "Purple": "#8B5CF6", "Green": "#10B981", 
            "Red": "#EF4444", "Orange": "#F59E0B"
        }
        color_name = self.w_data.get("color", "Default")
        border_color = color_map.get(color_name, "transparent")
        
        if border_color != "transparent":
            self.setStyleSheet(f"QFrame#WorkflowCard {{ border-left: 4px solid {border_color}; }}")
        else:
            self.setStyleSheet("")

    def dropEvent(self, event):
        source_name = event.mimeData().text()
        self.dragLeaveEvent(event)
        if source_name != self.w_name:
            self.reordered.emit(source_name, self.w_name)
            event.acceptProposedAction()

class NexusApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nexus")
        self.resize(1000, 700)
        
        # Generate and set icon
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_path, "nexus.ico")
        self.app_icon = QIcon(icon_path)
        self.setWindowIcon(self.app_icon)

        self.settings = self.load_settings()
        if "geometry" in self.settings:
            self.restoreGeometry(QByteArray.fromBase64(self.settings["geometry"].encode()))
            
        self.apply_theme()
        
        self.workflows = self.load_workflows()
        self._last_col_count = 0
        self.search_text = ""
        self.init_ui()
        self.init_tray()
        self.init_shortcuts()
        self._tray_shown = False

    def init_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+N"), self).activated.connect(self.create_workflow)
        QShortcut(QKeySequence("Ctrl+F"), self).activated.connect(self.search_bar.setFocus)
        QShortcut(QKeySequence("Escape"), self).activated.connect(lambda: self.search_bar.clear() if self.search_bar.text() else None)

    def init_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.app_icon)
        self.tray_menu = QMenu()
        self.tray_icon.setContextMenu(self.tray_menu)
        self.update_tray_menu()
        self.tray_icon.show()

    def update_tray_menu(self):
        self.tray_menu.clear()
        show_action = self.tray_menu.addAction("Show Window")
        show_action.triggered.connect(self.showNormal)
        self.tray_menu.addSeparator()
        
        for w_name in self.workflows:
            action = self.tray_menu.addAction(w_name)
            action.triggered.connect(lambda checked=False, n=w_name: self.run_workflow(n))
            
        self.tray_menu.addSeparator()
        quit_action = self.tray_menu.addAction("Quit")
        quit_action.triggered.connect(QApplication.quit)

    def set_run_on_startup(self, enable):
        if sys.platform == "win32":
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
                if enable:
                    path = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(sys.argv[0])
                    winreg.SetValueEx(key, "Nexus", 0, winreg.REG_SZ, f'"{path}"')
                else:
                    try:
                        winreg.DeleteValue(key, "Nexus")
                    except FileNotFoundError:
                        pass
                winreg.CloseKey(key)
            except Exception as e:
                print("Startup registry error:", e)

    def check_run_on_startup(self):
        if sys.platform == "win32":
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_READ)
                value, _ = winreg.QueryValueEx(key, "Nexus")
                winreg.CloseKey(key)
                return True
            except FileNotFoundError:
                return False
        return False

    def closeEvent(self, event):
        self.settings["geometry"] = self.saveGeometry().toBase64().data().decode()
        self.save_settings()
        self.hide()
        if not self._tray_shown:
            self.tray_icon.showMessage("Nexus", "Nexus is still running in the tray.", QSystemTrayIcon.Information, 2000)
            self._tray_shown = True
        event.ignore()

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, 'r') as f:
                    return json.load(f)
            except: pass
        return {"theme": "Dark"}

    def save_settings(self):
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(self.settings, f)

    def apply_theme(self):
        theme = self.settings.get("theme", "Dark")
        if theme == "Light":
            self.setStyleSheet(LIGHT_STYLESHEET)
        elif theme == "Dark":
            self.setStyleSheet(STYLESHEET)
        else:
            try:
                if QApplication.styleHints().colorScheme() == Qt.ColorScheme.Dark:
                    self.setStyleSheet(STYLESHEET)
                else:
                    self.setStyleSheet(LIGHT_STYLESHEET)
            except AttributeError:
                self.setStyleSheet(STYLESHEET)

    def open_settings(self):
        startup = self.check_run_on_startup()
        delay = self.settings.get("launch_delay", 1.5)
        dlg = SettingsDialog(self, self.settings.get("theme", "Dark"), startup, delay)
        if dlg.exec() == QDialog.Accepted:
            theme, start_en, dly = dlg.get_data()
            self.settings["theme"] = theme
            self.settings["launch_delay"] = dly
            self.save_settings()
            self.apply_theme()
            self.set_run_on_startup(start_en)

    def export_workflows(self, path):
        try:
            with open(path, 'w') as f:
                json.dump(self.workflows, f, indent=4)
            self.statusBar.showMessage(f"✅ Successfully exported workflows to {os.path.basename(path)}", 5000)
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export workflows:\n{e}")

    def import_workflows(self, path):
        try:
            with open(path, 'r') as f:
                data = json.load(f)
                
            new_w = []
            overwrite_w = []
            valid_data = {}
            for k, v in data.items():
                if isinstance(v, dict) and 'urls' in v and 'apps' in v:
                    valid_data[k] = v
                    if k in self.workflows:
                        overwrite_w.append(k)
                    else:
                        new_w.append(k)
            
            if not valid_data:
                return
                
            dlg = QDialog(self)
            dlg.setWindowTitle("Import Preview")
            dlg.resize(400, 300)
            layout = QVBoxLayout(dlg)
            
            h_lay = QHBoxLayout()
            new_layout = QVBoxLayout()
            new_layout.addWidget(QLabel("New workflows:"))
            new_list = QListWidget()
            new_list.addItems(new_w)
            new_layout.addWidget(new_list)
            h_lay.addLayout(new_layout)
            
            over_layout = QVBoxLayout()
            over_layout.addWidget(QLabel("Will overwrite:"))
            over_list = QListWidget()
            over_list.addItems(overwrite_w)
            over_layout.addWidget(over_list)
            h_lay.addLayout(over_layout)
            
            layout.addLayout(h_lay)

            btn_box = QHBoxLayout()
            btn_box.addStretch()
            c_btn = QPushButton("Cancel")
            c_btn.clicked.connect(dlg.reject)
            i_btn = QPushButton("Import")
            i_btn.setObjectName("AccentButton")
            i_btn.clicked.connect(dlg.accept)
            btn_box.addWidget(c_btn)
            btn_box.addWidget(i_btn)
            layout.addLayout(btn_box)
            
            if dlg.exec() == QDialog.Accepted:
                for k, v in valid_data.items():
                    self.workflows[k] = v
                self.save_workflows()
                self.refresh_grid(self._last_col_count)
                self.update_tray_menu()
                self.statusBar.showMessage(f"✅ Successfully imported workflows from {os.path.basename(path)}", 5000)
        except Exception as e:
            QMessageBox.critical(self, "Import Error", f"Failed to import workflows:\n{e}")

    def load_workflows(self):
        if os.path.exists(WORKFLOWS_FILE):
            try:
                with open(WORKFLOWS_FILE, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def save_workflows(self):
        with open(WORKFLOWS_FILE, 'w') as f:
            json.dump(self.workflows, f, indent=4)

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(60, 40, 60, 40)
        main_layout.setSpacing(20)
        
        top_layout = QHBoxLayout()
        title = QLabel("Nexus")
        title.setObjectName("Title")
        
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Search workflows...")
        self.search_bar.setFixedWidth(300)
        self.search_bar.textChanged.connect(self.on_search)
        
        self.settings_btn = QPushButton("⚙")
        self.settings_btn.setObjectName("MenuButton")
        self.settings_btn.setFixedSize(30, 30)
        self.settings_btn.setCursor(Qt.PointingHandCursor)
        self.settings_btn.clicked.connect(self.open_settings)
        
        top_layout.addWidget(title)
        top_layout.addStretch()
        top_layout.addWidget(self.search_bar)
        top_layout.addSpacing(10)
        top_layout.addWidget(self.settings_btn)
        
        main_layout.addLayout(top_layout)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.scroll_layout.setContentsMargins(0, 0, 0, 40)
        
        self.grid_container = QWidget()
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(24)
        
        self.scroll_layout.addWidget(self.grid_container)
        
        self.add_btn_layout = QHBoxLayout()
        self.add_btn_layout.setAlignment(Qt.AlignCenter)
        self.add_btn_layout.setContentsMargins(0, 30, 0, 0)
        
        self.scroll_layout.addLayout(self.add_btn_layout)
        
        self.scroll_area.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll_area)

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("✅ Ready", 5000)
        
    def on_search(self, text):
        self.search_text = text.lower().strip()
        self.refresh_grid(self._last_col_count)

    def clear_grid(self):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def refresh_grid(self, col_count=1):
        self.clear_grid()
        
        row, col = 0, 0
        for w_name, w_data in self.workflows.items():
            if self.search_text and self.search_text not in w_name.lower() and self.search_text not in w_data.get("description", "").lower():
                continue
            
            card = self.create_workflow_card(w_name, w_data)
            self.grid_layout.addWidget(card, row, col)
            col += 1
            if col >= col_count:
                col = 0
                row += 1
                
        # Handle Add Card below the grid
        while self.add_btn_layout.count():
            item = self.add_btn_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        if not self.search_text:
            add_card = self.create_add_card()
            self.add_btn_layout.addWidget(add_card)
        
    def create_workflow_card(self, w_name, w_data):
        card = WorkflowCard(w_name, w_data)
        card.clicked.connect(self.run_workflow)
        card.reordered.connect(self.reorder_workflows)
        
        menu = QMenu(card.menu_btn)
        edit_action = menu.addAction("✏️ Edit Workflow")
        duplicate_action = menu.addAction("📄 Duplicate Workflow")
        menu.addSeparator()
        delete_action = menu.addAction("🗑️ Delete Workflow")
        
        edit_action.triggered.connect(lambda checked=False, name=w_name: self.edit_workflow(name))
        duplicate_action.triggered.connect(lambda checked=False, name=w_name: self.duplicate_workflow(name))
        delete_action.triggered.connect(lambda checked=False, name=w_name: self.delete_workflow(name))
        
        card.menu_btn.setMenu(menu)
        card.menu_btn.setStyleSheet("QPushButton::menu-indicator{image:none;}")
        
        return card

    def create_add_card(self):
        card = QPushButton("➕ Add Workflow")
        card.setObjectName("AddCard")
        card.setFixedSize(300, 60)
        card.setCursor(Qt.PointingHandCursor)
        card.clicked.connect(lambda: self.create_workflow())
        return card

    def reorder_workflows(self, source_name, target_name):
        if source_name == target_name or self.search_text: 
            return
            
        keys = list(self.workflows.keys())
        try:
            source_idx = keys.index(source_name)
            target_idx = keys.index(target_name)
        except ValueError:
            return
            
        keys.pop(source_idx)
        keys.insert(target_idx, source_name)
        
        reordered = {k: self.workflows[k] for k in keys}
        self.workflows = reordered
        self.save_workflows()
        self.refresh_grid(self._last_col_count)

    def run_workflow(self, name):
        if name not in self.workflows: return
        data = self.workflows[name]
        
        urls = data.get("urls", [])
        apps = data.get("apps", [])
        
        if hasattr(self, 'executor') and self.executor.isRunning():
            QMessageBox.warning(self, "Warning", "A workflow is already running. Please wait.")
            return
            
        self.workflows[name]["last_run"] = datetime.now().isoformat()
        self.save_workflows()
        self.refresh_grid(self._last_col_count)
        
        self.statusBar.showMessage(f"🚀 Executing workflow: {name}...")
        delay = self.settings.get("launch_delay", 1.5)
        self.executor = WorkflowExecutor(urls, apps, delay)
        self.executor.finished_all.connect(self.on_workflow_finished)
        self.executor.start()

    def on_workflow_finished(self, errors):
        if errors:
            self.statusBar.showMessage("⚠️ Workflow finished with errors", 5000)
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Workflow Execution Errors")
            msg.setText("Some items in the workflow failed to launch.")
            msg.setInformativeText("<br/><br/>".join(errors))
            msg.exec()
        else:
            self.statusBar.showMessage("✅ Workflow executed successfully", 5000)

    def create_workflow(self):
        dlg = WorkflowDialog(self)
        if dlg.exec() == QDialog.Accepted:
            name, desc, color, apps, urls = dlg.get_data()
            if not name: return
            if name in self.workflows:
                QMessageBox.warning(self, "Error", "Workflow already exists!")
                return
            self.workflows[name] = {"description": desc, "color": color, "apps": apps, "urls": urls}
            self.save_workflows()
            self.refresh_grid(self._last_col_count)
            self.update_tray_menu()
            self.statusBar.showMessage(f"✅ Workflow '{name}' created", 5000)

    def edit_workflow(self, name):
        data = self.workflows[name]
        dlg = WorkflowDialog(self, name, data.get("description", ""), data.get("color", "Default"), data.get("apps", []), data.get("urls", []))
        if dlg.exec() == QDialog.Accepted:
            new_name, desc, color, apps, urls = dlg.get_data()
            if not new_name: return
            if new_name != name and new_name in self.workflows:
                QMessageBox.warning(self, "Error", "Name already exists!")
                return
            if new_name != name:
                self.workflows.pop(name)
            self.workflows[new_name] = {"description": desc, "color": color, "apps": apps, "urls": urls}
            self.save_workflows()
            self.refresh_grid(self._last_col_count)
            self.update_tray_menu()
            self.statusBar.showMessage(f"✅ Workflow '{new_name}' updated", 5000)

    def duplicate_workflow(self, name):
        data = self.workflows[name]
        new_name = name + " (Copy)"
        counter = 1
        while new_name in self.workflows:
            new_name = f"{name} (Copy {counter})"
            counter += 1
            
        self.workflows[new_name] = data.copy()
        self.save_workflows()
        self.refresh_grid(self._last_col_count)
        self.update_tray_menu()
        self.statusBar.showMessage(f"✅ Duplicated '{name}'", 5000)

    def delete_workflow(self, name):
        reply = QMessageBox.question(self, "Confirm Delete", 
                                     f"Are you sure you want to delete '{name}'?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.workflows.pop(name, None)
            self.save_workflows()
            self.refresh_grid(self._last_col_count)
            self.update_tray_menu()
            self.statusBar.showMessage(f"🗑️ Workflow '{name}' deleted", 5000)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.reflow_grid()

    def reflow_grid(self):
        card_width = 280
        spacing = 24
        margins = 60 * 2
        available_width = self.width() - margins
        
        if available_width < card_width:
            col_count = 1
        else:
            col_count = max(1, available_width // (card_width + spacing))
            
        if self._last_col_count == col_count:
            return
        self._last_col_count = col_count
        self.refresh_grid(col_count)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False) # need this for tray icon to work if window closed!
    window = NexusApp()
    window.show()
    sys.exit(app.exec())

# TO BUILD EXE:
# pip install pyinstaller platformdirs
# pyinstaller --onefile --windowed --name "Nexus" jarvis_control_center.py
#
# The --windowed flag suppresses the console window.
# The --onefile flag bundles everything into a single EXE.
# Data files (workflows.json, settings.json) are stored in:
#   Windows: %APPDATA%\FarazKayanHaque\Nexus\
#   macOS:   ~/Library/Application Support/Nexus/
#   Linux:   ~/.local/share/Nexus/

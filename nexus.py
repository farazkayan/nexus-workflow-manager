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

VERSION = "1.2"
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFileDialog, QInputDialog, QFrame, 
    QScrollArea, QGridLayout, QMenu, QDialog, QListWidget, QMessageBox,
    QLineEdit, QComboBox, QFormLayout, QStatusBar, QSystemTrayIcon,
    QDoubleSpinBox, QCheckBox
)
from PySide6.QtCore import Qt, Signal, QMimeData, QThread, QByteArray, QPropertyAnimation, Property
from PySide6.QtGui import QColor, QFont
from PySide6.QtGui import QAction, QDrag, QPixmap, QIcon, QPainter, QColor, QFont, QKeySequence, QShortcut

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


class WhatsNewDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"What's new in Nexus v{VERSION} ✨")
        self.resize(450, 400)
        self.setModal(True)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        
        title_lbl = QLabel(self.windowTitle())
        title_lbl.setObjectName("ModalTitle")
        layout.addWidget(title_lbl)
        
        layout.addSpacing(10)
        
        features = [
            "⭐ Pin workflows to the top",
            "🔢 Reorder items inside workflows",
            "📐 Compact view mode",
            "🎨 Emoji icons for each workflow",
            "🎉 UI polish and improvements"
        ]
        
        for f in features:
            lbl = QLabel(f)
            lbl.setStyleSheet("font-size: 14px; margin-bottom: 8px;")
            layout.addWidget(lbl)
            
        layout.addStretch()
        
        btn_box = QHBoxLayout()
        btn_box.addStretch()
        btn = QPushButton("Let's go!")
        btn.setObjectName("AccentButton")
        btn.clicked.connect(self.accept)
        btn_box.addWidget(btn)
        
        layout.addLayout(btn_box)

class EmojiPickerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Pick an Emoji")
        self.setModal(True)
        self.selected_emoji = "🚀"
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        categories = {
            "Work": ["💼", "📊", "📋", "💻", "📧", "📞", "🖥️", "🗂️"],
            "Creative": ["🎨", "🎵", "✏️", "📸", "🎬", "🎮", "🖌️", "📝"],
            "Personal": ["🏠", "🏋️", "📚", "☕", "🌙", "🎯", "💡", "🔑"],
            "Social": ["💬", "👥", "📱", "🌐", "📣", "🤝", "💌", "🔔"],
            "Misc": ["⚡", "🔥", "⭐", "🚀", "🛠️", "📦", "🔐", "❤️"]
        }
        
        for cat, emojis in categories.items():
            lbl = QLabel(cat)
            lbl.setStyleSheet("font-weight: bold; margin-top: 10px; color: #888; font-size: 12px;")
            scroll_layout.addWidget(lbl)
            
            grid = QGridLayout()
            grid.setSpacing(4)
            row, col = 0, 0
            for e in emojis:
                btn = QPushButton(e)
                btn.setFixedSize(52, 52)
                emoji_font = QFont("Segoe UI Emoji", 22)
                btn.setFont(emoji_font)
                btn.setStyleSheet("border: none; background: transparent; padding: 0;")
                btn.setCursor(Qt.PointingHandCursor)
                btn.clicked.connect(lambda checked=False, em=e: self.emoji_clicked(em))
                grid.addWidget(btn, row, col)
                col += 1
                if col > 7:
                    col = 0
                    row += 1
            scroll_layout.addLayout(grid)
            
        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        self.resize(400, 500)
        
    def emoji_clicked(self, e):
        self.selected_emoji = e
        self.accept()

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
        
        version_lbl = QLabel(f"Nexus v{VERSION} — by Faraz Kayan Haque")
        version_lbl.setStyleSheet("color: #666666; font-size: 11px;")
        version_lbl.setAlignment(Qt.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(version_lbl)
        
    def export_data(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export Workflows", "nexus_workflows.json", "JSON Files (*.json)")
        if path:
            self.parent().export_workflows(path)

    def import_data(self):
        path, _ = QFileDialog.getOpenFileName(self, "Import Workflows", "", "JSON Files (*.json)")
        if path:
            self.parent().import_workflows(path)
            self.accept()

    def pick_emoji(self):
        dlg = EmojiPickerDialog(self)
        if dlg.exec() == QDialog.Accepted:
            self.emoji = dlg.selected_emoji
            self.emoji_btn.setText(self.emoji)

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
    def __init__(self, parent=None, workflow_name="", description="", color="Default", emoji="🚀", apps=None, urls=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Workflow" if workflow_name else "Create Workflow")
        self.resize(500, 650)
        self.setModal(True)
        
        self.workflow_name = workflow_name
        self.description = description
        self.color = color
        self.emoji = emoji
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

        row_h = QHBoxLayout()
        icon_lbl = QLabel("Icon:")
        icon_lbl.setStyleSheet("font-weight: bold; color: #888888;")
        self.emoji_btn = QPushButton(self.emoji)
        self.emoji_btn.setFixedSize(40, 40)
        self.emoji_btn.setStyleSheet("font-size: 20px; padding: 0;")
        self.emoji_btn.clicked.connect(self.pick_emoji)
        
        color_lbl = QLabel("Tag Color:")
        color_lbl.setStyleSheet("font-weight: bold; color: #888888;")
        self.color_combo = QComboBox()
        self.color_combo.addItems(["Default", "Blue", "Purple", "Green", "Red", "Orange"])
        self.color_combo.setCurrentText(self.color)
        
        row_h.addWidget(icon_lbl)
        row_h.addWidget(self.emoji_btn)
        row_h.addSpacing(20)
        row_h.addWidget(color_lbl)
        row_h.addWidget(self.color_combo)
        row_h.addStretch()
        layout.addLayout(row_h)
        
        apps_lbl = QLabel("APPLICATIONS")
        apps_lbl.setStyleSheet("font-size: 12px; font-weight: bold; color: #888888; margin-top: 10px;")
        layout.addWidget(apps_lbl)
        
        self.apps_list = QListWidget()
        self.apps_list.setDragDropMode(QListWidget.InternalMove)
        self.apps_list.setDefaultDropAction(Qt.MoveAction)
        self.apps_list.setDragEnabled(True)
        self.apps_list.setAcceptDrops(True)
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
        self.urls_list.setDragDropMode(QListWidget.InternalMove)
        self.urls_list.setDefaultDropAction(Qt.MoveAction)
        self.urls_list.setDragEnabled(True)
        self.urls_list.setAcceptDrops(True)
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
        if file_path and file_path not in [self.apps_list.item(i).text() for i in range(self.apps_list.count())]:
            self.apps_list.addItem(file_path)

    def remove_app(self):
        selected = self.apps_list.selectedItems()
        if selected:
            row = self.apps_list.row(selected[0])
            self.apps_list.takeItem(row)

    def add_url(self):
        url, ok = QInputDialog.getText(self, "Add URL", "Enter website URL:")
        if ok and url:
            url = url.strip()
            if not url: return
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "https://" + url
            if url not in [self.urls_list.item(i).text() for i in range(self.urls_list.count())]:
                self.urls_list.addItem(url)

    def remove_url(self):
        selected = self.urls_list.selectedItems()
        if selected:
            row = self.urls_list.row(selected[0])
            self.urls_list.takeItem(row)
            
    def pick_emoji(self):
        dlg = EmojiPickerDialog(self)
        if dlg.exec() == QDialog.Accepted:
            self.emoji = dlg.selected_emoji
            self.emoji_btn.setText(self.emoji)

    def get_data(self):
        apps = [self.apps_list.item(i).text() for i in range(self.apps_list.count())]
        urls = [self.urls_list.item(i).text() for i in range(self.urls_list.count())]
        return self.name_input.text().strip(), self.desc_input.text().strip(), self.color_combo.currentText(), self.emoji, apps, urls

class WorkflowCard(QFrame):
    clicked = Signal(str)
    reordered = Signal(str, str)
    pinToggled = Signal(str)

    def _set_bg_color(self, color):
        self._bg_color = color
        style = f"QFrame#WorkflowCard {{ background-color: {color.name()}; border-radius: 12px;"
        if self._border_color != "transparent" and self._border_color != "Default":
            style += f" border: 1px solid {'#E5E7EB' if self.is_light else '#333333'}; border-bottom: 3px solid {self._border_color};"
        else:
            style += f" border: 1px solid {'#E5E7EB' if self.is_light else '#333333'};"
        style += "}"
        self.setStyleSheet(style)

    def _get_bg_color(self):
        return self._bg_color

    bg_color = Property(QColor, _get_bg_color, _set_bg_color)

    def __init__(self, w_name, w_data, compact_mode=False, is_light=False, parent=None):
        super().__init__(parent)
        self.w_name = w_name
        self.w_data = w_data
        self.compact_mode = compact_mode
        self.is_light = is_light
        self.setObjectName("WorkflowCard")
        
        if self.compact_mode:
            self.setMinimumWidth(220)
            self.setFixedHeight(52)
        else:
            self.setMinimumWidth(220)
            self.setFixedHeight(120)

        self.setCursor(Qt.PointingHandCursor)
        self.setAcceptDrops(True)
        self.drag_start_pos = None
        self._did_drag = False

        emoji = w_data.get("emoji", "🚀")
        pinned = w_data.get("pinned", False)
        
        self.color_name = w_data.get("color", "Default")
        color_map = {
            "Blue": "#3B82F6", "Purple": "#8B5CF6", "Green": "#10B981", 
            "Red": "#EF4444", "Orange": "#F59E0B"
        }
        self._border_color = color_map.get(self.color_name, "transparent")
        
        self.base_color = QColor("#FFFFFF") if self.is_light else QColor("#2A2A2A")
        self.hover_color = QColor("#F3F4F6") if self.is_light else QColor("#3E3E3E")
        self._bg_color = self.base_color
        self._set_bg_color(self.base_color)

        self.anim = QPropertyAnimation(self, b"bg_color")
        self.anim.setDuration(150)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 8, 8) if self.compact_mode else layout.setContentsMargins(16, 16, 12, 16)
        layout.setSpacing(12)
        
        emoji_lbl = QLabel(emoji)
        emoji_lbl.setAlignment(Qt.AlignCenter)
        if not self.compact_mode:
            emoji_lbl.setStyleSheet("font-size: 28px;")
            emoji_lbl.setFixedSize(40, 40)
            layout.addWidget(emoji_lbl, 0, Qt.AlignTop)
        else:
            emoji_lbl.setStyleSheet("font-size: 20px;")
            emoji_lbl.setFixedSize(30, 30)
            layout.addWidget(emoji_lbl, 0, Qt.AlignVCenter)

        title_layout = QVBoxLayout()
        title_layout.setSpacing(2 if self.compact_mode else 4)
        
        title_line = QHBoxLayout()
        if pinned:
            pin_lbl = QLabel("📌")
            title_line.addWidget(pin_lbl)
        
        title = QLabel(w_name)
        title.setObjectName("CardTitle")
        # Ensure title stretches and doesn't get cut off weirdly
        title.setWordWrap(True)
        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        title.setAttribute(Qt.WA_TransparentForMouseEvents)
        title_line.addWidget(title)
        title_line.addStretch()
        
        title_layout.addLayout(title_line)

        if not self.compact_mode:
            desc_text = w_data.get("description", "")
            if desc_text:
                desc = QLabel(desc_text)
                desc.setStyleSheet(f"color: {'#6B7280' if self.is_light else '#888888'}; font-size: 13px;")
                desc.setWordWrap(True)
                desc.setAlignment(Qt.AlignLeft | Qt.AlignTop)
                desc.setAttribute(Qt.WA_TransparentForMouseEvents)
                title_layout.addWidget(desc)
                
            last_run = w_data.get("last_run")
            if last_run:
                try:
                    from datetime import datetime
                    lr_dt = datetime.fromisoformat(last_run)
                    delta = (datetime.now() - lr_dt).days
                    if delta == 0:
                        lr_str = "🕐 Last run: Today"
                    elif delta == 1:
                        lr_str = "🕐 Last run: Yesterday"
                    else:
                        lr_str = f"🕐 Last run: {delta} days ago"
                    lr_lbl = QLabel(lr_str)
                    lr_lbl.setObjectName("CardSubtext")
                    lr_lbl.setAttribute(Qt.WA_TransparentForMouseEvents)
                    title_layout.addWidget(lr_lbl)
                except ValueError:
                    pass
            title_layout.addStretch()
            
        layout.addLayout(title_layout, 1)

        right_section = QHBoxLayout()
        right_section.setSpacing(6)
        
        apps = w_data.get("apps", [])
        urls = w_data.get("urls", [])
        total_items = len(apps) + len(urls)
        
        missing = any(not __import__("os").path.exists(app) for app in apps)
        if missing:
            warning_lbl = QLabel("!")
            warning_lbl.setFixedSize(20, 20)
            warning_lbl.setStyleSheet("background-color: #F59E0B; color: white; border-radius: 10px; font-weight: bold; font-size: 14px;")
            warning_lbl.setAlignment(Qt.AlignCenter)
            warning_lbl.setToolTip("One or more app paths are missing.")
            right_section.addWidget(warning_lbl)
            
        pill = QLabel(f"{total_items} items")
        pill_bg = "#E5E7EB" if self.is_light else "#404040"
        pill_fg = "#374151" if self.is_light else "#D1D5DB"
        pill.setStyleSheet(f"background-color: {pill_bg}; color: {pill_fg}; border-radius: 10px; padding: 2px 8px; font-size: 11px; font-weight: bold;")
        pill.setFixedHeight(20)
        right_section.addWidget(pill)
        
        self.menu_btn = QPushButton("⋮")
        self.menu_btn.setObjectName("MenuButton")
        self.menu_btn.setFixedSize(24, 24)
        self.menu_btn.setCursor(Qt.PointingHandCursor)
        right_section.addWidget(self.menu_btn)
        
        if self.compact_mode:
            layout.addLayout(right_section)
        else:
            right_v = QVBoxLayout()
            right_v.addLayout(right_section)
            right_v.addStretch()
            layout.addLayout(right_v)

    def enterEvent(self, event):
        self.anim.stop()
        self.anim.setStartValue(self._bg_color)
        self.anim.setEndValue(self.hover_color)
        self.anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.anim.stop()
        self.anim.setStartValue(self._bg_color)
        self.anim.setEndValue(self.base_color)
        self.anim.start()
        super().leaveEvent(event)

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
        if self._border_color != 'transparent' and self._border_color != 'Default':
            self.setStyleSheet(f"QFrame#WorkflowCard {{ background-color: {self._bg_color.name()}; border-radius: 12px; border: 1px solid {'#E5E7EB' if self.is_light else '#333333'}; border-bottom: 3px solid {self._border_color}; }}")
        else:
            self.setStyleSheet(f"QFrame#WorkflowCard {{ background-color: {self._bg_color.name()}; border-radius: 12px; border: 1px solid {'#E5E7EB' if self.is_light else '#333333'}; }}")

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
        
        # Load logo from embedded base64
        import base64 as _b64
        _logo_data = _b64.b64decode("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")
        _logo_pixmap = QPixmap()
        _logo_pixmap.loadFromData(_logo_data)
        self.app_icon = QIcon(_logo_pixmap)
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
        self.setMinimumSize(600, 450)
        self.check_whats_new()


    def check_whats_new(self):
        last_version = self.settings.get("last_seen_version")
        if last_version != VERSION:
            self.settings["last_seen_version"] = VERSION
            self.save_settings()
            dlg = WhatsNewDialog(self)
            dlg.exec()

    def toggle_compact_mode(self):
        current = self.settings.get("compact_mode", False)
        self.settings["compact_mode"] = not current
        self.toggle_mode_btn.setChecked(self.settings["compact_mode"])
        self.save_settings()
        self.toggle_mode_btn.setText("☰" if not self.settings["compact_mode"] else "▦")
        self.refresh_grid(self._last_col_count)

    def toggle_pin(self, name):
        if name in self.workflows:
             is_pinned = self.workflows[name].get("pinned", False)
             self.workflows[name]["pinned"] = not is_pinned
             self.save_workflows()
             self.refresh_grid(self._last_col_count)
             self.update_tray_menu()

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
        
        icon_lbl = QLabel()
        icon_lbl.setPixmap(self.app_icon.pixmap(28, 28))
        top_layout.addWidget(icon_lbl)
        
        title = QLabel("Nexus")
        title.setObjectName("Title")
        top_layout.addWidget(title)
        top_layout.addStretch()
        
        self.toggle_mode_btn = QPushButton("☰" if not self.settings.get("compact_mode", False) else "▦")
        self.toggle_mode_btn.setObjectName("MenuButton")
        self.toggle_mode_btn.setFixedSize(30, 30)
        self.toggle_mode_btn.setCursor(Qt.PointingHandCursor)
        self.toggle_mode_btn.setCheckable(True)
        self.toggle_mode_btn.setChecked(self.settings.get("compact_mode", False))
        self.toggle_mode_btn.clicked.connect(self.toggle_compact_mode)
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Search workflows...")
        self.search_bar.setFixedWidth(250)
        self.search_bar.textChanged.connect(self.on_search)
        top_layout.addWidget(self.search_bar)
        top_layout.addSpacing(10)
        top_layout.addWidget(self.toggle_mode_btn)
        top_layout.addSpacing(10)
        
        self.settings_btn = QPushButton("⚙")
        self.settings_btn.setObjectName("MenuButton")
        self.settings_btn.setFixedSize(30, 30)
        self.settings_btn.setCursor(Qt.PointingHandCursor)
        self.settings_btn.clicked.connect(self.open_settings)
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
        
        for i in range(self.grid_layout.columnCount()):
            self.grid_layout.setColumnStretch(i, 0)
        for i in range(col_count):
            self.grid_layout.setColumnStretch(i, 1)

        row, col = 0, 0
        keys_in_order = list(self.workflows.keys())
        pinned_keys = [k for k in keys_in_order if self.workflows[k].get("pinned", False)]
        unpinned_keys = [k for k in keys_in_order if not self.workflows[k].get("pinned", False)]
        
        for w_name in pinned_keys + unpinned_keys:
            w_data = self.workflows[w_name]
            if self.search_text and self.search_text not in w_name.lower() and self.search_text not in w_data.get("description", "").lower():
                continue
            
            card = self.create_workflow_card(w_name, w_data)
            self.grid_layout.addWidget(card, row, col)
            col += 1
            if col >= col_count:
                col = 0
                row += 1
                
        # Empty State
        if hasattr(self, 'empty_state_widget') and self.empty_state_widget:
            self.empty_state_widget.deleteLater()
            self.empty_state_widget = None
            
        if not self.workflows:
            self.empty_state_widget = QWidget()
            el = QVBoxLayout(self.empty_state_widget)
            el.setAlignment(Qt.AlignCenter)
            el.addSpacing(60)
            
            icon_l = QLabel()
            icon_l.setPixmap(self.app_icon.pixmap(64, 64))
            icon_l.setAlignment(Qt.AlignCenter)
            el.addWidget(icon_l)
            
            bold_l = QLabel("No workflows yet")
            bold_l.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 10px;")
            bold_l.setAlignment(Qt.AlignCenter)
            el.addWidget(bold_l)
            
            sub_l = QLabel("Create your first workflow to get started")
            sub_l.setStyleSheet("color: #888888; font-size: 14px; margin-bottom: 20px;")
            sub_l.setAlignment(Qt.AlignCenter)
            el.addWidget(sub_l)
            
            add_btn = QPushButton("+ Add Workflow")
            add_btn.setObjectName("AccentButton")
            add_btn.setFixedSize(200, 40)
            add_btn.setCursor(Qt.PointingHandCursor)
            add_btn.clicked.connect(self.create_workflow)
            
            bl = QHBoxLayout()
            bl.addStretch()
            bl.addWidget(add_btn)
            bl.addStretch()
            el.addLayout(bl)
            
            self.scroll_layout.insertWidget(0, self.empty_state_widget)
            
        while self.add_btn_layout.count():
            item = self.add_btn_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        if self.workflows and not self.search_text:
            add_card = self.create_add_card()
            self.add_btn_layout.addWidget(add_card)

    def create_workflow_card(self, w_name, w_data):
        compact = self.settings.get("compact_mode", False)
        is_light = self.settings.get("theme", "Dark") == "Light" # Simplification for active theme
        card = WorkflowCard(w_name, w_data, compact, is_light)
        card.clicked.connect(self.run_workflow)
        card.reordered.connect(self.reorder_workflows)
        
        menu = QMenu(card.menu_btn)
        pin_lbl = "📌 Unpin from top" if w_data.get("pinned", False) else "📌 Pin to top"
        pin_action = menu.addAction(pin_lbl)
        pin_action.triggered.connect(lambda checked=False, name=w_name: self.toggle_pin(name))
        menu.addSeparator()
        
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
            name, desc, color, emoji, apps, urls = dlg.get_data()
            if not name: return
            if name in self.workflows:
                QMessageBox.warning(self, "Error", "Workflow already exists!")
                return
            self.workflows[name] = {"description": desc, "color": color, "emoji": emoji, "apps": apps, "urls": urls, "pinned": False}
            self.save_workflows()
            self.refresh_grid(self._last_col_count)
            self.update_tray_menu()
            self.statusBar.showMessage(f"✅ Workflow '{name}' created", 5000)

    def edit_workflow(self, name):
        data = self.workflows[name]
        dlg = WorkflowDialog(self, name, data.get("description", ""), data.get("color", "Default"), data.get("emoji", "🚀"), data.get("apps", []), data.get("urls", []))
        if dlg.exec() == QDialog.Accepted:
            new_name, desc, color, emoji, apps, urls = dlg.get_data()
            if not new_name: return
            if new_name != name and new_name in self.workflows:
                QMessageBox.warning(self, "Error", "Name already exists!")
                return
            if new_name != name:
                self.workflows.pop(name)
            self.workflows[new_name] = {"description": desc, "color": color, "emoji": emoji, "apps": apps, "urls": urls, "pinned": data.get("pinned", False), "last_run": data.get("last_run")}
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
        card_width = 220
        spacing = 24
        margins = 120
        available_width = self.width() - margins
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


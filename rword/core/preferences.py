"""Preferencias de usuario y hojas de estilo de la interfaz."""

from __future__ import annotations

from PySide6.QtCore import QSettings
from PySide6.QtGui import QColor, QPalette

DARK_THEME_KEY = "ui/dark_theme"
LANGUAGE_KEY = "ui/language"
DEFAULT_ZOOM_KEY = "ui/default_zoom"
AUTOSAVE_KEY = "ui/autosave_seconds"


class UserPreferences:
    """Lee y guarda las preferencias del usuario."""

    def __init__(self, settings: QSettings) -> None:
        self._settings = settings

    @property
    def dark_theme(self) -> bool:
        return bool(self._settings.value(DARK_THEME_KEY, False))

    @dark_theme.setter
    def dark_theme(self, value: bool) -> None:
        self._settings.setValue(DARK_THEME_KEY, value)

    @property
    def language(self) -> str:
        return self._settings.value(LANGUAGE_KEY, "es")

    @language.setter
    def language(self, value: str) -> None:
        self._settings.setValue(LANGUAGE_KEY, value)

    @property
    def default_zoom(self) -> int:
        return int(self._settings.value(DEFAULT_ZOOM_KEY, 100))

    @default_zoom.setter
    def default_zoom(self, value: int) -> None:
        self._settings.setValue(DEFAULT_ZOOM_KEY, value)

    @property
    def autosave_seconds(self) -> int:
        return int(self._settings.value(AUTOSAVE_KEY, 0))

    @autosave_seconds.setter
    def autosave_seconds(self, value: int) -> None:
        self._settings.setValue(AUTOSAVE_KEY, value)

    @property
    def username(self) -> str:
        return self._settings.value("collab/username", "Usuario")

    @username.setter
    def username(self, value: str) -> None:
        self._settings.setValue("collab/username", value)


def _light_palette() -> QPalette:
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor("#f5f6f8"))
    palette.setColor(QPalette.ColorRole.WindowText, QColor("#1f2937"))
    palette.setColor(QPalette.ColorRole.Base, QColor("#ffffff"))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#f8fafc"))
    palette.setColor(QPalette.ColorRole.Text, QColor("#1f2937"))
    palette.setColor(QPalette.ColorRole.Button, QColor("#ffffff"))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor("#1f2937"))
    palette.setColor(QPalette.ColorRole.Highlight, QColor("#2563eb"))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#1f2937"))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#f9fafb"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor("#9ca3af"))
    return palette


def _dark_palette() -> QPalette:
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor("#232833"))
    palette.setColor(QPalette.ColorRole.WindowText, QColor("#e5e7eb"))
    palette.setColor(QPalette.ColorRole.Base, QColor("#1e232e"))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#2a3040"))
    palette.setColor(QPalette.ColorRole.Text, QColor("#e5e7eb"))
    palette.setColor(QPalette.ColorRole.Button, QColor("#2a3040"))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor("#e5e7eb"))
    palette.setColor(QPalette.ColorRole.Highlight, QColor("#3b82f6"))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#1f2937"))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#e5e7eb"))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor("#8b93a3"))
    return palette


def apply_ui_theme(app, dark: bool = False) -> None:
    """Aplica el estilo, la paleta y la hoja de estilos coherentes a la app."""
    app.setStyle("Fusion")
    app.setPalette(_dark_palette() if dark else _light_palette())
    app.setStyleSheet(DARK_STYLESHEET if dark else LIGHT_STYLESHEET)


LIGHT_STYLESHEET = """
QMainWindow, QDialog, QMessageBox, QInputDialog, QFrame#panel {
    background-color: #f5f6f8;
}
QWidget { color: #1f2937; }
QWidget:disabled { color: #9ca3af; }

QMenuBar {
    background-color: #ffffff;
    border-bottom: 1px solid #e5e7eb;
}
QMenuBar::item {
    background: transparent;
    padding: 6px 10px;
    border-radius: 4px;
}
QMenuBar::item:selected { background: #eef2ff; color: #1d4ed8; }
QMenuBar::item:pressed { background: #e0e7ff; }

QMenu {
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 6px;
    padding: 4px;
}
QMenu::item {
    padding: 6px 24px 6px 12px;
    border-radius: 4px;
}
QMenu::item:selected { background: #eef2ff; color: #1d4ed8; }
QMenu::item:disabled { color: #9ca3af; }
QMenu::separator { height: 1px; background: #e5e7eb; margin: 4px 8px; }

QToolBar {
    background-color: #f5f6f8;
    border: none;
    border-bottom: 1px solid #e5e7eb;
    spacing: 4px;
}
QToolBar::separator { background: #d1d5db; width: 1px; margin: 4px; }

QStatusBar {
    background-color: #ffffff;
    border-top: 1px solid #e5e7eb;
    color: #6b7280;
}
QStatusBar::item { border: none; }
QLabel { background: transparent; }

QWidget#ribbonBar {
    background-color: #ffffff;
    border-bottom: 1px solid #e5e7eb;
}

QToolButton {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 5px;
    padding: 3px;
    font-size: 9px;
}
QToolButton:hover {
    background-color: #eef2ff;
    border-color: #bfdbfe;
}
QToolButton:pressed { background-color: #e0e7ff; }
QToolButton:checked {
    background-color: #dbeafe;
    border-color: #93b8fd;
    color: #1d4ed8;
}
QToolButton:disabled {
    color: #9ca3af;
    background-color: #f3f4f6;
    border-color: #e5e7eb;
}

QToolButton#chevron {
    background: transparent;
    border: none;
    padding: 0;
}
QToolButton#chevron:hover { background: #eef2ff; border: none; }
QToolButton#chevron:pressed { background: #e0e7ff; border: none; }

QWidget#ribbonBar QScrollArea { border: none; background: transparent; }
QFrame#panel { background-color: #ffffff; border: 1px solid #e5e7eb; }

QPushButton {
    background-color: #ffffff;
    border: 1px solid #d1d5db;
    border-radius: 5px;
    padding: 5px 12px;
}
QPushButton:hover { background-color: #f3f4f6; border-color: #9ca3af; }
QPushButton:pressed { background-color: #e5e7eb; }
QPushButton:default {
    background-color: #2563eb;
    color: #ffffff;
    border-color: #2563eb;
}
QPushButton:default:hover { background-color: #1d4ed8; }
QPushButton:disabled { color: #9ca3af; background-color: #f3f4f6; }

QLineEdit, QSpinBox, QDoubleSpinBox, QFontComboBox, QComboBox {
    background-color: #ffffff;
    border: 1px solid #d1d5db;
    border-radius: 5px;
    padding: 3px 6px;
    selection-background-color: #bfdbfe;
    selection-color: #1f2937;
}
QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus,
QComboBox:focus { border-color: #2563eb; }
QLineEdit:disabled, QSpinBox:disabled, QComboBox:disabled {
    color: #9ca3af; background-color: #f3f4f6;
}

QComboBox:hover { border-color: #9ca3af; }
QComboBox::drop-down { border: none; width: 22px; }
QComboBox QAbstractItemView {
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 4px;
    selection-background-color: #eef2ff;
    selection-color: #1f2937;
}

QTextEdit, QPlainTextEdit {
    selection-background-color: #bfdbfe;
    selection-color: #1f2937;
}

QListWidget, QTreeWidget, QTableView, QTextBrowser {
    background-color: #ffffff;
    border: 1px solid #d1d5db;
    border-radius: 5px;
    padding: 2px;
    selection-background-color: #eef2ff;
    selection-color: #1f2937;
}
QListWidget:focus, QTreeWidget:focus, QTableView:focus {
    border-color: #2563eb;
}

QHeaderView::section {
    background-color: #f3f4f6;
    border: none;
    border-right: 1px solid #e5e7eb;
    border-bottom: 1px solid #e5e7eb;
    padding: 4px 8px;
    font-weight: 600;
}

QGroupBox {
    border: 1px solid #e5e7eb;
    border-radius: 6px;
    margin-top: 10px;
    padding-top: 8px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 4px;
    color: #374151;
}

QCheckBox, QRadioButton { spacing: 6px; }
QCheckBox::indicator, QRadioButton::indicator { width: 16px; height: 16px; }

QSplitter::handle { background-color: #e5e7eb; }
QSplitter::handle:horizontal { width: 3px; }
QSplitter::handle:vertical { height: 3px; }

QScrollBar:vertical { background: transparent; width: 12px; margin: 0; }
QScrollBar::handle:vertical {
    background: #d1d5db; border-radius: 6px; min-height: 24px; margin: 2px;
}
QScrollBar::handle:vertical:hover { background: #9ca3af; }
QScrollBar:horizontal { background: transparent; height: 12px; }
QScrollBar::handle:horizontal {
    background: #d1d5db; border-radius: 6px; min-width: 24px; margin: 2px;
}
QScrollBar::handle:horizontal:hover { background: #9ca3af; }
QScrollBar::add-line, QScrollBar::sub-line { width: 0; height: 0; }
QScrollBar::add-page, QScrollBar::sub-page { background: transparent; }

QProgressBar {
    background-color: #e5e7eb;
    border: none;
    border-radius: 4px;
    text-align: center;
    color: #374151;
}
QProgressBar::chunk { background-color: #2563eb; border-radius: 4px; }

QToolTip {
    background-color: #1f2937;
    color: #f9fafb;
    border: none;
    padding: 4px 8px;
    border-radius: 4px;
}

QTabBar::tab {
    background: transparent;
    color: #4b5563;
    padding: 6px 16px;
    font-size: 10px;
    border: none;
    border-bottom: 2px solid transparent;
}
QTabBar::tab:hover { color: #111827; background: #f1f5f9; }
QTabBar::tab:selected {
    color: #1d4ed8;
    font-weight: bold;
    border-bottom: 2px solid #2563eb;
}
QTabBar#ribbonTabs::tab { padding: 6px 18px; }
"""


DARK_STYLESHEET = """
QMainWindow, QDialog, QMessageBox, QInputDialog, QFrame#panel {
    background-color: #232833;
}
QWidget { color: #e5e7eb; }
QWidget:disabled { color: #6b7280; }

QMenuBar {
    background-color: #1c212b;
    border-bottom: 1px solid #343b4b;
}
QMenuBar::item {
    background: transparent;
    padding: 6px 10px;
    border-radius: 4px;
}
QMenuBar::item:selected { background: #2b3550; color: #93c5fd; }
QMenuBar::item:pressed { background: #33415f; }

QMenu {
    background-color: #2a3040;
    border: 1px solid #3a4152;
    border-radius: 6px;
    padding: 4px;
}
QMenu::item {
    padding: 6px 24px 6px 12px;
    border-radius: 4px;
}
QMenu::item:selected { background: #2b3550; color: #93c5fd; }
QMenu::item:disabled { color: #6b7280; }
QMenu::separator { height: 1px; background: #3a4152; margin: 4px 8px; }

QToolBar {
    background-color: #232833;
    border: none;
    border-bottom: 1px solid #343b4b;
    spacing: 4px;
}
QToolBar::separator { background: #3a4152; width: 1px; margin: 4px; }

QStatusBar {
    background-color: #1c212b;
    border-top: 1px solid #343b4b;
    color: #9ca3af;
}
QStatusBar::item { border: none; }
QLabel { background: transparent; }

QWidget#ribbonBar {
    background-color: #232833;
    border-bottom: 1px solid #343b4b;
}

QToolButton {
    background-color: #2a3040;
    border: 1px solid #3a4152;
    border-radius: 5px;
    padding: 3px;
    font-size: 9px;
}
QToolButton:hover {
    background-color: #33415f;
    border-color: #4b5a76;
}
QToolButton:pressed { background-color: #3a4152; }
QToolButton:checked {
    background-color: #2b3550;
    border-color: #3b82f6;
    color: #93c5fd;
}
QToolButton:disabled {
    color: #6b7280;
    background-color: #1c212b;
    border-color: #343b4b;
}

QToolButton#chevron {
    background: transparent;
    border: none;
    padding: 0;
}
QToolButton#chevron:hover { background: #33415f; border: none; }
QToolButton#chevron:pressed { background: #3a4152; border: none; }

QWidget#ribbonBar QScrollArea { border: none; background: transparent; }
QFrame#panel { background-color: #2a3040; border: 1px solid #3a4152; }

QPushButton {
    background-color: #2a3040;
    border: 1px solid #3a4152;
    border-radius: 5px;
    padding: 5px 12px;
}
QPushButton:hover { background-color: #343b4b; border-color: #4b5563; }
QPushButton:pressed { background-color: #3a4152; }
QPushButton:default {
    background-color: #2563eb;
    color: #ffffff;
    border-color: #2563eb;
}
QPushButton:default:hover { background-color: #1d4ed8; }
QPushButton:disabled { color: #6b7280; background-color: #1e232e; }

QLineEdit, QSpinBox, QDoubleSpinBox, QFontComboBox, QComboBox {
    background-color: #1e232e;
    border: 1px solid #3a4152;
    border-radius: 5px;
    padding: 3px 6px;
    selection-background-color: #2b3550;
    selection-color: #e5e7eb;
}
QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus,
QComboBox:focus { border-color: #3b82f6; }
QLineEdit:disabled, QSpinBox:disabled, QComboBox:disabled {
    color: #6b7280; background-color: #1c212b;
}

QComboBox:hover { border-color: #4b5563; }
QComboBox::drop-down { border: none; width: 22px; }
QComboBox QAbstractItemView {
    background-color: #2a3040;
    border: 1px solid #3a4152;
    border-radius: 4px;
    selection-background-color: #2b3550;
    selection-color: #e5e7eb;
}

QTextEdit, QPlainTextEdit {
    selection-background-color: #2b3550;
    selection-color: #e5e7eb;
}

QListWidget, QTreeWidget, QTableView, QTextBrowser {
    background-color: #1e232e;
    border: 1px solid #3a4152;
    border-radius: 5px;
    padding: 2px;
    selection-background-color: #2b3550;
    selection-color: #e5e7eb;
}
QListWidget:focus, QTreeWidget:focus, QTableView:focus {
    border-color: #3b82f6;
}

QHeaderView::section {
    background-color: #2a3040;
    border: none;
    border-right: 1px solid #3a4152;
    border-bottom: 1px solid #3a4152;
    padding: 4px 8px;
    font-weight: 600;
}

QGroupBox {
    border: 1px solid #3a4152;
    border-radius: 6px;
    margin-top: 10px;
    padding-top: 8px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 4px;
    color: #9ca3af;
}

QCheckBox, QRadioButton { spacing: 6px; }
QCheckBox::indicator, QRadioButton::indicator { width: 16px; height: 16px; }

QSplitter::handle { background-color: #343b4b; }
QSplitter::handle:horizontal { width: 3px; }
QSplitter::handle:vertical { height: 3px; }

QScrollBar:vertical { background: transparent; width: 12px; margin: 0; }
QScrollBar::handle:vertical {
    background: #3a4152; border-radius: 6px; min-height: 24px; margin: 2px;
}
QScrollBar::handle:vertical:hover { background: #4b5563; }
QScrollBar:horizontal { background: transparent; height: 12px; }
QScrollBar::handle:horizontal {
    background: #3a4152; border-radius: 6px; min-width: 24px; margin: 2px;
}
QScrollBar::handle:horizontal:hover { background: #4b5563; }
QScrollBar::add-line, QScrollBar::sub-line { width: 0; height: 0; }
QScrollBar::add-page, QScrollBar::sub-page { background: transparent; }

QProgressBar {
    background-color: #3a4152;
    border: none;
    border-radius: 4px;
    text-align: center;
    color: #e5e7eb;
}
QProgressBar::chunk { background-color: #2563eb; border-radius: 4px; }

QToolTip {
    background-color: #1f2937;
    color: #e5e7eb;
    border: 1px solid #3a4152;
    padding: 4px 8px;
    border-radius: 4px;
}

QTabBar::tab {
    background: transparent;
    color: #9ca3af;
    padding: 6px 16px;
    font-size: 10px;
    border: none;
    border-bottom: 2px solid transparent;
}
QTabBar::tab:hover { color: #e5e7eb; background: #2a3040; }
QTabBar::tab:selected {
    color: #93c5fd;
    font-weight: bold;
    border-bottom: 2px solid #3b82f6;
}
QTabBar#ribbonTabs::tab { padding: 6px 18px; }
"""

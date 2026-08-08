"""Preferencias de usuario."""

from __future__ import annotations

from PySide6.QtCore import QSettings

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


DARK_STYLESHEET = """
QMainWindow, QDialog, QMessageBox, QWidget { background-color: #2b2b2b; color: #dddddd; }
QMenuBar { background-color: #333333; }
QMenuBar::item:selected { background-color: #4a4a4a; }
QMenu { background-color: #333333; color: #dddddd; }
QMenu::item:selected { background-color: #4a4a4a; }
QToolBar { background-color: #333333; border-bottom: 1px solid #444444; }
QStatusBar { background-color: #333333; color: #dddddd; }
QLineEdit, QPlainTextEdit, QTextEdit, QSpinBox, QComboBox, QListWidget {
    background-color: #3a3a3a; color: #dddddd; border: 1px solid #555555;
}
QPushButton { background-color: #4a4a4a; color: #dddddd; border: 1px solid #666666; }
QPushButton:hover { background-color: #5a5a5a; }
"""

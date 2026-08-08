"""Diálogo de preferencias de usuario."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QSpinBox,
)

from rword.core.preferences import UserPreferences


class PreferencesDialog(QDialog):
    """Configura las preferencias generales de la aplicación."""

    def __init__(self, preferences: UserPreferences, parent=None) -> None:
        super().__init__(parent)
        self._preferences = preferences
        self.setWindowTitle("Preferencias")
        self.setMinimumWidth(360)
        form = QFormLayout(self)

        self._theme_combo = QComboBox(self)
        self._theme_combo.addItem("Claro", "light")
        self._theme_combo.addItem("Oscuro", "dark")
        self._theme_combo.setCurrentIndex(1 if preferences.dark_theme else 0)
        form.addRow("Tema visual:", self._theme_combo)

        self._language_combo = QComboBox(self)
        self._language_combo.addItem("Español", "es")
        self._language_combo.addItem("English", "en")
        index = self._language_combo.findData(preferences.language)
        self._language_combo.setCurrentIndex(max(0, index))
        form.addRow("Idioma de interfaz:", self._language_combo)

        self._username_input = QLineEdit(self)
        self._username_input.setText(preferences.username)
        form.addRow("Nombre de usuario:", self._username_input)

        self._zoom_spin = QSpinBox(self)
        self._zoom_spin.setRange(50, 300)
        self._zoom_spin.setValue(preferences.default_zoom)
        self._zoom_spin.setSuffix(" %")
        form.addRow("Zoom por defecto:", self._zoom_spin)

        self._autosave_spin = QSpinBox(self)
        self._autosave_spin.setRange(0, 600)
        self._autosave_spin.setValue(preferences.autosave_seconds)
        self._autosave_spin.setSuffix(" s (0 = desactivado)")
        form.addRow("Autoguardado:", self._autosave_spin)

        self._track_authors_check = QCheckBox("Registrar autor en cambios y comentarios", self)
        self._track_authors_check.setChecked(
            bool(self._preferences._settings.value("collab/track_authors", True))
        )
        form.addRow("", self._track_authors_check)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        buttons.accepted.connect(self._apply)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)

    def _apply(self) -> None:
        self._preferences.dark_theme = (
            self._theme_combo.currentData() == "dark"
        )
        self._preferences.language = self._language_combo.currentData()
        self._preferences.username = self._username_input.text().strip() or "Usuario"
        self._preferences.default_zoom = self._zoom_spin.value()
        self._preferences.autosave_seconds = self._autosave_spin.value()
        self._preferences._settings.setValue(
            "collab/track_authors", self._track_authors_check.isChecked()
        )
        self.accept()

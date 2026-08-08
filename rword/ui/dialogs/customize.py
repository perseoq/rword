"""Diálogo de personalización de la barra de herramientas."""

from __future__ import annotations

from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QListWidget,
    QPushButton,
    QVBoxLayout,
)

TOOLBAR_ACTIONS_KEY = "custom/toolbar_actions"


class ToolbarCustomizeDialog(QDialog):
    """Permite mostrar u ocultar acciones en la barra principal."""

    def __init__(self, actions: dict[str, QAction], settings, main_toolbar, parent=None) -> None:
        super().__init__(parent)
        self._actions = actions
        self._settings = settings
        self._toolbar = main_toolbar
        self.setWindowTitle("Personalizar barra de herramientas")
        self.setMinimumWidth(340)
        layout = QVBoxLayout(self)

        self._checks: dict[str, QCheckBox] = {}
        enabled = self._load_enabled()
        for key, action in actions.items():
            check = QCheckBox(action.text(), self)
            check.setChecked(key in enabled)
            self._checks[key] = check
            layout.addWidget(check)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        buttons.accepted.connect(self._apply)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _load_enabled(self) -> set[str]:
        stored = self._settings.value(TOOLBAR_ACTIONS_KEY, [])
        return set(stored) if stored else set(self._actions)

    def _apply(self) -> None:
        enabled = {key for key, check in self._checks.items() if check.isChecked()}
        self._settings.setValue(TOOLBAR_ACTIONS_KEY, sorted(enabled))
        self.accept()


class ShortcutsDialog(QDialog):
    """Permite consultar y modificar los atajos de teclado."""

    def __init__(self, actions: dict[str, QAction], settings, parent=None) -> None:
        super().__init__(parent)
        self._actions = actions
        self._settings = settings
        self.setWindowTitle("Atajos de teclado")
        self.setMinimumSize(460, 400)
        layout = QVBoxLayout(self)

        self._list = QListWidget(self)
        self._list.currentItemChanged.connect(self._load_shortcut)
        self._refresh_list()
        layout.addWidget(self._list)

        form = QFormLayout()
        self._shortcut_input = QLineEdit(self)
        self._shortcut_input.setPlaceholderText("p. ej. Ctrl+Shift+K")
        form.addRow("Atajo:", self._shortcut_input)

        self._apply_button = QPushButton("Aplicar atajo", self)
        self._apply_button.clicked.connect(self._apply)
        self._clear_button = QPushButton("Quitar atajo", self)
        self._clear_button.clicked.connect(self._clear)
        form.addRow(self._apply_button, self._clear_button)
        layout.addLayout(form)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close, self)
        buttons.rejected.connect(self.accept)
        layout.addWidget(buttons)

    def _refresh_list(self) -> None:
        self._list.clear()
        for key, action in self._actions.items():
            stored = self._settings.value(f"shortcuts/{key}", "")
            shortcut = stored or action.shortcut().toString()
            self._list.addItem(f"{action.text()}    ({shortcut})")

    def _current_key(self) -> str | None:
        row = self._list.currentRow()
        keys = list(self._actions)
        if 0 <= row < len(keys):
            return keys[row]
        return None

    def _load_shortcut(self) -> None:
        key = self._current_key()
        if key:
            stored = self._settings.value(f"shortcuts/{key}", "")
            self._shortcut_input.setText(stored)

    def _apply(self) -> None:
        key = self._current_key()
        if not key:
            return
        shortcut = self._shortcut_input.text().strip()
        self._settings.setValue(f"shortcuts/{key}", shortcut)
        if shortcut:
            self._actions[key].setShortcut(QKeySequence(shortcut))
        self._refresh_list()

    def _clear(self) -> None:
        key = self._current_key()
        if not key:
            return
        self._settings.remove(f"shortcuts/{key}")
        self._shortcut_input.clear()
        self._refresh_list()

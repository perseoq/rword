"""Diálogo para configurar la clave de API de DeepSeek."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QMessageBox,
)

from rword.core.ai.config import ApiKeyManager


class ApiKeyDialog(QDialog):
    """Permite introducir, cambiar o eliminar la clave de API."""

    def __init__(self, manager: ApiKeyManager, parent=None) -> None:
        super().__init__(parent)
        self._manager = manager
        self.setWindowTitle("Clave de API de DeepSeek")
        self.setMinimumWidth(400)
        form = QFormLayout(self)

        self._key_input = QLineEdit(self)
        self._key_input.setPlaceholderText("sk-...")
        self._key_input.setEchoMode(QLineEdit.EchoMode.Password)
        if manager.has_key():
            self._key_input.setText(manager.get())
        form.addRow("Clave de API:", self._key_input)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        buttons.accepted.connect(self._apply)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)

    def _apply(self) -> None:
        key = self._key_input.text().strip()
        if key:
            self._manager.set(key)
        else:
            self._manager.clear()
        QMessageBox.information(
            self, "Clave de API", "Clave de API guardada en los ajustes locales."
        )
        self.accept()

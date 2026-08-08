"""Diálogo para ir a una línea específica."""

from __future__ import annotations

from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QMessageBox,
)


class GoToDialog(QDialog):
    """Permite navegar a un número de línea o carácter."""

    def __init__(self, editor, parent=None) -> None:
        super().__init__(parent)
        self._editor = editor
        self.setWindowTitle("Ir a")
        self._build_ui()

    def _build_ui(self) -> None:
        form = QFormLayout(self)
        self._line_input = QLineEdit(self)
        self._line_input.setPlaceholderText("Número de línea (1...n)")
        form.addRow("Línea:", self._line_input)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        buttons.accepted.connect(self._go_to_line)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)
        self._line_input.setFocus()

    def _go_to_line(self) -> None:
        try:
            line = int(self._line_input.text())
        except ValueError:
            QMessageBox.warning(self, "Ir a", "Introduzca un número de línea válido.")
            return
        if line < 1:
            QMessageBox.warning(self, "Ir a", "La línea debe ser mayor o igual a 1.")
            return
        block = self._editor.document().findBlockByNumber(line - 1)
        if block.isValid():
            cursor = QTextCursor(block)
            self._editor.setTextCursor(cursor)
            self._editor.ensureCursorVisible()
            self.accept()
        else:
            QMessageBox.information(
                self,
                "Ir a",
                f"El documento solo tiene {self._editor.document().blockCount()} líneas.",
            )

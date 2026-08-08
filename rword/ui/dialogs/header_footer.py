"""Diálogo para configurar encabezado y pie de página."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
)

from rword.core.headers import FIELDS


class HeaderFooterDialog(QDialog):
    """Configura el texto del encabezado o del pie con campos automáticos."""

    def __init__(self, title: str, current: str = "", parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumWidth(400)
        form = QFormLayout(self)

        hint = "Campos: " + ", ".join(f"{v}" for v in FIELDS.values())
        self._template_input = QLineEdit(self)
        self._template_input.setPlaceholderText("p. ej. Mi empresa — {PAGE}")
        self._template_input.setText(current)
        form.addRow("Texto:", self._template_input)
        form.addRow("Ayuda:", _hint_label(hint))

        self._numbering_combo = QComboBox(self)
        self._numbering_combo.addItem("1, 2, 3...", "decimal")
        self._numbering_combo.addItem("I, II, III...", "roman")
        self._numbering_combo.addItem("a, b, c...", "alpha")
        form.addRow("Numeración:", self._numbering_combo)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)

    def template(self) -> str:
        return self._template_input.text()

    def numbering_format(self) -> str:
        return self._numbering_combo.currentData()


def _hint_label(text: str):
    from PySide6.QtWidgets import QLabel

    label = QLabel(text)
    label.setStyleSheet("color: #777;")
    return label

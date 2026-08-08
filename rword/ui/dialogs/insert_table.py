"""Diálogo para insertar una tabla."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QSpinBox,
)

from rword.core.tables import TABLE_STYLES


class InsertTableDialog(QDialog):
    """Configura filas, columnas y estilo de la nueva tabla."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Insertar tabla")
        self.setMinimumWidth(300)
        self._build_ui()

    def _build_ui(self) -> None:
        form = QFormLayout(self)

        self._rows_spin = QSpinBox(self)
        self._rows_spin.setRange(1, 100)
        self._rows_spin.setValue(3)
        form.addRow("Filas:", self._rows_spin)

        self._columns_spin = QSpinBox(self)
        self._columns_spin.setRange(1, 50)
        self._columns_spin.setValue(3)
        form.addRow("Columnas:", self._columns_spin)

        self._style_combo = QComboBox(self)
        self._style_combo.addItems(TABLE_STYLES.keys())
        form.addRow("Estilo:", self._style_combo)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)

    def rows(self) -> int:
        return self._rows_spin.value()

    def columns(self) -> int:
        return self._columns_spin.value()

    def style_name(self) -> str:
        return self._style_combo.currentText()

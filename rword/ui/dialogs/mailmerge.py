"""Diálogo de vista previa de la combinación de correspondencia."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QPlainTextEdit,
    QSpinBox,
)

from rword.core.mailmerge import merge_template


class MailMergePreviewDialog(QDialog):
    """Muestra el documento combinado con un registro concreto."""

    def __init__(self, editor, records, parent=None) -> None:
        super().__init__(parent)
        self._editor = editor
        self._records = records
        self.setWindowTitle("Vista previa de resultados")
        self.resize(520, 420)
        form = QFormLayout(self)

        self._index_spin = QSpinBox(self)
        self._index_spin.setRange(1, max(1, len(records)))
        self._index_spin.setValue(1)
        self._index_spin.valueChanged.connect(self._refresh)
        form.addRow("Registro:", self._index_spin)
        self._info_label = QLabel("", self)
        form.addRow("", self._info_label)

        self._preview = QPlainTextEdit(self)
        self._preview.setReadOnly(True)
        form.addRow(self._preview)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close, self)
        buttons.rejected.connect(self.accept)
        form.addRow(buttons)
        self._refresh()

    def _refresh(self) -> None:
        index = self._index_spin.value() - 1
        if not self._records:
            self._preview.setPlainText("(sin datos)")
            return
        record = self._records[index]
        cursor = self._editor.textCursor()
        cursor.select(cursor.SelectionType.Document)
        template = cursor.selectedText().replace("\u2029", "\n")
        self._preview.setPlainText(merge_template(template, record))
        self._info_label.setText(
            f"{index + 1} de {len(self._records)} destinatarios"
        )

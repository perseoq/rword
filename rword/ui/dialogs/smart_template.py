"""Diálogo de plantillas inteligentes."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QVBoxLayout,
)

from rword.core.assist import SMART_TEMPLATES, fill_template


class SmartTemplateDialog(QDialog):
    """Genera un documento a partir de una plantilla y sus campos."""

    def __init__(self, editor, parent=None) -> None:
        super().__init__(parent)
        self._editor = editor
        self.setWindowTitle("Plantillas inteligentes")
        self.setMinimumWidth(420)
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self._template_combo = QComboBox(self)
        self._template_combo.addItems(SMART_TEMPLATES.keys())
        self._template_combo.currentIndexChanged.connect(self._rebuild_fields)
        form.addRow("Plantilla:", self._template_combo)
        layout.addLayout(form)

        self._fields_layout = QFormLayout()
        layout.addLayout(self._fields_layout)
        self._inputs: dict[str, QLineEdit] = {}

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        buttons.accepted.connect(self._insert)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        self._rebuild_fields()

    def _rebuild_fields(self) -> None:
        while self._fields_layout.rowCount():
            self._fields_layout.removeRow(0)
        self._inputs.clear()
        template = SMART_TEMPLATES[self._template_combo.currentText()]
        for field in template["fields"]:
            line_edit = QLineEdit(self)
            line_edit.setPlaceholderText(field)
            self._inputs[field] = line_edit
            self._fields_layout.addRow(field, line_edit)

    def _insert(self) -> None:
        values = {
            field: line_edit.text() for field, line_edit in self._inputs.items()
        }
        fill_template(
            self._editor, self._template_combo.currentText(), values
        )
        self.accept()

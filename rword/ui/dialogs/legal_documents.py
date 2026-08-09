"""Diálogo para elegir un documento jurídico del catálogo de SKILL.md."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QTextEdit,
    QVBoxLayout,
)

from rword.core.legal.catalog import LegalDocument, legal_documents

ALL_MATERIAS = "Todas las materias"


class LegalDocumentDialog(QDialog):
    """Muestra la lista de documentos jurídicos para seleccionar uno."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._documents = legal_documents()
        self.setWindowTitle("Documentos jurídicos")
        self.setMinimumSize(680, 460)

        layout = QVBoxLayout(self)

        self._materia_combo = QComboBox(self)
        self._materia_combo.addItem(ALL_MATERIAS)
        for phase in sorted({document.phase for document in self._documents}):
            self._materia_combo.addItem(phase)
        self._materia_combo.currentIndexChanged.connect(self._filter)

        self._search = QLineEdit(self)
        self._search.setPlaceholderText("Buscar documento…")
        self._search.textChanged.connect(self._filter)

        top = QHBoxLayout()
        top.addWidget(QLabel("Materia:", self))
        top.addWidget(self._materia_combo, 1)
        top.addWidget(self._search, 2)
        layout.addLayout(top)

        self._list = QListWidget(self)
        self._list.currentItemChanged.connect(self._show_details)
        layout.addWidget(self._list, 3)

        self._details = QTextEdit(self)
        self._details.setReadOnly(True)
        self._details.setMinimumHeight(140)
        layout.addWidget(self._details, 2)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        buttons.button(QDialogButtonBox.StandardButton.Ok).setText("Generar")
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        if not self._documents:
            self._list.addItem("No se pudo cargar el catálogo (SKILL.md no encontrado).")
        else:
            self._filter()
        self._update_ok_state()

    def _filter(self) -> None:
        query = self._search.text().strip().casefold()
        materia = self._materia_combo.currentText()
        self._list.clear()
        for document in self._documents:
            if materia != ALL_MATERIAS and document.phase != materia:
                continue
            if query and query not in document.name.casefold():
                continue
            item = QListWidgetItem(document.name)
            item.setData(Qt.ItemDataRole.UserRole, document)
            self._list.addItem(item)

    def _show_details(self, current: QListWidgetItem | None, _previous=None) -> None:
        document = self._document_of(current)
        if document is None:
            self._details.clear()
            self._update_ok_state()
            return
        parts = [f"<b>{document.name}</b>"]
        if document.category:
            parts.append(f"<i>{document.category}</i>")
        parts.append(f"<b>Materia:</b> {document.phase}")
        if document.fundamento:
            parts.append(f"<b>Fundamento:</b> {document.fundamento}")
        if document.description:
            parts.append(f"<b>Descripción:</b> {document.description}")
        if document.requisitos:
            items = "".join(f"<li>{requisito}</li>" for requisito in document.requisitos)
            parts.append(f"<b>Requisitos:</b><ul>{items}</ul>")
        self._details.setHtml("<br>".join(parts))
        self._update_ok_state()

    def _update_ok_state(self) -> None:
        ok_button = self._ok_button()
        if ok_button is not None:
            ok_button.setEnabled(self.selected_document() is not None)

    def _ok_button(self):
        buttons = self.findChild(QDialogButtonBox)
        if buttons is None:
            return None
        return buttons.button(QDialogButtonBox.StandardButton.Ok)

    @staticmethod
    def _document_of(item: QListWidgetItem | None) -> LegalDocument | None:
        if item is None:
            return None
        document = item.data(Qt.ItemDataRole.UserRole)
        return document if isinstance(document, LegalDocument) else None

    def selected_document(self) -> LegalDocument | None:
        """Devuelve el documento seleccionado o None si no hay selección."""
        return self._document_of(self._list.currentItem())

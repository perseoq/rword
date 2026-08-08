"""Diálogos de plantillas de márgenes."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from rword.core.margin_templates import (
    MarginTemplateStore,
    apply_margins,
    current_margins,
)


class SaveMarginTemplateDialog(QDialog):
    """Guarda los márgenes actuales como plantilla con un nombre."""

    def __init__(
        self, editor, store: MarginTemplateStore, parent=None
    ) -> None:
        super().__init__(parent)
        self._editor = editor
        self._store = store
        self.setWindowTitle("Guardar márgenes como plantilla")
        self.setMinimumWidth(340)
        form = QFormLayout(self)

        margins = current_margins(editor)
        form.addRow(
            "Márgenes actuales:",
            QLabel(
                f"Izq {margins[0]:g} · Der {margins[1]:g} · "
                f"Sup {margins[2]:g} · Inf {margins[3]:g} mm"
            ),
        )
        self._name_input = QLineEdit(self)
        self._name_input.setPlaceholderText("Nombre de la plantilla")
        form.addRow("Nombre:", self._name_input)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        buttons.accepted.connect(self._accept)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)

    def _accept(self) -> None:
        name = self._name_input.text().strip()
        if not name:
            QMessageBox.warning(
                self, "Plantilla", "Introduzca un nombre para la plantilla."
            )
            return
        left, right, top, bottom = current_margins(self._editor)
        self._store.save(name, left, right, top, bottom)
        self.accept()


class MarginTemplateManagerDialog(QDialog):
    """Administra las plantillas personalizadas: aplicar, renombrar, eliminar."""

    def __init__(
        self, editor, store: MarginTemplateStore, parent=None
    ) -> None:
        super().__init__(parent)
        self._editor = editor
        self._store = store
        self.setWindowTitle("Administrar plantillas de márgenes")
        self.setMinimumWidth(380)
        layout = QVBoxLayout(self)

        self._list = QListWidget(self)
        self._refresh()
        layout.addWidget(self._list)

        buttons = QHBoxLayout()
        self._apply_button = QPushButton("Aplicar", self)
        self._apply_button.clicked.connect(self._apply)
        self._rename_button = QPushButton("Renombrar...", self)
        self._rename_button.clicked.connect(self._rename)
        self._delete_button = QPushButton("Eliminar", self)
        self._delete_button.clicked.connect(self._delete)
        buttons.addWidget(self._apply_button)
        buttons.addWidget(self._rename_button)
        buttons.addWidget(self._delete_button)
        layout.addLayout(buttons)

        close_button = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Close, self
        )
        close_button.rejected.connect(self.accept)
        layout.addWidget(close_button)

    def _refresh(self) -> None:
        self._list.clear()
        for name in sorted(self._store.names()):
            margins = self._store.get(name)
            label = (
                f"{name}  (Izq {margins[0]:g} · Der {margins[1]:g} · "
                f"Sup {margins[2]:g} · Inf {margins[3]:g} mm)"
            )
            self._list.addItem(label)

    def _selected(self) -> str | None:
        item = self._list.currentItem()
        if item is None:
            return None
        return item.text().split("  (")[0]

    def _apply(self) -> None:
        name = self._selected()
        if name is None:
            return
        margins = self._store.get(name)
        if margins is not None:
            apply_margins(self._editor, *margins)

    def _rename(self) -> None:
        name = self._selected()
        if name is None:
            return
        new_name, ok = QInputDialog.getText(
            self, "Renombrar plantilla", "Nuevo nombre:", text=name
        )
        if ok and new_name.strip() and new_name.strip() != name:
            if not self._store.rename(name, new_name.strip()):
                QMessageBox.warning(
                    self, "Plantilla", "No se pudo renombrar la plantilla."
                )
            self._refresh()

    def _delete(self) -> None:
        name = self._selected()
        if name is None:
            return
        answer = QMessageBox.question(
            self,
            "Eliminar plantilla",
            f"¿Eliminar la plantilla «{name}»?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if answer == QMessageBox.StandardButton.Yes:
            self._store.delete(name)
            self._refresh()

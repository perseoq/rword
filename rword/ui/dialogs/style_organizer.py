"""Organizador de estilos: listar, renombrar y eliminar estilos."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QInputDialog,
    QListWidget,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)


class StyleOrganizerDialog(QDialog):
    """Gestiona los estilos guardados del documento."""

    def __init__(self, manager, parent=None) -> None:
        super().__init__(parent)
        self._manager = manager
        self.setWindowTitle("Organizador de estilos")
        self.resize(340, 380)
        self._build_ui()
        self._reload()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        self._list = QListWidget(self)
        layout.addWidget(self._list)

        self._rename_button = QPushButton("Renombrar...", self)
        self._delete_button = QPushButton("Eliminar", self)
        self._rename_button.clicked.connect(self._rename)
        self._delete_button.clicked.connect(self._delete)
        layout.addWidget(self._rename_button)
        layout.addWidget(self._delete_button)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close, self)
        buttons.rejected.connect(self.accept)
        layout.addWidget(buttons)

    def _reload(self) -> None:
        self._list.clear()
        self._list.addItems(sorted(self._manager.names()))

    def _selected_name(self) -> str | None:
        item = self._list.currentItem()
        return item.text() if item else None

    def _rename(self) -> None:
        name = self._selected_name()
        if name is None:
            return
        new_name, ok = QInputDialog.getText(
            self, "Renombrar estilo", "Nuevo nombre:", text=name
        )
        if ok and new_name.strip() and new_name.strip() != name:
            if self._manager.rename(name, new_name.strip()):
                self._reload()
            else:
                QMessageBox.warning(
                    self, "Organizador", "No se pudo renombrar el estilo."
                )

    def _delete(self) -> None:
        name = self._selected_name()
        if name is None:
            return
        answer = QMessageBox.question(
            self,
            "Eliminar estilo",
            f"¿Eliminar el estilo «{name}»?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if answer == QMessageBox.StandardButton.Yes:
            self._manager.remove(name)
            self._reload()

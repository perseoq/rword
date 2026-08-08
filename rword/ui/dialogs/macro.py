"""Diálogo para administrar y editar macros."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QInputDialog,
    QListWidget,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
)

from rword.core.macros import MacroManager


class MacroDialog(QDialog):
    """Lista, crea, edita, ejecuta y elimina macros."""

    def __init__(self, manager: MacroManager, editor, parent=None) -> None:
        super().__init__(parent)
        self._manager = manager
        self._editor = editor
        self.setWindowTitle("Administrador de macros")
        self.resize(560, 420)
        self._build_ui()
        self._reload()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)

        self._list = QListWidget(self)
        self._list.currentItemChanged.connect(self._load_script)
        layout.addWidget(self._list)

        self._script_edit = QPlainTextEdit(self)
        self._script_edit.setPlaceholderText("Código de la macro...")
        layout.addWidget(self._script_edit)

        buttons = QHBoxLayout()
        self._new_button = QPushButton("Nueva", self)
        self._new_button.clicked.connect(self._new)
        self._save_button = QPushButton("Guardar", self)
        self._save_button.clicked.connect(self._save)
        self._run_button = QPushButton("Ejecutar", self)
        self._run_button.clicked.connect(self._run)
        self._delete_button = QPushButton("Eliminar", self)
        self._delete_button.clicked.connect(self._delete)
        buttons.addWidget(self._new_button)
        buttons.addWidget(self._save_button)
        buttons.addWidget(self._run_button)
        buttons.addWidget(self._delete_button)
        layout.addLayout(buttons)

        close_button = QDialogButtonBox(QDialogButtonBox.StandardButton.Close, self)
        close_button.rejected.connect(self.accept)
        layout.addWidget(close_button)

    def _reload(self) -> None:
        self._list.blockSignals(True)
        self._list.clear()
        self._list.addItems(sorted(self._manager.names()))
        self._list.blockSignals(False)

    def _current_name(self) -> str | None:
        item = self._list.currentItem()
        return item.text() if item else None

    def _load_script(self) -> None:
        name = self._current_name()
        if name:
            self._script_edit.setPlainText(self._manager.get(name))

    def _new(self) -> None:
        name, ok = QInputDialog.getText(self, "Nueva macro", "Nombre:")
        if ok and name.strip():
            self._manager.add(name, "")
            self._reload()
            self._list.setCurrentRow(self._list.count() - 1)
            self._script_edit.setPlainText("")

    def _save(self) -> None:
        name = self._current_name()
        if name is None:
            QMessageBox.warning(self, "Macros", "Seleccione una macro.")
            return
        self._manager.add(name, self._script_edit.toPlainText())

    def _run(self) -> None:
        name = self._current_name()
        if name is None:
            return
        self._save()
        self._manager.run(self._editor, name)

    def _delete(self) -> None:
        name = self._current_name()
        if name is not None:
            self._manager.delete(name)
            self._reload()

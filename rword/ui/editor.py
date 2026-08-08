"""Widget de edición de texto basado en QTextEdit."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QTextEdit

from rword.config import HTML_EXTENSIONS


class Editor(QTextEdit):
    """Área de edición con soporte de texto enriquecido y persistencia."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setAcceptRichText(True)
        self.setUndoRedoEnabled(True)
        self._file_path: Path | None = None

    @property
    def file_path(self) -> Path | None:
        return self._file_path

    def set_file_path(self, path: Path | None) -> None:
        self._file_path = path

    def load_file(self, path: Path) -> None:
        """Carga el contenido de un archivo en el editor."""
        content = path.read_text(encoding="utf-8")
        if path.suffix.lower() in HTML_EXTENSIONS:
            self.setHtml(content)
        else:
            self.setPlainText(content)
        self._file_path = path
        self.document().setModified(False)

    def save_file(self, path: Path) -> None:
        """Guarda el contenido del editor en un archivo."""
        content = (
            self.toHtml()
            if path.suffix.lower() in HTML_EXTENSIONS
            else self.toPlainText()
        )
        path.write_text(content, encoding="utf-8")
        self._file_path = path
        self.document().setModified(False)

    def word_count(self) -> int:
        """Número de palabras en el documento actual."""
        return len(self.toPlainText().split())

    def character_count(self) -> int:
        """Número de caracteres en el documento actual."""
        return len(self.toPlainText())

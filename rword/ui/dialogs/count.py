"""Diálogo de contar palabras y legibilidad."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
)

from rword.core import counters


class CountDialog(QDialog):
    """Muestra las estadísticas del documento."""

    def __init__(self, editor, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Contar palabras")
        self.setMinimumWidth(320)
        form = QFormLayout(self)

        if editor.textCursor().hasSelection():
            text = editor.textCursor().selectedText().replace("\u2029", "\n")
            form.addRow(QLabel("Selección:"), QLabel(""))
        else:
            text = editor.toPlainText()

        counts = counters.document_counts(editor) if not editor.textCursor().hasSelection() else {
            "words": counters.count_words(text),
            "characters": counters.count_characters(text),
            "characters_no_spaces": counters.count_characters_no_spaces(text),
            "paragraphs": counters.count_paragraphs(text),
            "lines": counters.count_lines(text),
            "pages": counters.count_pages(text),
            "sentences": counters.count_sentences(text),
        }

        labels = {
            "words": "Palabras",
            "characters": "Caracteres (con espacios)",
            "characters_no_spaces": "Caracteres (sin espacios)",
            "paragraphs": "Párrafos",
            "lines": "Líneas",
            "pages": "Páginas",
            "sentences": "Oraciones",
        }
        for key, label in labels.items():
            form.addRow(f"{label}:", QLabel(str(counts[key])))

        score, level = counters.readability_index(text)
        form.addRow("Legibilidad:", QLabel(f"{score} ({level})"))
        form.addRow("Longitud media de palabra:",
                    QLabel(str(counters.average_word_length(text))))

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close, self)
        buttons.rejected.connect(self.accept)
        form.addRow(buttons)

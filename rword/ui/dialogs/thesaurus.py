"""Diálogo de sinónimos y antónimos."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from rword.core import thesaurus


class ThesaurusDialog(QDialog):
    """Busca sinónimos y antónimos de una palabra."""

    def __init__(self, editor, parent=None) -> None:
        super().__init__(parent)
        self._editor = editor
        self.setWindowTitle("Sinónimos y antónimos")
        self.setMinimumWidth(380)
        layout = QVBoxLayout(self)
        form = QFormLayout()
        self._word_input = QLineEdit(self)
        self._word_input.returnPressed.connect(self._search)
        self._search_button = QPushButton("Buscar", self)
        self._search_button.clicked.connect(self._search)
        form.addRow("Palabra:", self._word_input)
        form.addRow("", self._search_button)
        self._syn_label = QLabel("", self)
        self._ant_label = QLabel("", self)
        form.addRow("Sinónimos:", self._syn_label)
        form.addRow("Antónimos:", self._ant_label)
        layout.addLayout(form)

        self._insert_button = QPushButton("Insertar en el documento", self)
        self._insert_button.clicked.connect(self._insert)
        layout.addWidget(self._insert_button)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close, self)
        buttons.rejected.connect(self.accept)
        layout.addWidget(buttons)

        selected = editor.textCursor().selectedText().strip()
        if selected:
            self._word_input.setText(selected)
            self._search()

    def _search(self) -> None:
        word = self._word_input.text().strip()
        if not word:
            return
        result = thesaurus.suggest(word)
        self._syn_label.setText(", ".join(result["sinónimos"]) or "(ninguno)")
        self._ant_label.setText(", ".join(result["antónimos"]) or "(ninguno)")

    def _insert(self) -> None:
        word = self._word_input.text().strip()
        if word:
            self._editor.insertPlainText(word)

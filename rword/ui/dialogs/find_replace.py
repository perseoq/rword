"""Diálogo de buscar y reemplazar."""

from __future__ import annotations

from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QColor, QTextCharFormat, QTextDocument
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QVBoxLayout,
)


class FindReplaceDialog(QDialog):
    """Buscar, reemplazar y resaltar coincidencias en el editor."""

    def __init__(self, editor, parent=None) -> None:
        super().__init__(parent)
        self._editor = editor
        self.setWindowTitle("Buscar y reemplazar")
        self.setModal(False)
        self.resize(420, 120)
        self._highlight_format = QTextCharFormat()
        self._highlight_format.setBackground(QColor("#ffe58f"))
        self._build_ui()
        self._update_actions()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)

        find_row = QHBoxLayout()
        find_row.addWidget(QLabel("Buscar:"))
        self._find_input = QLineEdit(self)
        self._find_input.setPlaceholderText("Texto a buscar")
        self._find_input.textChanged.connect(self._on_find_changed)
        self._find_input.returnPressed.connect(self._find_next)
        find_row.addWidget(self._find_input)
        layout.addLayout(find_row)

        replace_row = QHBoxLayout()
        replace_row.addWidget(QLabel("Reemplazar:"))
        self._replace_input = QLineEdit(self)
        self._replace_input.setPlaceholderText("Texto de reemplazo")
        replace_row.addWidget(self._replace_input)
        layout.addLayout(replace_row)

        options_row = QHBoxLayout()
        self._case_check = QCheckBox("Mayúsculas y minúsculas", self)
        self._word_check = QCheckBox("Solo palabra completa", self)
        self._case_check.toggled.connect(self._on_find_changed)
        self._word_check.toggled.connect(self._on_find_changed)
        options_row.addWidget(self._case_check)
        options_row.addWidget(self._word_check)
        layout.addLayout(options_row)

        buttons = QDialogButtonBox(self)
        self._find_prev_button = buttons.addButton(
            "Anterior", QDialogButtonBox.ButtonRole.ActionRole
        )
        self._find_next_button = buttons.addButton(
            "Siguiente", QDialogButtonBox.ButtonRole.ActionRole
        )
        self._replace_button = buttons.addButton(
            "Reemplazar", QDialogButtonBox.ButtonRole.ActionRole
        )
        self._replace_all_button = buttons.addButton(
            "Reemplazar todo", QDialogButtonBox.ButtonRole.ActionRole
        )
        buttons.addButton(QDialogButtonBox.StandardButton.Close)
        self._find_prev_button.clicked.connect(self._find_previous)
        self._find_next_button.clicked.connect(self._find_next)
        self._replace_button.clicked.connect(self._replace)
        self._replace_all_button.clicked.connect(self._replace_all)
        buttons.rejected.connect(self.close)
        layout.addWidget(buttons)

    def _find_regex(self):
        text = self._find_input.text()
        if not text:
            return None
        pattern = QRegularExpression.escape(text)
        flags = QRegularExpression.PatternOption(0)
        if self._word_check.isChecked():
            pattern = rf"\b{pattern}\b"
        if not self._case_check.isChecked():
            flags |= QRegularExpression.PatternOption.CaseInsensitiveOption
        return QRegularExpression(pattern, flags)

    def _find_from(self, start: int, backward: bool = False):
        regex = self._find_regex()
        if regex is None:
            return None
        flags = QTextDocument.FindFlag(0)
        if backward:
            flags |= QTextDocument.FindFlag.FindBackward
        document = self._editor.document()
        cursor = document.find(regex, start, flags)
        if cursor.isNull():
            start = len(document.toPlainText()) if backward else 0
            cursor = document.find(regex, start, flags)
        return cursor if not cursor.isNull() else None

    def _current_position(self) -> int:
        cursor = self._editor.textCursor()
        if cursor.hasSelection():
            return min(cursor.anchor(), cursor.position())
        return cursor.position()

    def _find_next(self) -> None:
        cursor = self._find_from(self._current_position())
        self._move_to(cursor)

    def _find_previous(self) -> None:
        cursor = self._find_from(self._current_position(), backward=True)
        self._move_to(cursor)

    def _move_to(self, cursor) -> None:
        if cursor is None:
            return
        self._editor.setTextCursor(cursor)
        self._editor.ensureCursorVisible()

    def _on_find_changed(self) -> None:
        self._update_actions()
        self._highlight_matches()

    def _update_actions(self) -> None:
        has_text = bool(self._find_input.text())
        self._find_next_button.setEnabled(has_text)
        self._find_prev_button.setEnabled(has_text)
        self._replace_button.setEnabled(has_text)
        self._replace_all_button.setEnabled(has_text)

    def _highlight_matches(self) -> None:
        regex = self._find_regex()
        selections = []
        if regex is not None:
            document = self._editor.document()
            cursor = document.find(regex, 0)
            while not cursor.isNull():
                selection = QTextEdit.ExtraSelection()
                selection.cursor = cursor
                selection.format = self._highlight_format
                selections.append(selection)
                cursor = document.find(regex, cursor.position())
        self._editor.setExtraSelections(selections)

    def _replace(self) -> None:
        text = self._find_input.text()
        if not text:
            return
        cursor = self._editor.textCursor()
        selected = cursor.selectedText()
        match = selected == text or (
            not self._case_check.isChecked() and selected.lower() == text.lower()
        )
        if cursor.hasSelection() and match:
            cursor.insertText(self._replace_input.text())
            self._find_next()
            self._highlight_matches()
        else:
            self._find_next()

    def _replace_all(self) -> None:
        regex = self._find_regex()
        if regex is None:
            return
        document = self._editor.document()
        replacement = self._replace_input.text()
        count = 0
        cursor = document.find(regex, 0)
        while not cursor.isNull():
            cursor.insertText(replacement)
            count += 1
            cursor = document.find(regex, cursor.position())
        if count:
            self._highlight_matches()

    def show_and_find(self, text: str = "") -> None:
        """Muestra el diálogo y opcionalmente busca el texto seleccionado."""
        self._find_input.setText(text)
        self.show()
        self.raise_()
        self._find_input.setFocus()
        self._find_input.selectAll()

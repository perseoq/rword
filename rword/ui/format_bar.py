"""Barra de herramientas de formato de fuente."""

from __future__ import annotations

from PySide6.QtGui import QAction, QColor, QFont, QTextCharFormat
from PySide6.QtWidgets import (
    QColorDialog,
    QFontComboBox,
    QSpinBox,
    QToolBar,
)

from rword.core import formatting
from rword.ui.editor import Editor


class FormatBar(QToolBar):
    """Barra de formato con fuente, tamaño y estilos de texto."""

    def __init__(self, editor: Editor, parent=None) -> None:
        super().__init__("Formato", parent)
        self.setObjectName("format_toolbar")
        self.setMovable(False)
        self._editor = editor
        self._build()

    def _build(self) -> None:
        self._font_combo = QFontComboBox(self)
        self._font_combo.setMinimumWidth(160)
        self._font_combo.currentFontChanged.connect(self._on_font_family)
        self.addWidget(self._font_combo)

        self._size_spin = QSpinBox(self)
        self._size_spin.setRange(4, 144)
        self._size_spin.setValue(12)
        self._size_spin.valueChanged.connect(self._on_font_size)
        self.addWidget(self._size_spin)

        self.grow_action = QAction("Aumentar tamaño", self)
        self.grow_action.triggered.connect(
            lambda: formatting.change_font_size(self._editor, 1.0)
        )
        self.addAction(self.grow_action)

        self.shrink_action = QAction("Disminuir tamaño", self)
        self.shrink_action.triggered.connect(
            lambda: formatting.change_font_size(self._editor, -1.0)
        )
        self.addAction(self.shrink_action)

        self.addSeparator()

        self.bold_action = self._add_toggle("Negrita", formatting._is_bold)
        self.italic_action = self._add_toggle("Cursiva", formatting._is_italic)
        self.underline_action = self._add_toggle("Subrayado", formatting._is_underline)
        self.strike_action = self._add_toggle("Tachado", formatting._is_strikeout)
        self.superscript_action = self._add_toggle("Superíndice", formatting._is_superscript)
        self.subscript_action = self._add_toggle("Subíndice", formatting._is_subscript)
        self._toggle_actions = [
            (self.bold_action, formatting._is_bold, formatting.toggle_bold),
            (self.italic_action, formatting._is_italic, formatting.toggle_italic),
            (self.underline_action, formatting._is_underline, formatting.toggle_underline),
            (self.strike_action, formatting._is_strikeout, formatting.toggle_strikeout),
            (self.superscript_action, formatting._is_superscript, formatting.toggle_superscript),
            (self.subscript_action, formatting._is_subscript, formatting.toggle_subscript),
        ]
        for action, _, toggle_fn in self._toggle_actions:
            action.toggled.connect(lambda checked, fn=toggle_fn: fn(self._editor))

        self.addSeparator()

        self.color_action = QAction("Color de texto...", self)
        self.color_action.triggered.connect(self._choose_text_color)
        self.addAction(self.color_action)

        self.highlight_action = QAction("Resaltado...", self)
        self.highlight_action.triggered.connect(self._choose_highlight)
        self.addAction(self.highlight_action)

        self.clear_format_action = QAction("Borrar formato", self)
        self.clear_format_action.triggered.connect(self._clear_format)
        self.addAction(self.clear_format_action)

        self._editor.currentCharFormatChanged.connect(self._on_char_format_changed)
        self._editor.cursorPositionChanged.connect(self._sync_from_cursor)

    def _add_toggle(self, label, is_active, shortcut: str = ""):
        action = QAction(label, self)
        action.setCheckable(True)
        self.addAction(action)
        return action

    def _on_font_family(self, font: QFont) -> None:
        formatting.set_font_family(self._editor, font.family())

    def _on_font_size(self, value: int) -> None:
        formatting.set_font_size(self._editor, float(value))

    def _choose_text_color(self) -> None:
        color = QColorDialog.getColor(QColor("black"), self, "Color de texto")
        if color.isValid():
            formatting.set_text_color(self._editor, color)

    def _choose_highlight(self) -> None:
        color = QColorDialog.getColor(QColor("#ffff00"), self, "Color de resaltado")
        if color.isValid():
            formatting.set_highlight(self._editor, color)

    def _clear_format(self) -> None:
        formatting.clear_formatting(self._editor)

    def _on_char_format_changed(self, _format: QTextCharFormat) -> None:
        self._sync_from_cursor()

    def _sync_from_cursor(self) -> None:
        for action, is_active, _ in self._toggle_actions:
            action.blockSignals(True)
            action.setChecked(is_active(self._editor))
            action.blockSignals(False)
        current = self._editor.currentCharFormat()
        family = current.fontFamilies()[0] if current.fontFamilies() else ""
        if family:
            self._font_combo.blockSignals(True)
            self._font_combo.setCurrentFont(QFont(family))
            self._font_combo.blockSignals(False)
        size = current.fontPointSize()
        if size > 0:
            self._size_spin.blockSignals(True)
            self._size_spin.setValue(int(round(size)))
            self._size_spin.blockSignals(False)

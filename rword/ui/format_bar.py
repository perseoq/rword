"""Controles de formato de fuente embebibles en la cinta."""

from __future__ import annotations

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction, QColor, QFont, QTextCharFormat
from PySide6.QtWidgets import (
    QColorDialog,
    QFontComboBox,
    QFrame,
    QGridLayout,
    QSizePolicy,
    QSpinBox,
    QToolButton,
    QWidget,
)

from rword.core import formatting
from rword.ui.editor import Editor
from rword.ui.icons import IconManager, icon_color_for


class FormatBar(QWidget):
    """Controles de fuente distribuidos en dos filas."""

    def __init__(self, editor: Editor, parent=None, icon_manager=None) -> None:
        super().__init__(parent)
        self._editor = editor
        self._icons = icon_manager or IconManager(icon_color_for(self))
        self._grid = QGridLayout(self)
        self._grid.setContentsMargins(2, 0, 2, 0)
        self._grid.setSpacing(2)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self._build()

    def _icon(self, action: QAction, name: str) -> QAction:
        self._icons.register(action, name, 16)
        return action

    def _add_button(self, action: QAction, row: int, col: int) -> QToolButton:
        button = QToolButton(self)
        button.setDefaultAction(action)
        button.setIconSize(QSize(16, 16))
        button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        button.setFixedSize(24, 24)
        button.setToolTip(action.text())
        self._grid.addWidget(button, row, col)
        return button

    def _add_separator(self, row: int, col: int, rows: int = 1) -> None:
        line = QFrame(self)
        line.setFrameShape(QFrame.Shape.VLine)
        line.setStyleSheet("color: #d1d5db;")
        self._grid.addWidget(line, row, col, rows, 1)

    def _build(self) -> None:
        self._font_combo = QFontComboBox(self)
        self._font_combo.setMinimumWidth(140)
        self._font_combo.currentFontChanged.connect(self._on_font_family)
        self._grid.addWidget(self._font_combo, 0, 0)

        self._size_spin = QSpinBox(self)
        self._size_spin.setRange(4, 144)
        self._size_spin.setValue(12)
        self._size_spin.setFixedWidth(56)
        self._size_spin.valueChanged.connect(self._on_font_size)
        self._grid.addWidget(self._size_spin, 0, 1)

        self.grow_action = QAction("Aumentar tamaño", self)
        self.grow_action.triggered.connect(
            lambda: formatting.change_font_size(self._editor, 1.0)
        )
        self._add_button(self._icon(self.grow_action, "maximize"), 0, 2)

        self.shrink_action = QAction("Disminuir tamaño", self)
        self.shrink_action.triggered.connect(
            lambda: formatting.change_font_size(self._editor, -1.0)
        )
        self._add_button(self._icon(self.shrink_action, "minimize"), 0, 3)

        self._add_separator(0, 4, 2)

        self.bold_action = self._add_toggle(
            "Negrita", formatting._is_bold, "bold", 1, 0
        )
        self.italic_action = self._add_toggle(
            "Cursiva", formatting._is_italic, "italic", 1, 1
        )
        self.underline_action = self._add_toggle(
            "Subrayado", formatting._is_underline, "underline", 1, 2
        )
        self.strike_action = self._add_toggle(
            "Tachado", formatting._is_strikeout, "strikethrough", 1, 3
        )
        self.superscript_action = self._add_toggle(
            "Superíndice", formatting._is_superscript, "superscript", 1, 4
        )
        self.subscript_action = self._add_toggle(
            "Subíndice", formatting._is_subscript, "subscript", 1, 5
        )
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

        self._add_separator(1, 6, 1)

        self.color_action = QAction("Color de texto...", self)
        self.color_action.triggered.connect(self._choose_text_color)
        self._add_button(self._icon(self.color_action, "palette"), 1, 7)

        self.highlight_action = QAction("Resaltado...", self)
        self.highlight_action.triggered.connect(self._choose_highlight)
        self._add_button(self._icon(self.highlight_action, "highlighter"), 1, 8)

        self.clear_format_action = QAction("Borrar formato", self)
        self.clear_format_action.triggered.connect(self._clear_format)
        self._add_button(self._icon(self.clear_format_action, "eraser"), 1, 9)

        self._editor.currentCharFormatChanged.connect(self._on_char_format_changed)
        self._editor.cursorPositionChanged.connect(self._sync_from_cursor)

    def _add_toggle(
        self, label, is_active, icon_name="", row: int = 0, col: int = 0,
        shortcut: str = "",
    ):
        action = QAction(label, self)
        action.setCheckable(True)
        if icon_name:
            self._icon(action, icon_name)
        self._add_button(action, row, col)
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

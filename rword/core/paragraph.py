"""Operaciones de formato de párrafo sobre el editor."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor, QTextBlockFormat, QTextFormat, QTextListFormat
from PySide6.QtWidgets import QTextEdit

INDENT_STEP = 20.0

_PROPORTIONAL_HEIGHT = QTextBlockFormat.LineHeightTypes.ProportionalHeight.value

_ALIGNMENTS = {
    "left": Qt.AlignmentFlag.AlignLeft,
    "center": Qt.AlignmentFlag.AlignCenter,
    "right": Qt.AlignmentFlag.AlignRight,
    "justify": Qt.AlignmentFlag.AlignJustify,
}


def _block_format(editor: QTextEdit) -> QTextBlockFormat:
    return editor.textCursor().block().blockFormat()


def _apply_block_format(editor: QTextEdit, fmt: QTextBlockFormat) -> None:
    cursor = editor.textCursor()
    cursor.mergeBlockFormat(fmt)


def set_alignment(editor: QTextEdit, alignment: str) -> None:
    fmt = QTextBlockFormat()
    fmt.setAlignment(_ALIGNMENTS[alignment])
    _apply_block_format(editor, fmt)


def current_alignment(editor: QTextEdit) -> Qt.AlignmentFlag:
    return _block_format(editor).alignment()


def set_left_indent(editor: QTextEdit, value: float) -> None:
    fmt = QTextBlockFormat()
    fmt.setLeftMargin(value)
    _apply_block_format(editor, fmt)


def set_right_indent(editor: QTextEdit, value: float) -> None:
    fmt = QTextBlockFormat()
    fmt.setRightMargin(value)
    _apply_block_format(editor, fmt)


def set_first_line_indent(editor: QTextEdit, value: float) -> None:
    fmt = QTextBlockFormat()
    fmt.setTextIndent(value)
    _apply_block_format(editor, fmt)


def set_hanging_indent(editor: QTextEdit, value: float) -> None:
    fmt = QTextBlockFormat()
    fmt.setLeftMargin(value)
    fmt.setTextIndent(-value)
    _apply_block_format(editor, fmt)


def increase_indent(editor: QTextEdit) -> None:
    current = _block_format(editor).leftMargin()
    set_left_indent(editor, current + INDENT_STEP)


def decrease_indent(editor: QTextEdit) -> None:
    current = _block_format(editor).leftMargin()
    set_left_indent(editor, max(0.0, current - INDENT_STEP))


def set_line_spacing(editor: QTextEdit, factor: float) -> None:
    """Ajusta el interlineado en múltiplos (1.0, 1.5, 2.0, ...)."""
    fmt = QTextBlockFormat()
    fmt.setLineHeight(factor * 100.0, _PROPORTIONAL_HEIGHT)
    _apply_block_format(editor, fmt)


def current_line_spacing(editor: QTextEdit) -> float:
    fmt = _block_format(editor)
    if fmt.lineHeightType() != _PROPORTIONAL_HEIGHT:
        return 1.0
    return fmt.lineHeight() / 100.0


def set_space_before(editor: QTextEdit, value: float) -> None:
    fmt = QTextBlockFormat()
    fmt.setTopMargin(value)
    _apply_block_format(editor, fmt)


def set_space_after(editor: QTextEdit, value: float) -> None:
    fmt = QTextBlockFormat()
    fmt.setBottomMargin(value)
    _apply_block_format(editor, fmt)


def toggle_bullets(editor: QTextEdit) -> None:
    _toggle_list(editor, QTextListFormat.Style.ListDisc)


def toggle_numbering(editor: QTextEdit) -> None:
    _toggle_list(editor, QTextListFormat.Style.ListDecimal)


def _toggle_list(editor: QTextEdit, style: QTextListFormat.Style) -> None:
    cursor = editor.textCursor()
    current_list = cursor.currentList()
    if current_list is not None and current_list.format().style() == style:
        _remove_from_list(cursor)
    else:
        list_format = QTextListFormat()
        list_format.setStyle(style)
        cursor.createList(list_format)


def _remove_from_list(cursor) -> None:
    block_format = cursor.block().blockFormat()
    block_format.clearProperty(QTextFormat.Property.ListIndent)
    block_format.clearProperty(QTextFormat.Property.ObjectIndex)
    cursor.setBlockFormat(block_format)


def set_list_level(editor: QTextEdit, level: int) -> None:
    cursor = editor.textCursor()
    current_list = cursor.currentList()
    if current_list is None:
        return
    list_format = current_list.format()
    list_format.setIndent(level)
    current_list.setFormat(list_format)


def current_list_style(editor: QTextEdit):
    cursor = editor.textCursor()
    current_list = cursor.currentList()
    if current_list is None:
        return None
    return current_list.format().style()


def set_paragraph_shading(editor: QTextEdit, color: QColor) -> None:
    fmt = QTextBlockFormat()
    fmt.setBackground(QBrush(color))
    _apply_block_format(editor, fmt)


def set_tab_stop_distance(editor: QTextEdit, distance: float) -> None:
    option = editor.document().defaultTextOption()
    option.setTabStopDistance(distance)
    editor.document().setDefaultTextOption(option)


def current_tab_stop_distance(editor: QTextEdit) -> float:
    return editor.document().defaultTextOption().tabStopDistance()


def clear_paragraph_format(editor: QTextEdit) -> None:
    fmt = QTextBlockFormat()
    fmt.setAlignment(Qt.AlignmentFlag.AlignLeft)
    fmt.setLeftMargin(0.0)
    fmt.setRightMargin(0.0)
    fmt.setTextIndent(0.0)
    fmt.setTopMargin(0.0)
    fmt.setBottomMargin(0.0)
    fmt.setLineHeight(100.0, _PROPORTIONAL_HEIGHT)
    cursor = editor.textCursor()
    cursor.setBlockFormat(fmt)

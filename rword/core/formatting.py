"""Operaciones de formato de fuente y párrafo sobre el editor."""

from __future__ import annotations

import re

from PySide6.QtGui import QBrush, QColor, QFont, QTextCharFormat
from PySide6.QtWidgets import QTextEdit

from rword.config import LINE_SEPARATOR, PARAGRAPH_SEPARATOR

_SENTENCE_START = re.compile(r"(^|[.!?¿¡]\s*)(\w)")


def _cursor_format(editor: QTextEdit) -> QTextCharFormat:
    return editor.currentCharFormat()


def _is_bold(editor: QTextEdit) -> bool:
    return _cursor_format(editor).fontWeight() >= QFont.Weight.Bold


def _is_italic(editor: QTextEdit) -> bool:
    return _cursor_format(editor).fontItalic()


def _is_underline(editor: QTextEdit) -> bool:
    return _cursor_format(editor).fontUnderline()


def _is_strikeout(editor: QTextEdit) -> bool:
    return _cursor_format(editor).fontStrikeOut()


def _is_superscript(editor: QTextEdit) -> bool:
    return (
        _cursor_format(editor).verticalAlignment()
        == QTextCharFormat.VerticalAlignment.AlignSuperScript
    )


def _is_subscript(editor: QTextEdit) -> bool:
    return (
        _cursor_format(editor).verticalAlignment()
        == QTextCharFormat.VerticalAlignment.AlignSubScript
    )


def toggle_bold(editor: QTextEdit) -> None:
    fmt = QTextCharFormat()
    fmt.setFontWeight(
        QFont.Weight.Normal if _is_bold(editor) else QFont.Weight.Bold
    )
    editor.mergeCurrentCharFormat(fmt)


def toggle_italic(editor: QTextEdit) -> None:
    fmt = QTextCharFormat()
    fmt.setFontItalic(not _is_italic(editor))
    editor.mergeCurrentCharFormat(fmt)


def toggle_underline(editor: QTextEdit) -> None:
    fmt = QTextCharFormat()
    fmt.setFontUnderline(not _is_underline(editor))
    editor.mergeCurrentCharFormat(fmt)


def toggle_strikeout(editor: QTextEdit) -> None:
    fmt = QTextCharFormat()
    fmt.setFontStrikeOut(not _is_strikeout(editor))
    editor.mergeCurrentCharFormat(fmt)


def toggle_superscript(editor: QTextEdit) -> None:
    fmt = QTextCharFormat()
    fmt.setVerticalAlignment(
        QTextCharFormat.VerticalAlignment.AlignNormal
        if _is_superscript(editor)
        else QTextCharFormat.VerticalAlignment.AlignSuperScript
    )
    editor.mergeCurrentCharFormat(fmt)


def toggle_subscript(editor: QTextEdit) -> None:
    fmt = QTextCharFormat()
    fmt.setVerticalAlignment(
        QTextCharFormat.VerticalAlignment.AlignNormal
        if _is_subscript(editor)
        else QTextCharFormat.VerticalAlignment.AlignSubScript
    )
    editor.mergeCurrentCharFormat(fmt)


def set_font_family(editor: QTextEdit, family: str) -> None:
    fmt = QTextCharFormat()
    fmt.setFontFamilies([family])
    editor.mergeCurrentCharFormat(fmt)


def set_font_size(editor: QTextEdit, size: float) -> None:
    fmt = QTextCharFormat()
    fmt.setFontPointSize(size)
    editor.mergeCurrentCharFormat(fmt)


def change_font_size(editor: QTextEdit, delta: float) -> None:
    current = _cursor_format(editor).fontPointSize()
    if current <= 0:
        current = editor.font().pointSizeF()
    set_font_size(editor, max(1.0, current + delta))


def set_text_color(editor: QTextEdit, color: QColor) -> None:
    fmt = QTextCharFormat()
    fmt.setForeground(QBrush(color))
    editor.mergeCurrentCharFormat(fmt)


def set_highlight(editor: QTextEdit, color: QColor | None) -> None:
    fmt = QTextCharFormat()
    if color is None:
        fmt.setBackground(QBrush(QColor("transparent")))
    else:
        fmt.setBackground(QBrush(color))
    editor.mergeCurrentCharFormat(fmt)


def set_letter_spacing(editor: QTextEdit, percent: int) -> None:
    fmt = QTextCharFormat()
    fmt.setFontLetterSpacing(float(percent))
    editor.mergeCurrentCharFormat(fmt)


def clear_formatting(editor: QTextEdit) -> None:
    fmt = QTextCharFormat()
    fmt.setFontWeight(QFont.Weight.Normal)
    fmt.setFontItalic(False)
    fmt.setFontUnderline(False)
    fmt.setFontStrikeOut(False)
    fmt.setVerticalAlignment(QTextCharFormat.VerticalAlignment.AlignNormal)
    fmt.setFontLetterSpacing(0.0)
    editor.mergeCurrentCharFormat(fmt)


def apply_case(editor: QTextEdit, mode: str) -> None:
    """Transforma las mayúsculas de la selección según el modo indicado."""
    cursor = editor.textCursor()
    if not cursor.hasSelection():
        return
    text = cursor.selectedText()
    text = text.replace(PARAGRAPH_SEPARATOR, "\n").replace(LINE_SEPARATOR, "\n")
    new_text = _transform_case(text, mode)
    if new_text != text:
        cursor.insertText(new_text)


def _transform_case(text: str, mode: str) -> str:
    if mode == "upper":
        return text.upper()
    if mode == "lower":
        return text.lower()
    if mode == "title":
        return text.title()
    if mode == "toggle":
        return text.swapcase()
    if mode == "sentence":
        return _SENTENCE_START.sub(lambda m: m.group(1) + m.group(2).upper(), text)
    return text

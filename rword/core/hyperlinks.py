"""Hipervínculos, marcadores y navegación por títulos."""

from __future__ import annotations

from PySide6.QtGui import QBrush, QColor, QTextCharFormat, QTextCursor
from PySide6.QtWidgets import QTextEdit

LINK_COLOR = QColor("#0563c1")
BOOKMARKS_KEY = "bookmarks"
HEADING_THRESHOLDS = [
    (24.0, 1),
    (20.0, 2),
    (16.0, 3),
]


def insert_hyperlink(editor: QTextEdit, text: str, url: str) -> None:
    """Inserta o convierte texto en un hipervínculo."""
    cursor = editor.textCursor()
    fmt = QTextCharFormat()
    fmt.setAnchor(True)
    fmt.setAnchorHref(url)
    fmt.setForeground(QBrush(LINK_COLOR))
    fmt.setFontUnderline(True)
    if cursor.hasSelection():
        cursor.mergeCharFormat(fmt)
    else:
        cursor.insertText(text or url, fmt)
        editor.setTextCursor(cursor)


def hyperlink_at_cursor(editor: QTextEdit) -> tuple[str, str] | None:
    """Devuelve (texto, url) del hipervínculo en el cursor."""
    cursor = editor.textCursor()
    fmt = cursor.charFormat()
    if not fmt.isAnchor():
        return None
    text = cursor.selectedText() or ""
    if not text:
        block = cursor.block()
        text = block.text()
    return text, fmt.anchorHref()


def remove_hyperlink(editor: QTextEdit) -> None:
    """Elimina el formato de hipervínculo del texto seleccionado."""
    cursor = editor.textCursor()
    if not cursor.hasSelection():
        return
    fmt = QTextCharFormat()
    fmt.setAnchor(False)
    fmt.setAnchorHref("")
    fmt.setFontUnderline(False)
    fmt.setForeground(QBrush(QColor("#000000")))
    cursor.mergeCharFormat(fmt)


def add_bookmark(editor: QTextEdit, name: str) -> bool:
    """Registra un marcador en la posición actual del cursor."""
    if not name:
        return False
    bookmarks = getattr(editor, BOOKMARKS_KEY, None)
    if bookmarks is None:
        bookmarks = {}
        setattr(editor, BOOKMARKS_KEY, bookmarks)
    bookmarks[name] = editor.textCursor().position()
    return True


def bookmarks(editor: QTextEdit) -> dict[str, int]:
    return dict(getattr(editor, BOOKMARKS_KEY, {}))


def goto_bookmark(editor: QTextEdit, name: str) -> bool:
    bookmarks = getattr(editor, BOOKMARKS_KEY, {})
    position = bookmarks.get(name)
    if position is None:
        return False
    cursor = editor.textCursor()
    cursor.setPosition(min(position, editor.document().characterCount() - 1))
    editor.setTextCursor(cursor)
    editor.ensureCursorVisible()
    return True


def remove_bookmark(editor: QTextEdit, name: str) -> bool:
    bookmarks = getattr(editor, BOOKMARKS_KEY, None)
    if bookmarks is None or name not in bookmarks:
        return False
    del bookmarks[name]
    return True


def heading_level(block, default_size: float = 12.0) -> int | None:
    """Estima el nivel de título de un bloque por su formato."""
    heading = block.blockFormat().headingLevel()
    if heading > 0:
        return heading
    cursor = QTextCursor(block)
    fmt = cursor.charFormat()
    size = fmt.fontPointSize()
    if size <= 0:
        size = default_size
    weight = fmt.fontWeight()
    if weight >= 700 and not fmt.fontItalic():
        for threshold, level in HEADING_THRESHOLDS:
            if size >= threshold:
                return level
    return None


def headings(editor: QTextEdit) -> list[tuple[str, int]]:
    """Devuelve los títulos del documento como (texto, nivel)."""
    default_size = editor.document().defaultFont().pointSizeF()
    result = []
    block = editor.document().begin()
    while block.isValid():
        level = heading_level(block, default_size)
        text = block.text().strip()
        if level is not None and text:
            result.append((text, level))
        block = block.next()
    return result


def goto_block(editor: QTextEdit, block_number: int) -> None:
    block = editor.document().findBlockByNumber(block_number)
    if block.isValid():
        editor.setTextCursor(QTextCursor(block))
        editor.ensureCursorVisible()

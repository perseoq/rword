"""Encabezados, pies de página y campos automáticos."""

from __future__ import annotations

from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtGui import QTextBlockFormat, QTextCharFormat, QTextFormat
from PySide6.QtWidgets import QTextEdit

HEADER_MARK = QTextFormat.Property.UserProperty + 1
FOOTER_MARK = QTextFormat.Property.UserProperty + 2
TEMPLATE_PROP = QTextFormat.Property.UserProperty + 3
FIELD_ANCHOR = "rword:field:"

FIELDS = {
    "PAGE": "{PAGE}",
    "DATE": "{DATE}",
    "TIME": "{TIME}",
    "FILE": "{FILE}",
    "PATH": "{PATH}",
}

_NUMBERING_FORMATS = {
    "decimal": lambda n: str(n),
    "roman": lambda n: _to_roman(n),
    "alpha": lambda n: _to_alpha(n),
}


def _to_roman(number: int) -> str:
    if number <= 0:
        return str(number)
    numerals = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
    ]
    result = ""
    for value, symbol in numerals:
        while number >= value:
            result += symbol
            number -= value
    return result


def _to_alpha(number: int) -> str:
    result = ""
    while number > 0:
        number, remainder = divmod(number - 1, 26)
        result = chr(ord("A") + remainder) + result
    return result or "A"


def page_at_block(editor: QTextEdit, block_number: int) -> int:
    """Número de página calculado contando los saltos de página previos."""
    page = 1
    block = editor.document().begin()
    index = 0
    while block.isValid() and index < block_number:
        if block.blockFormat().pageBreakPolicy() & (
            QTextFormat.PageBreakFlag.PageBreak_AlwaysBefore
        ):
            page += 1
        block = block.next()
        index += 1
    return page


def resolve_field(kind: str, editor: QTextEdit, block_number: int = 0) -> str:
    now = datetime.now()
    if kind == "PAGE":
        fmt_name = editor.document().property("rword:page-numbering") or "decimal"
        number = page_at_block(editor, block_number)
        return _NUMBERING_FORMATS.get(fmt_name, _NUMBERING_FORMATS["decimal"])(number)
    if kind == "DATE":
        return now.strftime("%d/%m/%Y")
    if kind == "TIME":
        return now.strftime("%H:%M")
    if kind == "FILE":
        if editor.file_path is not None:
            return editor.file_path.name
        return "Sin título"
    if kind == "PATH":
        if editor.file_path is not None:
            return str(editor.file_path.parent)
        return ""
    return ""


def resolve_template(template: str, editor: QTextEdit, block_number: int = 0) -> str:
    for kind in FIELDS:
        template = template.replace(
            FIELDS[kind], resolve_field(kind, editor, block_number)
        )
    return template


def _make_block_format(kind: int, template: str) -> QTextBlockFormat:
    fmt = QTextBlockFormat()
    fmt.setProperty(HEADER_MARK if kind == 1 else FOOTER_MARK, 1)
    fmt.setProperty(TEMPLATE_PROP, template)
    fmt.setAlignment(Qt.AlignmentFlag.AlignCenter)
    return fmt


def _blocks_of_kind(editor: QTextEdit, mark: int) -> list[int]:
    numbers = []
    block = editor.document().begin()
    while block.isValid():
        if block.blockFormat().property(mark):
            numbers.append(block.blockNumber())
        block = block.next()
    return numbers


def _remove_blocks(editor: QTextEdit, numbers: list[int]) -> None:
    cursor = editor.textCursor()
    for block_number in sorted(numbers, reverse=True):
        block = editor.document().findBlockByNumber(block_number)
        if block.isValid():
            cursor.setPosition(block.position())
            cursor.movePosition(
                cursor.MoveOperation.NextBlock, cursor.MoveMode.KeepAnchor
            )
            cursor.removeSelectedText()


def apply_header(editor: QTextEdit, template: str) -> None:
    _remove_blocks(editor, _blocks_of_kind(editor, HEADER_MARK))
    if not template.strip():
        return
    fmt = _make_block_format(1, template)
    cursor = editor.textCursor()
    cursor.beginEditBlock()
    cursor.movePosition(cursor.MoveOperation.Start)
    cursor.setBlockFormat(fmt)
    cursor.insertText(resolve_template(template, editor, 0))
    cursor.insertBlock()
    cursor.setBlockFormat(QTextBlockFormat())
    cursor.endEditBlock()


def apply_footer(editor: QTextEdit, template: str) -> None:
    _remove_blocks(editor, _blocks_of_kind(editor, FOOTER_MARK))
    if not template.strip():
        return
    fmt = _make_block_format(2, template)
    cursor = editor.textCursor()
    cursor.beginEditBlock()
    cursor.movePosition(cursor.MoveOperation.End)
    cursor.insertBlock()
    cursor.setBlockFormat(fmt)
    block_number = cursor.block().blockNumber()
    cursor.insertText(resolve_template(template, editor, block_number))
    cursor.insertBlock()
    cursor.setBlockFormat(QTextBlockFormat())
    cursor.endEditBlock()


def remove_header(editor: QTextEdit) -> None:
    _remove_blocks(editor, _blocks_of_kind(editor, HEADER_MARK))


def remove_footer(editor: QTextEdit) -> None:
    _remove_blocks(editor, _blocks_of_kind(editor, FOOTER_MARK))


def refresh_fields(editor: QTextEdit) -> None:
    """Reemplaza los campos marcados con su valor actualizado."""
    updates: list[tuple[int, str]] = []
    block = editor.document().begin()
    while block.isValid():
        iterator = block.begin()
        while not iterator.atEnd():
            fragment = iterator.fragment()
            names = fragment.charFormat().anchorNames()
            for name in names:
                if name.startswith(FIELD_ANCHOR):
                    kind = name[len(FIELD_ANCHOR):]
                    updates.append(
                        (
                            fragment.position(),
                            resolve_field(kind, editor, block.blockNumber()),
                        )
                    )
            iterator += 1
        block = block.next()
    for position, value in updates:
        cursor = editor.textCursor()
        cursor.setPosition(position)
        cursor.setPosition(position + 1, cursor.MoveMode.KeepAnchor)
        fmt = cursor.charFormat()
        cursor.insertText(value, fmt)
    if updates:
        editor.document().setModified(True)


def insert_field(editor: QTextEdit, kind: str) -> None:
    """Inserta un campo automático en la posición del cursor."""
    fmt = QTextCharFormat()
    fmt.setAnchor(False)
    fmt.setAnchorNames([FIELD_ANCHOR + kind])
    cursor = editor.textCursor()
    cursor.insertText(
        resolve_field(kind, editor, cursor.block().blockNumber()), fmt
    )
    editor.setTextCursor(cursor)


def set_numbering_format(editor: QTextEdit, fmt_name: str) -> None:
    """Guarda el formato de numeración de página en el documento."""
    editor.document().setProperty(
        "rword:page-numbering", fmt_name
    )

"""Referencias: tabla de contenido, notas, citas, bibliografía e índice."""

from __future__ import annotations

from PySide6.QtGui import (
    QBrush,
    QColor,
    QFont,
    QTextBlockFormat,
    QTextCharFormat,
    QTextCursor,
    QTextFormat,
)
from PySide6.QtWidgets import QTextEdit

from rword.core.hyperlinks import heading_level

TOC_MARK = QTextFormat.Property.UserProperty + 10
NOTE_MARK = QTextFormat.Property.UserProperty + 11
CAPTION_MARK = QTextFormat.Property.UserProperty + 12
INDEX_MARK = QTextFormat.Property.UserProperty + 13
TOC_ANCHOR = "rword-toc-"
NOTE_ANCHOR = "rword-note-"
CAPTION_ANCHOR = "rword-caption-"
SOURCES_KEY = "rword:sources"


def _link_format() -> QTextCharFormat:
    fmt = QTextCharFormat()
    fmt.setAnchor(True)
    fmt.setForeground(QBrush(QColor("#0563c1")))
    fmt.setFontUnderline(True)
    return fmt


def _title_format(level: int = 0) -> QTextCharFormat:
    fmt = QTextCharFormat()
    fmt.setFontWeight(QFont.Weight.Bold)
    fmt.setFontPointSize(16.0 - level * 1.0)
    return fmt


def _anchor_heading(editor: QTextEdit, block_number: int) -> None:
    block = editor.document().findBlockByNumber(block_number)
    if not block.isValid() or not block.text():
        return
    cursor = QTextCursor(block)
    cursor.setPosition(block.position())
    cursor.setPosition(block.position() + 1, cursor.MoveMode.KeepAnchor)
    fmt = QTextCharFormat()
    fmt.setAnchorNames([TOC_ANCHOR + str(block_number)])
    cursor.mergeCharFormat(fmt)


def goto_anchor(editor: QTextEdit, name: str) -> bool:
    """Mueve el cursor a un ancla por nombre."""
    block = editor.document().begin()
    while block.isValid():
        iterator = block.begin()
        while not iterator.atEnd():
            fragment = iterator.fragment()
            if name in fragment.charFormat().anchorNames():
                cursor = editor.textCursor()
                cursor.setPosition(fragment.position())
                editor.setTextCursor(cursor)
                editor.ensureCursorVisible()
                return True
            iterator += 1
        block = block.next()
    return False


def _remove_blocks(editor: QTextEdit, mark: int) -> None:
    numbers = []
    block = editor.document().begin()
    while block.isValid():
        if block.blockFormat().property(mark):
            numbers.append(block.blockNumber())
        block = block.next()
    cursor = editor.textCursor()
    for block_number in sorted(numbers, reverse=True):
        block = editor.document().findBlockByNumber(block_number)
        if block.isValid():
            cursor.setPosition(block.position())
            cursor.movePosition(
                cursor.MoveOperation.NextBlock, cursor.MoveMode.KeepAnchor
            )
            cursor.removeSelectedText()



def _headings_with_numbers(editor: QTextEdit) -> list[tuple[str, int, int]]:
    default_size = editor.document().defaultFont().pointSizeF()
    result: list[tuple[str, int, int]] = []
    block = editor.document().begin()
    while block.isValid():
        level = heading_level(block, default_size)
        text = block.text().strip()
        if level is not None and text:
            result.append((text, level, block.blockNumber()))
        block = block.next()
    return result


def _mark_block(editor: QTextEdit, block, mark: int) -> None:
    block_format = block.blockFormat()
    block_format.setProperty(mark, 1)
    mark_cursor = QTextCursor(block)
    mark_cursor.setBlockFormat(block_format)


def insert_toc(editor: QTextEdit) -> None:
    """Genera una tabla de contenido automática a partir de los títulos."""
    _remove_blocks(editor, TOC_MARK)
    entries = _headings_with_numbers(editor)
    cursor = editor.textCursor()
    cursor.beginEditBlock()
    cursor.movePosition(cursor.MoveOperation.StartOfBlock)
    cursor.insertText("Tabla de contenido\n", _title_format(0))
    _mark_block(editor, cursor.block().previous(), TOC_MARK)
    for text, level, block_number in entries:
        _anchor_heading(editor, block_number)
        line_fmt = _link_format()
        line_fmt.setAnchorHref(f"#{TOC_ANCHOR}{block_number}")
        indent = "  " * (level - 1)
        cursor.insertText(f"{indent}{text}\n", line_fmt)
        _mark_block(editor, cursor.block().previous(), TOC_MARK)
    cursor.endEditBlock()


def update_toc(editor: QTextEdit) -> None:
    insert_toc(editor)


def insert_note(editor: QTextEdit, text: str, kind: str) -> None:
    """Inserta una nota al pie o al final con su número superíndice."""
    count = _note_count(editor) + 1
    marker_fmt = QTextCharFormat()
    marker_fmt.setVerticalAlignment(
        QTextCharFormat.VerticalAlignment.AlignSuperScript
    )
    marker_fmt.setAnchorNames([NOTE_ANCHOR + str(count)])
    cursor = editor.textCursor()
    cursor.insertText(f"[{count}]", marker_fmt)

    note_fmt = QTextBlockFormat()
    note_fmt.setProperty(NOTE_MARK, 1)
    end_cursor = editor.textCursor()
    end_cursor.movePosition(end_cursor.MoveOperation.End)
    end_cursor.insertBlock()
    end_cursor.setBlockFormat(note_fmt)
    end_cursor.insertText(f"{count}. {text}", QTextCharFormat())


def _note_count(editor: QTextEdit) -> int:
    count = 0
    block = editor.document().begin()
    while block.isValid():
        iterator = block.begin()
        while not iterator.atEnd():
            names = iterator.fragment().charFormat().anchorNames()
            for name in names:
                if name.startswith(NOTE_ANCHOR):
                    count += 1
            iterator += 1
        block = block.next()
    return count


def add_footnote(editor: QTextEdit, text: str) -> None:
    insert_note(editor, text, "footnote")


def add_endnote(editor: QTextEdit, text: str) -> None:
    insert_note(editor, text, "endnote")


def insert_cross_reference(editor: QTextEdit, target: str) -> None:
    """Inserta una referencia cruzada a un título o marcador."""
    link = _link_format()
    link.setAnchorHref(f"#{target}")
    cursor = editor.textCursor()
    cursor.insertText(f"(ver: {target})", link)
    editor.setTextCursor(cursor)


def sources(editor: QTextEdit) -> list[dict]:
    return list(getattr(editor, SOURCES_KEY, []))


def add_source(editor: QTextEdit, author: str, year: str, title: str) -> None:
    current = list(getattr(editor, SOURCES_KEY, []))
    current.append({"author": author, "year": year, "title": title})
    setattr(editor, SOURCES_KEY, current)


def insert_citation(editor: QTextEdit, author: str, year: str) -> None:
    cursor = editor.textCursor()
    cursor.insertText(f"({author}, {year})")
    editor.setTextCursor(cursor)


def insert_bibliography(editor: QTextEdit) -> None:
    entries = sources(editor)
    cursor = editor.textCursor()
    cursor.movePosition(cursor.MoveOperation.End)
    cursor.insertBlock()
    cursor.insertText("Bibliografía\n", _title_format(0))
    for entry in entries:
        cursor.insertText(
            f"{entry['author']} ({entry['year']}). {entry['title']}.\n"
        )


def insert_caption(editor: QTextEdit, text: str) -> None:
    """Inserta una leyenda de figura con numeración automática."""
    count = _caption_count(editor) + 1
    cursor = editor.textCursor()
    cursor.insertText(f"Figura {count}: {text}\n")
    block = cursor.block()
    fmt = block.blockFormat()
    fmt.setProperty(CAPTION_MARK, 1)
    cursor.setBlockFormat(fmt)


def _caption_count(editor: QTextEdit) -> int:
    count = 0
    block = editor.document().begin()
    while block.isValid():
        if block.blockFormat().property(CAPTION_MARK):
            count += 1
        block = block.next()
    return count


def insert_table_of_figures(editor: QTextEdit) -> None:
    captions = []
    block = editor.document().begin()
    while block.isValid():
        if block.blockFormat().property(CAPTION_MARK):
            captions.append(block.text())
        block = block.next()
    cursor = editor.textCursor()
    cursor.movePosition(cursor.MoveOperation.End)
    cursor.insertBlock()
    cursor.insertText("Tabla de figuras\n", _title_format(0))
    for caption in captions:
        cursor.insertText(caption + "\n")


def mark_index_entry(editor: QTextEdit, entry: str) -> None:
    """Marca la selección como entrada del índice analítico."""
    cursor = editor.textCursor()
    if not cursor.hasSelection():
        return
    fmt = QTextCharFormat()
    fmt.setProperty(INDEX_MARK, entry)
    cursor.mergeCharFormat(fmt)


def insert_index(editor: QTextEdit) -> None:
    """Genera un índice analítico alfabético con las entradas marcadas."""
    entries: set[str] = set()
    block = editor.document().begin()
    while block.isValid():
        iterator = block.begin()
        while not iterator.atEnd():
            fragment = iterator.fragment()
            entry = fragment.charFormat().property(INDEX_MARK)
            if entry:
                entries.add(entry)
            iterator += 1
        block = block.next()
    cursor = editor.textCursor()
    cursor.movePosition(cursor.MoveOperation.End)
    cursor.insertBlock()
    cursor.insertText("Índice analítico\n", _title_format(0))
    for entry in sorted(entries, key=str.casefold):
        cursor.insertText(f"{entry}\n")

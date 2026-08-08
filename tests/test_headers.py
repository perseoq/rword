
from rword.core.headers import (
    FOOTER_MARK,
    HEADER_MARK,
    _blocks_of_kind,
    _to_alpha,
    _to_roman,
    apply_footer,
    apply_header,
    insert_field,
    page_at_block,
    refresh_fields,
    remove_footer,
    remove_header,
    resolve_field,
    resolve_template,
    set_numbering_format,
)


def test_to_roman():
    assert _to_roman(1) == "I"
    assert _to_roman(4) == "IV"
    assert _to_roman(9) == "IX"
    assert _to_roman(12) == "XII"
    assert _to_roman(2024) == "MMXXIV"


def test_to_alpha():
    assert _to_alpha(1) == "A"
    assert _to_alpha(2) == "B"
    assert _to_alpha(26) == "Z"
    assert _to_alpha(27) == "AA"


def test_resolve_field_date(editor):
    value = resolve_field("DATE", editor)
    assert "/" in value


def test_resolve_field_file(editor):
    editor.set_file_path(__import__("pathlib").Path("/tmp/documento.txt"))
    assert resolve_field("FILE", editor) == "documento.txt"
    assert resolve_field("PATH", editor) == "/tmp"


def test_resolve_template(editor):
    text = resolve_template("Informe {DATE} — página {PAGE}", editor)
    assert "Informe" in text
    assert "/" in text
    assert "página 1" in text


def test_page_at_block_counts_breaks(editor):
    editor.setPlainText("a\nb\nc")
    assert page_at_block(editor, 0) == 1
    from PySide6.QtGui import QTextBlockFormat, QTextFormat

    block = editor.document().findBlockByNumber(1)
    cursor = editor.textCursor()
    cursor.setPosition(block.position())
    fmt = QTextBlockFormat()
    fmt.setPageBreakPolicy(QTextFormat.PageBreakFlag.PageBreak_AlwaysBefore)
    cursor.mergeBlockFormat(fmt)
    assert page_at_block(editor, 2) == 2


def test_apply_header_inserts_block(editor):
    editor.setPlainText("contenido")
    apply_header(editor, "Mi encabezado")
    assert editor.document().firstBlock().text() == "Mi encabezado"
    assert _blocks_of_kind(editor, HEADER_MARK) == [0]


def test_apply_footer_inserts_block(editor):
    editor.setPlainText("contenido")
    apply_footer(editor, "Pie {PAGE}")
    assert "Pie 1" in editor.toPlainText()
    assert _blocks_of_kind(editor, FOOTER_MARK)


def test_apply_header_replaces_old(editor):
    editor.setPlainText("contenido")
    apply_header(editor, "Versión 1")
    apply_header(editor, "Versión 2")
    assert len(_blocks_of_kind(editor, HEADER_MARK)) == 1
    assert editor.document().firstBlock().text() == "Versión 2"


def test_remove_header_footer(editor):
    editor.setPlainText("contenido")
    apply_header(editor, "H")
    apply_footer(editor, "F")
    remove_header(editor)
    remove_footer(editor)
    assert _blocks_of_kind(editor, HEADER_MARK) == []
    assert _blocks_of_kind(editor, FOOTER_MARK) == []


def test_insert_field_and_refresh(editor):
    editor.setPlainText("texto")
    editor.moveCursor(editor.textCursor().MoveOperation.End)
    insert_field(editor, "PAGE")
    assert "1" in editor.toPlainText()
    refresh_fields(editor)
    assert "1" in editor.toPlainText()


def test_set_numbering_format(editor):
    set_numbering_format(editor, "roman")
    assert editor.document().property("rword:page-numbering") == "roman"


def test_numbering_roman_used_in_field(editor):
    from PySide6.QtGui import QTextBlockFormat, QTextFormat

    editor.setPlainText("a\nb\nc")
    block = editor.document().findBlockByNumber(1)
    cursor = editor.textCursor()
    cursor.setPosition(block.position())
    fmt = QTextBlockFormat()
    fmt.setPageBreakPolicy(QTextFormat.PageBreakFlag.PageBreak_AlwaysBefore)
    cursor.mergeBlockFormat(fmt)
    set_numbering_format(editor, "roman")
    assert resolve_field("PAGE", editor, 2) == "II"

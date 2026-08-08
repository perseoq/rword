import pytest
from PySide6.QtGui import QTextFormat, QTextTable

from rword.core.pages import (
    MM_TO_PX,
    PageSetup,
    apply_page_setup,
    current_page_setup,
    insert_page_break,
    insert_section_break,
    set_columns,
)


def _table(editor):
    for frame in editor.document().rootFrame().childFrames():
        if isinstance(frame, QTextTable):
            return frame
    return None


def test_page_setup_a4_dimensions():
    setup = PageSetup()
    size = setup.page_size_px()
    assert size.width() == pytest.approx(210 * MM_TO_PX)
    assert size.height() == pytest.approx(297 * MM_TO_PX)


def test_page_setup_landscape_swaps():
    setup = PageSetup(orientation="landscape")
    size = setup.page_size_px()
    assert size.width() > size.height()


def test_page_setup_margins():
    setup = PageSetup(left_margin_mm=10, top_margin_mm=20)
    assert setup.left_margin_mm == 10
    assert setup.top_margin_mm == 20


def test_apply_and_read_back(editor):
    setup = PageSetup(
        size="Letter",
        orientation="portrait",
        left_margin_mm=30,
        right_margin_mm=20,
        top_margin_mm=15,
        bottom_margin_mm=10,
    )
    apply_page_setup(editor, setup)
    read_back = current_page_setup(editor)
    assert read_back.size == "Letter"
    assert read_back.orientation == "portrait"
    assert read_back.left_margin_mm == pytest.approx(30)
    assert read_back.right_margin_mm == pytest.approx(20)


def test_apply_landscape_read_back(editor):
    setup = PageSetup(size="A4", orientation="landscape")
    apply_page_setup(editor, setup)
    read_back = current_page_setup(editor)
    assert read_back.orientation == "landscape"
    assert read_back.size == "A4"


def test_insert_page_break(editor):
    editor.insertPlainText("primera página")
    insert_page_break(editor)
    editor.insertPlainText("segunda página")
    block = editor.document().begin().next()
    fmt = block.blockFormat()
    assert fmt.pageBreakPolicy() & QTextFormat.PageBreakFlag.PageBreak_AlwaysBefore


def test_insert_section_break_creates_marker(editor):
    editor.insertPlainText("sección uno")
    insert_section_break(editor)
    assert "Salto de sección" in editor.toPlainText()


def test_set_columns_two(editor):
    editor.setPlainText("a\nb\nc\nd")
    set_columns(editor, 2)
    table = _table(editor)
    assert table is not None
    assert table.columns() == 2
    assert table.rows() == 2


def test_set_columns_restores(editor):
    editor.setPlainText("a\nb\nc\nd")
    set_columns(editor, 2)
    set_columns(editor, 1)
    assert _table(editor) is None


def test_editor_line_numbers_toggle(editor):
    assert not editor.line_numbers_enabled()
    editor.set_line_numbers_enabled(True)
    assert editor.line_numbers_enabled()
    assert editor.viewportMargins().left() > 0
    editor.set_line_numbers_enabled(False)
    assert editor.viewportMargins().left() == 0


def test_editor_watermark(editor):
    editor.set_watermark("CONFIDENCIAL")
    assert editor.watermark() == "CONFIDENCIAL"
    editor.set_watermark("")
    assert editor.watermark() == ""


def test_page_setup_roundtrip_dict():
    setup = PageSetup(
        size="A5",
        orientation="landscape",
        left_margin_mm=12,
        page_color="#f0f0f0",
        watermark="BORRADOR",
    )
    restored = PageSetup.from_dict(
        {**setup.__dict__, "unknown": True}
    )
    assert restored.size == "A5"
    assert restored.orientation == "landscape"
    assert restored.watermark == "BORRADOR"


def test_main_window_page_break(main_window):
    main_window._editor.insertPlainText("contenido")
    main_window._insert_page_break()
    main_window._editor.insertPlainText("más")
    block = main_window._editor.document().begin().next()
    assert (
        block.blockFormat().pageBreakPolicy()
        & QTextFormat.PageBreakFlag.PageBreak_AlwaysBefore
    )


def test_main_window_line_numbers(main_window):
    main_window.line_numbers_action.setChecked(True)
    main_window._toggle_line_numbers(True)
    assert main_window._editor.line_numbers_enabled()

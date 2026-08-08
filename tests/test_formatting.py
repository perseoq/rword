from PySide6.QtGui import QColor, QFont, QTextCharFormat

from rword.core import formatting


def _select(editor, start, end):
    cursor = editor.textCursor()
    cursor.setPosition(start)
    cursor.setPosition(end, cursor.MoveMode.KeepAnchor)
    editor.setTextCursor(cursor)


def _cf(editor):
    return editor.currentCharFormat()


def test_toggle_bold(editor):
    editor.insertPlainText("hola")
    editor.selectAll()
    formatting.toggle_bold(editor)
    assert _cf(editor).fontWeight() >= QFont.Weight.Bold
    formatting.toggle_bold(editor)
    assert _cf(editor).fontWeight() < QFont.Weight.Bold


def test_toggle_italic(editor):
    editor.insertPlainText("hola")
    editor.selectAll()
    formatting.toggle_italic(editor)
    assert _cf(editor).fontItalic()
    formatting.toggle_italic(editor)
    assert not _cf(editor).fontItalic()


def test_toggle_underline(editor):
    editor.insertPlainText("hola")
    editor.selectAll()
    formatting.toggle_underline(editor)
    assert _cf(editor).fontUnderline()


def test_toggle_strikeout(editor):
    editor.insertPlainText("hola")
    editor.selectAll()
    formatting.toggle_strikeout(editor)
    assert _cf(editor).fontStrikeOut()


def test_toggle_superscript(editor):
    editor.insertPlainText("x2")
    editor.selectAll()
    formatting.toggle_superscript(editor)
    assert (
        _cf(editor).verticalAlignment()
        == QTextCharFormat.VerticalAlignment.AlignSuperScript
    )
    formatting.toggle_superscript(editor)
    assert (
        _cf(editor).verticalAlignment()
        == QTextCharFormat.VerticalAlignment.AlignNormal
    )


def test_toggle_subscript(editor):
    editor.insertPlainText("H2O")
    editor.selectAll()
    formatting.toggle_subscript(editor)
    assert (
        _cf(editor).verticalAlignment()
        == QTextCharFormat.VerticalAlignment.AlignSubScript
    )


def test_set_font_family(editor):
    editor.insertPlainText("texto")
    editor.selectAll()
    formatting.set_font_family(editor, "Arial")
    assert "Arial" in _cf(editor).fontFamilies()


def test_set_font_size(editor):
    editor.insertPlainText("texto")
    editor.selectAll()
    formatting.set_font_size(editor, 20)
    assert _cf(editor).fontPointSize() == 20.0


def test_change_font_size(editor):
    editor.insertPlainText("texto")
    editor.selectAll()
    formatting.set_font_size(editor, 12)
    formatting.change_font_size(editor, 4)
    assert _cf(editor).fontPointSize() == 16.0
    formatting.change_font_size(editor, -4)
    assert _cf(editor).fontPointSize() == 12.0


def test_set_text_color(editor):
    editor.insertPlainText("rojo")
    editor.selectAll()
    formatting.set_text_color(editor, QColor("#ff0000"))
    assert _cf(editor).foreground().color().name() == "#ff0000"


def test_set_highlight(editor):
    editor.insertPlainText("amarillo")
    editor.selectAll()
    formatting.set_highlight(editor, QColor("#ffff00"))
    assert _cf(editor).background().color().name() == "#ffff00"


def test_set_letter_spacing(editor):
    editor.insertPlainText("espaciado")
    editor.selectAll()
    formatting.set_letter_spacing(editor, 150)
    assert _cf(editor).fontLetterSpacing() == 150.0


def test_clear_formatting(editor):
    editor.insertPlainText("texto")
    editor.selectAll()
    formatting.toggle_bold(editor)
    formatting.toggle_italic(editor)
    formatting.toggle_underline(editor)
    formatting.set_text_color(editor, QColor("#ff0000"))
    formatting.clear_formatting(editor)
    cf = _cf(editor)
    assert not cf.fontItalic()
    assert not cf.fontUnderline()
    assert cf.fontWeight() < QFont.Weight.Bold


def test_apply_case_upper(editor):
    editor.insertPlainText("hola mundo")
    editor.selectAll()
    formatting.apply_case(editor, "upper")
    assert editor.toPlainText() == "HOLA MUNDO"


def test_apply_case_lower(editor):
    editor.insertPlainText("HOLA Mundo")
    editor.selectAll()
    formatting.apply_case(editor, "lower")
    assert editor.toPlainText() == "hola mundo"


def test_apply_case_title(editor):
    editor.insertPlainText("el perro corre")
    editor.selectAll()
    formatting.apply_case(editor, "title")
    assert editor.toPlainText() == "El Perro Corre"


def test_apply_case_toggle(editor):
    editor.insertPlainText("AbC")
    editor.selectAll()
    formatting.apply_case(editor, "toggle")
    assert editor.toPlainText() == "aBc"


def test_apply_case_sentence(editor):
    editor.insertPlainText("hola mundo. esto es una prueba!")
    editor.selectAll()
    formatting.apply_case(editor, "sentence")
    assert editor.toPlainText() == "Hola mundo. Esto es una prueba!"


def test_apply_case_no_selection(editor):
    editor.insertPlainText("sin selección")
    formatting.apply_case(editor, "upper")
    assert editor.toPlainText() == "sin selección"


def test_format_bar_toggles(main_window):
    bar = main_window.format_bar
    editor = main_window._editor
    editor.insertPlainText("negrita")
    editor.selectAll()
    bar.bold_action.trigger()
    assert editor.currentCharFormat().fontWeight() >= QFont.Weight.Bold

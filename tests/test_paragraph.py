from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QTextListFormat

from rword.core import paragraph


def _block_fmt(editor):
    return editor.textCursor().block().blockFormat()


def _select_block(editor, text):
    editor.insertPlainText(text)
    cursor = editor.textCursor()
    cursor.setPosition(0)
    cursor.setPosition(len(text), cursor.MoveMode.KeepAnchor)
    editor.setTextCursor(cursor)


def test_align_left(editor):
    _select_block(editor, "texto")
    paragraph.set_alignment(editor, "left")
    assert paragraph.current_alignment(editor) == Qt.AlignmentFlag.AlignLeft


def test_align_center(editor):
    _select_block(editor, "texto")
    paragraph.set_alignment(editor, "center")
    assert paragraph.current_alignment(editor) == Qt.AlignmentFlag.AlignCenter


def test_align_right(editor):
    _select_block(editor, "texto")
    paragraph.set_alignment(editor, "right")
    assert paragraph.current_alignment(editor) == Qt.AlignmentFlag.AlignRight


def test_align_justify(editor):
    _select_block(editor, "texto")
    paragraph.set_alignment(editor, "justify")
    assert paragraph.current_alignment(editor) == Qt.AlignmentFlag.AlignJustify


def test_left_indent(editor):
    _select_block(editor, "texto")
    paragraph.set_left_indent(editor, 40)
    assert _block_fmt(editor).leftMargin() == 40


def test_right_indent(editor):
    _select_block(editor, "texto")
    paragraph.set_right_indent(editor, 30)
    assert _block_fmt(editor).rightMargin() == 30


def test_first_line_indent(editor):
    _select_block(editor, "texto")
    paragraph.set_first_line_indent(editor, 25)
    assert _block_fmt(editor).textIndent() == 25


def test_hanging_indent(editor):
    _select_block(editor, "texto")
    paragraph.set_hanging_indent(editor, 30)
    fmt = _block_fmt(editor)
    assert fmt.leftMargin() == 30
    assert fmt.textIndent() == -30


def test_increase_decrease_indent(editor):
    _select_block(editor, "texto")
    paragraph.increase_indent(editor)
    assert _block_fmt(editor).leftMargin() == paragraph.INDENT_STEP
    paragraph.increase_indent(editor)
    assert _block_fmt(editor).leftMargin() == paragraph.INDENT_STEP * 2
    paragraph.decrease_indent(editor)
    assert _block_fmt(editor).leftMargin() == paragraph.INDENT_STEP
    paragraph.decrease_indent(editor)
    paragraph.decrease_indent(editor)
    assert _block_fmt(editor).leftMargin() == 0


def test_line_spacing(editor):
    _select_block(editor, "texto")
    paragraph.set_line_spacing(editor, 1.5)
    assert paragraph.current_line_spacing(editor) == 1.5
    paragraph.set_line_spacing(editor, 2.0)
    assert paragraph.current_line_spacing(editor) == 2.0


def test_space_before_after(editor):
    _select_block(editor, "texto")
    paragraph.set_space_before(editor, 12)
    paragraph.set_space_after(editor, 18)
    assert _block_fmt(editor).topMargin() == 12
    assert _block_fmt(editor).bottomMargin() == 18


def test_toggle_bullets(editor):
    editor.insertPlainText("primer elemento")
    paragraph.toggle_bullets(editor)
    assert paragraph.current_list_style(editor) == QTextListFormat.Style.ListDisc
    paragraph.toggle_bullets(editor)
    assert paragraph.current_list_style(editor) is None


def test_toggle_numbering(editor):
    editor.insertPlainText("elemento")
    paragraph.toggle_numbering(editor)
    assert (
        paragraph.current_list_style(editor) == QTextListFormat.Style.ListDecimal
    )
    paragraph.toggle_numbering(editor)
    assert paragraph.current_list_style(editor) is None


def test_list_level(editor):
    editor.insertPlainText("item")
    paragraph.toggle_bullets(editor)
    paragraph.set_list_level(editor, 2)
    cursor = editor.textCursor()
    assert cursor.currentList().format().indent() == 2


def test_paragraph_shading(editor):
    _select_block(editor, "texto")
    paragraph.set_paragraph_shading(editor, QColor("#ffffcc"))
    assert _block_fmt(editor).background().color().name() == "#ffffcc"


def test_tab_stop_distance(editor):
    paragraph.set_tab_stop_distance(editor, 80)
    assert paragraph.current_tab_stop_distance(editor) == 80


def test_clear_paragraph_format(editor):
    _select_block(editor, "texto")
    paragraph.set_alignment(editor, "center")
    paragraph.set_left_indent(editor, 50)
    paragraph.set_line_spacing(editor, 2.0)
    paragraph.clear_paragraph_format(editor)
    fmt = _block_fmt(editor)
    assert fmt.alignment() == Qt.AlignmentFlag.AlignLeft
    assert fmt.leftMargin() == 0
    assert paragraph.current_line_spacing(editor) == 1.0


def test_paragraph_bar_alignment_sync(main_window):
    bar = main_window.paragraph_bar
    editor = main_window._editor
    editor.insertPlainText("centro")
    editor.selectAll()
    paragraph.set_alignment(editor, "center")
    bar._sync()
    assert bar.align_center_action.isChecked()
    assert not bar.align_left_action.isChecked()


def test_paragraph_bar_bullets(main_window):
    bar = main_window.paragraph_bar
    editor = main_window._editor
    editor.insertPlainText("lista")
    bar.bullets_action.trigger()
    assert (
        editor.textCursor().currentList().format().style()
        == QTextListFormat.Style.ListDisc
    )


def test_paragraph_dialog_applies_values(main_window, editor_factory=None):
    editor = main_window._editor
    editor.insertPlainText("parrafo")
    editor.selectAll()
    from rword.ui.dialogs.paragraph import ParagraphDialog

    dialog = ParagraphDialog(editor, main_window)
    dialog._left_spin.setValue(60)
    dialog._spacing_spin.setValue(1.5)
    dialog._apply()
    fmt = editor.textCursor().block().blockFormat()
    assert fmt.leftMargin() == 60
    assert fmt.lineHeight() == 150.0
    dialog.deleteLater()

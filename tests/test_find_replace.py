import pytest

from rword.ui.dialogs.find_replace import FindReplaceDialog
from rword.ui.dialogs.go_to import GoToDialog


@pytest.fixture
def dialog(editor):
    dlg = FindReplaceDialog(editor)
    yield dlg
    dlg.deleteLater()


@pytest.fixture
def go_dialog(editor):
    dlg = GoToDialog(editor)
    yield dlg
    dlg.deleteLater()


def _text(editor):
    return editor.toPlainText()


def test_find_next_selects_match(dialog, editor):
    editor.setPlainText("hola mundo hola")
    dialog._find_input.setText("mundo")
    dialog._find_next()
    cursor = editor.textCursor()
    assert cursor.selectedText() == "mundo"


def test_find_next_wraps_around(dialog, editor):
    editor.setPlainText("abc abc")
    cursor = editor.textCursor()
    cursor.setPosition(len("abc abc"))
    editor.setTextCursor(cursor)
    dialog._find_input.setText("abc")
    dialog._find_next()
    assert editor.textCursor().selectedText() == "abc"
    assert editor.textCursor().selectionStart() == 0


def test_find_previous_selects_last_match(dialog, editor):
    editor.setPlainText("uno dos tres")
    dialog._find_input.setText("s")
    dialog._find_previous()
    assert editor.textCursor().selectedText() == "s"


def test_find_case_insensitive_by_default(dialog, editor):
    editor.setPlainText("HOLA hola")
    dialog._find_input.setText("hola")
    dialog._find_next()
    assert editor.textCursor().selectedText() == "HOLA"


def test_find_case_sensitive(dialog, editor):
    editor.setPlainText("HOLA hola")
    dialog._find_input.setText("hola")
    dialog._case_check.setChecked(True)
    dialog._find_next()
    assert editor.textCursor().selectedText() == "HOLA"


def test_find_case_sensitive_skips_other_case(dialog, editor):
    editor.setPlainText("HOLA hola")
    dialog._find_input.setText("HOLA")
    dialog._case_check.setChecked(True)
    dialog._find_next()
    dialog._find_next()
    assert editor.textCursor().selectedText() == "HOLA"


def test_replace_changes_text(dialog, editor):
    editor.setPlainText("hola mundo")
    dialog._find_input.setText("mundo")
    dialog._replace_input.setText("rword")
    dialog._find_next()
    dialog._replace()
    assert _text(editor) == "hola rword"


def test_replace_all_changes_all_matches(dialog, editor):
    editor.setPlainText("a1 b2 a3")
    dialog._find_input.setText("a")
    dialog._replace_input.setText("X")
    dialog._replace_all()
    assert _text(editor) == "X1 b2 X3"


def test_replace_all_handles_overlap(dialog, editor):
    editor.setPlainText("aaaa")
    dialog._find_input.setText("aa")
    dialog._replace_input.setText("Z")
    dialog._replace_all()
    assert _text(editor) == "ZZ"


def test_whole_word_option(dialog, editor):
    editor.setPlainText("casa casamiento casa")
    dialog._find_input.setText("casa")
    dialog._word_check.setChecked(True)
    dialog._replace_input.setText("X")
    dialog._replace_all()
    assert _text(editor) == "X casamiento X"


def test_whole_word_without_option_matches_substrings(dialog, editor):
    editor.setPlainText("casa casamiento casa")
    dialog._find_input.setText("casa")
    dialog._replace_input.setText("X")
    dialog._replace_all()
    assert _text(editor) == "X Xmiento X"


def test_highlight_matches_sets_extra_selections(dialog, editor):
    editor.setPlainText("hola hola hola")
    dialog._find_input.setText("hola")
    dialog._on_find_changed()
    assert len(editor.extraSelections()) == 3


def test_highlight_cleared_when_empty(dialog, editor):
    editor.setPlainText("hola")
    dialog._find_input.setText("hola")
    dialog._on_find_changed()
    assert len(editor.extraSelections()) == 1
    dialog._find_input.setText("")
    dialog._on_find_changed()
    assert editor.extraSelections() == []


def test_go_to_line(go_dialog, editor):
    editor.setPlainText("línea1\nlínea2\nlínea3")
    go_dialog._line_input.setText("3")
    go_dialog._go_to_line()
    cursor = editor.textCursor()
    assert cursor.blockNumber() == 2


def test_go_to_line_single_line_document(go_dialog, editor):
    editor.setPlainText("única línea")
    go_dialog._line_input.setText("1")
    go_dialog._go_to_line()
    assert editor.textCursor().blockNumber() == 0

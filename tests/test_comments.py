from PySide6.QtGui import QTextCursor

from rword.core import comments
from rword.core.comments import (
    accept_all_changes,
    add_comment,
    compare_documents,
    delete_comment,
    deleted_format,
    edit_comment,
    goto_comment,
    inserted_format,
    is_inserted,
    reject_all_changes,
    reply_comment,
    set_resolved,
)
from rword.ui.comments_panel import CommentsPanel


def _select(editor, start, end):
    cursor = editor.textCursor()
    cursor.setPosition(start)
    cursor.setPosition(end, cursor.MoveMode.KeepAnchor)
    editor.setTextCursor(cursor)


def test_add_comment_on_selection(editor):
    editor.insertPlainText("texto con selección")
    _select(editor, 6, 10)
    comment = add_comment(editor, "revisar esto", "Ana")
    assert comment.start == 6
    assert comment.length == 4
    assert len(comments.comments(editor)) == 1


def test_add_comment_at_cursor(editor):
    editor.insertPlainText("texto")
    editor.moveCursor(QTextCursor.MoveOperation.End)
    comment = add_comment(editor, "nota")
    assert comment.length == 0


def test_edit_comment(editor):
    editor.insertPlainText("abc")
    comment = add_comment(editor, "original")
    assert edit_comment(editor, comment.id, "editado")
    assert comments.comments(editor)[0].text == "editado"
    assert not edit_comment(editor, "no-existe", "x")


def test_reply_comment(editor):
    editor.insertPlainText("abc")
    comment = add_comment(editor, "mensaje")
    assert reply_comment(editor, comment.id, "Luis", "estoy de acuerdo")
    assert len(comments.comments(editor)[0].replies) == 1
    assert not reply_comment(editor, "no-existe", "L", "x")


def test_resolve_and_delete(editor):
    editor.insertPlainText("abc")
    comment = add_comment(editor, "listo")
    assert set_resolved(editor, comment.id, True)
    assert comments.comments(editor)[0].resolved
    assert delete_comment(editor, comment.id)
    assert comments.comments(editor) == []
    assert not delete_comment(editor, "no-existe")


def test_goto_comment(editor):
    editor.insertPlainText("hola mundo")
    _select(editor, 5, 10)
    comment = add_comment(editor, "nota")
    editor.moveCursor(QTextCursor.MoveOperation.End)
    assert goto_comment(editor, comment.id)
    assert editor.textCursor().hasSelection()
    assert editor.textCursor().selectionStart() == 5


def test_comment_highlight_selections(editor):
    editor.insertPlainText("resaltar")
    _select(editor, 0, 4)
    add_comment(editor, "nota")
    selections = comments.comment_selections(editor)
    assert len(selections) == 1


def test_track_changes_insert(editor):
    from PySide6.QtTest import QTest

    editor.set_track_changes(True)
    editor.setFocus()
    QTest.keyClicks(editor, "hola")
    found = False
    block = editor.document().begin()
    while block.isValid():
        iterator = block.begin()
        while not iterator.atEnd():
            fmt = iterator.fragment().charFormat()
            if is_inserted(fmt):
                found = True
            iterator += 1
        block = block.next()
    assert found


def test_mark_deletion(editor):
    editor.insertPlainText("hola")
    editor.moveCursor(QTextCursor.MoveOperation.End)
    cursor = editor.textCursor()
    cursor.setPosition(2)
    cursor.setPosition(3, cursor.MoveMode.KeepAnchor)
    editor.setTextCursor(cursor)
    fmt = deleted_format()
    cursor.mergeCharFormat(fmt)


def test_accept_all_changes_removes_deleted(editor):
    editor.insertPlainText("hola mundo")
    cursor = editor.textCursor()
    cursor.setPosition(4)
    cursor.setPosition(5, cursor.MoveMode.KeepAnchor)
    editor.setTextCursor(cursor)
    cursor.mergeCharFormat(deleted_format())
    assert accept_all_changes(editor) >= 1
    assert " " not in editor.toPlainText().replace("hola", "")


def test_reject_all_changes_removes_inserted(editor):
    editor.insertPlainText("hola")
    cursor = editor.textCursor()
    cursor.movePosition(cursor.MoveOperation.End)
    editor.setTextCursor(cursor)
    cursor.insertText(" extra", inserted_format())
    assert reject_all_changes(editor) >= 1
    assert "extra" not in editor.toPlainText()


def test_compare_documents(editor):
    compare_documents(editor, "línea uno\nlínea dos", "línea uno\nlínea nueva\nlínea dos")
    text = editor.toPlainText()
    assert "línea uno" in text
    assert "línea nueva" in text
    found_inserted = False
    block = editor.document().begin()
    while block.isValid():
        iterator = block.begin()
        while not iterator.atEnd():
            fmt = iterator.fragment().charFormat()
            found_inserted = found_inserted or is_inserted(fmt)
            iterator += 1
        block = block.next()
    assert found_inserted


def test_comments_panel_lists(main_window):
    panel = CommentsPanel(main_window._editor, main_window)
    main_window._editor.insertPlainText("contenido")
    add_comment(main_window._editor, "revisar")
    panel.refresh()
    assert panel._list.count() == 1
    panel.deleteLater()


def test_track_changes_toggle(main_window):
    main_window._toggle_track_changes(True)
    assert main_window._editor.track_changes()
    main_window._toggle_track_changes(False)
    assert not main_window._editor.track_changes()

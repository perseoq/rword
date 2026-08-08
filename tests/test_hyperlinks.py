from PySide6.QtGui import QTextCursor

from rword.core import hyperlinks
from rword.core.hyperlinks import (
    add_bookmark,
    bookmarks,
    goto_bookmark,
    headings,
    hyperlink_at_cursor,
    insert_hyperlink,
    remove_bookmark,
    remove_hyperlink,
)
from rword.ui.navigation_panel import NavigationPanel


def test_insert_hyperlink_on_selection(editor):
    editor.insertPlainText("visita el sitio")
    cursor = editor.textCursor()
    cursor.setPosition(0)
    cursor.setPosition(len("visita"), cursor.MoveMode.KeepAnchor)
    editor.setTextCursor(cursor)
    insert_hyperlink(editor, "visita", "https://example.com")
    probe = QTextCursor(editor.document())
    probe.setPosition(cursor.selectionStart() + 1)
    fmt = probe.charFormat()
    assert fmt.isAnchor()
    assert fmt.anchorHref() == "https://example.com"


def test_insert_hyperlink_new_text(editor):
    insert_hyperlink(editor, "enlace", "mailto:test@example.com")
    assert "enlace" in editor.toPlainText()
    info = hyperlink_at_cursor(editor)
    assert info is not None
    assert info[1] == "mailto:test@example.com"


def test_hyperlink_at_cursor(editor):
    editor.insertPlainText("texto")
    insert_hyperlink(editor, "enlace", "https://example.org")
    editor.moveCursor(QTextCursor.MoveOperation.PreviousCharacter)
    info = hyperlink_at_cursor(editor)
    assert info is not None
    assert info[1] == "https://example.org"


def test_remove_hyperlink(editor):
    insert_hyperlink(editor, "enlace", "https://example.com")
    editor.moveCursor(QTextCursor.MoveOperation.PreviousCharacter)
    editor.moveCursor(
        QTextCursor.MoveOperation.StartOfWord,
        QTextCursor.MoveMode.KeepAnchor,
    )
    remove_hyperlink(editor)


def test_add_and_goto_bookmark(editor):
    editor.insertPlainText("primera\nsegunda")
    cursor = editor.textCursor()
    cursor.setPosition(len("primera\n"))
    editor.setTextCursor(cursor)
    assert add_bookmark(editor, "ini")
    assert "ini" in bookmarks(editor)
    cursor.setPosition(0)
    editor.setTextCursor(cursor)
    assert goto_bookmark(editor, "ini")
    assert editor.textCursor().position() == len("primera\n")


def test_remove_bookmark(editor):
    editor.insertPlainText("x")
    add_bookmark(editor, "a")
    assert remove_bookmark(editor, "a")
    assert "a" not in bookmarks(editor)
    assert not remove_bookmark(editor, "inexistente")


def test_heading_level_detection(editor):
    editor.setHtml(
        "<h1>Título grande</h1><p>párrafo normal</p><h2>Sub</h2>"
    )
    found = headings(editor)
    assert len(found) >= 2
    assert found[0][1] == 1


def test_headings_empty(editor):
    editor.setPlainText("sin títulos")
    assert headings(editor) == []


def test_navigation_panel_lists_headings(main_window, editor):
    panel = NavigationPanel(main_window._editor, main_window)
    main_window._editor.setHtml(
        "<h1>Capítulo 1</h1><p>texto</p><h2>Sección</h2>"
    )
    panel.refresh()
    assert panel._headings_list.count() >= 2
    panel.deleteLater()


def test_navigation_panel_bookmarks(main_window):
    panel = NavigationPanel(main_window._editor, main_window)
    main_window._editor.insertPlainText("contenido")
    add_bookmark(main_window._editor, "m1")
    panel.refresh()
    assert panel._bookmarks_list.count() == 1
    panel.deleteLater()


def test_goto_block(editor):
    editor.setPlainText("línea1\nlínea2\nlínea3")
    hyperlinks.goto_block(editor, 2)
    assert editor.textCursor().blockNumber() == 2

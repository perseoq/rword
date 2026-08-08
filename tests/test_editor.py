

def test_editor_starts_empty(editor):
    assert editor.toPlainText() == ""
    assert editor.file_path is None
    assert editor.word_count() == 0
    assert editor.character_count() == 0


def test_editor_counts(editor):
    editor.setPlainText("hola mundo de prueba")
    assert editor.word_count() == 4
    assert editor.character_count() == len("hola mundo de prueba")


def test_editor_load_and_save_plain_text(editor, tmp_path):
    source = tmp_path / "source.txt"
    source.write_text("línea uno\nlínea dos", encoding="utf-8")
    editor.load_file(source)
    assert editor.toPlainText() == "línea uno\nlínea dos"
    assert editor.file_path == source
    assert not editor.document().isModified()

    cursor = editor.textCursor()
    cursor.movePosition(cursor.MoveOperation.End)
    editor.setTextCursor(cursor)
    editor.insertPlainText(" añadida")
    target = tmp_path / "target.txt"
    editor.save_file(target)
    assert target.read_text(encoding="utf-8") == "línea uno\nlínea dos añadida"
    assert editor.file_path == target
    assert not editor.document().isModified()


def test_editor_load_html(editor, tmp_path):
    source = tmp_path / "doc.html"
    source.write_text("<html><body><b>negrita</b></body></html>", encoding="utf-8")
    editor.load_file(source)
    assert "<b" in editor.toHtml()
    assert editor.file_path == source


def test_editor_save_html_preserves_extension(editor, tmp_path):
    editor.setHtml("<p>contenido</p>")
    target = tmp_path / "doc.html"
    editor.save_file(target)
    assert "<p" in target.read_text(encoding="utf-8")

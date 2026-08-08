

def test_main_window_title(main_window):
    assert "rword" in main_window.windowTitle()


def test_main_window_has_editor(main_window):
    assert main_window._editor is not None


def test_new_document_clears_editor(main_window):
    main_window._editor.setPlainText("contenido a borrar")
    main_window._editor.document().setModified(False)
    main_window._new_document()
    assert main_window._editor.toPlainText() == ""


def test_save_document_as_writes_file(main_window, tmp_path, monkeypatch):
    main_window._editor.setPlainText("texto de prueba")
    target = tmp_path / "out.txt"

    def fake_dialog(parent, title, default, file_filter):
        return str(target), file_filter

    monkeypatch.setattr(
        "PySide6.QtWidgets.QFileDialog.getSaveFileName", fake_dialog
    )
    main_window._save_document_as()
    assert target.read_text(encoding="utf-8") == "texto de prueba"
    assert main_window._editor.file_path == target
    assert not main_window._editor.document().isModified()


def test_save_document_as_adds_default_extension(main_window, tmp_path, monkeypatch):
    main_window._editor.setPlainText("sin extension")
    target = tmp_path / "out"

    def fake_dialog(parent, title, default, file_filter):
        return str(target), "Documentos de texto (*.txt *.md *.rst *.log)"

    monkeypatch.setattr(
        "PySide6.QtWidgets.QFileDialog.getSaveFileName", fake_dialog
    )
    main_window._save_document_as()
    assert main_window._editor.file_path == tmp_path / "out.txt"


def test_open_document_loads_file(main_window, tmp_path, monkeypatch):
    source = tmp_path / "in.txt"
    source.write_text("contenido abierto", encoding="utf-8")

    def fake_dialog(parent, title, directory, file_filter):
        return str(source), file_filter

    monkeypatch.setattr(
        "PySide6.QtWidgets.QFileDialog.getOpenFileName", fake_dialog
    )
    main_window._open_document()
    assert main_window._editor.toPlainText() == "contenido abierto"
    assert main_window._editor.file_path == source
    assert not main_window._editor.document().isModified()


def test_statusbar_shows_counts(main_window):
    main_window._editor.setPlainText("palabra1 palabra2")
    main_window._update_statusbar()
    assert "2" in main_window.words_label.text()
    assert main_window.chars_label.text() == f"Caracteres: {len('palabra1 palabra2')}"


def test_title_shows_modified_marker(main_window):
    main_window._editor.insertPlainText("cambio")
    assert main_window._editor.document().isModified()
    main_window._update_title()
    assert "*" in main_window.windowTitle()

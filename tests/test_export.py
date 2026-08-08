import zipfile

from rword.core.export import (
    EPUB_MIMETYPE,
    ODT_MIMETYPE,
    export_epub,
    export_html,
    export_odt,
    export_pdf,
    export_rtf,
    export_text,
)


def _fill(editor):
    editor.setPlainText("Hola mundo.\nSegunda línea.")


def test_export_text(editor, tmp_path):
    _fill(editor)
    path = tmp_path / "out.txt"
    export_text(editor, path)
    assert path.read_text(encoding="utf-8") == "Hola mundo.\nSegunda línea."


def test_export_html(editor, tmp_path):
    _fill(editor)
    path = tmp_path / "out.html"
    export_html(editor, path)
    content = path.read_text(encoding="utf-8")
    assert "<html>" in content
    assert "Hola mundo" in content


def test_export_rtf(editor, tmp_path):
    _fill(editor)
    path = tmp_path / "out.rtf"
    export_rtf(editor, path)
    content = path.read_text(encoding="utf-8")
    assert content.startswith("{\\rtf1")
    assert "Hola mundo" in content


def test_export_pdf(editor, tmp_path):
    _fill(editor)
    path = tmp_path / "out.pdf"
    export_pdf(editor, path)
    assert path.exists()
    assert path.stat().st_size > 100
    assert path.read_bytes().startswith(b"%PDF")


def test_export_odt(editor, tmp_path):
    _fill(editor)
    path = tmp_path / "out.odt"
    export_odt(editor, path)
    assert path.exists()
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        assert "mimetype" in names
        assert "content.xml" in names
        assert archive.read("mimetype") == ODT_MIMETYPE.encode()
        content = archive.read("content.xml").decode("utf-8")
        assert "Hola mundo" in content


def test_export_epub(editor, tmp_path):
    _fill(editor)
    path = tmp_path / "out.epub"
    export_epub(editor, path)
    assert path.exists()
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        assert "mimetype" in names
        assert "META-INF/container.xml" in names
        assert "OEBPS/content.xhtml" in names
        assert archive.read("mimetype") == EPUB_MIMETYPE.encode()


def test_main_window_export_txt(main_window, tmp_path, monkeypatch):
    main_window._editor.setPlainText("contenido exportable")
    target = tmp_path / "salida.txt"

    def fake_dialog(parent, title, default, file_filter):
        return str(target), file_filter

    monkeypatch.setattr(
        "PySide6.QtWidgets.QFileDialog.getSaveFileName", fake_dialog
    )
    main_window._export("texto", "*.txt", export_text)
    assert target.read_text(encoding="utf-8") == "contenido exportable"

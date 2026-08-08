
from rword.core.accessibility import (
    check_accessibility,
    image_alt_text,
    image_alt_text_at_cursor,
    set_image_alt_text,
)
from rword.core.images import insert_image_from_data
from rword.core.themes import default_themes


def _insert_image(editor):
    from PySide6.QtGui import QColor, QImage

    image = QImage(40, 30, QImage.Format.Format_RGB32)
    image.fill(QColor("blue"))
    return insert_image_from_data(editor, image)


def test_set_image_alt_text(editor):
    assert _insert_image(editor)
    assert set_image_alt_text(editor, "Gráfico de ventas")
    assert image_alt_text_at_cursor(editor) == "Gráfico de ventas"


def test_set_alt_text_no_image(editor):
    editor.insertPlainText("sin imagen")
    assert not set_image_alt_text(editor, "x")


def test_check_accessibility_no_issues(editor):
    editor.setHtml("<h1>Título</h1><p>Texto con palabras normales.</p>")
    issues = check_accessibility(editor)
    assert issues == []


def test_check_accessibility_empty_document(editor):
    issues = check_accessibility(editor)
    assert any(category == "Estructura" for category, _ in issues)


def test_check_accessibility_image_without_alt(editor):
    assert _insert_image(editor)
    issues = check_accessibility(editor)
    assert any(category == "Imágenes" for category, _ in issues)


def test_check_accessibility_long_word(editor):
    long_word = "supercalifragilisticoespialidosoextraordinariamentelarguísimo"
    editor.setHtml(f"<h1>Capítulo</h1><p>Una {long_word} palabra.</p>")
    issues = check_accessibility(editor)
    assert any(category == "Legibilidad" for category, _ in issues)


def test_image_alt_text_by_position(editor):
    assert _insert_image(editor)
    from rword.core.images import _image_position

    position = _image_position(editor)
    assert image_alt_text(editor, position) == ""


def test_high_contrast_theme_available():
    names = [theme.name for theme in default_themes()]
    assert "Alto contraste" in names


def test_high_contrast_colors():
    theme = next(t for t in default_themes() if t.name == "Alto contraste")
    assert theme.page_color == "#000000"
    assert theme.text_color == "#ffffff"


def test_main_window_high_contrast(main_window):
    main_window._apply_high_contrast()
    assert main_window._theme_manager.current.name == "Alto contraste"


def test_immersive_toggle(main_window):
    main_window.show()
    main_window._toggle_immersive(True)
    assert not main_window.menuBar().isVisible()
    main_window._toggle_immersive(False)
    assert main_window.menuBar().isVisible()
    main_window.close()

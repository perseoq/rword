from PySide6.QtGui import QImage

from rword.core.images import image_at_cursor
from rword.core.shapes import (
    WORDART_STYLES,
    insert_shape,
    insert_text_box,
    insert_wordart,
    make_shape_image,
    make_wordart_image,
)
from rword.core.tables import current_table


def test_make_shape_image_rectangle():
    image = make_shape_image("rectangle")
    assert not image.isNull()
    assert image.width() == 120
    assert image.height() == 80


def test_make_shape_image_all_kinds():
    for kind in ("rectangle", "ellipse", "line", "arrow", "triangle", "diamond"):
        image = make_shape_image(kind)
        assert not image.isNull(), kind


def test_insert_shape(editor):
    assert insert_shape(editor, "rectangle")
    assert image_at_cursor(editor) is not None


def test_insert_shape_custom(editor):
    assert insert_shape(editor, "circle", 100, 100, "#ff0000", "#0000ff", 3)
    _, image = image_at_cursor(editor)
    assert image.width() == 100
    assert image.height() == 100


def test_make_wordart_image():
    image = make_wordart_image("Prueba", "Azul")
    assert not image.isNull()
    assert image.format() != QImage.Format.Format_Invalid


def test_insert_wordart(editor):
    assert insert_wordart(editor, "Título elegante", "Oro")
    assert image_at_cursor(editor) is not None


def test_insert_wordart_empty(editor):
    assert not insert_wordart(editor, "   ", "Azul")


def test_wordart_styles():
    assert len(WORDART_STYLES) >= 5


def test_insert_text_box(editor):
    insert_text_box(editor, "contenido", width=200)
    table = current_table(editor)
    assert table is not None
    assert table.rows() == 1
    assert table.columns() == 1
    cell_text = table.cellAt(0, 0).firstCursorPosition().block().text()
    assert cell_text == "contenido"

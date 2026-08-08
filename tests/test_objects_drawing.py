from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QColor, QMouseEvent

from rword.core.hyperlinks import hyperlink_at_cursor
from rword.core.images import image_at_cursor
from rword.core.inserts import (
    EQUATION_SYMBOLS,
    SYMBOLS,
    insert_attachment,
    insert_chart,
    insert_date,
    insert_equation,
    insert_file_contents,
    insert_smartart,
    insert_symbol,
    insert_time,
    make_chart_image,
    make_smartart_image,
)


def test_symbols_categories():
    assert len(SYMBOLS) >= 5
    assert "→" in SYMBOLS["Símbolos"]


def test_insert_symbol(editor):
    insert_symbol(editor, "€")
    assert "€" in editor.toPlainText()


def test_insert_date_time(editor):
    insert_date(editor)
    insert_time(editor)
    import re

    text = editor.toPlainText()
    assert re.search(r"\d{2}/\d{2}/\d{4}", text)
    assert re.search(r"\d{2}:\d{2}", text)


def test_insert_file_contents(editor, tmp_path):
    path = tmp_path / "datos.txt"
    path.write_text("contenido importado", encoding="utf-8")
    assert insert_file_contents(editor, path)
    assert "contenido importado" in editor.toPlainText()


def test_insert_file_missing(editor):
    assert not insert_file_contents(editor, "/no/existe.txt")


def test_insert_attachment(editor, tmp_path):
    path = tmp_path / "informe.pdf"
    path.write_bytes(b"dummy")
    insert_attachment(editor, path)
    assert hyperlink_at_cursor(editor) is not None


def test_make_chart_image():
    image = make_chart_image([10, 20, 15], ["A", "B", "C"])
    assert not image.isNull()
    assert image.width() == 420


def test_insert_chart(editor):
    assert insert_chart(editor, [5, 8, 3], ["X", "Y", "Z"])
    assert image_at_cursor(editor) is not None


def test_make_smartart_image():
    image = make_smartart_image(["Jefe", "Subordinado"])
    assert not image.isNull()


def test_insert_smartart(editor):
    assert insert_smartart(editor, ["Director", "Gerente"])
    assert image_at_cursor(editor) is not None


def test_equation_symbols():
    assert "Pitágoras" in EQUATION_SYMBOLS


def test_insert_equation(editor):
    insert_equation(editor, "a² + b² = c²")
    assert "a² + b² = c²" in editor.toPlainText()


def test_drawing_toggle(editor):
    editor.set_drawing(True, "pencil", QColor("red"), 3.0)
    assert editor.drawing_enabled()
    editor.set_drawing(False)
    assert not editor.drawing_enabled()


def test_drawing_inserts_image(editor, qapp):
    editor.set_drawing(True, "pencil", QColor("black"), 3.0)
    editor.resize(300, 200)
    editor.show()
    press = QMouseEvent(
        QMouseEvent.Type.MouseButtonPress,
        QPointF(50, 50),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )
    move = QMouseEvent(
        QMouseEvent.Type.MouseMove,
        QPointF(120, 90),
        Qt.MouseButton.NoButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )
    release = QMouseEvent(
        QMouseEvent.Type.MouseButtonRelease,
        QPointF(120, 90),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.NoButton,
        Qt.KeyboardModifier.NoModifier,
    )
    editor.mousePressEvent(press)
    editor.mouseMoveEvent(move)
    editor.mouseReleaseEvent(release)
    assert image_at_cursor(editor) is not None
    editor.set_drawing(False)
    editor.hide()

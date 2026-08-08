from PySide6.QtCore import QRect
from PySide6.QtGui import QColor, QImage

from rword.core.images import (
    _adjust_image,
    adjust_pixels,
    crop_image,
    current_image_size,
    delete_image,
    flip_image,
    image_at_cursor,
    insert_image_from_data,
    replace_image,
    rotate_image,
    set_image_size,
)


def _make_image(width=50, height=30, color="#ff0000"):
    image = QImage(width, height, QImage.Format.Format_RGB32)
    image.fill(QColor(color))
    return image


def _insert(editor):
    assert insert_image_from_data(editor, _make_image())


def test_insert_image(editor):
    _insert(editor)
    info = image_at_cursor(editor)
    assert info is not None
    name, image = info
    assert image.width() == 50
    assert image.height() == 30


def test_insert_image_failure(editor):
    assert not insert_image_from_data(editor, QImage())


def test_set_image_size(editor):
    _insert(editor)
    set_image_size(editor, 100, 60)
    assert current_image_size(editor) == (100, 60)


def test_rotate_image(editor):
    _insert(editor)
    rotate_image(editor, 90)
    _, image = image_at_cursor(editor)
    assert image.width() == 30
    assert image.height() == 50


def test_flip_image(editor):
    _insert(editor)
    name, before = image_at_cursor(editor)
    flip_image(editor, True)
    _, after = image_at_cursor(editor)
    assert after.width() == before.width()


def test_crop_image(editor):
    _insert(editor)
    crop_image(editor, QRect(0, 0, 20, 20))
    _, image = image_at_cursor(editor)
    assert image.width() == 20
    assert image.height() == 20


def test_crop_out_of_bounds(editor):
    _insert(editor)
    crop_image(editor, QRect(40, 20, 100, 100))
    _, image = image_at_cursor(editor)
    assert image.width() <= 50
    assert image.height() <= 30


def test_grayscale(editor):
    image = _make_image(color="#ff0000")
    gray = _adjust_image(image, grayscale=True)
    color = gray.pixelColor(0, 0)
    assert color.red() == color.green() == color.blue()


def test_sepia(editor):
    image = _make_image(color="#808080")
    sepia = _adjust_image(image, sepia=True)
    color = sepia.pixelColor(0, 0)
    assert color.red() > color.blue()


def test_brightness(editor):
    image = _make_image(color="#808080")
    brighter = _adjust_image(image, brightness=40)
    assert brighter.pixelColor(0, 0).red() > 0x80


def test_contrast(editor):
    image = _make_image(color="#a0a0a0")
    high = _adjust_image(image, contrast=2.0)
    assert high.pixelColor(0, 0).red() > 0x80


def test_saturation(editor):
    image = _make_image(color="#ff0000")
    desat = _adjust_image(image, saturation=0.0)
    color = desat.pixelColor(0, 0)
    assert color.red() == color.green() == color.blue()


def test_replace_image(editor, tmp_path):
    _insert(editor)
    path = tmp_path / "new.png"
    _make_image(width=10, height=10, color="#0000ff").save(str(path))
    assert replace_image(editor, str(path))
    _, image = image_at_cursor(editor)
    assert image.width() == 10
    assert image.height() == 10
    assert image.pixelColor(0, 0).name() == "#0000ff"


def test_delete_image(editor):
    _insert(editor)
    assert image_at_cursor(editor) is not None
    delete_image(editor)
    assert image_at_cursor(editor) is None


def test_adjust_pixels_updates_resource(editor):
    _insert(editor)
    adjust_pixels(editor, brightness=50)
    _, image = image_at_cursor(editor)
    assert image is not None

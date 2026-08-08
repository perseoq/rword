"""Operaciones sobre imágenes del documento."""

from __future__ import annotations

import uuid
from pathlib import Path

from PySide6.QtCore import QRect, Qt, QUrl
from PySide6.QtGui import (
    QColor,
    QImage,
    QTextCursor,
    QTextDocument,
    QTextFormat,
    QTextImageFormat,
    QTransform,
)
from PySide6.QtWidgets import QTextEdit


def _char_format_at(editor: QTextEdit, position: int):
    cursor = QTextCursor(editor.document())
    cursor.setPosition(position)
    return cursor.charFormat()


def insert_image(editor: QTextEdit, path: str | Path) -> bool:
    """Inserta una imagen en la posición del cursor."""
    image = QImage(str(path))
    if image.isNull():
        return False
    return insert_image_from_data(editor, image)


def insert_image_from_data(editor: QTextEdit, image: QImage) -> bool:
    if image.isNull():
        return False
    name = f"rword-image-{uuid.uuid4().hex}"
    editor.document().addResource(
        QTextDocument.ImageResource, QUrl(name), image
    )
    cursor = editor.textCursor()
    fmt = QTextImageFormat()
    fmt.setName(name)
    fmt.setWidth(image.width())
    fmt.setHeight(image.height())
    cursor.insertText("\uFFFC", fmt)
    editor.setTextCursor(cursor)
    return True


def _is_image_char(editor: QTextEdit, position: int) -> bool:
    limit = editor.document().characterCount() - 1
    if position < 0 or position >= limit:
        return False
    return _char_format_at(editor, position + 1).isImageFormat()


def _image_position(editor: QTextEdit) -> int | None:
    start = editor.textCursor().position()
    limit = editor.document().characterCount() - 1
    for pos in range(start - 1, -1, -1):
        if _is_image_char(editor, pos):
            return pos
    for pos in range(start, limit):
        if _is_image_char(editor, pos):
            return pos
    return None


def image_at_cursor(editor: QTextEdit) -> tuple[str, QImage] | None:
    """Devuelve (nombre, imagen) de la imagen cercana a la posición del cursor."""
    position = _image_position(editor)
    if position is None:
        return None
    format_at = _char_format_at(editor, position + 1)
    name = format_at.stringProperty(QTextFormat.Property.ImageName)
    if not name:
        return None
    resource = editor.document().resource(
        QTextDocument.ImageResource, QUrl(name)
    )
    if resource is not None and isinstance(resource, QImage):
        return name, resource
    return None


def set_image_size(editor: QTextEdit, width: int, height: int) -> None:
    image_info = image_at_cursor(editor)
    image_position = _image_position(editor)
    if image_info is None or image_position is None:
        return
    name, _image = image_info
    cursor = editor.textCursor()
    cursor.setPosition(image_position)
    cursor.setPosition(image_position + 1, cursor.MoveMode.KeepAnchor)
    fmt = QTextImageFormat()
    fmt.setName(name)
    fmt.setWidth(width)
    fmt.setHeight(height)
    cursor.mergeCharFormat(fmt)
    editor.setTextCursor(cursor)


def current_image_size(editor: QTextEdit) -> tuple[int, int] | None:
    image_info = image_at_cursor(editor)
    if image_info is None:
        return None
    fmt = _char_format_at(editor, editor.textCursor().position())
    if fmt.isImageFormat():
        width = int(fmt.doubleProperty(QTextFormat.Property.ImageWidth) or 0)
        height = int(fmt.doubleProperty(QTextFormat.Property.ImageHeight) or 0)
        if width and height:
            return width, height
    name, image = image_info
    return image.width(), image.height()

def _replace_resource(editor: QTextEdit, name: str, new_image: QImage) -> None:
    editor.document().addResource(QTextDocument.ImageResource, QUrl(name), new_image)
    editor.document().setModified(True)


def rotate_image(editor: QTextEdit, degrees: float) -> None:
    image_info = image_at_cursor(editor)
    if image_info is None:
        return
    name, image = image_info
    transform = QTransform()
    transform.rotate(degrees)
    rotated = image.transformed(transform, Qt.SmoothTransformation)
    _replace_resource(editor, name, rotated)


def flip_image(editor: QTextEdit, horizontal: bool = True) -> None:
    image_info = image_at_cursor(editor)
    if image_info is None:
        return
    name, image = image_info
    transform = QTransform()
    transform.scale(-1.0 if horizontal else 1.0, -1.0 if not horizontal else 1.0)
    flipped = image.transformed(transform)
    _replace_resource(editor, name, flipped)


def crop_image(editor: QTextEdit, rect: QRect) -> None:
    image_info = image_at_cursor(editor)
    if image_info is None:
        return
    name, image = image_info
    valid = rect.intersected(QRect(0, 0, image.width(), image.height()))
    cropped = image.copy(valid)
    _replace_resource(editor, name, cropped)


def adjust_pixels(editor: QTextEdit, brightness=0, contrast=1.0, saturation=1.0,
                  grayscale=False, sepia=False) -> None:
    image_info = image_at_cursor(editor)
    if image_info is None:
        return
    name, image = image_info
    adjusted = _adjust_image(
        image, brightness, contrast, saturation, grayscale, sepia
    )
    _replace_resource(editor, name, adjusted)


def _adjust_image(image: QImage, brightness=0, contrast=1.0, saturation=1.0,
                  grayscale=False, sepia=False) -> QImage:
    img = image.convertToFormat(QImage.Format.Format_ARGB32)
    for y in range(img.height()):
        for x in range(img.width()):
            color = img.pixelColor(x, y)
            red, green, blue = color.red(), color.green(), color.blue()
            if grayscale:
                gray = int(0.299 * red + 0.587 * green + 0.114 * blue)
                red = green = blue = gray
            if sepia:
                gray = 0.299 * red + 0.587 * green + 0.114 * blue
                red = int(min(255, gray * 1.07 + 30))
                green = int(min(255, gray * 0.99 + 20))
                blue = int(min(255, gray * 0.78))
            if brightness:
                red = max(0, min(255, red + brightness))
                green = max(0, min(255, green + brightness))
                blue = max(0, min(255, blue + brightness))
            if contrast != 1.0:
                red = int(max(0, min(255, (red - 128) * contrast + 128)))
                green = int(max(0, min(255, (green - 128) * contrast + 128)))
                blue = int(max(0, min(255, (blue - 128) * contrast + 128)))
            if saturation != 1.0:
                gray = 0.299 * red + 0.587 * green + 0.114 * blue
                red = int(max(0, min(255, gray + (red - gray) * saturation)))
                green = int(max(0, min(255, gray + (green - gray) * saturation)))
                blue = int(max(0, min(255, gray + (blue - gray) * saturation)))
            img.setPixelColor(
                x, y, QColor(red, green, blue, color.alpha())
            )
    return img


def replace_image(editor: QTextEdit, path: str | Path) -> bool:
    image_info = image_at_cursor(editor)
    if image_info is None:
        return False
    name, _ = image_info
    new_image = QImage(str(path))
    if new_image.isNull():
        return False
    _replace_resource(editor, name, new_image)
    return True


def delete_image(editor: QTextEdit) -> None:
    image_position = _image_position(editor)
    if image_position is None:
        return
    cursor = editor.textCursor()
    cursor.setPosition(image_position)
    cursor.setPosition(image_position + 1, cursor.MoveMode.KeepAnchor)
    cursor.removeSelectedText()
    editor.setTextCursor(cursor)

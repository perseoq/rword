"""Accesibilidad: comprobador, texto alternativo y lectura en voz alta."""

from __future__ import annotations

import re

from PySide6.QtGui import QColor, QTextCursor, QTextFormat
from PySide6.QtTextToSpeech import QTextToSpeech
from PySide6.QtWidgets import QTextEdit

ALT_TEXT_PROP = QTextFormat.Property.ImageAltText


def set_image_alt_text(editor: QTextEdit, alt_text: str) -> bool:
    """Asigna texto alternativo a la imagen del cursor."""
    position = _image_position(editor)
    if position is None:
        return False
    cursor = QTextCursor(editor.document())
    cursor.setPosition(position)
    cursor.setPosition(position + 1, cursor.MoveMode.KeepAnchor)
    fmt = cursor.charFormat()
    fmt.setProperty(ALT_TEXT_PROP, alt_text)
    cursor.mergeCharFormat(fmt)
    return True


def image_alt_text(editor: QTextEdit, position: int) -> str:
    cursor = QTextCursor(editor.document())
    cursor.setPosition(position + 1)
    return cursor.charFormat().stringProperty(ALT_TEXT_PROP)


def image_alt_text_at_cursor(editor: QTextEdit) -> str:
    position = _image_position(editor)
    if position is None:
        return ""
    return image_alt_text(editor, position)


def _image_position(editor: QTextEdit) -> int | None:
    from rword.core.images import _image_position as _images_position

    return _images_position(editor)


def _images_without_alt(editor: QTextEdit) -> list[int]:
    positions = []
    block = editor.document().begin()
    while block.isValid():
        iterator = block.begin()
        while not iterator.atEnd():
            fragment = iterator.fragment()
            fmt = fragment.charFormat()
            if fmt.isImageFormat() and not fmt.stringProperty(ALT_TEXT_PROP):
                positions.append(fragment.position())
            iterator += 1
        block = block.next()
    return positions


def _heading_structure(editor: QTextEdit) -> list[str]:
    from rword.core.hyperlinks import headings

    return [text for text, _ in headings(editor)]


def check_accessibility(editor: QTextEdit) -> list[tuple[str, str]]:
    """Devuelve una lista de (categoría, problema) de accesibilidad."""
    issues: list[tuple[str, str]] = []
    for position in _images_without_alt(editor):
        issues.append(
            ("Imágenes", f"Imagen sin texto alternativo (posición {position}).")
        )
    headings = _heading_structure(editor)
    if not headings:
        issues.append(
            ("Estructura", "No se detectaron encabezados en el documento.")
        )
    text = editor.toPlainText()
    if not text.strip():
        issues.append(("Estructura", "El documento está vacío."))
    long_words = [
        word for word in re.findall(r"\S{40,}", text)
    ]
    for word in long_words[:5]:
        issues.append(("Legibilidad", f"Palabra muy larga: {word[:30]}…"))
    contrast_issues = _low_contrast(editor)
    issues.extend(contrast_issues)
    return issues


def _low_contrast(editor: QTextEdit) -> list[tuple[str, str]]:
    issues = []
    seen = set()
    block = editor.document().begin()
    while block.isValid():
        iterator = block.begin()
        while not iterator.atEnd():
            fragment = iterator.fragment()
            fmt = fragment.charFormat()
            color = fmt.foreground().color()
            if color.isValid() and color.name() not in seen:
                seen.add(color.name())
                if _contrast_ratio(color, QColor("#ffffff")) < 3.0:
                    issues.append(
                        ("Contraste", f"Color de texto con bajo contraste: {color.name()}.")
                    )
            iterator += 1
        block = block.next()
    return issues


def _relative_luminance(color: QColor) -> float:
    def _channel(value: int) -> float:
        channel = value / 255.0
        return channel / 12.92 if channel <= 0.03928 else ((channel + 0.055) / 1.055) ** 2.4

    return (
        0.2126 * _channel(color.red())
        + 0.7152 * _channel(color.green())
        + 0.0722 * _channel(color.blue())
    )


def _contrast_ratio(color: QColor, background: QColor) -> float:
    l1 = _relative_luminance(color)
    l2 = _relative_luminance(background)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


class SpeechReader:
    """Lee el documento o la selección en voz alta."""

    def __init__(self, parent=None) -> None:
        self._engine = QTextToSpeech(parent)
        self._engine.setRate(0)
        self._engine.setVolume(1.0)

    def speak(self, text: str) -> None:
        if text.strip():
            self._engine.say(text)

    def stop(self) -> None:
        self._engine.stop()

    def is_speaking(self) -> bool:
        return self._engine.state() == QTextToSpeech.State.Speaking

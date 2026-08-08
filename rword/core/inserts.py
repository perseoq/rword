"""Objetos insertados: símbolos, gráficos, SmartArt y ecuaciones."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import (
    QColor,
    QFont,
    QImage,
    QLinearGradient,
    QPainter,
    QPen,
)
from PySide6.QtWidgets import QTextEdit

from rword.core.hyperlinks import insert_hyperlink
from rword.core.images import insert_image_from_data

SYMBOLS = {
    "Símbolos": ["©", "®", "™", "§", "¶", "†", "‡", "•", "→", "←", "↑", "↓"],
    "Matemáticos": ["±", "×", "÷", "∑", "√", "∞", "π", "≤", "≥", "≠", "≈", "°"],
    "Moneda": ["€", "£", "¥", "$", "¢"],
    "Comillas": ["«", "»", "“", "”", "‘", "’"],
    "Letras acentuadas": ["á", "é", "í", "ó", "ú", "ü", "ñ", "Á", "É", "Í", "Ó", "Ú", "Ñ"],
}

EQUATION_SYMBOLS = {
    "Fracción": r"a/b",
    "Potencia": "x²",
    "Subíndice": "x₂",
    "Raíz": "√x",
    "Suma": "∑(i=1, n)",
    "Integral": "∫f(x)dx",
    "Fórmula cuadrática": "x = (-b ± √(b²-4ac)) / 2a",
    "Pitágoras": "a² + b² = c²",
    "Ecuación de Einstein": "E = mc²",
}


def insert_symbol(editor: QTextEdit, symbol: str) -> None:
    cursor = editor.textCursor()
    cursor.insertText(symbol)
    editor.setTextCursor(cursor)


def insert_date(editor: QTextEdit) -> None:
    cursor = editor.textCursor()
    cursor.insertText(datetime.now().strftime("%d/%m/%Y"))
    editor.setTextCursor(cursor)


def insert_time(editor: QTextEdit) -> None:
    cursor = editor.textCursor()
    cursor.insertText(datetime.now().strftime("%H:%M"))
    editor.setTextCursor(cursor)


def insert_file_contents(editor: QTextEdit, path: str | Path) -> bool:
    try:
        content = Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    editor.insertPlainText(content)
    return True


def insert_attachment(editor: QTextEdit, path: str | Path) -> None:
    """Inserta un enlace a un archivo adjunto (PDF, video, audio...)."""
    path = Path(path)
    insert_hyperlink(editor, f"[Adjunto] {path.name}", path.as_uri())


def make_chart_image(values: list[float], labels: list[str]) -> QImage:
    """Genera un gráfico de barras a partir de valores."""
    width, height = 420, 240
    image = QImage(width, height, QImage.Format.Format_ARGB32_Premultiplied)
    image.fill(QColor("#ffffff"))
    painter = QPainter(image)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    margin = 40
    max_value = max(values) if values else 1
    if max_value == 0:
        max_value = 1
    bar_width = (width - 2 * margin) / max(1, len(values)) * 0.6
    step = (width - 2 * margin) / max(1, len(values))
    painter.setPen(QPen(QColor("#333333")))
    for index, value in enumerate(values):
        x = margin + index * step + (step - bar_width) / 2
        bar_height = (value / max_value) * (height - 2 * margin)
        y = height - margin - bar_height
        gradient = QLinearGradient(x, y, x, height - margin)
        gradient.setColorAt(0, QColor("#1e90ff"))
        gradient.setColorAt(1, QColor("#004b8f"))
        painter.fillRect(QRectF(x, y, bar_width, bar_height), gradient)
        if index < len(labels):
            painter.drawText(
                QRectF(x - step / 2, height - margin, step, 30),
                Qt.AlignmentFlag.AlignCenter,
                labels[index],
            )
        painter.drawText(
            QRectF(x - step / 2, y - 20, step, 20),
            Qt.AlignmentFlag.AlignCenter,
            str(value),
        )
    painter.end()
    return image


def insert_chart(editor: QTextEdit, values: list[float], labels: list[str]) -> bool:
    image = make_chart_image(values, labels)
    return insert_image_from_data(editor, image)


def make_smartart_image(items: list[str]) -> QImage:
    """Genera un diagrama de organigrama simple."""
    width, height = 460, 60 + len(items) * 70
    image = QImage(width, height, QImage.Format.Format_ARGB32_Premultiplied)
    image.fill(QColor("#ffffff"))
    painter = QPainter(image)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    box_width, box_height = 240, 44
    center_x = width / 2
    font = QFont("Sans Serif", 11)
    painter.setFont(font)
    for index, item in enumerate(items):
        y = 30 + index * 70
        rect = QRectF(center_x - box_width / 2, y, box_width, box_height)
        gradient = QLinearGradient(rect.topLeft(), rect.bottomLeft())
        gradient.setColorAt(0, QColor("#dbe9ff"))
        gradient.setColorAt(1, QColor("#b3d4ff"))
        painter.fillRect(rect, gradient)
        painter.setPen(QPen(QColor("#1a5bbf"), 1.5))
        painter.drawRect(rect)
        painter.setPen(QColor("#1a1a2e"))
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, item)
        if index > 0:
            painter.drawLine(
                int(center_x), int(30 + index * 70),
                int(center_x), int(y),
            )
    painter.end()
    return image


def insert_smartart(editor: QTextEdit, items: list[str]) -> bool:
    image = make_smartart_image(items)
    return insert_image_from_data(editor, image)


def insert_equation(editor: QTextEdit, equation: str) -> None:
    cursor = editor.textCursor()
    cursor.insertText(equation)
    editor.setTextCursor(cursor)

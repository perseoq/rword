"""Formas, cuadros de texto y WordArt."""

from __future__ import annotations

from PySide6.QtCore import QPointF, QRectF
from PySide6.QtGui import (
    QColor,
    QFont,
    QImage,
    QLinearGradient,
    QPainter,
    QPen,
    QPolygonF,
    QTextFrameFormat,
    QTextLength,
    QTextTableFormat,
)
from PySide6.QtWidgets import QTextEdit

from rword.core.images import insert_image_from_data

SHAPE_TYPES = ["rectangle", "ellipse", "line", "arrow", "triangle", "diamond"]
SHAPE_LABELS = {
    "rectangle": "Rectángulo",
    "ellipse": "Círculo",
    "line": "Línea",
    "arrow": "Flecha",
    "triangle": "Triángulo",
    "diamond": "Rombo",
}

WORDART_STYLES = {
    "Azul": ("#1e90ff", "#004b8f"),
    "Rojo": ("#ff4444", "#8f0000"),
    "Verde": ("#44bb44", "#0a6f0a"),
    "Oro": ("#ffd700", "#8f6a00"),
    "Plata": ("#c0c0c0", "#666666"),
}


def make_shape_image(
    kind: str,
    width: int = 120,
    height: int = 80,
    fill: str = "#ffffff",
    border: str = "#000000",
    border_width: int = 2,
) -> QImage:
    """Genera una imagen con la forma geométrica dibujada."""
    image = QImage(width, height, QImage.Format.Format_ARGB32_Premultiplied)
    image.fill(QColor(0, 0, 0, 0))
    painter = QPainter(image)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setPen(QPen(QColor(border), border_width))
    painter.setBrush(QColor(fill))
    rect = QRectF(1, 1, width - 2, height - 2)
    if kind == "rectangle":
        painter.drawRect(rect)
    elif kind == "ellipse":
        painter.drawEllipse(rect)
    elif kind == "line":
        painter.drawLine(QPointF(1, height - 2), QPointF(width - 2, 1))
    elif kind == "arrow":
        painter.drawLine(QPointF(2, height - 2), QPointF(width - 2, 2))
        painter.drawLine(QPointF(width - 2, 2), QPointF(width - 14, 2))
        painter.drawLine(QPointF(width - 2, 2), QPointF(width - 2, 14))
    elif kind == "triangle":
        points = QPolygonF(
            [
                QPointF(width / 2, 2),
                QPointF(2, height - 2),
                QPointF(width - 2, height - 2),
            ]
        )
        painter.drawPolygon(points)
    elif kind == "diamond":
        points = QPolygonF(
            [
                QPointF(width / 2, 2),
                QPointF(width - 2, height / 2),
                QPointF(width / 2, height - 2),
                QPointF(2, height / 2),
            ]
        )
        painter.drawPolygon(points)
    painter.end()
    return image


def insert_shape(
    editor: QTextEdit,
    kind: str,
    width: int = 120,
    height: int = 80,
    fill: str = "#ffffff",
    border: str = "#000000",
    border_width: int = 2,
) -> bool:
    image = make_shape_image(kind, width, height, fill, border, border_width)
    return insert_image_from_data(editor, image)


def make_wordart_image(text: str, style: str, width: int = 300, height: int = 90) -> QImage:
    """Genera una imagen de texto con estilo WordArt (gradiente)."""
    image = QImage(width, height, QImage.Format.Format_ARGB32_Premultiplied)
    image.fill(QColor(0, 0, 0, 0))
    gradient = QLinearGradient(0, 0, width, height)
    start, end = WORDART_STYLES.get(style, WORDART_STYLES["Azul"])
    gradient.setColorAt(0.0, QColor(start))
    gradient.setColorAt(1.0, QColor(end))
    painter = QPainter(image)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    font = QFont("Sans Serif", 26)
    font.setBold(True)
    painter.setFont(font)
    font_metrics = painter.fontMetrics()
    text_width = font_metrics.horizontalAdvance(text)
    text_height = font_metrics.height()
    x = max(2.0, (width - text_width) / 2.0)
    y = (height - text_height) / 2.0 + font_metrics.ascent()
    painter.setPen(QPen(QColor("#333333"), 2))
    painter.drawText(QPointF(x + 2, y + 2), text)
    painter.fillRect(QRectF(x, y - font_metrics.ascent(), text_width, text_height), gradient)
    painter.end()
    return image


def insert_wordart(editor: QTextEdit, text: str, style: str) -> bool:
    if not text.strip():
        return False
    image = make_wordart_image(text, style)
    return insert_image_from_data(editor, image)


def insert_text_box(editor: QTextEdit, text: str = "", width: float = 200) -> None:
    """Inserta un cuadro de texto como una tabla de una celda con borde."""
    cursor = editor.textCursor()
    table_format = QTextTableFormat()
    table_format.setBorder(1)
    table_format.setBorderBrush(QColor("#000000"))
    table_format.setBorderStyle(QTextFrameFormat.BorderStyle.BorderStyle_Solid)
    table_format.setWidth(QTextLength(QTextLength.Type.FixedLength, width))
    table = cursor.insertTable(1, 1, table_format)
    if text:
        table.cellAt(0, 0).firstCursorPosition().insertText(text)
    editor.setTextCursor(table.cellAt(0, 0).firstCursorPosition())

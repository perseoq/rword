"""Widget de edición de texto basado en QTextEdit."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QPointF, Qt, Signal
from PySide6.QtGui import (
    QColor,
    QFont,
    QKeyEvent,
    QMouseEvent,
    QPainter,
    QPaintEvent,
)
from PySide6.QtWidgets import QTextEdit

from rword.config import HTML_EXTENSIONS

_LINE_NUMBER_WIDTH = 36
_WATERMARK_COLOR = QColor(180, 180, 180, 80)


class Editor(QTextEdit):
    """Área de edición con soporte de texto enriquecido y persistencia."""

    link_clicked = Signal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setAcceptRichText(True)
        self.setUndoRedoEnabled(True)
        self._file_path: Path | None = None
        self._line_numbers_enabled = False
        self._watermark = ""
        self._track_changes = False
        self._find_selections: list = []
        self._comment_selections: list = []

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            href = self.anchorAt(event.position().toPoint())
            if href:
                self.link_clicked.emit(href)
                return
        super().mouseReleaseEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if not self._track_changes:
            super().keyPressEvent(event)
            return
        key = event.key()
        if key in (Qt.Key.Key_Backspace, Qt.Key.Key_Delete):
            self._mark_deletion(key)
            return
        if len(event.text()) > 0:
            self._insert_tracked_text(event.text())
            return
        super().keyPressEvent(event)

    def _mark_deletion(self, key: int) -> None:
        from rword.core.comments import deleted_format

        cursor = self.textCursor()
        if cursor.hasSelection():
            cursor.mergeCharFormat(deleted_format())
            cursor.clearSelection()
            self.setTextCursor(cursor)
            return
        if key == Qt.Key.Key_Backspace:
            if cursor.position() > 0:
                cursor.setPosition(cursor.position() - 1)
                cursor.setPosition(cursor.position() + 1, cursor.MoveMode.KeepAnchor)
                cursor.mergeCharFormat(deleted_format())
                cursor.clearSelection()
                self.setTextCursor(cursor)
        else:
            cursor.setPosition(cursor.position())
            cursor.setPosition(cursor.position() + 1, cursor.MoveMode.KeepAnchor)
            cursor.mergeCharFormat(deleted_format())
            cursor.clearSelection()
            self.setTextCursor(cursor)

    def _insert_tracked_text(self, text: str) -> None:
        from rword.core.comments import inserted_format

        cursor = self.textCursor()
        cursor.insertText(text, inserted_format())
        self.setTextCursor(cursor)

    def set_track_changes(self, enabled: bool) -> None:
        self._track_changes = enabled

    def track_changes(self) -> bool:
        return self._track_changes

    def set_find_selections(self, selections: list) -> None:
        self._find_selections = selections
        self._refresh_extra_selections()

    def _refresh_extra_selections(self) -> None:
        self.setExtraSelections(self._find_selections + self._comment_selections)

    @property
    def file_path(self) -> Path | None:
        return self._file_path

    def set_file_path(self, path: Path | None) -> None:
        self._file_path = path

    def load_file(self, path: Path) -> None:
        """Carga el contenido de un archivo en el editor."""
        content = path.read_text(encoding="utf-8")
        if path.suffix.lower() in HTML_EXTENSIONS:
            self.setHtml(content)
        else:
            self.setPlainText(content)
        self._file_path = path
        self.document().setModified(False)

    def save_file(self, path: Path) -> None:
        """Guarda el contenido del editor en un archivo."""
        content = (
            self.toHtml()
            if path.suffix.lower() in HTML_EXTENSIONS
            else self.toPlainText()
        )
        path.write_text(content, encoding="utf-8")
        self._file_path = path
        self.document().setModified(False)

    def word_count(self) -> int:
        """Número de palabras en el documento actual."""
        return len(self.toPlainText().split())

    def character_count(self) -> int:
        """Número de caracteres en el documento actual."""
        return len(self.toPlainText())

    def set_line_numbers_enabled(self, enabled: bool) -> None:
        self._line_numbers_enabled = enabled
        left = _LINE_NUMBER_WIDTH if enabled else 0
        self.setViewportMargins(left, 0, 0, 0)
        self.viewport().update()

    def line_numbers_enabled(self) -> bool:
        return self._line_numbers_enabled

    def set_watermark(self, text: str) -> None:
        self._watermark = text
        self.viewport().update()

    def watermark(self) -> str:
        return self._watermark

    def paintEvent(self, event: QPaintEvent) -> None:
        if self._line_numbers_enabled:
            self._paint_line_numbers()
        super().paintEvent(event)
        if self._watermark:
            self._paint_watermark()

    def _paint_line_numbers(self) -> None:
        painter = QPainter(self.viewport())
        font = QFont(self.font())
        font.setPointSizeF(max(7.0, font.pointSizeF() - 1))
        painter.setFont(font)
        first_block = self.cursorForPosition(QPointF(0, 0)).block()
        current = self.textCursor().block()
        block = first_block
        y = -self.verticalScrollBar().value()
        while block.isValid() and y < self.viewport().height():
            number = block.blockNumber() + 1
            rect = self.blockBoundingRect(block)
            if block == current:
                painter.setPen(QColor("#c00000"))
            else:
                painter.setPen(QColor(140, 140, 140))
            painter.drawText(
                -self.verticalScrollBar().value() + 8,
                y + int(rect.height() / 2) + 4,
                _LINE_NUMBER_WIDTH - 12,
                20,
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                str(number),
            )
            y += int(rect.height())
            block = block.next()
        painter.end()

    def _paint_watermark(self) -> None:
        painter = QPainter(self.viewport())
        painter.save()
        painter.setPen(_WATERMARK_COLOR)
        font = QFont(self.font())
        font.setPointSizeF(max(24.0, font.pointSizeF() * 2.5))
        font.setBold(True)
        painter.setFont(font)
        painter.translate(self.viewport().width() / 2.0, self.viewport().height() / 2.0)
        painter.rotate(-30.0)
        painter.drawText(
            QPointF(0, 0), self._watermark
        )
        painter.restore()
        painter.end()

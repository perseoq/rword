"""Regla horizontal del editor."""

from __future__ import annotations

from PySide6.QtCore import QPoint
from PySide6.QtGui import QColor, QPainter, QPaintEvent
from PySide6.QtWidgets import QWidget

from rword.core.pages import MM_TO_PX


class Ruler(QWidget):
    """Regla que muestra la posición horizontal del cursor sobre la página."""

    def __init__(self, editor, parent=None) -> None:
        super().__init__(parent)
        self._editor = editor
        self.setFixedHeight(22)
        self.setMouseTracking(True)

    def _page_offset(self) -> int:
        if self._editor.parentWidget() is None:
            return 0
        top_left = self._editor.mapTo(self.parentWidget(), QPoint(0, 0))
        return top_left.x() - self.x()

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("#f5f5f5"))
        painter.setPen(QColor("#aaaaaa"))
        painter.drawLine(0, self.height() - 1, self.width(), self.height() - 1)

        offset = self._page_offset()
        zoom = self._editor.zoom() / 100.0
        step = int(20 * MM_TO_PX * zoom)
        if step < 5:
            step = 5
        label_step = step * 5
        page_width = self._editor.width()
        for x in range(offset, offset + page_width + 1, step):
            height = 8 if (x - offset) % label_step else 14
            painter.drawLine(x, self.height() - height, x, self.height())
            if (x - offset) % label_step == 0:
                painter.setPen(QColor("#777777"))
                painter.drawText(
                    x + 2, 12, str(int((x - offset) / (MM_TO_PX * zoom)))
                )
                painter.setPen(QColor("#aaaaaa"))
        cursor_x = offset + self._editor.cursorRect().x()
        painter.setPen(QColor("#c00000"))
        painter.drawLine(cursor_x, 0, cursor_x, self.height())
        painter.end()

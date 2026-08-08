"""Vista de página: hoja de papel centrada sobre un fondo gris."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QPalette, QResizeEvent
from PySide6.QtWidgets import QWidget

from rword.core.pages import PageSetup

_MARGIN = 28
_GRAY_BACKGROUND = QColor("#909090")
_PAGE_BORDER = QColor("#b0b0b0")


class PageView(QWidget):
    """Contiene al editor como una hoja de papel centrada sobre fondo gris."""

    def __init__(self, editor, parent=None) -> None:
        super().__init__(parent)
        self._editor = editor
        self._page_width = int(PageSetup().page_size_px().width())
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, _GRAY_BACKGROUND)
        self.setPalette(palette)
        editor.setParent(self)
        editor.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        editor.show()
        self.update_paper_color("#ffffff")

    def set_page_width(self, width: int) -> None:
        self._page_width = max(200, int(width))
        self._layout_editor()

    def update_paper_color(self, color: str) -> None:
        palette = self._editor.palette()
        palette.setColor(QPalette.ColorRole.Base, QColor(color))
        palette.setColor(QPalette.ColorRole.Text, QColor("#000000"))
        self._editor.setPalette(palette)

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self._layout_editor()

    def _layout_editor(self) -> None:
        available = self.width() - 2 * _MARGIN
        page = min(available, self._page_width)
        if page < 120:
            page = max(120, available)
        x = (self.width() - page) // 2
        y = _MARGIN
        height = self.height() - 2 * _MARGIN
        if height < 120:
            height = 120
        self._editor.setGeometry(x, y, page, height)
        self.update()

    def paintEvent(self, event) -> None:
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(_PAGE_BORDER)
        painter.drawRect(self._editor.geometry().adjusted(0, 0, -1, -1))
        painter.end()

"""Vista de página: hoja de papel que se desplaza sobre un fondo gris."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QScrollArea, QWidget

from rword.core.pages import PageSetup

_MARGIN = 28
_GRAY_BACKGROUND = QColor("#909090")


class PageView(QScrollArea):
    """Muestra el editor como una hoja de papel con el scroll en el área gris."""

    layout_changed = Signal()

    def __init__(self, editor, parent=None) -> None:
        super().__init__(parent)
        self._editor = editor
        setup = PageSetup()
        editor._applied_page_setup = setup
        self._page_width = int(setup.page_size_px().width())
        self._min_sheet_height = int(setup.page_size_px().height())

        self.setWidgetResizable(False)
        self.setFrameShape(self.Shape.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, _GRAY_BACKGROUND)
        palette.setColor(QPalette.ColorRole.Base, _GRAY_BACKGROUND)
        self.setPalette(palette)

        self._container = QWidget()
        self._container.setAutoFillBackground(True)
        container_palette = self._container.palette()
        container_palette.setColor(QPalette.ColorRole.Window, _GRAY_BACKGROUND)
        self._container.setPalette(container_palette)

        editor.setParent(self._container)
        editor.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        editor.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        editor.show()
        self.update_paper_color("#ffffff")
        self.setWidget(self._container)

        editor.document().contentsChange.connect(self._relayout)

    def set_page_size(self, width: int, height: int) -> None:
        self._page_width = max(200, int(width))
        self._min_sheet_height = max(200, int(height))
        self._relayout()

    def update_paper_color(self, color: str) -> None:
        palette = self._editor.palette()
        palette.setColor(QPalette.ColorRole.Base, QColor(color))
        palette.setColor(QPalette.ColorRole.Text, QColor("#000000"))
        self._editor.setPalette(palette)
        viewport_palette = self._editor.viewport().palette()
        viewport_palette.setColor(QPalette.ColorRole.Base, QColor(color))
        viewport_palette.setColor(QPalette.ColorRole.Text, QColor("#000000"))
        self._editor.viewport().setPalette(viewport_palette)

    def refresh(self) -> None:
        self._relayout()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._relayout()

    def _relayout(self) -> None:
        editor = self._editor
        zoom = editor.zoom() / 100.0
        display_page = self._page_width * zoom
        available = self.viewport().width() - 2 * _MARGIN
        page = min(available, display_page)
        if page < 160:
            page = max(120, available)
        page = max(120, int(page))

        editor.setFixedWidth(page)
        editor.document().setTextWidth(editor.viewport().width())

        content_height = int(editor.document().size().height())
        min_sheet = self._min_sheet_height * zoom
        sheet_height = max(content_height, int(min_sheet))
        sheet_height = max(120, sheet_height)
        editor.setFixedHeight(sheet_height)

        container_width = max(self.viewport().width(), page + 2 * _MARGIN)
        container_height = max(sheet_height + 2 * _MARGIN, self.viewport().height())
        self._container.setFixedSize(container_width, container_height)
        editor.move((container_width - page) // 2, _MARGIN)
        self.layout_changed.emit()

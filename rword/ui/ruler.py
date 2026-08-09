"""Reglas estilo Word: horizontal (superior) y vertical (izquierda)."""

from __future__ import annotations

from PySide6.QtCore import QPoint, QRect, Qt, Signal
from PySide6.QtGui import (
    QColor,
    QFont,
    QMouseEvent,
    QPainter,
    QPaintEvent,
    QPalette,
    QPen,
    QPolygon,
)
from PySide6.QtWidgets import QWidget

from rword.core import paragraph
from rword.core.pages import MM_TO_PX, current_page_setup

_THICKNESS = 24
_HIT_TOLERANCE = 8


def _doc_x(zoom: float, page_left: float, screen_x: float) -> float:
    return (screen_x - page_left) / zoom


def _doc_y(zoom: float, page_top: float, screen_y: float) -> float:
    return (screen_y - page_top) / zoom


def _triangle(top: int, left: int, right: int, bottom: int) -> QPolygon:
    return QPolygon(
        [QPoint(left, top), QPoint(right, top), QPoint((left + right) // 2, bottom)]
    )


class Ruler(QWidget):
    """Base común para las reglas del editor."""

    margins_changed = Signal(object)

    def __init__(self, editor, parent=None) -> None:
        super().__init__(parent)
        self._editor = editor
        self._drag = None
        self.setMouseTracking(True)

    # --- utilidades --------------------------------------------------------

    def _ui_colors(self) -> dict[str, QColor]:
        """Colores de la regla adaptados al tema de la aplicación y del papel."""
        text = self.palette().color(QPalette.ColorRole.Text)
        dark = text.lightness() > 128
        band = self._editor.palette().color(QPalette.ColorRole.Base)
        ink = (
            QColor("#374151")
            if band.lightness() > 128
            else QColor("#d6dae2")
        )
        if dark:
            return {
                "bg": QColor("#232833"),
                "margin": QColor("#262c39"),
                "edge": QColor("#4b5563"),
                "margin_line": QColor("#5b6472"),
                "band": band,
                "marker": ink,
                "tick": ink,
                "number": ink,
                "cursor": QColor("#f87171"),
            }
        return {
            "bg": QColor("#f3f4f6"),
            "margin": QColor("#eceff3"),
            "edge": QColor("#b6bcc6"),
            "margin_line": QColor("#9aa1ab"),
            "band": band,
            "marker": ink,
            "tick": ink,
            "number": ink,
            "cursor": QColor("#dc2626"),
        }

    def _zoom(self) -> float:
        return self._editor.zoom() / 100.0

    def _setup(self):
        return current_page_setup(self._editor)

    def _page_origin(self) -> QPoint:
        return self._editor.mapTo(self.parentWidget(), QPoint(0, 0))

    def _page_left(self) -> int:
        return self._page_origin().x() - self.x()

    def _page_top(self) -> int:
        return self._page_origin().y() - self.y()

    def _page_width(self) -> int:
        return self._editor.width()

    def _page_height(self) -> int:
        return self._editor.height()

    def _mm_px(self) -> float:
        return MM_TO_PX * self._zoom()

    def _doc_page_width(self) -> float:
        return self._page_width() / self._zoom()

    def _doc_page_height(self) -> float:
        return self._page_height() / self._zoom()

    def _set_margin(self, which: str, value_mm: float) -> None:
        setup = self._setup()
        page_w, page_h = setup.size_mm()
        if setup.orientation == "landscape":
            page_w, page_h = page_h, page_w
        limit = page_w - 10 if which in ("left", "right") else page_h - 10
        clamped = max(0.0, min(value_mm, limit))
        if which == "left":
            setup.left_margin_mm = clamped
        elif which == "right":
            setup.right_margin_mm = clamped
        elif which == "top":
            setup.top_margin_mm = clamped
        elif which == "bottom":
            setup.bottom_margin_mm = clamped
        self.margins_changed.emit(setup)

    def _draw_ticks(
        self,
        painter: QPainter,
        length_mm: float,
        axis: str,
        origin: float,
        mm_px: float,
        thickness: int,
    ) -> None:
        minor_mm = 1
        if mm_px < 3:
            minor_mm = 5
        if mm_px * 5 < 3:
            minor_mm = 10
        medium_mm = 5 if minor_mm <= 5 else 10
        major_mm = 10

        colors = self._ui_colors()
        tick_pen = QPen(
            colors["tick"], 1, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap
        )
        painter.setPen(tick_pen)
        font = QFont(self.font())
        font.setPixelSize(9)
        painter.setFont(font)

        ticks = int(length_mm / minor_mm) + 1
        for index in range(ticks):
            value_mm = index * minor_mm
            if value_mm > length_mm + 0.5:
                break
            if minor_mm <= 1 and value_mm % 5 != 0:
                height = 3
            elif value_mm % medium_mm != 0:
                height = 5
            elif value_mm % major_mm != 0:
                height = 8
            else:
                height = 12
            pos = origin + value_mm * mm_px
            if axis == "h":
                painter.drawLine(int(pos), thickness, int(pos), thickness - height)
                if value_mm % major_mm == 0:
                    painter.setPen(QPen(colors["number"], 1))
                    painter.drawText(
                        QRect(
                            int(pos) - 14,
                            0,
                            28,
                            thickness - height,
                        ),
                        Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom,
                        str(int(value_mm)),
                    )
                    painter.setPen(tick_pen)
            else:
                painter.drawLine(thickness - height, int(pos), thickness, int(pos))
                if value_mm % major_mm == 0:
                    painter.setPen(QPen(colors["number"], 1))
                    painter.save()
                    painter.translate(3, int(pos))
                    painter.rotate(-90)
                    painter.drawText(
                        QRect(-16, -8, 16, 16),
                        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                        str(int(value_mm)),
                    )
                    painter.restore()
                    painter.setPen(tick_pen)

    # --- interacción (por defecto sin acción) ------------------------------

    def mousePressEvent(self, event: QMouseEvent) -> None:
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self._drag = None
        super().mouseReleaseEvent(event)


class HRuler(Ruler):
    """Regla horizontal con marcadores de sangría, tabulaciones y márgenes."""

    def __init__(self, editor, parent=None) -> None:
        super().__init__(editor, parent)
        self.setFixedHeight(_THICKNESS)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        colors = self._ui_colors()
        painter.fillRect(self.rect(), colors["bg"])

        page_left = self._page_left()
        page_width = self._page_width()
        zoom = self._zoom()
        mm_px = self._mm_px()
        setup = self._setup()

        page_right = page_left + page_width
        margin_l = page_left + setup.left_margin_mm * mm_px
        margin_r = page_right - setup.right_margin_mm * mm_px

        painter.fillRect(QRect(page_left, 0, page_width, self.height()), colors["band"])
        if margin_l > page_left:
            self._fill_zone(
                painter, page_left, int(margin_l - page_left)
            )
        if margin_r < page_right:
            self._fill_zone(painter, int(margin_r), int(page_right - margin_r))

        painter.setPen(QPen(colors["edge"], 1))
        painter.drawLine(page_left, 0, page_left, self.height())
        painter.drawLine(page_right - 1, 0, page_right - 1, self.height())

        painter.setPen(QPen(colors["margin_line"], 1))
        painter.drawLine(int(margin_l), 0, int(margin_l), self.height())
        painter.drawLine(int(margin_r), 0, int(margin_r), self.height())

        self._draw_ticks(
            painter, page_width / mm_px, "h", page_left, mm_px, self.height()
        )

        indents = paragraph.current_indents(self._editor)
        first_line_x = page_left + indents["first_line"] * zoom
        left_x = page_left + indents["left"] * zoom
        right_x = page_right - indents["right"] * zoom
        self._draw_first_line(painter, first_line_x, left_x)
        self._draw_left_marker(painter, left_x, indents["left"] == indents["first_line"])
        self._draw_right_marker(painter, right_x)

        painter.setPen(QPen(colors["marker"], 1))
        for tab in paragraph.tab_stops(self._editor):
            x = page_left + tab.position * zoom
            painter.drawLine(int(x), 0, int(x), 8)
            painter.drawLine(int(x), 8, int(x) + 6, 8)

        painter.setPen(QPen(colors["cursor"], 1))
        cursor_x = page_left + self._editor.cursorRect().x()
        painter.drawLine(cursor_x, 0, cursor_x, self.height())
        painter.end()

    def _fill_zone(self, painter: QPainter, x: int, width: int) -> None:
        painter.fillRect(QRect(x, 0, width, self.height()), self._ui_colors()["margin"])

    def _draw_first_line(self, painter: QPainter, x: float, left_x: float) -> None:
        marker = self._ui_colors()["marker"]
        painter.setBrush(marker)
        painter.setPen(QPen(marker, 1))
        if abs(x - left_x) < 2:
            painter.drawPolygon(_triangle(0, int(x) - 4, int(x) + 4, 7))
        else:
            painter.drawPolygon(_triangle(0, int(x) - 4, int(x) + 4, 7))
            painter.drawPolygon(_triangle(7, int(left_x) - 4, int(left_x) + 4, 0))

    def _draw_left_marker(self, painter: QPainter, x: float, combined: bool) -> None:
        marker = self._ui_colors()["marker"]
        painter.setBrush(marker)
        painter.setPen(QPen(marker, 1))
        if combined:
            painter.drawRect(int(x) - 3, self.height() - 6, 6, 6)
        else:
            painter.drawPolygon(
                _triangle(
                    self.height() - 6,
                    int(x) - 4,
                    int(x) + 4,
                    self.height(),
                )
            )

    def _draw_right_marker(self, painter: QPainter, x: float) -> None:
        marker = self._ui_colors()["marker"]
        painter.setBrush(marker)
        painter.setPen(QPen(marker, 1))
        painter.drawPolygon(
            _triangle(
                self.height() - 6,
                int(x) - 4,
                int(x) + 4,
                self.height(),
            )
        )

    # --- interacción -------------------------------------------------------

    def _handles(self):
        zoom = self._zoom()
        page_left = self._page_left()
        page_right = page_left + self._page_width()
        indents = paragraph.current_indents(self._editor)
        setup = self._setup()
        mm_px = self._mm_px()
        handles = []
        for tab in paragraph.tab_stops(self._editor):
            handles.append(("tab", page_left + tab.position * zoom))
        handles.extend(
            [
                ("first_line", page_left + indents["first_line"] * zoom),
                ("left", page_left + indents["left"] * zoom),
                ("right", page_right - indents["right"] * zoom),
                ("margin_l", page_left + setup.left_margin_mm * mm_px),
                ("margin_r", page_right - setup.right_margin_mm * mm_px),
            ]
        )
        return handles

    def _hit(self, x: float):
        for kind, pos in self._handles():
            if abs(pos - x) <= _HIT_TOLERANCE:
                return kind, pos
        return None

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.RightButton:
            hit = self._hit(event.position().x())
            if hit and hit[0] == "tab":
                zoom = self._zoom()
                page_left = self._page_left()
                paragraph.remove_tab_stop(self._editor, (hit[1] - page_left) / zoom)
                self.update()
            event.accept()
            return
        if event.button() == Qt.MouseButton.LeftButton:
            hit = self._hit(event.position().x())
            self._drag = hit
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self._drag is None:
            super().mouseMoveEvent(event)
            return
        x = event.position().x()
        zoom = self._zoom()
        page_left = self._page_left()
        page_width = self._page_width()
        kind, _ = self._drag
        if kind == "first_line":
            value = max(-page_width, min(page_width, _doc_x(zoom, page_left, x)))
            paragraph.set_first_line_indent(self._editor, value)
        elif kind == "left":
            doc = _doc_x(zoom, page_left, x)
            paragraph.set_left_indent(self._editor, max(0.0, doc))
            indents = paragraph.current_indents(self._editor)
            if abs(indents["first_line"] - indents["left"]) < 2:
                paragraph.set_first_line_indent(self._editor, max(0.0, doc))
        elif kind == "right":
            doc = _doc_x(zoom, page_left, x)
            paragraph.set_right_indent(
                self._editor, max(0.0, self._doc_page_width() - doc)
            )
        elif kind == "tab":
            doc = max(0.0, _doc_x(zoom, page_left, x))
            self._move_tab(doc)
        elif kind == "margin_l":
            self._set_margin("left", _doc_x(zoom, page_left, x) / MM_TO_PX)
        elif kind == "margin_r":
            doc = self._doc_page_width() - _doc_x(zoom, page_left, x)
            self._set_margin("right", doc / MM_TO_PX)
        self._drag = (kind, x)
        self.update()
        event.accept()

    def _move_tab(self, doc: float) -> None:
        from PySide6.QtGui import QTextOption

        current_pos = self._drag_doc_pos()
        tabs = [
            tab for tab in paragraph.tab_stops(self._editor)
            if tab.position != current_pos
        ]
        tabs.append(QTextOption.Tab(doc, QTextOption.TabType.LeftTab))
        tabs.sort(key=lambda tab: tab.position)
        paragraph.set_tab_stops(self._editor, tabs)

    def _drag_doc_pos(self) -> float:
        if self._drag is None:
            return -1.0
        kind, pos = self._drag
        if kind != "tab":
            return -1.0
        return (pos - self._page_left()) / self._zoom()

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            hit = self._hit(event.position().x())
            if hit is None:
                zoom = self._zoom()
                doc = _doc_x(zoom, self._page_left(), event.position().x())
                paragraph.add_tab_stop(self._editor, max(0.0, doc))
                self.update()
                event.accept()
                return
        super().mouseDoubleClickEvent(event)


class VRuler(Ruler):
    """Regla vertical con márgenes superior e inferior arrastrables."""

    def __init__(self, editor, parent=None) -> None:
        super().__init__(editor, parent)
        self.setFixedWidth(_THICKNESS)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        colors = self._ui_colors()
        painter.fillRect(self.rect(), colors["bg"])

        page_top = self._page_top()
        page_height = self._page_height()
        mm_px = self._mm_px()
        setup = self._setup()

        page_bottom = page_top + page_height
        margin_top = page_top + setup.top_margin_mm * mm_px
        margin_bottom = page_bottom - setup.bottom_margin_mm * mm_px

        painter.fillRect(QRect(0, page_top, self.width(), page_height), colors["band"])
        if margin_top > page_top:
            self._fill_zone(
                painter, page_top, int(margin_top - page_top)
            )
        if margin_bottom < page_bottom:
            self._fill_zone(
                painter, int(margin_bottom), int(page_bottom - margin_bottom)
            )

        painter.setPen(QPen(colors["edge"], 1))
        painter.drawLine(0, page_top, self.width(), page_top)
        painter.drawLine(0, page_bottom - 1, self.width(), page_bottom - 1)

        painter.setPen(QPen(colors["margin_line"], 1))
        painter.drawLine(0, int(margin_top), self.width(), int(margin_top))
        painter.drawLine(0, int(margin_bottom), self.width(), int(margin_bottom))

        self._draw_ticks(
            painter, page_height / mm_px, "v", page_top, mm_px, self.width()
        )

        marker = colors["marker"]
        painter.setBrush(marker)
        painter.setPen(QPen(marker, 1))
        painter.drawPolygon(_triangle(int(margin_top) - 4, 0, 8, int(margin_top)))
        painter.drawPolygon(_triangle(int(margin_bottom) - 4, 0, 8, int(margin_bottom)))
        painter.end()

    def _fill_zone(self, painter: QPainter, y: int, height: int) -> None:
        painter.fillRect(QRect(0, y, self.width(), height), self._ui_colors()["margin"])

    def _handles(self):
        setup = self._setup()
        mm_px = self._mm_px()
        page_top = self._page_top()
        page_height = self._page_height()
        return [
            ("margin_top", page_top + setup.top_margin_mm * mm_px),
            (
                "margin_bottom",
                page_top + page_height - setup.bottom_margin_mm * mm_px,
            ),
        ]

    def _hit(self, y: float):
        for kind, pos in self._handles():
            if abs(pos - y) <= _HIT_TOLERANCE:
                return kind, pos
        return None

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag = self._hit(event.position().y())
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self._drag is None:
            super().mouseMoveEvent(event)
            return
        kind, _ = self._drag
        y = event.position().y()
        page_top = self._page_top()
        zoom = self._zoom()
        if kind == "margin_top":
            self._set_margin("top", _doc_y(zoom, page_top, y) / MM_TO_PX)
        elif kind == "margin_bottom":
            doc = self._doc_page_height() - _doc_y(zoom, page_top, y)
            self._set_margin("bottom", doc / MM_TO_PX)
        self._drag = (kind, y)
        self.update()
        event.accept()

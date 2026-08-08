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
    QTextCursor,
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
        self._spelling_selections: list = []
        self._grid_visible = False
        self._view_mode = "print"
        self._zoom_percent = 100
        self._macro_recorder = None
        self._completer = None
        self._completer_words: set[str] = set()

    def set_completion_words(self, words: list[str]) -> None:
        from PySide6.QtWidgets import QCompleter

        self._completer_words = set(words)
        completer = QCompleter(sorted(words), self)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setWidget(self)
        completer.activated.connect(self._insert_completion)
        self._completer = completer
        self.setCompleter(completer)

    def completion_words(self) -> list[str]:
        return sorted(self._completer_words)

    def setCompleter(self, completer) -> None:
        if completer is None:
            self._completer = None
            return
        self._completer = completer
        completer.setWidget(self)
        completer.setCompletionMode(completer.CompletionMode.PopupCompletion)
        completer.activated.connect(self._insert_completion)

    def completer(self):
        return self._completer

    def _insert_completion(self, completion: str) -> None:
        cursor = self.textCursor()
        cursor.select(QTextCursor.SelectionType.WordUnderCursor)
        cursor.insertText(completion)
        self.setTextCursor(cursor)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if self._macro_recorder is not None:
            self._macro_recorder.key_pressed(event)
        if self._completer is not None and self._completer.popup().isVisible():
            key = event.key()
            if key in (
                Qt.Key.Key_Enter, Qt.Key.Key_Return, Qt.Key.Key_Escape,
                Qt.Key.Key_Tab, Qt.Key.Key_Backtab,
            ):
                event.ignore()
                return
        if self._track_changes:
            key = event.key()
            if key in (Qt.Key.Key_Backspace, Qt.Key.Key_Delete):
                self._mark_deletion(key)
                return
            if len(event.text()) > 0:
                self._insert_tracked_text(event.text())
                return
        super().keyPressEvent(event)
        self._trigger_completer(event)

    def _trigger_completer(self, event: QKeyEvent) -> None:
        if self._completer is None:
            return
        if event.key() == Qt.Key.Key_Backspace and self.textCursor().positionInBlock() == 0:
            self._completer.popup().hide()
            return
        if event.text() == "" or event.key() == Qt.Key.Key_Backspace:
            return
        cursor = self.textCursor()
        cursor.select(QTextCursor.SelectionType.WordUnderCursor)
        prefix = cursor.selectedText()
        if len(prefix) < 2:
            self._completer.popup().hide()
            return
        self._completer.setCompletionPrefix(prefix)
        if self._completer.completionCount() == 0:
            self._completer.popup().hide()
            return
        rect = self.cursorRect()
        rect.setWidth(
            self._completer.popup().sizeHintForColumn(0)
            + self._completer.popup().verticalScrollBar().sizeHint().width()
        )
        self._completer.complete(rect)

    def set_macro_recorder(self, recorder) -> None:
        self._macro_recorder = recorder

    def macro_recorder(self):
        return self._macro_recorder

    def set_zoom(self, percent: int) -> None:
        target = max(20, min(500, percent))
        delta = (target - self._zoom_percent) / 10.0
        self.zoomInF(delta)
        self._zoom_percent = target

    def zoom(self) -> int:
        return self._zoom_percent

    def set_grid_visible(self, visible: bool) -> None:
        self._grid_visible = visible
        self.viewport().update()

    def grid_visible(self) -> bool:
        return self._grid_visible

    def set_view_mode(self, mode: str) -> None:
        """Modos: 'read', 'print', 'web', 'outline', 'draft'."""
        self._view_mode = mode
        if mode == "web":
            self.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
            self.document().setDefaultStyleSheet(
                "body { max-width: 900px; margin: 0 auto; }"
            )
        else:
            self.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)

    def view_mode(self) -> str:
        return self._view_mode

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if self.isReadOnly():
            position = self.cursorForPosition(event.position().toPoint()).position()
            from rword.core.forms import field_at, handle_field_click

            if field_at(self, position) is not None:
                handle_field_click(self, position)
                return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            href = self.anchorAt(event.position().toPoint())
            if href:
                self.link_clicked.emit(href)
                return
        super().mouseReleaseEvent(event)

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
        self.setExtraSelections(
            self._find_selections
            + self._comment_selections
            + self._spelling_selections
        )

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
        if self._grid_visible:
            self._paint_grid()
        if self._watermark:
            self._paint_watermark()

    def _paint_grid(self) -> None:
        painter = QPainter(self.viewport())
        painter.setPen(QColor(0, 0, 0, 18))
        step = 20
        width = self.viewport().width()
        height = self.viewport().height()
        for x in range(step, width, step):
            painter.drawLine(x, 0, x, height)
        for y in range(step, height, step):
            painter.drawLine(0, y, width, y)
        painter.end()

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

"""Controles de formato de párrafo embebibles en la cinta."""

from __future__ import annotations

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QSizePolicy,
    QToolButton,
    QWidget,
)

from rword.core import paragraph
from rword.ui.editor import Editor
from rword.ui.icons import IconManager, icon_color_for


class ParagraphBar(QWidget):
    """Controles de párrafo distribuidos en dos filas."""

    def __init__(self, editor: Editor, parent=None, icon_manager=None) -> None:
        super().__init__(parent)
        self._editor = editor
        self._icons = icon_manager or IconManager(icon_color_for(self))
        self._grid = QGridLayout(self)
        self._grid.setContentsMargins(2, 0, 2, 0)
        self._grid.setSpacing(2)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self._build()

    def _icon(self, action: QAction, name: str) -> QAction:
        self._icons.register(action, name, 16)
        return action

    def _add_button(self, action: QAction, row: int, col: int) -> QToolButton:
        button = QToolButton(self)
        button.setDefaultAction(action)
        button.setIconSize(QSize(16, 16))
        button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        button.setFixedSize(24, 24)
        button.setToolTip(action.text())
        self._grid.addWidget(button, row, col)
        return button

    def _add_separator(self, row: int, col: int, rows: int = 1) -> None:
        line = QFrame(self)
        line.setFrameShape(QFrame.Shape.VLine)
        line.setStyleSheet("color: #d1d5db;")
        self._grid.addWidget(line, row, col, rows, 1)

    def _build(self) -> None:
        self.align_left_action = self._add_alignment(
            "Alinear izquierda", "left", "align-left", 0, 0
        )
        self.align_center_action = self._add_alignment(
            "Centrar", "center", "align-center", 0, 1
        )
        self.align_right_action = self._add_alignment(
            "Alinear derecha", "right", "align-right", 0, 2
        )
        self.align_justify_action = self._add_alignment(
            "Justificar", "justify", "align-justify", 0, 3
        )

        self._add_separator(0, 4, 2)

        self.bullets_action = QAction("Viñetas", self)
        self.bullets_action.triggered.connect(
            lambda: paragraph.toggle_bullets(self._editor)
        )
        self._add_button(self._icon(self.bullets_action, "list"), 0, 5)

        self.numbering_action = QAction("Numeración", self)
        self.numbering_action.triggered.connect(
            lambda: paragraph.toggle_numbering(self._editor)
        )
        self._add_button(self._icon(self.numbering_action, "list-ordered"), 0, 6)

        self._add_separator(0, 7, 2)

        self.indent_more_action = QAction("Aumentar sangría", self)
        self.indent_more_action.triggered.connect(
            lambda: paragraph.increase_indent(self._editor)
        )
        self._add_button(
            self._icon(self.indent_more_action, "indent-increase"), 1, 0
        )

        self.indent_less_action = QAction("Disminuir sangría", self)
        self.indent_less_action.triggered.connect(
            lambda: paragraph.decrease_indent(self._editor)
        )
        self._add_button(
            self._icon(self.indent_less_action, "indent-decrease"), 1, 1
        )

        self._add_separator(1, 2, 1)

        self.spacing_single_action = self._add_spacing(
            "Interlineado sencillo", 1.0, "align-left", 1, 3
        )
        self.spacing_1_5_action = self._add_spacing(
            "Interlineado 1,5", 1.5, "align-center", 1, 4
        )
        self.spacing_double_action = self._add_spacing(
            "Interlineado doble", 2.0, "align-right", 1, 5
        )

        self._alignment_actions = [
            (self.align_left_action, Qt.AlignmentFlag.AlignLeft),
            (self.align_center_action, Qt.AlignmentFlag.AlignCenter),
            (self.align_right_action, Qt.AlignmentFlag.AlignRight),
            (self.align_justify_action, Qt.AlignmentFlag.AlignJustify),
        ]
        self._editor.cursorPositionChanged.connect(self._sync)

    def _add_alignment(self, label, name, icon_name="", row: int = 0, col: int = 0):
        action = QAction(label, self)
        action.setCheckable(True)
        action.triggered.connect(
            lambda checked, a=name: paragraph.set_alignment(self._editor, a)
        )
        if icon_name:
            self._icon(action, icon_name)
        self._add_button(action, row, col)
        return action

    def _add_spacing(self, label, factor, icon_name="", row: int = 0, col: int = 0):
        action = QAction(label, self)
        action.setCheckable(True)
        action.triggered.connect(
            lambda checked, f=factor: paragraph.set_line_spacing(self._editor, f)
        )
        if icon_name:
            self._icon(action, icon_name)
        self._add_button(action, row, col)
        return action

    def _sync(self) -> None:
        alignment = paragraph.current_alignment(self._editor)
        for action, flag in self._alignment_actions:
            action.blockSignals(True)
            action.setChecked(alignment == flag)
            action.blockSignals(False)
        spacing = paragraph.current_line_spacing(self._editor)
        spacing_actions = {
            1.0: self.spacing_single_action,
            1.5: self.spacing_1_5_action,
            2.0: self.spacing_double_action,
        }
        for factor, action in spacing_actions.items():
            action.blockSignals(True)
            action.setChecked(abs(spacing - factor) < 0.01)
            action.blockSignals(False)

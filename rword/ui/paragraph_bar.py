"""Controles de formato de párrafo embebibles en la cinta."""

from __future__ import annotations

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QSizePolicy,
    QToolButton,
    QWidget,
)

from rword.core import paragraph
from rword.ui.editor import Editor


class ParagraphBar(QWidget):
    """Fila de controles de párrafo: alineación, listas, sangrías y espaciado."""

    def __init__(self, editor: Editor, parent=None) -> None:
        super().__init__(parent)
        self._editor = editor
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(2, 0, 2, 0)
        self._layout.setSpacing(2)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self._build()

    def _add_button(self, action: QAction) -> QToolButton:
        button = QToolButton(self)
        button.setDefaultAction(action)
        button.setIconSize(QSize(16, 16))
        button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        button.setFixedSize(24, 24)
        button.setToolTip(action.text())
        self._layout.addWidget(button)
        return button

    def _add_separator(self) -> None:
        line = QFrame(self)
        line.setFrameShape(QFrame.Shape.VLine)
        line.setStyleSheet("color: #d1d5db;")
        self._layout.addWidget(line)

    def _build(self) -> None:
        self.align_left_action = self._add_alignment("Alinear izquierda", "left")
        self.align_center_action = self._add_alignment("Centrar", "center")
        self.align_right_action = self._add_alignment("Alinear derecha", "right")
        self.align_justify_action = self._add_alignment("Justificar", "justify")

        self._add_separator()

        self.bullets_action = QAction("Viñetas", self)
        self.bullets_action.triggered.connect(
            lambda: paragraph.toggle_bullets(self._editor)
        )
        self._add_button(self.bullets_action)

        self.numbering_action = QAction("Numeración", self)
        self.numbering_action.triggered.connect(
            lambda: paragraph.toggle_numbering(self._editor)
        )
        self._add_button(self.numbering_action)

        self._add_separator()

        self.indent_more_action = QAction("Aumentar sangría", self)
        self.indent_more_action.triggered.connect(
            lambda: paragraph.increase_indent(self._editor)
        )
        self._add_button(self.indent_more_action)

        self.indent_less_action = QAction("Disminuir sangría", self)
        self.indent_less_action.triggered.connect(
            lambda: paragraph.decrease_indent(self._editor)
        )
        self._add_button(self.indent_less_action)

        self._add_separator()

        self.spacing_single_action = self._add_spacing("Interlineado sencillo", 1.0)
        self.spacing_1_5_action = self._add_spacing("Interlineado 1,5", 1.5)
        self.spacing_double_action = self._add_spacing("Interlineado doble", 2.0)

        self._alignment_actions = [
            (self.align_left_action, Qt.AlignmentFlag.AlignLeft),
            (self.align_center_action, Qt.AlignmentFlag.AlignCenter),
            (self.align_right_action, Qt.AlignmentFlag.AlignRight),
            (self.align_justify_action, Qt.AlignmentFlag.AlignJustify),
        ]
        self._editor.cursorPositionChanged.connect(self._sync)

    def _add_alignment(self, label, name):
        action = QAction(label, self)
        action.setCheckable(True)
        action.triggered.connect(
            lambda checked, a=name: paragraph.set_alignment(self._editor, a)
        )
        self._add_button(action)
        return action

    def _add_spacing(self, label, factor):
        action = QAction(label, self)
        action.setCheckable(True)
        action.triggered.connect(
            lambda checked, f=factor: paragraph.set_line_spacing(self._editor, f)
        )
        self._add_button(action)
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

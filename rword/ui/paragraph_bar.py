"""Barra de herramientas de formato de párrafo."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QToolBar

from rword.core import paragraph
from rword.ui.editor import Editor


class ParagraphBar(QToolBar):
    """Barra de párrafo con alineación, sangría, listas y espaciado."""

    def __init__(self, editor: Editor, parent=None) -> None:
        super().__init__("Párrafo", parent)
        self.setObjectName("paragraph_toolbar")
        self.setMovable(False)
        self._editor = editor
        self._build()

    def _build(self) -> None:
        self.align_left_action = self._add_alignment(
            "Alinear izquierda", "left"
        )
        self.align_center_action = self._add_alignment(
            "Centrar", "center"
        )
        self.align_right_action = self._add_alignment(
            "Alinear derecha", "right"
        )
        self.align_justify_action = self._add_alignment(
            "Justificar", "justify"
        )

        self.addSeparator()

        self.bullets_action = QAction("Viñetas", self)
        self.bullets_action.triggered.connect(
            lambda: paragraph.toggle_bullets(self._editor)
        )
        self.addAction(self.bullets_action)

        self.numbering_action = QAction("Numeración", self)
        self.numbering_action.triggered.connect(
            lambda: paragraph.toggle_numbering(self._editor)
        )
        self.addAction(self.numbering_action)

        self.addSeparator()

        self.indent_more_action = QAction("Aumentar sangría", self)
        self.indent_more_action.triggered.connect(
            lambda: paragraph.increase_indent(self._editor)
        )
        self.addAction(self.indent_more_action)

        self.indent_less_action = QAction("Disminuir sangría", self)
        self.indent_less_action.triggered.connect(
            lambda: paragraph.decrease_indent(self._editor)
        )
        self.addAction(self.indent_less_action)

        self.addSeparator()

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
        self.addAction(action)
        return action

    def _add_spacing(self, label, factor):
        action = QAction(label, self)
        action.setCheckable(True)
        action.triggered.connect(
            lambda checked, f=factor: paragraph.set_line_spacing(self._editor, f)
        )
        self.addAction(action)
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

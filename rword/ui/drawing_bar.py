"""Barra de herramientas de dibujo a mano alzada."""

from __future__ import annotations

from PySide6.QtGui import QAction, QColor
from PySide6.QtWidgets import (
    QColorDialog,
    QComboBox,
    QSpinBox,
    QToolBar,
)

from rword.ui.editor import Editor


class DrawingBar(QToolBar):
    """Barra de dibujo con lápiz, resaltador y borrador."""

    def __init__(self, editor: Editor, parent=None) -> None:
        super().__init__("Dibujar", parent)
        self.setObjectName("drawing_toolbar")
        self.setMovable(False)
        self._editor = editor
        self._color = QColor("#000000")
        self._width = 2.0
        self._build()

    def _build(self) -> None:
        self._tool_combo = QComboBox(self)
        self._tool_combo.addItems(["Lápiz", "Pluma", "Resaltador", "Borrador"])
        self._tool_combo.currentIndexChanged.connect(self._update_tool)
        self.addWidget(self._tool_combo)

        self._width_spin = QSpinBox(self)
        self._width_spin.setRange(1, 20)
        self._width_spin.setValue(2)
        self._width_spin.valueChanged.connect(self._update_width)
        self.addWidget(self._width_spin)

        self.color_action = QAction("Color...", self)
        self.color_action.triggered.connect(self._choose_color)
        self.addAction(self.color_action)

        self.addSeparator()

        self.enable_action = QAction("Activar dibujo", self)
        self.enable_action.setCheckable(True)
        self.enable_action.triggered.connect(self._toggle)
        self.addAction(self.enable_action)

    def _tool_key(self) -> str:
        return {
            0: "pencil",
            1: "pen",
            2: "highlighter",
            3: "eraser",
        }.get(self._tool_combo.currentIndex(), "pencil")

    def _update_tool(self) -> None:
        if self.enable_action.isChecked():
            self._apply()

    def _update_width(self, value: int) -> None:
        self._width = float(value)
        if self.enable_action.isChecked():
            self._apply()

    def _choose_color(self) -> None:
        color = QColorDialog.getColor(self._color, self, "Color de dibujo")
        if color.isValid():
            self._color = color
            if self.enable_action.isChecked():
                self._apply()

    def _toggle(self, checked: bool) -> None:
        self._apply() if checked else self._editor.set_drawing(False)

    def _apply(self) -> None:
        kind = self._tool_key()
        width = self._width
        if kind == "highlighter":
            width = max(6.0, width * 2)
        self._editor.set_drawing(
            True, kind, self._color, self._width
        )

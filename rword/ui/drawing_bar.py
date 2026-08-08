"""Controles de dibujo a mano alzada embebibles en la cinta."""

from __future__ import annotations

from PySide6.QtCore import QSize
from PySide6.QtGui import QAction, QColor
from PySide6.QtWidgets import (
    QColorDialog,
    QComboBox,
    QGridLayout,
    QLabel,
    QSizePolicy,
    QSpinBox,
    QWidget,
)

from rword.ui.editor import Editor
from rword.ui.icons import IconManager, icon_color_for


class DrawingBar(QWidget):
    """Controles de dibujo distribuidos en dos filas."""

    def __init__(self, editor: Editor, parent=None, icon_manager=None) -> None:
        super().__init__(parent)
        self._editor = editor
        self._icons = icon_manager or IconManager(icon_color_for(self))
        self._color = QColor("#000000")
        self._width = 2.0
        self._grid = QGridLayout(self)
        self._grid.setContentsMargins(2, 0, 2, 0)
        self._grid.setSpacing(4)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self._build()

    def _build(self) -> None:
        self._grid.addWidget(QLabel("Herramienta:", self), 0, 0)
        self._tool_combo = QComboBox(self)
        self._tool_combo.addItems(["Lápiz", "Pluma", "Resaltador", "Borrador"])
        self._tool_combo.setFixedWidth(110)
        self._tool_combo.currentIndexChanged.connect(self._update_tool)
        self._grid.addWidget(self._tool_combo, 0, 1)

        self._grid.addWidget(QLabel("Grosor:", self), 0, 2)
        self._width_spin = QSpinBox(self)
        self._width_spin.setRange(1, 20)
        self._width_spin.setValue(2)
        self._width_spin.valueChanged.connect(self._update_width)
        self._grid.addWidget(self._width_spin, 0, 3)

        self.color_action = QAction("Color...", self)
        self.color_action.triggered.connect(self._choose_color)
        self._icons.register(self.color_action, "palette", 16)
        self._grid.addWidget(self._action_button(self.color_action), 1, 0)

        self.enable_action = QAction("Activar dibujo", self)
        self.enable_action.setCheckable(True)
        self.enable_action.toggled.connect(self._toggle)
        self._icons.register(self.enable_action, "paintbrush", 16)
        self._grid.addWidget(self._action_button(self.enable_action), 1, 1)

    def _action_button(self, action: QAction):
        from PySide6.QtCore import Qt
        from PySide6.QtWidgets import QToolButton

        button = QToolButton(self)
        button.setDefaultAction(action)
        button.setIconSize(QSize(16, 16))
        button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        button.setFixedHeight(26)
        return button

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
        self._editor.set_drawing(True, kind, self._color, self._width)

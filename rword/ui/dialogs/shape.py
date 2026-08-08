"""Diálogos para insertar formas y WordArt."""

from __future__ import annotations

from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QSpinBox,
)

from rword.core.shapes import SHAPE_LABELS, WORDART_STYLES


class ShapeDialog(QDialog):
    """Configura tipo, tamaño y colores de la forma."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Insertar forma")
        self.setMinimumWidth(320)
        self._fill_color = "#ffffff"
        self._border_color = "#000000"
        self._build_ui()

    def _build_ui(self) -> None:
        form = QFormLayout(self)

        self._kind_combo = QComboBox(self)
        for key, label in SHAPE_LABELS.items():
            self._kind_combo.addItem(label, key)
        form.addRow("Forma:", self._kind_combo)

        self._width_spin = QSpinBox(self)
        self._width_spin.setRange(20, 1000)
        self._width_spin.setValue(120)
        form.addRow("Ancho:", self._width_spin)

        self._height_spin = QSpinBox(self)
        self._height_spin.setRange(20, 1000)
        self._height_spin.setValue(80)
        form.addRow("Alto:", self._height_spin)

        self._fill_button = QPushButton("Elegir...", self)
        self._fill_button.clicked.connect(self._choose_fill)
        form.addRow("Relleno:", self._fill_button)

        self._border_button = QPushButton("Elegir...", self)
        self._border_button.clicked.connect(self._choose_border)
        form.addRow("Contorno:", self._border_button)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)

    def _choose_fill(self) -> None:
        from PySide6.QtWidgets import QColorDialog

        color = QColorDialog.getColor(QColor(self._fill_color), self, "Color de relleno")
        if color.isValid():
            self._fill_color = color.name()

    def _choose_border(self) -> None:
        from PySide6.QtWidgets import QColorDialog

        color = QColorDialog.getColor(QColor(self._border_color), self, "Color de contorno")
        if color.isValid():
            self._border_color = color.name()

    def values(self) -> dict:
        return {
            "kind": self._kind_combo.currentData(),
            "width": self._width_spin.value(),
            "height": self._height_spin.value(),
            "fill": self._fill_color,
            "border": self._border_color,
        }


class WordArtDialog(QDialog):
    """Configura el texto y el estilo del WordArt."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Insertar WordArt")
        self.setMinimumWidth(340)
        form = QFormLayout(self)
        self._text_input = QLineEdit(self)
        self._text_input.setPlaceholderText("Texto del WordArt")
        form.addRow("Texto:", self._text_input)
        self._style_combo = QComboBox(self)
        self._style_combo.addItems(WORDART_STYLES.keys())
        form.addRow("Estilo:", self._style_combo)
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)

    def values(self) -> tuple[str, str]:
        return self._text_input.text(), self._style_combo.currentText()

"""Diálogo de configuración de página."""

from __future__ import annotations

from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QColorDialog,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from rword.core.pages import PAPER_SIZES_MM, PageSetup


class PageSetupDialog(QDialog):
    """Configura tamaño, orientación, márgenes, color de página y marca de agua."""

    def __init__(self, setup: PageSetup, parent=None) -> None:
        super().__init__(parent)
        self._setup = setup
        self.setWindowTitle("Configurar página")
        self.setMinimumWidth(380)
        self._build_ui()
        self._load(setup)

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self._size_combo = QComboBox(self)
        self._size_combo.addItems(list(PAPER_SIZES_MM) + ["Personalizado"])
        form.addRow("Tamaño de papel:", self._size_combo)

        size_row = QHBoxLayout()
        self._width_spin = QDoubleSpinBox(self)
        self._width_spin.setRange(50, 1200)
        self._width_spin.setSuffix(" mm")
        self._height_spin = QDoubleSpinBox(self)
        self._height_spin.setRange(50, 1200)
        self._height_spin.setSuffix(" mm")
        size_row.addWidget(self._width_spin)
        size_row.addWidget(self._height_spin)
        form.addRow("Ancho × Alto:", size_row)

        self._orientation_combo = QComboBox(self)
        self._orientation_combo.addItem("Vertical", "portrait")
        self._orientation_combo.addItem("Horizontal", "landscape")
        form.addRow("Orientación:", self._orientation_combo)

        self._left_spin = self._margin_spin(form, "Margen izquierdo:")
        self._right_spin = self._margin_spin(form, "Margen derecho:")
        self._top_spin = self._margin_spin(form, "Margen superior:")
        self._bottom_spin = self._margin_spin(form, "Margen inferior:")

        self._color_button = QPushButton("Elegir color...", self)
        self._color_button.clicked.connect(self._choose_color)
        form.addRow("Color de página:", self._color_button)

        self._watermark_input = QLineEdit(self)
        self._watermark_input.setPlaceholderText("Texto de marca de agua (vacío = sin marca)")
        form.addRow("Marca de agua:", self._watermark_input)

        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _margin_spin(self, form, label) -> QDoubleSpinBox:
        spin = QDoubleSpinBox(self)
        spin.setRange(0, 200)
        spin.setValue(25)
        spin.setSuffix(" mm")
        form.addRow(label, spin)
        return spin

    def _load(self, setup: PageSetup) -> None:
        index = self._size_combo.findText(setup.size)
        self._size_combo.setCurrentIndex(index if index >= 0 else 0)
        self._width_spin.setValue(setup.custom_width_mm)
        self._height_spin.setValue(setup.custom_height_mm)
        index = self._orientation_combo.findData(setup.orientation)
        self._orientation_combo.setCurrentIndex(max(0, index))
        self._left_spin.setValue(setup.left_margin_mm)
        self._right_spin.setValue(setup.right_margin_mm)
        self._top_spin.setValue(setup.top_margin_mm)
        self._bottom_spin.setValue(setup.bottom_margin_mm)
        self._watermark_input.setText(setup.watermark)

    def _choose_color(self) -> None:
        color = QColorDialog.getColor(
            QColor(self._setup.page_color), self, "Color de página"
        )
        if color.isValid():
            self._setup.page_color = color.name()

    def setup(self) -> PageSetup:
        return PageSetup(
            size=self._size_combo.currentText(),
            custom_width_mm=self._width_spin.value(),
            custom_height_mm=self._height_spin.value(),
            orientation=self._orientation_combo.currentData(),
            left_margin_mm=self._left_spin.value(),
            right_margin_mm=self._right_spin.value(),
            top_margin_mm=self._top_spin.value(),
            bottom_margin_mm=self._bottom_spin.value(),
            page_color=self._setup.page_color,
            watermark=self._watermark_input.text().strip(),
        )

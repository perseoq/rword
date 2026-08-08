"""Diálogos de ajuste de imágenes."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QSlider,
    QSpinBox,
    QVBoxLayout,
)


class ImageSizeDialog(QDialog):
    """Configura el tamaño de la imagen en píxeles."""

    def __init__(self, width: int, height: int, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Tamaño de imagen")
        self.setMinimumWidth(280)
        form = QFormLayout(self)
        self._width_spin = QSpinBox(self)
        self._width_spin.setRange(1, 5000)
        self._width_spin.setValue(width)
        self._height_spin = QSpinBox(self)
        self._height_spin.setRange(1, 5000)
        self._height_spin.setValue(height)
        form.addRow("Ancho (px):", self._width_spin)
        form.addRow("Alto (px):", self._height_spin)
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)

    def width(self) -> int:
        return self._width_spin.value()

    def height(self) -> int:
        return self._height_spin.value()


class CropDialog(QDialog):
    """Configura la región de recorte de la imagen."""

    def __init__(self, width: int, height: int, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Recortar imagen")
        self.setMinimumWidth(280)
        form = QFormLayout(self)
        self._x_spin = self._add_spin(form, "X:", 0, width)
        self._y_spin = self._add_spin(form, "Y:", 0, height)
        self._w_spin = self._add_spin(form, "Ancho:", 1, width)
        self._h_spin = self._add_spin(form, "Alto:", 1, height)
        self._w_spin.setValue(width)
        self._h_spin.setValue(height)
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)

    def _add_spin(self, form, label, minimum, maximum):
        spin = QSpinBox(self)
        spin.setRange(minimum, maximum)
        form.addRow(label, spin)
        return spin

    def rect(self):
        from PySide6.QtCore import QRect

        return QRect(
            self._x_spin.value(),
            self._y_spin.value(),
            self._w_spin.value(),
            self._h_spin.value(),
        )


class AdjustDialog(QDialog):
    """Ajusta brillo, contraste y saturación de la imagen."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Ajustar imagen")
        self.setMinimumWidth(340)
        layout = QVBoxLayout(self)
        self._sliders = {}
        for label, minimum, maximum, default in (
            ("Brillo", -100, 100, 0),
            ("Contraste", -100, 100, 0),
            ("Saturación", -100, 100, 0),
        ):
            row = QHBoxLayout()
            row.addWidget(QLabel(label, self))
            slider = QSlider(Qt.Orientation.Horizontal, self)
            slider.setRange(minimum, maximum)
            slider.setValue(default)
            row.addWidget(slider)
            layout.addLayout(row)
            self._sliders[label] = slider
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def values(self) -> tuple[int, float, float]:
        brightness = self._sliders["Brillo"].value()
        contrast = 1.0 + self._sliders["Contraste"].value() / 100.0
        saturation = 1.0 + self._sliders["Saturación"].value() / 100.0
        return brightness, contrast, saturation

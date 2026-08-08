"""Diálogo para crear y modificar estilos."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QLineEdit,
)

from rword.core.styles import Style


class StyleDialog(QDialog):
    """Crea o modifica un estilo de párrafo/carácter."""

    def __init__(self, style: Style | None = None, parent=None) -> None:
        super().__init__(parent)
        self._style = style
        self.setWindowTitle(
            "Modificar estilo" if style else "Nuevo estilo"
        )
        self.setMinimumWidth(380)
        self._build_ui()
        self._load(style or Style(""))

    def _build_ui(self) -> None:
        form = QFormLayout(self)

        self._name_input = QLineEdit(self)
        form.addRow("Nombre:", self._name_input)

        self._family_input = QLineEdit(self)
        self._family_input.setPlaceholderText("p. ej. Arial, Sans Serif, Monospace")
        form.addRow("Fuente:", self._family_input)

        self._size_spin = QDoubleSpinBox(self)
        self._size_spin.setRange(4, 144)
        form.addRow("Tamaño:", self._size_spin)

        self._bold_check = QCheckBox("Negrita", self)
        self._italic_check = QCheckBox("Cursiva", self)
        form.addRow("", self._bold_check)
        form.addRow("", self._italic_check)

        self._color_input = QLineEdit(self)
        self._color_input.setPlaceholderText("#000000")
        form.addRow("Color (hex):", self._color_input)

        self._alignment_combo = QComboBox(self)
        for label, value in (
            ("Izquierda", "left"),
            ("Centrado", "center"),
            ("Derecha", "right"),
            ("Justificado", "justify"),
        ):
            self._alignment_combo.addItem(label, value)
        form.addRow("Alineación:", self._alignment_combo)

        self._spacing_spin = QDoubleSpinBox(self)
        self._spacing_spin.setRange(0.5, 5.0)
        self._spacing_spin.setSingleStep(0.5)
        form.addRow("Interlineado:", self._spacing_spin)

        self._indent_spin = QDoubleSpinBox(self)
        self._indent_spin.setRange(0, 500)
        self._indent_spin.setSuffix(" px")
        form.addRow("Sangría izquierda:", self._indent_spin)

        self._space_before_spin = QDoubleSpinBox(self)
        self._space_before_spin.setRange(0, 500)
        self._space_before_spin.setSuffix(" px")
        form.addRow("Espacio antes:", self._space_before_spin)

        self._space_after_spin = QDoubleSpinBox(self)
        self._space_after_spin.setRange(0, 500)
        self._space_after_spin.setSuffix(" px")
        form.addRow("Espacio después:", self._space_after_spin)

        self._heading_check = QCheckBox("Estilo de título", self)
        form.addRow("", self._heading_check)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)

    def _load(self, style: Style) -> None:
        self._name_input.setText(style.name)
        self._family_input.setText(style.font_family)
        self._size_spin.setValue(style.font_size)
        self._bold_check.setChecked(style.bold)
        self._italic_check.setChecked(style.italic)
        self._color_input.setText(style.color)
        index = self._alignment_combo.findData(style.alignment)
        if index >= 0:
            self._alignment_combo.setCurrentIndex(index)
        self._spacing_spin.setValue(style.line_spacing)
        self._indent_spin.setValue(style.left_indent)
        self._space_before_spin.setValue(style.space_before)
        self._space_after_spin.setValue(style.space_after)
        self._heading_check.setChecked(style.is_heading)

    def style(self) -> Style:
        return Style(
            name=self._name_input.text().strip(),
            font_family=self._family_input.text().strip() or "Sans Serif",
            font_size=self._size_spin.value(),
            bold=self._bold_check.isChecked(),
            italic=self._italic_check.isChecked(),
            color=self._color_input.text().strip() or "#000000",
            alignment=self._alignment_combo.currentData(),
            line_spacing=self._spacing_spin.value(),
            left_indent=self._indent_spin.value(),
            space_before=self._space_before_spin.value(),
            space_after=self._space_after_spin.value(),
            is_heading=self._heading_check.isChecked(),
        )

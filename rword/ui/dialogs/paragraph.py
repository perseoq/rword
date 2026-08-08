"""Diálogo avanzado de formato de párrafo."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
)

from rword.core import paragraph


class ParagraphDialog(QDialog):
    """Configura sangrías, espaciado e interlineado de los párrafos."""

    def __init__(self, editor, parent=None) -> None:
        super().__init__(parent)
        self._editor = editor
        self.setWindowTitle("Formato de párrafo")
        self.setMinimumWidth(360)
        self._build_ui()
        self._load_current()

    def _build_ui(self) -> None:
        form = QFormLayout(self)

        self._alignment_combo = QComboBox(self)
        self._alignment_combo.addItem("Izquierda", "left")
        self._alignment_combo.addItem("Centrado", "center")
        self._alignment_combo.addItem("Derecha", "right")
        self._alignment_combo.addItem("Justificado", "justify")
        form.addRow("Alineación:", self._alignment_combo)

        self._left_spin = self._add_spin(form, "Sangría izquierda:")
        self._right_spin = self._add_spin(form, "Sangría derecha:")
        self._first_line_spin = self._add_spin(form, "Primera línea:")

        self._spacing_spin = QDoubleSpinBox(self)
        self._spacing_spin.setRange(0.5, 5.0)
        self._spacing_spin.setSingleStep(0.5)
        form.addRow("Interlineado (x):", self._spacing_spin)

        self._space_before_spin = self._add_spin(form, "Espacio antes:")
        self._space_after_spin = self._add_spin(form, "Espacio después:")

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        buttons.accepted.connect(self._apply)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)

    def _add_spin(self, form, label) -> QDoubleSpinBox:
        spin = QDoubleSpinBox(self)
        spin.setRange(0.0, 500.0)
        spin.setSuffix(" px")
        form.addRow(label, spin)
        return spin

    def _load_current(self) -> None:
        fmt = self._editor.textCursor().block().blockFormat()
        self._left_spin.setValue(fmt.leftMargin())
        self._right_spin.setValue(fmt.rightMargin())
        self._first_line_spin.setValue(fmt.textIndent())
        index = self._alignment_combo.findData(
            paragraph.current_alignment(self._editor)
        )
        if index >= 0:
            self._alignment_combo.setCurrentIndex(index)
        if fmt.lineHeightType() == 1:
            self._spacing_spin.setValue(fmt.lineHeight() / 100.0)
        self._space_before_spin.setValue(fmt.topMargin())
        self._space_after_spin.setValue(fmt.bottomMargin())

    def _apply(self) -> None:
        paragraph.set_alignment(
            self._editor, self._alignment_combo.currentData()
        )
        paragraph.set_left_indent(self._editor, self._left_spin.value())
        paragraph.set_right_indent(self._editor, self._right_spin.value())
        paragraph.set_first_line_indent(
            self._editor, self._first_line_spin.value()
        )
        paragraph.set_line_spacing(self._editor, self._spacing_spin.value())
        paragraph.set_space_before(self._editor, self._space_before_spin.value())
        paragraph.set_space_after(self._editor, self._space_after_spin.value())
        self.accept()

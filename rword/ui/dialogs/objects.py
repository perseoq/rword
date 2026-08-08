"""Diálogos para insertar símbolos, gráficos, SmartArt y ecuaciones."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
)

from rword.core.inserts import EQUATION_SYMBOLS, SYMBOLS


class SymbolDialog(QDialog):
    """Inserta un símbolo o carácter especial en el documento."""

    def __init__(self, editor, parent=None) -> None:
        super().__init__(parent)
        self._editor = editor
        self.setWindowTitle("Símbolo")
        self.setMinimumSize(320, 380)
        layout = QVBoxLayout(self)

        self._category_combo = QComboBox(self)
        self._category_combo.addItems(SYMBOLS.keys())
        self._category_combo.currentIndexChanged.connect(self._reload)
        layout.addWidget(self._category_combo)

        self._list = QListWidget(self)
        self._list.itemClicked.connect(self._insert)
        self._list.itemDoubleClicked.connect(lambda _: self.accept())
        layout.addWidget(self._list)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close, self)
        buttons.rejected.connect(self.accept)
        layout.addWidget(buttons)
        self._reload()

    def _reload(self) -> None:
        self._list.clear()
        category = self._category_combo.currentText()
        for symbol in SYMBOLS.get(category, []):
            self._list.addItem(QListWidgetItem(symbol))

    def _insert(self, item: QListWidgetItem) -> None:
        from rword.core.inserts import insert_symbol

        insert_symbol(self._editor, item.text())


class ChartDialog(QDialog):
    """Configura los valores de un gráfico de barras."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Insertar gráfico")
        self.setMinimumWidth(360)
        form = QFormLayout(self)
        self._values_input = QLineEdit(self)
        self._values_input.setPlaceholderText("10, 20, 15, 30")
        form.addRow("Valores:", self._values_input)
        self._labels_input = QLineEdit(self)
        self._labels_input.setPlaceholderText("A, B, C, D")
        form.addRow("Etiquetas:", self._labels_input)
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)

    def values(self) -> list[float]:
        parts = self._values_input.text().split(",")
        result = []
        for part in parts:
            try:
                result.append(float(part.strip()))
            except ValueError:
                continue
        return result

    def labels(self) -> list[str]:
        return [label.strip() for label in self._labels_input.text().split(",")]


class SmartArtDialog(QDialog):
    """Configura los elementos de un diagrama."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Insertar SmartArt")
        self.setMinimumWidth(380)
        form = QFormLayout(self)
        self._items_input = QLineEdit(self)
        self._items_input.setPlaceholderText("Director, Gerente, Supervisor")
        form.addRow("Elementos:", self._items_input)
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)

    def items(self) -> list[str]:
        return [
            item.strip()
            for item in self._items_input.text().split(",")
            if item.strip()
        ]


class EquationDialog(QDialog):
    """Inserta una ecuación predefinida o personalizada."""

    def __init__(self, editor, parent=None) -> None:
        super().__init__(parent)
        self._editor = editor
        self.setWindowTitle("Insertar ecuación")
        self.setMinimumSize(360, 340)
        layout = QVBoxLayout(self)
        self._list = QListWidget(self)
        for label, equation in EQUATION_SYMBOLS.items():
            item = QListWidgetItem(f"{label}   {equation}")
            item.setData(256, equation)
            self._list.addItem(item)
        self._list.itemDoubleClicked.connect(self._insert)
        layout.addWidget(self._list)

        form = QHBoxLayout()
        self._custom_input = QLineEdit(self)
        self._custom_input.setPlaceholderText("Ecuación personalizada...")
        form.addWidget(self._custom_input)
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Close,
            self,
        )
        buttons.accepted.connect(self._insert_custom)
        buttons.rejected.connect(self.accept)
        layout.addLayout(form)
        layout.addWidget(buttons)

    def _insert(self, item: QListWidgetItem) -> None:
        from rword.core.inserts import insert_equation

        insert_equation(self._editor, item.data(256))
        self.accept()

    def _insert_custom(self) -> None:
        from rword.core.inserts import insert_equation

        insert_equation(self._editor, self._custom_input.text())
        self.accept()

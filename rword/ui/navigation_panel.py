"""Panel de navegación por títulos y marcadores."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDockWidget,
    QListWidget,
    QListWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from rword.core import hyperlinks


class NavigationPanel(QDockWidget):
    """Muestra títulos y marcadores para navegar por el documento."""

    def __init__(self, editor, parent=None) -> None:
        super().__init__("Navegación", parent)
        self._editor = editor
        self.setObjectName("navigation_panel")
        self.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea
            | Qt.DockWidgetArea.RightDockWidgetArea
        )
        self._build_ui()
        self._editor.document().contentsChange.connect(self.refresh)

    def _build_ui(self) -> None:
        container = QWidget(self)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(2, 2, 2, 2)
        self._tabs = QTabWidget(container)
        self._headings_list = QListWidget(self._tabs)
        self._headings_list.itemClicked.connect(self._on_heading_clicked)
        self._bookmarks_list = QListWidget(self._tabs)
        self._bookmarks_list.itemClicked.connect(self._on_bookmark_clicked)
        self._tabs.addTab(self._headings_list, "Títulos")
        self._tabs.addTab(self._bookmarks_list, "Marcadores")
        layout.addWidget(self._tabs)
        container.setLayout(layout)
        self.setWidget(container)
        self.refresh()

    def refresh(self) -> None:
        if not hasattr(self, "_headings_list"):
            return
        self._headings_list.blockSignals(True)
        self._headings_list.clear()
        for text, level in hyperlinks.headings(self._editor):
            item = QListWidgetItem(f"{'  ' * (level - 1)}• {text}")
            item.setData(256, level)
            self._headings_list.addItem(item)
        self._headings_list.blockSignals(False)

        self._bookmarks_list.blockSignals(True)
        self._bookmarks_list.clear()
        for name in sorted(hyperlinks.bookmarks(self._editor)):
            self._bookmarks_list.addItem(name)
        self._bookmarks_list.blockSignals(False)

    def _on_heading_clicked(self, item: QListWidgetItem) -> None:
        text = item.text().lstrip(" •")
        default_size = self._editor.document().defaultFont().pointSizeF()
        for heading, level in hyperlinks.headings(self._editor):
            if heading == text:
                block = self._editor.document().begin()
                while block.isValid():
                    candidate = hyperlinks.heading_level(block, default_size)
                    if candidate == level and block.text().strip() == heading:
                        hyperlinks.goto_block(self._editor, block.blockNumber())
                        return
                    block = block.next()
                break

    def _on_bookmark_clicked(self, item: QListWidgetItem) -> None:
        hyperlinks.goto_bookmark(self._editor, item.text())

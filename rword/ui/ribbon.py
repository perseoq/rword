"""Cinta de opciones estilo Word con pestañas, grupos y desplazamiento."""

from __future__ import annotations

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QStackedWidget,
    QTabBar,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from rword.ui.icons import IconManager

_RICON = 16
_LICON = 28
_CONTENT_HEIGHT = 78
_CAPTION_HEIGHT = 16


class RibbonGroup(QWidget):
    """Grupo de la cinta: fila de acciones con un título al pie."""

    def __init__(self, title: str, parent=None) -> None:
        super().__init__(parent)
        self.title = title
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(6, 4, 6, 2)
        self._layout.setSpacing(2)
        self._row = QHBoxLayout()
        self._row.setSpacing(2)
        self._layout.addLayout(self._row)
        self._layout.addStretch(1)
        self._caption = QLabel(title, self)
        self._caption.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._caption.setStyleSheet(
            "font-size: 9px; color: #6b7280; border-top: 1px solid #d1d5db;"
        )
        self._layout.addWidget(self._caption)
        self.setMaximumHeight(_CONTENT_HEIGHT + _CAPTION_HEIGHT)

    def add_action(self, action: QAction, large: bool = False) -> QToolButton:
        button = QToolButton(self)
        button.setDefaultAction(action)
        if large:
            button.setToolButtonStyle(
                Qt.ToolButtonStyle.ToolButtonTextUnderIcon
            )
            button.setIconSize(QSize(_LICON, _LICON))
            button.setFixedSize(58, _CONTENT_HEIGHT - 10)
            button.setStyleSheet("font-size: 9px;")
        else:
            button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
            button.setIconSize(QSize(_RICON, _RICON))
            button.setFixedSize(_RICON + 8, _RICON + 8)
            button.setToolTip(action.text())
        self._row.addWidget(button, 0, Qt.AlignmentFlag.AlignTop)
        return button

    def add_dropdown(self, action: QAction, menu) -> QToolButton:
        button = QToolButton(self)
        button.setDefaultAction(action)
        button.setMenu(menu)
        button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        button.setToolButtonStyle(
            Qt.ToolButtonStyle.ToolButtonTextBesideIcon
        )
        button.setIconSize(QSize(_RICON, _RICON))
        button.setFixedHeight(_RICON + 8)
        button.setStyleSheet("font-size: 9px;")
        self._row.addWidget(button, 0, Qt.AlignmentFlag.AlignTop)
        return button

    def add_widget(self, widget: QWidget) -> None:
        widget.setParent(self)
        self._row.addWidget(widget, 0, Qt.AlignmentFlag.AlignTop)

    def add_separator(self) -> None:
        line = QFrame(self)
        line.setFrameShape(QFrame.Shape.VLine)
        line.setStyleSheet("color: #d1d5db;")
        self._row.addWidget(line, 0, Qt.AlignmentFlag.AlignTop)


class RibbonTab(QWidget):
    """Pestaña de la cinta: fila desplazable de grupos con botones «/»."""

    def __init__(self, icon_manager: IconManager, parent=None) -> None:
        super().__init__(parent)
        self._icon_manager = icon_manager
        self._groups: list[RibbonGroup] = []
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._scroll = QScrollArea(self)
        self._scroll.setWidgetResizable(False)
        self._scroll.setFrameShape(QFrame.Shape.NoFrame)
        self._scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self._scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self._content = QWidget()
        self._content_layout = QHBoxLayout(self._content)
        self._content_layout.setContentsMargins(4, 0, 4, 0)
        self._content_layout.setSpacing(4)
        self._content_layout.addStretch(1)
        self._scroll.setWidget(self._content)
        layout.addWidget(self._scroll, 1)

        self._chevrons_widget = QWidget(self)
        chevrons = QVBoxLayout(self._chevrons_widget)
        chevrons.setContentsMargins(2, 2, 2, 2)
        chevrons.setSpacing(2)
        self._left_button = self._make_chevron("chevrons-left")
        self._right_button = self._make_chevron("chevrons-right")
        chevrons.addWidget(self._left_button)
        chevrons.addWidget(self._right_button)
        layout.addWidget(self._chevrons_widget)

        self._scroll.horizontalScrollBar().valueChanged.connect(
            self._sync_chevrons
        )
        self._hide_chevrons()

    def _make_chevron(self, icon_name: str) -> QToolButton:
        button = QToolButton(self)
        button.setIcon(self._icon_manager.make_icon(icon_name, _RICON))
        button.setIconSize(QSize(_RICON, _RICON))
        button.setFixedSize(22, 22)
        button.setAutoRepeat(True)
        button.clicked.connect(
            lambda checked=False, name=icon_name: self._scroll_chevron(name)
        )
        button.setToolTip(
            "Desplazar cintillas"
            if icon_name == "chevrons-right"
            else "Volver a las cintillas anteriores"
        )
        return button

    def _scroll_chevron(self, icon_name: str) -> None:
        bar = self._scroll.horizontalScrollBar()
        direction = 1 if icon_name == "chevrons-right" else -1
        step = max(bar.pageStep() // 2, 40)
        bar.setValue(bar.value() + direction * step)

    def _sync_chevrons(self) -> None:
        bar = self._scroll.horizontalScrollBar()
        self._left_button.setEnabled(bar.value() > bar.minimum())
        self._right_button.setEnabled(bar.value() < bar.maximum())
        self._chevrons_widget.setVisible(bar.maximum() > bar.minimum())

    def _hide_chevrons(self) -> None:
        self._chevrons_widget.hide()
        self._left_button.setEnabled(False)
        self._right_button.setEnabled(False)

    def add_group(self, title: str) -> RibbonGroup:
        group = RibbonGroup(title, self._content)
        self._groups.append(group)
        self._content_layout.insertWidget(
            self._content_layout.count() - 1, group
        )
        return group

    def set_group_visible(self, title: str, visible: bool) -> None:
        for group in self._groups:
            if group.title == title:
                group.setVisible(visible)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._sync_chevrons()


class RibbonBar(QWidget):
    """Barra de cinta con pestañas y grupos estilo Word."""

    def __init__(self, icon_manager: IconManager | None = None, parent=None) -> None:
        super().__init__(parent)
        self._icon_manager = icon_manager or IconManager()
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        self._tab_bar = QTabBar(self)
        self._tab_bar.setDocumentMode(True)
        self._tab_bar.setExpanding(False)
        self._layout.addWidget(self._tab_bar)

        self._stack = QStackedWidget(self)
        self._layout.addWidget(self._stack)
        self._tab_bar.currentChanged.connect(self._stack.setCurrentIndex)

        self.setStyleSheet(
            "QTabBar::tab { padding: 5px 14px; font-size: 10px; }"
            "QTabBar::tab:selected { font-weight: bold; }"
        )

    def add_tab(self, title: str) -> RibbonTab:
        tab = RibbonTab(self._icon_manager, self._stack)
        self._stack.addWidget(tab)
        self._tab_bar.addTab(title)
        return tab

    def set_current_tab(self, index: int) -> None:
        self._tab_bar.setCurrentIndex(index)

    def current_tab_index(self) -> int:
        return self._tab_bar.currentIndex()

    def tab_titles(self) -> list[str]:
        return [self._tab_bar.tabText(i) for i in range(self._tab_bar.count())]

    def set_group_visible(self, tab_title: str, group_title: str, visible: bool) -> None:
        for index in range(self._tab_bar.count()):
            if self._tab_bar.tabText(index) == tab_title:
                self._stack.widget(index).set_group_visible(group_title, visible)
                return

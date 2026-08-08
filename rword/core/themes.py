"""Temas de documento: colores, fuentes y efectos."""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields

from PySide6.QtGui import QColor, QFont, QPalette
from PySide6.QtWidgets import QTextEdit

THEME_KEY = "theme/current"


@dataclass
class Theme:
    """Conjunto de colores y fuentes que define la apariencia del editor."""

    name: str
    page_color: str = "#ffffff"
    text_color: str = "#000000"
    font_family: str = "Sans Serif"
    font_size: float = 12.0
    highlight_color: str = "#ffe58f"
    selection_color: str = "#cce5ff"

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> Theme:
        valid = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in valid})


def default_themes() -> list[Theme]:
    return [
        Theme("Claro"),
        Theme(
            "Oscuro",
            page_color="#1e1e1e",
            text_color="#d4d4d4",
            font_family="Sans Serif",
            selection_color="#264f78",
            highlight_color="#3a2f00",
        ),
        Theme(
            "Sepia",
            page_color="#f4ecd8",
            text_color="#3b2f1e",
            selection_color="#d8c9a3",
        ),
        Theme(
            "Alto contraste",
            page_color="#000000",
            text_color="#ffffff",
            selection_color="#003366",
        ),
    ]


def apply_theme(editor: QTextEdit, theme: Theme) -> None:
    """Aplica el tema al editor: colores de página, texto y fuente por defecto."""
    palette = editor.palette()
    palette.setColor(QPalette.ColorRole.Base, QColor(theme.page_color))
    palette.setColor(QPalette.ColorRole.Text, QColor(theme.text_color))
    editor.setPalette(palette)

    document = editor.document()
    document.setDefaultFont(
        QFont(theme.font_family, int(theme.font_size))
    )
    document.setDefaultStyleSheet(
        f"body {{ color: {theme.text_color}; }}"
    )
    if theme.name != "Claro":
        editor.setStyleSheet(f"QTextEdit {{ background-color: {theme.page_color}; }}")
    else:
        editor.setStyleSheet("")


class ThemeManager:
    """Registro de temas con persistencia en QSettings."""

    def __init__(self, settings) -> None:
        self._settings = settings
        self._themes: dict[str, Theme] = {
            theme.name: theme for theme in default_themes()
        }
        self.current_name = self._settings.value(THEME_KEY, "Claro")

    def names(self) -> list[str]:
        return list(self._themes)

    def get(self, name: str) -> Theme:
        return self._themes[name]

    def set_current(self, name: str) -> None:
        self.current_name = name
        self._settings.setValue(THEME_KEY, name)

    @property
    def current(self) -> Theme:
        return self._themes.get(self.current_name, self._themes["Claro"])

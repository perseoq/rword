"""Gestión de estilos de documento y pincel de formato."""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields

from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor, QFont, QTextBlockFormat, QTextCharFormat
from PySide6.QtWidgets import QTextEdit

STYLES_KEY = "styles/custom"


@dataclass
class Style:
    """Definición de un estilo de párrafo/carácter."""

    name: str
    font_family: str = "Sans Serif"
    font_size: float = 12.0
    bold: bool = False
    italic: bool = False
    color: str = "#000000"
    alignment: str = "left"
    line_spacing: float = 1.0
    left_indent: float = 0.0
    space_before: float = 0.0
    space_after: float = 0.0
    is_heading: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> Style:
        names = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in names})

    def to_dict(self) -> dict:
        return asdict(self)


def default_styles() -> list[Style]:
    return [
        Style("Normal"),
        Style(
            "Título 1",
            font_size=26.0,
            bold=True,
            color="#1a1a2e",
            alignment="left",
            space_before=24.0,
            space_after=12.0,
            is_heading=True,
        ),
        Style(
            "Título 2",
            font_size=20.0,
            bold=True,
            color="#1a1a2e",
            alignment="left",
            space_before=18.0,
            space_after=10.0,
            is_heading=True,
        ),
        Style(
            "Título 3",
            font_size=16.0,
            bold=True,
            color="#33334d",
            alignment="left",
            space_before=14.0,
            space_after=8.0,
            is_heading=True,
        ),
        Style(
            "Cita",
            font_size=13.0,
            italic=True,
            color="#444444",
            alignment="left",
            left_indent=40.0,
            space_after=10.0,
        ),
        Style(
            "Código",
            font_family="Monospace",
            font_size=11.0,
            color="#2d2d2d",
            left_indent=20.0,
            space_after=8.0,
        ),
    ]


def style_char_format(style: Style) -> QTextCharFormat:
    fmt = QTextCharFormat()
    fmt.setFontFamilies([style.font_family])
    fmt.setFontPointSize(style.font_size)
    fmt.setFontWeight(
        QFont.Weight.Bold if style.bold else QFont.Weight.Normal
    )
    fmt.setFontItalic(style.italic)
    fmt.setForeground(QBrush(QColor(style.color)))
    return fmt


def style_block_format(style: Style) -> QTextBlockFormat:
    fmt = QTextBlockFormat()
    align_map = {
        "left": Qt.AlignmentFlag.AlignLeft,
        "center": Qt.AlignmentFlag.AlignCenter,
        "right": Qt.AlignmentFlag.AlignRight,
        "justify": Qt.AlignmentFlag.AlignJustify,
    }
    fmt.setAlignment(align_map.get(style.alignment, Qt.AlignmentFlag.AlignLeft))
    fmt.setLeftMargin(style.left_indent)
    fmt.setTopMargin(style.space_before)
    fmt.setBottomMargin(style.space_after)
    fmt.setLineHeight(
        style.line_spacing * 100.0,
        QTextBlockFormat.LineHeightTypes.ProportionalHeight.value,
    )
    return fmt


def apply_style(editor: QTextEdit, style: Style) -> None:
    """Aplica el estilo al párrafo actual o a la selección."""
    cursor = editor.textCursor()
    cursor.mergeBlockFormat(style_block_format(style))
    editor.mergeCurrentCharFormat(style_char_format(style))


class StyleManager:
    """Registro de estilos con persistencia en QSettings."""

    def __init__(self, settings) -> None:
        self._settings = settings
        self._styles: dict[str, Style] = {
            style.name: style for style in default_styles()
        }
        self._load()

    def _load(self) -> None:
        data = self._settings.value(STYLES_KEY, [])
        if not data:
            return
        for entry in data:
            try:
                style = Style.from_dict(entry)
            except TypeError:
                continue
            self._styles[style.name] = style

    def save(self) -> None:
        self._settings.setValue(
            STYLES_KEY, [style.to_dict() for style in self._styles.values()]
        )

    def names(self) -> list[str]:
        return list(self._styles)

    def get(self, name: str) -> Style:
        return self._styles[name]

    def add(self, style: Style) -> None:
        self._styles[style.name] = style
        self.save()

    def remove(self, name: str) -> bool:
        if name not in self._styles:
            return False
        del self._styles[name]
        self.save()
        return True

    def rename(self, old_name: str, new_name: str) -> bool:
        if old_name not in self._styles or new_name in self._styles:
            return False
        style = self._styles.pop(old_name)
        style.name = new_name
        self._styles[new_name] = style
        self.save()
        return True


class FormatPainter:
    """Copiar y aplicar el formato de fuente de una selección."""

    def __init__(self) -> None:
        self._format: QTextCharFormat | None = None
        self.active = False

    def capture(self, editor: QTextEdit) -> None:
        self._format = editor.currentCharFormat()
        self.active = True

    def apply(self, editor: QTextEdit) -> bool:
        if not self.active or self._format is None:
            return False
        editor.mergeCurrentCharFormat(self._format)
        return True

    def clear(self) -> None:
        self._format = None
        self.active = False

"""Operaciones de diseño de página."""

from __future__ import annotations

import math
from dataclasses import dataclass, fields

from PySide6.QtCore import QSizeF
from PySide6.QtGui import QTextBlockFormat, QTextFormat
from PySide6.QtWidgets import QTextEdit

MM_TO_PX = 96.0 / 25.4

PAPER_SIZES_MM = {
    "A4": (210.0, 297.0),
    "A5": (148.0, 210.0),
    "A3": (297.0, 420.0),
    "Carta": (215.9, 279.4),
    "Legal": (215.9, 355.6),
}


@dataclass
class PageSetup:
    """Configuración de página del documento."""

    size: str = "A4"
    custom_width_mm: float = 210.0
    custom_height_mm: float = 297.0
    orientation: str = "portrait"
    left_margin_mm: float = 25.0
    right_margin_mm: float = 25.0
    top_margin_mm: float = 25.0
    bottom_margin_mm: float = 25.0
    page_color: str = "#ffffff"
    watermark: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> PageSetup:
        valid = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in valid})

    def size_mm(self) -> tuple[float, float]:
        if self.size == "Personalizado":
            return self.custom_width_mm, self.custom_height_mm
        return PAPER_SIZES_MM.get(self.size, PAPER_SIZES_MM["A4"])

    def page_size_px(self) -> QSizeF:
        width, height = self.size_mm()
        if self.orientation == "landscape":
            width, height = height, width
        return QSizeF(width * MM_TO_PX, height * MM_TO_PX)


def apply_page_setup(editor: QTextEdit, setup: PageSetup) -> None:
    """Aplica tamaño, orientación y márgenes al documento."""
    document = editor.document()
    document.setPageSize(setup.page_size_px())
    frame_format = document.rootFrame().frameFormat()
    frame_format.setLeftMargin(setup.left_margin_mm * MM_TO_PX)
    frame_format.setRightMargin(setup.right_margin_mm * MM_TO_PX)
    frame_format.setTopMargin(setup.top_margin_mm * MM_TO_PX)
    frame_format.setBottomMargin(setup.bottom_margin_mm * MM_TO_PX)
    document.rootFrame().setFrameFormat(frame_format)
    editor._applied_page_setup = setup


def current_page_setup(editor: QTextEdit) -> PageSetup:
    """Obtiene la configuración de página aplicada al documento."""
    stored = getattr(editor, "_applied_page_setup", None)
    if stored is not None:
        margins = editor.document().rootFrame().frameFormat()
        stored.left_margin_mm = margins.leftMargin() / MM_TO_PX
        stored.right_margin_mm = margins.rightMargin() / MM_TO_PX
        stored.top_margin_mm = margins.topMargin() / MM_TO_PX
        stored.bottom_margin_mm = margins.bottomMargin() / MM_TO_PX
        return stored
    document = editor.document()
    size = document.pageSize()
    setup = PageSetup()
    width_mm = size.width() / MM_TO_PX
    height_mm = size.height() / MM_TO_PX
    if width_mm >= height_mm:
        setup.orientation = "landscape"
        width_mm, height_mm = height_mm, width_mm
    for name, (w, h) in PAPER_SIZES_MM.items():
        if abs(w - width_mm) < 1 and abs(h - height_mm) < 1:
            setup.size = name
            break
    else:
        setup.size = "Personalizado"
        setup.custom_width_mm = width_mm
        setup.custom_height_mm = height_mm
    margins = document.rootFrame().frameFormat()
    setup.left_margin_mm = margins.leftMargin() / MM_TO_PX
    setup.right_margin_mm = margins.rightMargin() / MM_TO_PX
    setup.top_margin_mm = margins.topMargin() / MM_TO_PX
    setup.bottom_margin_mm = margins.bottomMargin() / MM_TO_PX
    return setup


def insert_page_break(editor: QTextEdit) -> None:
    """Inserta un salto de página (nuevo bloque con salto antes)."""
    cursor = editor.textCursor()
    cursor.beginEditBlock()
    fmt = QTextBlockFormat()
    fmt.setPageBreakPolicy(QTextFormat.PageBreakFlag.PageBreak_AlwaysBefore)
    cursor.insertBlock(fmt)
    cursor.endEditBlock()


def insert_section_break(editor: QTextEdit) -> None:
    """Inserta un salto de sección: salto de página con separador visible."""
    cursor = editor.textCursor()
    cursor.beginEditBlock()
    fmt = QTextBlockFormat()
    fmt.setPageBreakPolicy(QTextFormat.PageBreakFlag.PageBreak_AlwaysBefore)
    cursor.insertBlock(fmt)
    cursor.insertText("----- Salto de sección -----")
    cursor.insertBlock()
    cursor.endEditBlock()


def set_columns(editor: QTextEdit, columns: int) -> None:
    """Distribuye el texto en N columnas (mediante tabla) o lo restaura."""
    if columns <= 1:
        _flatten_columns(editor)
        return
    paragraphs = _collect_paragraphs(editor)
    if not paragraphs:
        return
    rows = math.ceil(len(paragraphs) / columns)
    cursor = editor.textCursor()
    cursor.beginEditBlock()
    cursor.select(cursor.SelectionType.Document)
    cursor.removeSelectedText()
    cursor.setPosition(0)
    table = cursor.insertTable(rows, columns)
    for index, text in enumerate(paragraphs):
        row = index % rows
        col = index // rows
        cell = table.cellAt(row, col)
        cell_cursor = cell.firstCursorPosition()
        cell_cursor.insertText(text)
    cursor.endEditBlock()


def _collect_paragraphs(editor: QTextEdit) -> list[str]:
    document = editor.document()
    texts: list[str] = []
    block = document.begin()
    while block.isValid():
        texts.append(block.text())
        block = block.next()
    return texts


def _flatten_columns(editor: QTextEdit) -> None:
    document = editor.document()
    texts: list[str] = []
    block = document.begin()
    while block.isValid():
        if block.text().strip():
            texts.append(block.text())
        block = block.next()
    cursor = editor.textCursor()
    cursor.beginEditBlock()
    cursor.select(cursor.SelectionType.Document)
    cursor.removeSelectedText()
    cursor.setPosition(0)
    for text in texts:
        cursor.insertText(text + "\n")
    cursor.endEditBlock()

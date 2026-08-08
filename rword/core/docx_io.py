"""Lectura y escritura de documentos en formato .docx (Word)."""

from __future__ import annotations

import html as html_module
from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtGui import QTextDocument, QTextListFormat, QTextTable
from PySide6.QtWidgets import QTextEdit

_ALIGN_MAP = {
    0: "left",
    1: "center",
    2: "right",
    3: "justify",
}


def _run_html(run) -> str:
    text = html_module.escape(run.text)
    if run.bold:
        text = f"<b>{text}</b>"
    if run.italic:
        text = f"<i>{text}</i>"
    if run.underline:
        text = f"<u>{text}</u>"
    styles = []
    if run.font.color and run.font.color.rgb is not None:
        styles.append(f"color:{run.font.color.rgb}")
    if run.font.size is not None:
        styles.append(f"font-size:{run.font.size.pt}pt")
    if run.font.name:
        styles.append(f"font-family:{run.font.name}")
    if styles:
        text = f"<span style='{'; '.join(styles)}'>{text}</span>"
    return text


def _paragraph_html(paragraph) -> str:
    if not paragraph.text and not paragraph.runs:
        return "<p><br/></p>"
    content = "".join(_run_html(run) for run in paragraph.runs)
    style = paragraph.style.name or ""
    if style.startswith("Heading"):
        level = style.replace("Heading", "").strip()
        try:
            level = min(6, max(1, int(level)))
        except ValueError:
            level = 1
        return f"<h{level}>{content}</h{level}>"
    return f"<p>{content}</p>"


def _table_html(table) -> str:
    rows = []
    for row in table.rows:
        cells = []
        for cell in row.cells:
            text = html_module.escape(cell.text).replace("\n", "<br/>")
            cells.append(f"<td>{text}</td>")
        rows.append("<tr>" + "".join(cells) + "</tr>")
    return "<table border='1'>" + "".join(rows) + "</table>"


def load_docx(editor: QTextEdit, path: str | Path) -> None:
    """Carga un documento .docx en el editor como HTML."""
    from docx import Document

    doc = Document(str(path))
    parts: list[str] = []
    list_kind: str | None = None
    body = doc.element.body
    from docx.table import Table
    from docx.text.paragraph import Paragraph

    for child in body.iterchildren():
        if child.tag.endswith("}p"):
            paragraph = Paragraph(child, doc)
            style = paragraph.style.name or ""
            if "List Bullet" in style:
                if list_kind != "ul":
                    if list_kind == "ol":
                        parts.append("</ol>")
                    parts.append("<ul>")
                    list_kind = "ul"
                parts.append(f"<li>{''.join(_run_html(r) for r in paragraph.runs)}</li>")
            elif "List Number" in style:
                if list_kind != "ol":
                    if list_kind == "ul":
                        parts.append("</ul>")
                    parts.append("<ol>")
                    list_kind = "ol"
                parts.append(f"<li>{''.join(_run_html(r) for r in paragraph.runs)}</li>")
            else:
                if list_kind:
                    parts.append("</ol>" if list_kind == "ol" else "</ul>")
                    list_kind = None
                parts.append(_paragraph_html(paragraph))
        elif child.tag.endswith("}tbl"):
            if list_kind:
                parts.append("</ol>" if list_kind == "ol" else "</ul>")
                list_kind = None
            parts.append(_table_html(Table(child, doc)))
    if list_kind:
        parts.append("</ol>" if list_kind == "ol" else "</ul>")
    editor.setHtml("".join(parts))
    editor.document().setModified(False)


def save_docx(editor: QTextEdit, path: str | Path) -> None:
    """Guarda el contenido del editor en un documento .docx."""
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH

    doc = Document()
    document = editor.document()
    _write_blocks(doc, document, WD_ALIGN_PARAGRAPH)
    doc.save(str(path))


def _write_blocks(doc, document: QTextDocument, wd_align) -> None:

    block = document.begin()
    while block.isValid():
        frame = block.textList()
        table = _table_of_block(document, block)
        if table is not None:
            _write_table(doc, table, wd_align)
            block = table.lastCursorPosition().block()
        elif frame is not None:
            style = "List Bullet" if frame.format().style() in (
                QTextListFormat.Style.ListDisc,
                QTextListFormat.Style.ListCircle,
                QTextListFormat.Style.ListSquare,
            ) else "List Number"
            paragraph = doc.add_paragraph(style=style)
            _fill_paragraph(paragraph, block, document)
        else:
            paragraph = doc.add_paragraph()
            _fill_paragraph(paragraph, block, document)
        block = block.next()


def _table_of_block(document: QTextDocument, block):
    position = block.position()
    for frame in document.rootFrame().childFrames():
        if (
            isinstance(frame, QTextTable)
            and frame.firstPosition() <= position <= frame.lastPosition()
        ):
            return frame
    return None


def _fill_paragraph(paragraph, block, document) -> None:
    from PySide6.QtCore import Qt

    fmt = block.blockFormat()
    alignment = fmt.alignment()
    from docx.enum.text import WD_ALIGN_PARAGRAPH

    if alignment & Qt.AlignmentFlag.AlignHCenter:
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif alignment & Qt.AlignmentFlag.AlignRight:
        paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    elif alignment & Qt.AlignmentFlag.AlignJustify:
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    else:
        paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT

    if fmt.leftMargin():
        paragraph.paragraph_format.left_indent = int(fmt.leftMargin() / 1.5)
    if fmt.topMargin() or fmt.bottomMargin():
        paragraph.paragraph_format.space_before = int(fmt.topMargin() / 1.5)
        paragraph.paragraph_format.space_after = int(fmt.bottomMargin() / 1.5)

    iterator = block.begin()
    while not iterator.atEnd():
        fragment = iterator.fragment()
        text = fragment.text()
        fmt = fragment.charFormat()
        if fmt.isImageFormat():
            _append_image(paragraph, fmt, document)
        elif text:
            run = paragraph.add_run(text)
            if fmt.fontWeight() >= 700:
                run.bold = True
            if fmt.fontItalic():
                run.italic = True
            if fmt.fontUnderline():
                run.underline = True
            if fmt.fontStrikeOut():
                run.font.strike = True
            if fmt.fontPointSize() > 0:
                run.font.size = __import__("docx.shared", fromlist=["Pt"]).Pt(
                    fmt.fontPointSize()
                )
            foreground = fmt.foreground().color()
            if foreground.isValid() and foreground.name() != "#000000":
                run.font.color.rgb = __import__(
                    "docx.shared", fromlist=["RGBColor"]
                ).RGBColor(*foreground.getRgb()[:3])
        iterator += 1


def _append_image(paragraph, char_format, document) -> None:
    import uuid

    from PySide6.QtGui import QImage, QTextFormat

    name = char_format.stringProperty(QTextFormat.Property.ImageName)
    if not name:
        return
    resource = document.resource(QTextDocument.ImageResource, QUrl(name))
    if resource is None or not isinstance(resource, QImage) or resource.isNull():
        return
    temp_dir = Path.home() / ".cache" / "rword"
    temp_dir.mkdir(parents=True, exist_ok=True)
    tmp_path = temp_dir / f"rword_{uuid.uuid4().hex}.png"
    resource.save(str(tmp_path))
    try:
        paragraph.add_run().add_picture(str(tmp_path))
    finally:
        tmp_path.unlink(missing_ok=True)


def _write_table(doc, table, wd_align) -> None:
    rows = table.rows()
    cols = table.columns()
    if rows == 0 or cols == 0:
        return
    doc_table = doc.add_table(rows=rows, cols=cols)
    doc_table.style = "Table Grid"
    for r in range(rows):
        for c in range(cols):
            cell = table.cellAt(r, c)
            text = cell.firstCursorPosition().block().text()
            doc_table.cell(r, c).text = text
    doc.add_paragraph()

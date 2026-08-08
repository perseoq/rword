"""Impresión y exportación de documentos."""

from __future__ import annotations

import html as html_module
import zipfile
from pathlib import Path

from PySide6.QtGui import QPageLayout, QPageSize
from PySide6.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog
from PySide6.QtWidgets import QTextEdit

from rword.core.pages import PageSetup, current_page_setup

ODT_MIMETYPE = "application/vnd.oasis.opendocument.text"
EPUB_MIMETYPE = "application/epub+zip"


def _prepare_printer(editor: QTextEdit, printer: QPrinter, setup: PageSetup) -> None:
    orientation = (
        QPageLayout.Orientation.Landscape
        if setup.orientation == "landscape"
        else QPageLayout.Orientation.Portrait
    )
    page_size = QPageSize(QPageSize.PageSizeId.A4)
    printer.setPageSize(page_size)
    printer.setPageOrientation(orientation)


def print_document(editor: QTextEdit, parent=None) -> bool:
    printer = QPrinter(QPrinter.PrinterMode.HighResolution)
    dialog = QPrintDialog(printer, parent)
    if dialog.exec() != QPrintDialog.DialogCode.Accepted:
        return False
    setup = current_page_setup(editor)
    _prepare_printer(editor, printer, setup)
    editor.document().print_(printer)
    return True


def print_preview(editor: QTextEdit, parent=None) -> None:
    printer = QPrinter(QPrinter.PrinterMode.HighResolution)
    dialog = QPrintPreviewDialog(printer, parent)
    dialog.paintRequested.connect(
        lambda _printer: editor.document().print_(_printer)
    )
    dialog.exec()


def export_pdf(editor: QTextEdit, path: str | Path) -> None:
    printer = QPrinter(QPrinter.PrinterMode.HighResolution)
    printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
    printer.setOutputFileName(str(path))
    setup = current_page_setup(editor)
    _prepare_printer(editor, printer, setup)
    editor.document().print_(printer)


def export_html(editor: QTextEdit, path: str | Path) -> None:
    title = editor.file_path.name if editor.file_path else "rword documento"
    document = (
        "<!DOCTYPE html>\n<html>\n<head>\n<meta charset='utf-8'>\n"
        f"<title>{html_module.escape(title)}</title>\n</head>\n<body>\n"
        f"{editor.toHtml()}\n</body>\n</html>"
    )
    Path(path).write_text(document, encoding="utf-8")


def export_text(editor: QTextEdit, path: str | Path) -> None:
    Path(path).write_text(editor.toPlainText(), encoding="utf-8")


def _escape_rtf(text: str) -> str:
    return (
        text.replace("\\", "\\\\")
        .replace("{", "\\{")
        .replace("}", "\\}")
        .replace("\n", "\\par ")
    )


def export_rtf(editor: QTextEdit, path: str | Path) -> None:
    body = "\n".join(
        _escape_rtf(line) for line in editor.toPlainText().split("\n")
    )
    rtf = (
        "{\\rtf1\\ansi\\deff0 {\\fonttbl {\\f0 Sans Serif;}}\n"
        f"\\viewkind4\\uc1\\pard {body} \\par\n}}"
    )
    Path(path).write_text(rtf, encoding="utf-8")


def _odt_content(editor: QTextEdit) -> str:
    paragraphs = "".join(
        f"<text:p>{html_module.escape(line)}</text:p>"
        for line in editor.toPlainText().split("\n")
        if line
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<office:document-content '
        'xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" '
        'xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" '
        'office:version="1.2">'
        "<office:body><office:text>"
        f"{paragraphs}"
        "</office:text></office:body></office:document-content>"
    )


def export_odt(editor: QTextEdit, path: str | Path) -> None:
    manifest = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<manifest:manifest '
        'xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" '
        'manifest:version="1.2">'
        '<manifest:file-entry manifest:full-path="/" '
        f'manifest:media-type="{ODT_MIMETYPE}"/>'
        '<manifest:file-entry manifest:full-path="content.xml" '
        'manifest:media-type="text/xml"/>'
        "</manifest:manifest>"
    )
    styles = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<office:document-styles xmlns:office="urn:oasis:names:tc:opendocument:'
        'xmlns:office:1.0" office:version="1.2"/>'
    )
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr(
            "mimetype", ODT_MIMETYPE, compress_type=zipfile.ZIP_STORED
        )
        archive.writestr("content.xml", _odt_content(editor))
        archive.writestr("styles.xml", styles)
        archive.writestr("META-INF/manifest.xml", manifest)


def export_epub(editor: QTextEdit, path: str | Path) -> None:
    title = editor.file_path.name if editor.file_path else "Documento"
    container = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<container version="1.0" '
        'xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
        '<rootfiles><rootfile full-path="OEBPS/content.opf" '
        'media-type="application/oebps-package+xml"/>'
        "</rootfiles></container>"
    )
    opf = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<package xmlns="http://www.idpf.org/2007/opf" version="2.0" '
        'unique-identifier="id">'
        "<metadata><dc:title "
        'xmlns:dc="http://purl.org/dc/elements/1.1/">'
        f"{html_module.escape(title)}</dc:title>"
        '<dc:identifier xmlns:dc="http://purl.org/dc/elements/1.1" '
        'id="id">rword-1</dc:identifier>'
        '<dc:language xmlns:dc="http://purl.org/dc/elements/1.1">es</dc:language>'
        "</metadata>"
        '<manifest><item id="c1" href="content.xhtml" '
        'media-type="application/xhtml+xml"/></manifest>'
        '<spine><itemref idref="c1"/></spine></package>'
    )
    toc = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">'
        "<head><meta name='dtb:uid' content='rword-1'/></head>"
        '<docTitle><text>'
        f"{html_module.escape(title)}"
        "</text></docTitle>"
        '<navMap><navPoint id="np1" playOrder="1">'
        '<navLabel><text>Comenzar</text></navLabel>'
        '<content src="content.xhtml"/></navPoint></navMap></ncx>'
    )
    content = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" '
        '"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n'
        '<html xmlns="http://www.w3.org/1999/xhtml"><head><title>'
        f"{html_module.escape(title)}</title></head><body>"
        f"{editor.toHtml()}</body></html>"
    )
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr(
            "mimetype", EPUB_MIMETYPE, compress_type=zipfile.ZIP_STORED
        )
        archive.writestr("META-INF/container.xml", container)
        archive.writestr("OEBPS/content.opf", opf)
        archive.writestr("OEBPS/toc.ncx", toc)
        archive.writestr("OEBPS/content.xhtml", content)

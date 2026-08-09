"""Iconografía Lucide (SVG) para toda la interfaz.

Qt no soporta `currentColor` en SVG, por lo que cada icono se renderiza
sustituyendo `currentColor` por un color explícito derivado de la paleta.
"""

from __future__ import annotations

from PySide6.QtCore import QByteArray
from PySide6.QtGui import QColor, QIcon, QPalette, QPixmap
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QWidget


def _svg(inner: str) -> str:
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" '
        'viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
        f"{inner}</svg>"
    )


def _p(d: str) -> str:
    return f'<path d="{d}"/>'


LUCIDE_ICONS: dict[str, str] = {
    # Archivo
    "file-plus": _svg(_p("M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7z") + _p("M14 2v4a2 2 0 0 0 2 2h4") + _p("M9 15h6") + _p("M12 12v6")),
    "folder-open": _svg(_p("M6 14l1.5-2.9A2 2 0 0 1 9.24 10H20a2 2 0 0 1 1.94 2.5l-1.54 6a2 2 0 0 1-1.95 1.5H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h3.9a2 2 0 0 1 1.69.9l.81 1.2a2 2 0 0 0 1.67.9H18a2 2 0 0 1 2 2v2")),
    "save": _svg(_p("M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z") + _p("M17 21v-8H7v8") + _p("M7 3v5h8")),
    "files": _svg(_p("M8.5 2H15a2 2 0 0 1 2 2v4h2a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H9a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z") + _p("M8.5 2v4H15") + _p("M7 9H5a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2")),
    "print": _svg(_p("M6 9V3h12v6") + _p("M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2") + _p("M6 14h12v7H6z")),
    "eye": _svg(_p("M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7z") + "<circle cx='12' cy='12' r='3'/>"),
    "file-text": _svg(_p("M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7z") + _p("M14 2v4a2 2 0 0 0 2 2h4") + _p("M10 9H8") + _p("M16 13H8") + _p("M16 17H8")),
    "x": _svg(_p("M18 6 6 18") + _p("M6 6l12 12")),
    "download": _svg(_p("M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4") + _p("M7 10l5 5 5-5") + _p("M12 15V3")),
    "upload": _svg(_p("M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4") + _p("M17 8l-5-5-5 5") + _p("M12 3v12")),
    # Deshacer / rehacer
    "undo-2": _svg(_p("M9 14 4 9l5-5") + _p("M4 9h10.5a5.5 5.5 0 0 1 5.5 5.5v.5a5.5 5.5 0 0 1-5.5 5.5H11")),
    "redo-2": _svg(_p("M15 14l5-5-5-5") + _p("M20 9H9.5A5.5 5.5 0 0 0 4 14.5v.5A5.5 5.5 0 0 0 9.5 20H13")),
    # Portapapeles
    "scissors": _svg("<circle cx='6' cy='6' r='3'/><circle cx='6' cy='18' r='3'/>" + _p("M20 4 8.12 15.88") + _p("M14.47 14.48 20 20") + _p("M8.12 8.12 12 12")),
    "copy": _svg(_p("M20 9H9a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2v-9a2 2 0 0 0-2-2z") + _p("M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1")),
    "clipboard": _svg(_p("M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2") + "<rect x='8' y='2' width='8' height='4' rx='1'/>"),
    "paintbrush": _svg(_p("M18.37 2.63 14 7l-1.59-1.59a2 2 0 0 0-2.82 0L8 7l9 9 1.59-1.59a2 2 0 0 0 0-2.82L17 10l4.37-4.37a2.12 2.12 0 1 0-3-3z") + _p("M9 8c-2 3-4 3.5-7 4l8 10c2-1 6-5 6-7") + _p("M14.5 17.5 4.5 15")),
    # Edición
    "search": _svg("<circle cx='11' cy='11' r='8'/>" + _p("m21 21-4.3-4.3")),
    "replace": _svg(_p("M17 5a3 3 0 0 0-5.5-1.5") + _p("M3 17a3 3 0 0 1 5.5 1.5") + _p("M5.5 3.5 19 17")),
    "corner-down-right": _svg(_p("m15 10 5 5-5 5") + _p("M4 4v7a4 4 0 0 0 4 4h12")),
    # Zoom
    "zoom-in": _svg("<circle cx='11' cy='11' r='8'/>" + _p("m21 21-4.3-4.3") + _p("M11 8v6") + _p("M8 11h6")),
    "zoom-out": _svg("<circle cx='11' cy='11' r='8'/>" + _p("m21 21-4.3-4.3") + _p("M8 11h6")),
    "percent": _svg(_p("M19 5 5 19") + "<circle cx='6.5' cy='6.5' r='2.5'/><circle cx='17.5' cy='17.5' r='2.5'/>"),
    "maximize": _svg(_p("M8 3H5a2 2 0 0 0-2 2v3") + _p("M21 8V5a2 2 0 0 0-2-2h-3") + _p("M3 16v3a2 2 0 0 0 2 2h3") + _p("M16 21h3a2 2 0 0 0 2-2v-3")),
    "chevron-up": _svg(_p("m18 15-6-6-6 6")),
    "chevron-down": _svg(_p("m6 9 6 6 6-6")),
    "chevrons-up": _svg(_p("m7 11 5-5 5 5") + _p("m7 18 5-5 5 5")),
    "chevrons-down": _svg(_p("m7 6 5 5 5-5") + _p("m7 13 5 5 5-5")),
    "chevrons-left": _svg(_p("m11 17-5-5 5-5") + _p("m18 17-5-5 5-5")),
    "chevrons-right": _svg(_p("m6 17 5-5-5-5") + _p("m13 17 5-5-5-5")),
    "scan": _svg(_p("M3 7V5a2 2 0 0 1 2-2h2") + _p("M17 3h2a2 2 0 0 1 2 2v2") + _p("M21 17v2a2 2 0 0 1-2 2h-2") + _p("M7 21H5a2 2 0 0 1-2-2v-2") + _p("M3 12h18")),
    # Fuente
    "bold": _svg(_p("M14 12a4 4 0 0 0 0-8H6v8") + _p("M15 20a4 4 0 0 0 0-8H6v8z")),
    "italic": _svg(_p("M19 4h-9") + _p("M14 20H5") + _p("M15 4 9 20")),
    "underline": _svg(_p("M6 4v6a6 6 0 0 0 12 0V4") + _p("M4 20h16")),
    "strikethrough": _svg(_p("M16 4H9a3 3 0 0 0-2.83 4") + _p("M14 12a4 4 0 0 1 0 8H6") + _p("M4 12h16")),
    "superscript": _svg(_p("m4 19 8-8") + _p("m12 19-8-8") + _p("M20 8h-4") + _p("M20 5h-4") + _p("M18 5v3")),
    "subscript": _svg(_p("m4 19 8-8") + _p("m12 19-8-8") + _p("M20 19h-4") + _p("M20 16h-4") + _p("M18 16v3")),
    "palette": _svg("<circle cx='13.5' cy='6.5' r='.5'/><circle cx='17.5' cy='10.5' r='.5'/><circle cx='8.5' cy='7.5' r='.5'/><circle cx='6.5' cy='12.5' r='.5'/>" + _p("M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2z")),
    "highlighter": _svg(_p("m9 11-6 6v3h9l3-3") + _p("m22 12-4.6 4.6a2 2 0 0 1-2.8 0l-5.2-5.2a2 2 0 0 1 0-2.8L14 4") + _p("m14 4 3-3 6 6-3 3")),
    "eraser": _svg(_p("m7 21-4.3-4.3c-1-1-1-2.5 0-3.4l9.6-9.6c1-1 2.5-1 3.4 0l5.6 5.6c1 1 1 2.5 0 3.4L13 21") + _p("M22 21H7") + _p("m5 11 9 9")),
    "type": _svg(_p("M4 7V4h16v3") + _p("M9 20h6") + _p("M12 4v16")),
    # Párrafo
    "align-left": _svg(_p("M21 6H3") + _p("M15 12H3") + _p("M17 18H3")),
    "align-center": _svg(_p("M21 6H3") + _p("M17 12H7") + _p("M19 18H5")),
    "align-right": _svg(_p("M21 6H3") + _p("M21 12H9") + _p("M21 18H7")),
    "align-justify": _svg(_p("M3 6h18") + _p("M3 12h18") + _p("M3 18h18")),
    "list": _svg(_p("M3 12h.01") + _p("M3 18h.01") + _p("M3 6h.01") + _p("M8 12h13") + _p("M8 18h13") + _p("M8 6h13")),
    "list-ordered": _svg(_p("M10 12h11") + _p("M10 18h11") + _p("M10 6h11") + _p("M4 10h2") + _p("M4 6h1v4") + _p("M6 18H4c0-1 2-2 2-3s-1-1.5-2-1")),
    "indent-increase": _svg(_p("M21 6H3") + _p("M21 12h-9") + _p("M21 18H3") + _p("M9 9 5 12l4 3")),
    "indent-decrease": _svg(_p("M21 6H3") + _p("M21 12h-9") + _p("M21 18H3") + _p("M5 9l4 3-4 3")),
    # Columnas
    "columns-3": _svg(_p("M3 3h18v18H3z") + _p("M9 3v18") + _p("M15 3v18")),
    "columns-2": _svg(_p("M12 3v18") + _p("M3 3h18v18H3z")),
    # Tablas / ilustraciones
    "table": _svg(_p("M12 3v18") + _p("M3 12h18") + "<rect x='3' y='3' width='18' height='18' rx='2'/>"),
    "image": _svg("<rect x='3' y='3' width='18' height='18' rx='2'/>" + "<circle cx='9' cy='9' r='2'/>" + _p("m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21")),
    "shapes": _svg(_p("M8.3 10a.7.7 0 0 1-.626-1.079L11.4 3a.7.7 0 0 1 1.198-.043L16.3 8.9a.7.7 0 0 1-.572 1.1Z") + "<rect x='3' y='14' width='7' height='7' rx='1'/><circle cx='17.5' cy='17.5' r='3.5'/>"),
    "square": _svg("<rect x='3' y='3' width='18' height='18' rx='2'/>"),
    "circle": _svg("<circle cx='12' cy='12' r='10'/>"),
    "sigma": _svg(_p("M18 7V5a1 1 0 0 0-1-1H6.5a.5.5 0 0 0-.4.8l4.5 6a2 2 0 0 1 0 2.4l-4.5 6a.5.5 0 0 0 .4.8H17a1 1 0 0 0 1-1v-2")),
    "function-square": _svg("<rect x='3' y='3' width='18' height='18' rx='2'/>" + _p("M9 17c2 0 2.8-1 2.8-2.8V10c0-2 1-3.3 3.2-3") + _p("M9 11.2h5.7")),
    "bar-chart": _svg(_p("M12 20V10") + _p("M18 20V4") + _p("M6 20v-4")),
    "network": _svg("<rect x='16' y='16' width='6' height='6' rx='1'/><rect x='2' y='16' width='6' height='6' rx='1'/><rect x='9' y='2' width='6' height='6' rx='1'/>" + _p("M5 16v-3a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v3") + _p("M12 12V8")),
    "diamond": _svg(_p("M6 3h12l4 6-10 13L2 9Z")),
    # Enlaces
    "link": _svg(_p("M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71") + _p("M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71")),
    "bookmark": _svg(_p("M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z")),
    "heading": _svg(_p("M6 4v16") + _p("M18 4v16") + _p("M6 12h12")),
    "quote": _svg(_p("M3 21c3 0 7-1 7-8V5c0-1.25-.756-2.017-2-2H4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2 1 0 1 0 1 1v1c0 1-1 2-2 2s-1 .008-1 1.031V20c0 1 0 1 1 1z") + _p("M15 21c3 0 7-1 7-8V5c0-1.25-.757-2.017-2-2h-4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2h.75c0 2.25.25 4-2.75 4v3c0 1 0 1 1 1z")),
    # Encabezado / pie
    "heading-plus": _svg(_p("M6 4v16") + _p("M18 4v16") + _p("M6 12h12")),
    "hash": _svg(_p("M4 9h16") + _p("M4 15h16") + _p("M10 3 8 21") + _p("M16 3l-2 18")),
    "clock": _svg("<circle cx='12' cy='12' r='10'/>" + _p("M12 6v6l4 2")),
    "calendar": _svg("<rect x='3' y='4' width='18' height='18' rx='2'/>" + _p("M16 2v4") + _p("M8 2v4") + _p("M3 10h18")),
    "file-output": _svg(_p("M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z") + _p("M14 2v6h6") + _p("M2 12h10") + _p("M9 9l-3 3 3 3")),
    # Revisión
    "message-square": _svg(_p("M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z")),
    "check-circle-2": _svg(_p("M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z") + _p("m9 12 2 2 4-4")),
    "check-square": _svg(_p("m9 11 3 3L22 4") + _p("M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11")),
    "x-circle": _svg("<circle cx='12' cy='12' r='10'/>" + _p("m15 9-6 6") + _p("m9 9 6 6")),
    "alert-triangle": _svg(_p("m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3z") + _p("M12 9v4") + _p("M12 17h.01")),
    "help-circle": _svg("<circle cx='12' cy='12' r='10'/>" + _p("M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3") + _p("M12 17h.01")),
    "check": _svg(_p("M20 6 9 17l-5-5")),
    "bot": _svg(_p("M12 8V4H8") + "<rect width='16' height='12' x='4' y='8' rx='2'/>" + _p("M2 14h2") + _p("M20 14h2") + _p("M15 13v2") + _p("M9 13v2")),
    "sparkles": _svg(_p("M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z")),
    # Vista
    "panel-left": _svg("<rect x='3' y='3' width='18' height='18' rx='2'/>" + _p("M9 3v18")),
    "layout": _svg("<rect x='3' y='3' width='18' height='18' rx='2'/>" + _p("M3 9h18") + _p("M9 21V9")),
    "ruler": _svg(_p("M21.3 15.3a2.4 2.4 0 0 1 0 3.4l-2.6 2.6a2.4 2.4 0 0 1-3.4 0L2.7 8.7a2.41 2.41 0 0 1 0-3.4l2.6-2.6a2.41 2.41 0 0 1 3.4 0Z") + _p("m14.5 12.5 2-2") + _p("m11.5 9.5 2-2") + _p("m8.5 6.5 2-2") + _p("m17.5 15.5 2-2")),
    "grid": _svg("<rect x='3' y='3' width='7' height='7'/><rect x='14' y='3' width='7' height='7'/><rect x='14' y='14' width='7' height='7'/><rect x='3' y='14' width='7' height='7'/>"),
    "split": _svg(_p("M16 3h5v5") + _p("M8 3H3v5") + _p("M12 3v18") + _p("M3 16v5h5") + _p("M21 16v5h-5")),
    "copy-plus": _svg(_p("M20 9H9a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2v-9a2 2 0 0 0-2-2z") + _p("M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1") + _p("M14.5 14v-4") + _p("M12.5 12h4")),
    "maximize-2": _svg(_p("M15 3h6v6") + _p("M9 21H3v-6") + _p("M21 3l-7 7") + _p("M3 21l7-7")),
    # Correspondencia
    "mail": _svg("<rect x='2' y='4' width='20' height='16' rx='2'/>" + _p("m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7")),
    "database": _svg("<ellipse cx='12' cy='5' rx='9' ry='3'/>" + _p("M3 5V19A9 3 0 0 0 21 19V5") + _p("M3 12A9 3 0 0 0 21 12")),
    "filter": _svg(_p("M22 3H2l8 9.46V19l4 2v-8.54Z")),
    "sort-asc": _svg(_p("m3 8 4-4 4 4") + _p("M7 4v16") + _p("M11 12h4") + _p("M11 16h7") + _p("M11 20h10")),
    "send": _svg(_p("M22 2 11 13") + _p("M22 2l-7 20-4-9-9-4Z")),
    "file-check": _svg(_p("M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7z") + _p("M14 2v4a2 2 0 0 0 2 2h4") + _p("m9 15 2 2 4-4")),
    # Automatización / macros
    "play": _svg(_p("m6 3 14 9-14 9V3z")),
    "square-stop": _svg(_p("M4 4h16v16H4z")),
    "variable": _svg(_p("M8 21s-4-3-4-9 4-9 4-9") + _p("M16 3s4 3 4 9-4 9-4 9") + _p("M15 9l-6 6") + _p("M9 9l6 6")),
    "settings": _svg(_p("M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z") + "<circle cx='12' cy='12' r='3'/>"),
    # Seguridad
    "lock": _svg("<rect x='3' y='11' width='18' height='11' rx='2'/>" + _p("M7 11V7a5 5 0 0 1 10 0v4")),
    "unlock": _svg("<rect x='3' y='11' width='18' height='11' rx='2'/>" + _p("M7 11V7a5 5 0 0 1 9.9-1")),
    "shield": _svg(_p("M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z")),
    "fingerprint": _svg(_p("M12 10a2 2 0 0 0-2 2c0 1.02-.1 2.51-.26 4") + _p("M14 13.12c0 2.38 0 6.38-1 8.88") + _p("M17.29 21.02c.12-.6.43-2.3.5-3.02") + _p("M2 12a10 10 0 0 1 18-6") + _p("M2 16h.01") + _p("M21.8 16c.2-2 .131-5.354 0-6") + _p("M5 19.5C5.5 18 6 15 6 12a6 6 0 0 1 .34-2") + _p("M8.65 22c.21-.66.45-1.32.57-2") + _p("M9 6.8a6 6 0 0 1 9 5.2v2")),
    "eye-off": _svg(_p("M9.88 9.88a3 3 0 1 0 4.24 4.24") + _p("M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68") + _p("M6.61 6.61A13.526 13.526 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61") + _p("M2 2l20 20")),
    # Colaboración
    "users": _svg(_p("M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2") + "<circle cx='9' cy='7' r='4'/>" + _p("M22 21v-2a4 4 0 0 0-3-3.87") + _p("M16 3.13a4 4 0 0 1 0 7.75")),
    "user": _svg(_p("M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2") + "<circle cx='12' cy='7' r='4'/>"),
    "share": _svg(_p("M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8") + _p("m16 6-4-4-4 4") + _p("M12 2v13")),
    "activity": _svg(_p("M22 12h-4l-3 9L9 3l-3 9H2")),
    # Accesibilidad
    "volume-2": _svg(_p("M11 5 6 9H2v6h4l5 4V5z") + _p("M15.54 8.46a5 5 0 0 1 0 7.07") + _p("M19.07 4.93a10 10 0 0 1 0 14.14")),
    "mic": _svg(_p("M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z") + _p("M19 10v2a7 7 0 0 1-14 0v-2") + _p("M12 19v3")),
    "accessibility": _svg("<circle cx='16' cy='4' r='1'/><path d='m18 19 1-7-6 1'/><path d='m5 8 3-3 5.5 3-2.36 3.5'/><path d='M4.24 14.5a5 5 0 0 0 6.88 6'/><path d='M13.76 17.5a5 5 0 0 0-6.88-6'/>"),
    # Dominios
    "scale": _svg(_p("m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z") + _p("m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z") + _p("M7 21h10") + _p("M12 3v18") + _p("M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2")),
    "terminal": _svg(_p("m4 17 6-6-6-6") + _p("M12 19h8")),
    "book-open": _svg(_p("M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z") + _p("M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z")),
    "briefcase": _svg(_p("M16 20V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16") + "<rect x='2' y='6' width='20' height='14' rx='2'/>"),
    "flask-conical": _svg(_p("M14 2v6a2 2 0 0 0 .245.96l5.51 10.08A2 2 0 0 1 18 22H6a2 2 0 0 1-1.755-2.96l5.51-10.08A2 2 0 0 0 10 8V2") + _p("M6.453 15h11.094") + _p("M8.5 2h7")),
    # Herramientas
    "spell-check": _svg(_p("m6 16 6-12 6 12") + _p("M8 12h8") + _p("m16 20 2 2 4-4")),
    "languages": _svg(_p("m5 8 6 6") + _p("m4 14 6-6 2-3") + _p("M2 5h12") + _p("M7 2h1") + _p("m22 22-5-10-5 10") + _p("M14 18h6")),
    "calculator": _svg("<rect x='4' y='2' width='16' height='20' rx='2'/>" + _p("M8 6h8") + _p("M8 11h.01") + _p("M12 11h.01") + _p("M16 11h.01") + _p("M8 15h.01") + _p("M12 15h.01") + _p("M16 15h.01") + _p("M8 19h.01") + _p("M12 19h.01")),
    "list-checks": _svg(_p("m3 17 2 2 4-4") + _p("m3 7 2 2 4-4") + _p("M13 6h8") + _p("M13 12h8") + _p("M13 18h8")),
    "sliders-horizontal": _svg(_p("M21 4h-7") + _p("M10 4H3") + _p("M21 12h-9") + _p("M8 12H3") + _p("M21 20h-5") + _p("M12 20H3") + _p("M14 2v4") + _p("M8 10v4") + _p("M16 18v4")),
    "crop": _svg(_p("M6 2v14a2 2 0 0 0 2 2h14") + _p("M18 22V8a2 2 0 0 0-2-2H2")),
    "rotate-cw": _svg(_p("M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8") + _p("M21 3v5h-5")),
    "flip-horizontal": _svg(_p("M8 3H5a2 2 0 0 0-2 2v14c0 1.1.9 2 2 2h3") + _p("M16 3h3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-3") + _p("M12 20v2") + _p("M12 14v2") + _p("M12 8v2") + _p("M12 2v2")),
    "contrast": _svg("<circle cx='12' cy='12' r='10'/>" + _p("M12 18a6 6 0 0 0 0-12v12z")),
    "wand": _svg(_p("M15 4V2") + _p("M15 16v-2") + _p("M8 9h2") + _p("M20 9h2") + _p("M17.8 11.8 19 13") + _p("M15 9h.01") + _p("M17.8 6.2 19 5") + _p("m3 21 9-9") + _p("M12.2 6.2 11 5")),
    "zap": _svg(_p("M13 2 3 14h9l-1 8 10-12h-9l1-8z")),
    "star": _svg(_p("m12 2 3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z")),
    "layers": _svg(_p("m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z") + _p("m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65") + _p("m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65")),
    "bookmark-plus": _svg(_p("M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z") + _p("M12 7v6") + _p("M9 10h6")),
    "refresh-cw": _svg(_p("M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8") + _p("M21 3v5h-5") + _p("M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16") + _p("M8 16H3v5")),
    "paperclip": _svg(_p("m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l8.57-8.57A4 4 0 1 1 18 8.84l-8.59 8.57a2 2 0 0 1-2.83-2.83l8.49-8.48")),
    "globe": _svg("<circle cx='12' cy='12' r='10'/>" + _p("M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20") + _p("M2 12h20")),
    "keyboard": _svg("<rect x='2' y='6' width='20' height='12' rx='2'/>" + _p("M6 10h.01") + _p("M10 10h.01") + _p("M14 10h.01") + _p("M18 10h.01") + _p("M6 14h.01") + _p("M18 14h.01") + _p("M10 14h4")),
    "puzzle": _svg(_p("M19.439 7.85c-.049.322.059.648.289.878l1.568 1.568c.47.47.706 1.087.706 1.704s-.235 1.233-.706 1.704l-1.611 1.611a.98.98 0 0 1-.837.276c-.47-.07-.802-.48-.968-.925a2.501 2.501 0 1 0-3.214 3.214c.446.166.855.497.925.968a.979.979 0 0 1-.276.837l-1.61 1.61a2.404 2.404 0 0 1-1.705.707 2.402 2.402 0 0 1-1.704-.706l-1.568-1.568a1.026 1.026 0 0 0-.877-.29c-.493.074-.84.504-1.02.968a2.5 2.5 0 1 1-3.237-3.237c.464-.18.894-.527.967-1.02a1.026 1.026 0 0 0-.289-.877l-1.568-1.568A2.402 2.402 0 0 1 1.998 12c0-.617.236-1.234.706-1.704L4.23 8.77c.24-.24.581-.353.917-.303.515.077.877.528 1.073 1.01a2.5 2.5 0 1 0 3.259-3.259c-.482-.196-.933-.558-1.01-1.073-.05-.336.062-.676.303-.917l1.525-1.525A2.402 2.402 0 0 1 12 1.998c.617 0 1.234.236 1.704.706l1.568 1.568c.23.23.556.338.877.29.493-.074.84-.504 1.02-.968a2.5 2.5 0 1 1 3.237 3.237c-.464.18-.894.527-.967 1.02Z")),
    "key": _svg(_p("m21 2-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0 3 3L22 7l-3-3m-3.5 3.5L19 4")),
    "minimize": _svg(_p("M8 3v3a2 2 0 0 1-2 2H3") + _p("M21 8h-3a2 2 0 0 1-2-2V3") + _p("M3 16h3a2 2 0 0 1 2 2v3") + _p("M16 21v-3a2 2 0 0 1 2-2h3")),
    "repeat": _svg(_p("m17 2 4 4-4 4") + _p("M3 11v-1a4 4 0 0 1 4-4h14") + _p("m7 22-4-4 4-4") + _p("M21 13v1a4 4 0 0 1-4 4H3")),
    "waves": _svg(_p("M2 6c.6.5 1.2 1 2.5 1C7 7 7 5 9.5 5c2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1") + _p("M2 12c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1") + _p("M2 18c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1")),
    "lightbulb": _svg(_p("M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5") + _p("M9 18h6") + _p("M10 22h4")),
    "panel-top": _svg("<rect x='3' y='3' width='18' height='18' rx='2'/>" + _p("M3 9h18")),
}


class IconManager:
    """Genera QIcon desde el catálogo Lucide y mantiene el color de tema."""

    def __init__(self, color: str = "#1f1f1f") -> None:
        self._color = color
        self._cache: dict[tuple[str, str, int], QIcon] = {}
        self._registered: list[tuple[object, str, int]] = []

    @property
    def color(self) -> str:
        return self._color

    def set_color(self, color: str) -> None:
        self._color = color
        self._cache.clear()
        self.recolor()

    def make_icon(self, name: str, size: int = 20, color: str | None = None) -> QIcon:
        color = color or self._color
        key = (name, color, size)
        cached = self._cache.get(key)
        if cached is not None:
            return cached
        svg = LUCIDE_ICONS.get(name)
        icon = QIcon()
        if svg is not None:
            renderer = QSvgRenderer(
                QByteArray(svg.replace("currentColor", color).encode("utf-8"))
            )
            pixmap = QPixmap(size, size)
            pixmap.fill(QColor(0, 0, 0, 0))
            from PySide6.QtGui import QPainter

            painter = QPainter(pixmap)
            renderer.render(painter)
            painter.end()
            icon = QIcon(pixmap)
        self._cache[key] = icon
        return icon

    def register(self, action, name: str, size: int = 16) -> None:
        self._registered.append((action, name, size))
        action.setIcon(self.make_icon(name, size))

    def recolor(self) -> None:
        for action, name, size in self._registered:
            action.setIcon(self.make_icon(name, size))


def icon_color_for(widget: QWidget) -> str:
    """Color de icono según el tema: gris pizarra en claro, claro en oscuro."""
    color = widget.palette().color(QPalette.ColorRole.Text)
    if color.lightness() > 128:
        return "#cbd5e1"
    return "#475569"

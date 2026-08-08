"""Constantes globales de la aplicación."""

APP_NAME = "rword"
ORG_NAME = "perseoq"
APP_VERSION = "0.1.0"

WINDOW_GEOMETRY_KEY = "ui/window_geometry"
WINDOW_STATE_KEY = "ui/window_state"
TOOLBAR_VISIBLE_KEY = "ui/toolbar_visible"
FORMATBAR_VISIBLE_KEY = "ui/formatbar_visible"
STATUSBAR_VISIBLE_KEY = "ui/statusbar_visible"

TEXT_FILTER = "Documentos de texto (*.txt *.md *.rst *.log)"
HTML_FILTER = "Documentos HTML (*.html *.htm)"
ALL_FILES_FILTER = "Todos los archivos (*)"

HTML_EXTENSIONS = {".html", ".htm"}
TEXT_EXTENSIONS = {".txt", ".md", ".rst", ".log"}
SUPPORTED_EXTENSIONS = HTML_EXTENSIONS | TEXT_EXTENSIONS

PARAGRAPH_SEPARATOR = "\u2029"
LINE_SEPARATOR = "\u2028"

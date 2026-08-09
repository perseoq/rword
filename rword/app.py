"""Punto de entrada de la aplicación."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from rword.config import APP_NAME, ORG_NAME
from rword.ui.main_window import MainWindow


def run(argv: list[str] | None = None) -> int:
    """Arranca la aplicación y devuelve el código de salida."""
    _silence_wayland_logging()
    app = QApplication(argv if argv is not None else sys.argv)
    app.setStyle("Fusion")
    app.setOrganizationName(ORG_NAME)
    app.setApplicationName(APP_NAME)
    app.setApplicationDisplayName(APP_NAME)
    window = MainWindow()
    window.show()
    return app.exec()


def _silence_wayland_logging() -> None:
    """Silencia el ruido de logs de entrada de texto de Qt bajo Wayland."""
    rule = "qt.qpa.wayland.textinput=false"
    current = os.environ.get("QT_LOGGING_RULES", "")
    if current.strip():
        rule = f"{current.strip()};{rule}"
    os.environ["QT_LOGGING_RULES"] = rule


if __name__ == "__main__":
    raise SystemExit(run())

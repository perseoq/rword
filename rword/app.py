"""Punto de entrada de la aplicación."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from rword.config import APP_NAME, ORG_NAME
from rword.ui.main_window import MainWindow


def run(argv: list[str] | None = None) -> int:
    """Arranca la aplicación y devuelve el código de salida."""
    app = QApplication(argv if argv is not None else sys.argv)
    app.setOrganizationName(ORG_NAME)
    app.setApplicationName(APP_NAME)
    app.setApplicationDisplayName(APP_NAME)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(run())

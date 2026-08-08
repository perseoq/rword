"""Complemento de ejemplo: inserta la fecha y hora actuales."""

from datetime import datetime

from PySide6.QtGui import QAction

PLUGIN_NAME = "Fecha y hora"


def register(main_window):
    action = QAction("Insertar fecha y hora (complemento)", main_window)
    main_window._icon_manager.register(action, "calendar", 16)
    action.triggered.connect(
        lambda: main_window._editor.insertPlainText(
            datetime.now().strftime("%d/%m/%Y %H:%M")
        )
    )
    main_window.add_ribbon_action(action, "Insertar", "Complementos")

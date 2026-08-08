"""Ejecución de operaciones de IA en un hilo secundario."""

from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import QThread, Signal


class AiWorker(QThread):
    """Ejecuta una operación de IA sin bloquear la interfaz."""

    finished_ok = Signal(str)
    finished_error = Signal(str)

    def __init__(
        self, operation: Callable[[], str], parent=None
    ) -> None:
        super().__init__(parent)
        self._operation = operation

    def run(self) -> None:
        try:
            result = self._operation()
            self.finished_ok.emit(result)
        except Exception as error:  # noqa: BLE001 - se notifica al usuario
            self.finished_error.emit(str(error))

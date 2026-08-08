"""Historial de portapapeles múltiple."""

from __future__ import annotations


class ClipboardHistory:
    """Almacena los textos copiados más recientes."""

    def __init__(self, max_entries: int = 10) -> None:
        self._max_entries = max_entries
        self._items: list[str] = []

    def add(self, text: str) -> None:
        """Registra un texto copiado, moviéndolo al frente si ya existía."""
        if not text.strip():
            return
        if text in self._items:
            self._items.remove(text)
        self._items.insert(0, text)
        del self._items[self._max_entries :]

    @property
    def items(self) -> list[str]:
        """Los elementos en orden de más reciente a más antiguo."""
        return list(self._items)

    def clear(self) -> None:
        self._items.clear()

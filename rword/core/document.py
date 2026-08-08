"""Modelo de documento del editor."""

from __future__ import annotations

from pathlib import Path


class Document:
    """Representa un documento abierto en el editor."""

    def __init__(self, file_path: Path | None = None) -> None:
        self._file_path = file_path

    @property
    def file_path(self) -> Path | None:
        """Ruta del archivo asociado, o None si es un documento nuevo."""
        return self._file_path

    @file_path.setter
    def file_path(self, value: Path | None) -> None:
        self._file_path = value

    @property
    def name(self) -> str:
        """Nombre de archivo o marcador de documento sin título."""
        if self._file_path is None:
            return "Sin título"
        return self._file_path.name

    @property
    def is_new(self) -> bool:
        """Indica si el documento aún no ha sido guardado en disco."""
        return self._file_path is None

    @property
    def extension(self) -> str:
        """Extensión del archivo (vacía si no hay ruta)."""
        if self._file_path is None:
            return ""
        return self._file_path.suffix.lower()

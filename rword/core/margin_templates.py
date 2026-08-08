"""Plantillas de márgenes: presets estándar y personalizados con nombre."""

from __future__ import annotations

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QTextEdit

from rword.core.pages import apply_page_setup, current_page_setup

MARGIN_TEMPLATES_KEY = "page/margin_templates"

# Nombre -> (left, right, top, bottom) en milímetros.
STANDARD_TEMPLATES: dict[str, tuple[float, float, float, float]] = {
    "Normal": (25.4, 25.4, 25.4, 25.4),
    "Estrecho": (12.7, 12.7, 12.7, 12.7),
    "Moderado": (19.05, 19.05, 25.4, 25.4),
    "Ancho": (50.8, 50.8, 25.4, 25.4),
    "Oficina 2003": (31.75, 31.75, 25.4, 25.4),
}


class MarginTemplateStore:
    """Guarda y gestiona plantillas de márgenes personalizadas."""

    def __init__(self, settings: QSettings) -> None:
        self._settings = settings
        self._templates: dict[str, dict[str, float]] = {}
        self._load()

    def _load(self) -> None:
        stored = self._settings.value(MARGIN_TEMPLATES_KEY, [])
        if not isinstance(stored, list):
            return
        for entry in stored:
            if isinstance(entry, dict) and entry.get("name"):
                self._templates[entry["name"]] = entry

    def _save(self) -> None:
        self._settings.setValue(MARGIN_TEMPLATES_KEY, list(self._templates.values()))

    def names(self) -> list[str]:
        return list(self._templates)

    def get(self, name: str) -> tuple[float, float, float, float] | None:
        entry = self._templates.get(name)
        if entry is None:
            return None
        return (
            entry["left"],
            entry["right"],
            entry["top"],
            entry["bottom"],
        )

    def save(
        self, name: str, left: float, right: float, top: float, bottom: float
    ) -> None:
        self._templates[name] = {
            "name": name,
            "left": left,
            "right": right,
            "top": top,
            "bottom": bottom,
        }
        self._save()

    def rename(self, old_name: str, new_name: str) -> bool:
        if old_name not in self._templates or new_name in self._templates:
            return False
        entry = self._templates.pop(old_name)
        entry["name"] = new_name
        self._templates[new_name] = entry
        self._save()
        return True

    def delete(self, name: str) -> bool:
        if name not in self._templates:
            return False
        del self._templates[name]
        self._save()
        return True


def apply_margins(
    editor: QTextEdit, left: float, right: float, top: float, bottom: float
):
    """Aplica márgenes al documento conservando el resto de la configuración."""
    setup = current_page_setup(editor)
    setup.left_margin_mm = left
    setup.right_margin_mm = right
    setup.top_margin_mm = top
    setup.bottom_margin_mm = bottom
    apply_page_setup(editor, setup)
    return setup


def current_margins(editor: QTextEdit) -> tuple[float, float, float, float]:
    setup = current_page_setup(editor)
    return (
        setup.left_margin_mm,
        setup.right_margin_mm,
        setup.top_margin_mm,
        setup.bottom_margin_mm,
    )

"""Sistema de complementos (plugins)."""

from __future__ import annotations

import importlib.util
from pathlib import Path

from PySide6.QtCore import QSettings

PLUGINS_ENABLED_KEY = "plugins/enabled"


class Plugin:
    """Representa un complemento cargado desde un archivo Python."""

    def __init__(self, name: str, module) -> None:
        self.name = name
        self._module = module

    def register(self, main_window) -> None:
        register = getattr(self._module, "register", None)
        if callable(register):
            register(main_window)


def discover_plugins(plugins_dir: Path) -> list[Plugin]:
    """Descubre los complementos disponibles en un directorio."""
    plugins = []
    if not plugins_dir.is_dir():
        return plugins
    for file in sorted(plugins_dir.glob("*.py")):
        if file.name.startswith("_"):
            continue
        module_name = f"rword_plugin_{file.stem}"
        spec = importlib.util.spec_from_file_location(module_name, file)
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except Exception:
            continue
        name = getattr(module, "PLUGIN_NAME", file.stem)
        plugins.append(Plugin(name, module))
    return plugins


class PluginManager:
    """Carga y gestiona los complementos habilitados."""

    def __init__(self, settings: QSettings, plugins_dir: Path) -> None:
        self._settings = settings
        self._plugins_dir = plugins_dir
        self._plugins = discover_plugins(plugins_dir)
        self._enabled = self._load_enabled()

    def _load_enabled(self) -> set[str]:
        stored = self._settings.value(PLUGINS_ENABLED_KEY, [])
        return set(stored) if stored else set()

    def _save_enabled(self) -> None:
        self._settings.setValue(PLUGINS_ENABLED_KEY, sorted(self._enabled))

    def available(self) -> list[Plugin]:
        return list(self._plugins)

    def is_enabled(self, name: str) -> bool:
        return name in self._enabled

    def set_enabled(self, name: str, enabled: bool) -> None:
        if enabled:
            self._enabled.add(name)
        else:
            self._enabled.discard(name)
        self._save_enabled()

    def load_enabled(self, main_window) -> None:
        for plugin in self._plugins:
            if plugin.name in self._enabled:
                plugin.register(main_window)

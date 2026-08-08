"""Configuración de la integración con DeepSeek."""

from __future__ import annotations

from PySide6.QtCore import QSettings

API_URL = "https://api.deepseek.com/chat/completions"
DEFAULT_MODEL = "deepseek-chat"
API_KEY_SETTING = "ai/api_key"
TIMEOUT_SECONDS = 60


class ApiKeyManager:
    """Almacena la clave de API de DeepSeek en los ajustes del usuario."""

    def __init__(self, settings: QSettings) -> None:
        self._settings = settings

    def get(self) -> str:
        return str(self._settings.value(API_KEY_SETTING, "") or "")

    def set(self, api_key: str) -> None:
        self._settings.setValue(API_KEY_SETTING, api_key.strip())

    def clear(self) -> None:
        self._settings.remove(API_KEY_SETTING)

    def has_key(self) -> bool:
        return bool(self.get())

"""Colaboración: usuarios, actividad, permisos y uso compartido."""

from __future__ import annotations

import urllib.parse
from datetime import datetime

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QTextEdit

USERNAME_KEY = "collab/username"
ACTIVITY_KEY = "rword:collab:activity"
PERMISSIONS_KEY = "rword:collab:permissions"
TRACK_AUTHORS_KEY = "collab/track_authors"


class CollaborationManager:
    """Gestiona usuarios, actividad y permisos del documento."""

    def __init__(self, editor: QTextEdit, settings: QSettings) -> None:
        self._editor = editor
        self._settings = settings

    @property
    def username(self) -> str:
        return self._settings.value(USERNAME_KEY, "Usuario")

    def set_username(self, name: str) -> None:
        self._settings.setValue(USERNAME_KEY, name)

    def log(self, event: str, detail: str = "") -> None:
        activity = self._activity()
        activity.append(
            {
                "time": datetime.now().strftime("%H:%M:%S"),
                "user": self.username,
                "event": event,
                "detail": detail,
            }
        )
        del activity[:-200]
        self._editor.document().setProperty(ACTIVITY_KEY, activity)

    def _activity(self) -> list[dict]:
        stored = self._editor.document().property(ACTIVITY_KEY)
        return list(stored) if stored else []

    def activity(self) -> list[dict]:
        return list(self._activity())

    def set_permission(self, username: str, mode: str) -> None:
        permissions = self._permissions()
        permissions[username] = mode
        self._editor.document().setProperty(PERMISSIONS_KEY, permissions)

    def _permissions(self) -> dict:
        stored = self._editor.document().property(PERMISSIONS_KEY)
        return dict(stored) if stored else {}

    def permission(self, username: str) -> str:
        return self._permissions().get(username, "write")

    def apply_permissions(self) -> None:
        mode = self.permission(self.username)
        self._editor.setReadOnly(mode != "write")

    def track_authors(self) -> bool:
        return bool(self._settings.value(TRACK_AUTHORS_KEY, True))

    def set_track_authors(self, enabled: bool) -> None:
        self._settings.setValue(TRACK_AUTHORS_KEY, enabled)

    def share_link(self) -> str:
        path = self._editor.file_path
        if path is not None:
            return path.as_uri() + "#compartido"
        return "rword://documento/compartido"

    def share_mailto(self, subject: str, body: str = "") -> str:
        return (
            f"mailto:?subject={urllib.parse.quote(subject)}"
            f"&body={urllib.parse.quote(body)}"
        )

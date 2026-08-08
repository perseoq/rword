"""Sesiones de conversación y contexto del documento."""

from __future__ import annotations


class ChatSession:
    """Mantiene el historial de mensajes de una conversación."""

    SYSTEM_ROLE = "system"
    USER_ROLE = "user"
    ASSISTANT_ROLE = "assistant"

    def __init__(self, system_prompt: str = "") -> None:
        self._messages: list[dict] = []
        self._system_prompt = system_prompt

    def reset(self, system_prompt: str = "") -> None:
        self._messages = []
        if system_prompt:
            self._system_prompt = system_prompt

    def add(self, role: str, content: str) -> None:
        self._messages.append({"role": role, "content": content})

    def history(self, limit: int = 20) -> list[dict]:
        messages = []
        if self._system_prompt:
            messages.append(
                {"role": self.SYSTEM_ROLE, "content": self._system_prompt}
            )
        messages.extend(self._messages[-limit:])
        return messages

    @property
    def is_empty(self) -> bool:
        return not self._messages


def document_context(editor) -> str:
    """Devuelve el contenido del documento o de la selección."""
    cursor = editor.textCursor()
    if cursor.hasSelection():
        return cursor.selectedText().replace("\u2029", "\n")
    return editor.toPlainText()


def build_messages(prompt: str, context: str = "") -> list[dict]:
    """Construye los mensajes del sistema para una operación con contexto."""
    messages = []
    if context.strip():
        messages.append(
            {
                "role": "system",
                "content": (
                    "Eres una herramienta de procesamiento de texto integrada "
                    "en un editor. Responde únicamente con el texto procesado, "
                    "sin explicaciones adicionales."
                ),
            }
        )
        messages.append({"role": "user", "content": f"Documento:\n{context}\n\n{prompt}"})
    else:
        messages.append({"role": "user", "content": prompt})
    return messages

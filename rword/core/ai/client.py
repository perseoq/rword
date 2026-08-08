"""Cliente HTTP para la API de DeepSeek."""

from __future__ import annotations

import json
import urllib.error
import urllib.request

from rword.core.ai.config import API_URL, DEFAULT_MODEL, TIMEOUT_SECONDS


class AiError(Exception):
    """Error de la API de DeepSeek."""


class DeepSeekClient:
    """Realiza llamadas a la API de chat de DeepSeek."""

    def __init__(self, api_key: str, model: str = DEFAULT_MODEL) -> None:
        self._api_key = api_key
        self._model = model

    @property
    def configured(self) -> bool:
        return bool(self._api_key)

    def chat(
        self,
        messages: list[dict],
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        """Envía una conversación y devuelve la respuesta de texto."""
        if not self._api_key:
            raise AiError(
                "No hay clave de API configurada. Configure su clave en el menú IA."
            )
        payload = json.dumps(
            {
                "model": self._model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }
        ).encode("utf-8")
        request = urllib.request.Request(
            API_URL,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._api_key}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
                data = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            detail = _read_error(error)
            raise AiError(f"Error de la API ({error.code}): {detail}") from error
        except urllib.error.URLError as error:
            raise AiError(f"No se pudo conectar: {error.reason}") from error
        except TimeoutError as error:
            raise AiError("La solicitud superó el tiempo de espera.") from error
        try:
            return data["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, TypeError) as error:
            raise AiError(f"Respuesta inesperada de la API: {data}") from error


def _read_error(error: urllib.error.HTTPError) -> str:
    try:
        body = error.read().decode("utf-8")
        data = json.loads(body)
        return str(data.get("error", {}).get("message", body))
    except Exception:
        return str(error)

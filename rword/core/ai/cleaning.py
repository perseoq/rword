"""Limpieza de texto generado por IA: convierte Markdown a texto plano."""

from __future__ import annotations

import re


def strip_markdown(text: str) -> str:
    """Elimina la sintaxis Markdown y devuelve solo el texto plano."""
    if not text:
        return text

    # Bloques de código (```lang ... ``` y ``` ... ```)
    text = re.sub(r"```[a-zA-Z0-9_+-]*\s*", "", text)
    text = re.sub(r"```", "", text)

    # Encabezados (#, ##, ...)
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.MULTILINE)

    # Código en línea
    text = re.sub(r"`([^`]*)`", r"\1", text)

    # Negrita y cursiva
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"__([^_]+)__", r"\1", text)
    text = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"\1", text)
    text = re.sub(r"(?<!_)_([^_\n]+)_(?!_)", r"\1", text)

    # Tachado
    text = re.sub(r"~~([^~]+)~~", r"\1", text)

    # Enlaces [texto](url) -> texto
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)

    # Imágenes ![alt](url) -> alt
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", text)

    # Citas en bloque
    text = re.sub(r"^\s*>\s?", "", text, flags=re.MULTILINE)

    # Marcas de lista (-, *, +, 1.)
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*\d+[.)]\s+", "", text, flags=re.MULTILINE)

    # Líneas separadoras
    text = re.sub(r"^\s*([-*_]){3,}\s*$", "", text, flags=re.MULTILINE)

    # Normalizar líneas en blanco
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

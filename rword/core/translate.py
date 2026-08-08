"""Traducción básica español-inglés con diccionario reducido."""

from __future__ import annotations

import re

_ES_EN: dict[str, str] = {
    "hola": "hello",
    "adiós": "goodbye",
    "gracias": "thank you",
    "por favor": "please",
    "si": "yes",
    "no": "no",
    "casa": "house",
    "perro": "dog",
    "gato": "cat",
    "agua": "water",
    "pan": "bread",
    "sol": "sun",
    "luna": "moon",
    "amor": "love",
    "amigo": "friend",
    "trabajo": "work",
    "día": "day",
    "noche": "night",
    "mañana": "morning",
    "tarde": "afternoon",
    "bueno": "good",
    "malo": "bad",
    "grande": "big",
    "pequeño": "small",
    "rápido": "fast",
    "lento": "slow",
    "nuevo": "new",
    "viejo": "old",
    "feliz": "happy",
    "triste": "sad",
    "hacer": "to do",
    "ir": "to go",
    "comer": "to eat",
    "beber": "to drink",
    "ver": "to see",
    "tener": "to have",
    "ser": "to be",
    "estar": "to be",
    "querer": "to want",
    "poder": "can",
    "mucho": "much",
    "poco": "little",
    "aquí": "here",
    "allí": "there",
    "hoy": "today",
    "ahora": "now",
    "mundo": "world",
    "tiempo": "time",
}

_EN_ES = {v: k for k, v in _ES_EN.items()}


def translate_word(word: str, target: str = "en") -> str | None:
    key = word.lower().strip().rstrip(".,;:!?")
    if target == "en":
        return _ES_EN.get(key)
    return _EN_ES.get(key)


def translate_text(text: str, target: str = "en") -> str:
    """Traduce el texto palabra a palabra con el diccionario disponible."""
    if not text.strip():
        return text
    words = re.split(r"(\W+)", text)
    translated = []
    for piece in words:
        if re.match(r"^\w+$", piece):
            result = translate_word(piece, target)
            translated.append(result if result is not None else piece)
        else:
            translated.append(piece)
    return "".join(translated)

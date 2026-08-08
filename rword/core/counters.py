"""Contadores y legibilidad del documento."""

from __future__ import annotations

import re

from PySide6.QtWidgets import QTextEdit

_WORD_RE = re.compile(r"\b[\wáéíóúüñÁÉÍÓÚÜÑ]+\b", re.UNICODE)

# Palabras por página aproximadas (estándar de legibilidad).
WORDS_PER_PAGE = 300
CHARS_PER_PAGE = 1800


def count_words(text: str) -> int:
    return len(_WORD_RE.findall(text))


def count_characters(text: str) -> int:
    return len(text)


def count_characters_no_spaces(text: str) -> int:
    return len(re.sub(r"\s", "", text))


def count_paragraphs(text: str) -> int:
    return sum(1 for block in text.split("\n") if block.strip())


def count_lines(text: str) -> int:
    return len(text.split("\n"))


def count_pages(text: str) -> int:
    return max(1, (len(text) + CHARS_PER_PAGE - 1) // CHARS_PER_PAGE)


def count_sentences(text: str) -> int:
    sentences = re.findall(r"[.!?]", text)
    return len(sentences)


def count_syllables(word: str) -> int:
    word = word.lower()
    vowels = "aeiouáéíóúü"
    syllables = 0
    previous_vowel = False
    for char in word:
        if char in vowels:
            if not previous_vowel:
                syllables += 1
            previous_vowel = True
        else:
            previous_vowel = False
    return max(1, syllables)


def document_counts(editor: QTextEdit) -> dict[str, int]:
    text = editor.toPlainText()
    return {
        "words": count_words(text),
        "characters": count_characters(text),
        "characters_no_spaces": count_characters_no_spaces(text),
        "paragraphs": count_paragraphs(text),
        "lines": count_lines(text),
        "pages": count_pages(text),
        "sentences": count_sentences(text),
    }


def readability_index(text: str) -> tuple[float, str]:
    """Índice de legibilidad tipo Flesch adaptado al español."""
    if not text.strip():
        return 0.0, "Sin texto"
    words = count_words(text)
    if words == 0:
        return 0.0, "Sin palabras"
    sentences = count_sentences(text) or 1
    total_syllables = sum(count_syllables(w) for w in _WORD_RE.findall(text))
    score = 206.835 - (1.015 * (words / sentences)) - (84.6 * (total_syllables / words))
    score = max(0.0, min(100.0, score))
    if score >= 60:
        level = "Fácil de leer"
    elif score >= 40:
        level = "Legible"
    elif score >= 25:
        level = "Difícil"
    else:
        level = "Muy difícil"
    return round(score, 1), level


def average_word_length(text: str) -> float:
    words = _WORD_RE.findall(text)
    if not words:
        return 0.0
    return round(sum(len(word) for word in words) / len(words), 1)

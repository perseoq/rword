"""Corrector ortográfico con diccionario personalizado."""

from __future__ import annotations

import re
import string

from PySide6.QtCore import QSettings
from PySide6.QtGui import QColor, QTextCharFormat
from PySide6.QtWidgets import QTextEdit

WORDS_KEY = "spelling/user_words"
MISSPELLED_COLOR = QColor("#ffe0e0")

# Palabras comunes del español usadas como diccionario base.
COMMON_SPANISH_WORDS = {
    "a", "al", "algo", "algunos", "antes", "año", "años", "aquí", "así",
    "aunque", "bueno", "bien", "cada", "casa", "perro", "gato", "árbol",
    "ciudad", "niño", "niña", "hombre",
    "mujer", "libro", "agua", "pan", "sol", "luna", "mar", "cielo", "tierra",
    "amigo", "amiga", "padre", "madre", "hijo", "hija", "escuela", "mesa",
    "silla", "puerta", "ventana", "calle", "plaza", "pueblo", "mundo", "vida",
    "como", "con", "contra",
    "cuando", "de", "del", "desde", "después", "día", "días", "donde",
    "dos", "durante", "e", "el", "ella", "ello", "ellos", "en", "entre",
    "era", "es", "ese", "eso", "esta", "este", "esto", "etc", "fin",
    "forma", "fue", "gran", "ha", "había", "hace", "hacer", "hacia",
    "han", "hasta", "hay", "hecho", "hoy", "importante", "la", "las",
    "le", "lo", "los", "más", "me", "mediante", "menos", "mi", "mientras",
    "misma", "mismo", "muy", "nada", "no", "nuestra", "nuestro", "nueva",
    "nuevo", "o", "otra", "otro", "para", "parte", "pero", "poco", "por",
    "porque", "puede", "que", "quien", "quienes", "qué", "se", "según",
    "ser", "si", "sin", "sino", "sobre", "solo", "su", "sus", "tal",
    "tan", "también", "tanto", "tema", "tiempo", "tiene", "toda", "todo",
    "todos", "tras", "tu", "un", "una", "uno", "unos", "usted", "valor",
    "vez", "ya", "y",
}

_WORD_PATTERN = re.compile(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+")


class SpellChecker:
    """Corrector ortográfico basado en diccionario y palabras de usuario."""

    def __init__(self, settings: QSettings | None = None) -> None:
        self._settings = settings
        self._user_words: set[str] = set()
        if settings is not None:
            stored = settings.value(WORDS_KEY, [])
            self._user_words = set(stored) if stored else set()

    def is_known(self, word: str) -> bool:
        clean = word.strip().strip(string.punctuation)
        lowered = clean.lower()
        return (
            not clean
            or not _WORD_PATTERN.fullmatch(clean)
            or lowered in COMMON_SPANISH_WORDS
            or lowered in self._user_words
        )

    def add_word(self, word: str) -> None:
        clean = word.strip().lower()
        if clean:
            self._user_words.add(clean)
            self._save()

    def remove_word(self, word: str) -> bool:
        clean = word.strip().lower()
        if clean in self._user_words:
            self._user_words.discard(clean)
            self._save()
            return True
        return False

    def user_words(self) -> list[str]:
        return sorted(self._user_words)

    def _save(self) -> None:
        if self._settings is not None:
            self._settings.setValue(WORDS_KEY, sorted(self._user_words))

    def misspelled_ranges(self, editor: QTextEdit):
        """Devuelve los rangos (inicio, fin) de palabras desconocidas."""
        text = editor.toPlainText()
        ranges = []
        for match in _WORD_PATTERN.finditer(text):
            word = match.group(0)
            if word.lower() in COMMON_SPANISH_WORDS:
                continue
            if not self.is_known(word):
                ranges.append((match.start(), match.end()))
        return ranges

    def highlight_misspelled(self, editor: QTextEdit) -> int:
        """Resalta las palabras mal escritas y devuelve el número de ellas."""
        selections = []
        for start, end in self.misspelled_ranges(editor):

            cursor = editor.textCursor()
            cursor.setPosition(start)
            cursor.setPosition(end, cursor.MoveMode.KeepAnchor)
            selection = QTextEdit.ExtraSelection()
            selection.cursor = cursor
            fmt = QTextCharFormat()
            fmt.setBackground(MISSPELLED_COLOR)
            selection.format = fmt
            selections.append(selection)
        editor._spelling_selections = selections
        editor._refresh_extra_selections()
        return len(selections)

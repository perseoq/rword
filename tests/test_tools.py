import pytest
from PySide6.QtCore import QSettings

from rword.core import counters
from rword.core.counters import (
    average_word_length,
    count_characters,
    count_characters_no_spaces,
    count_lines,
    count_paragraphs,
    count_sentences,
    count_syllables,
    count_words,
    readability_index,
)
from rword.core.spelling import SpellChecker
from rword.core.thesaurus import antonyms, suggest, synonyms
from rword.core.translate import translate_text, translate_word


def test_count_words():
    assert count_words("hola mundo amigo") == 3
    assert count_words("") == 0


def test_count_characters():
    assert count_characters("hola") == 4


def test_count_characters_no_spaces():
    assert count_characters_no_spaces("hola mundo") == 9


def test_count_paragraphs():
    assert count_paragraphs("uno\n\ndos\n") == 2


def test_count_lines():
    assert count_lines("a\nb\nc") == 3


def test_count_sentences():
    assert count_sentences("Hola. ¿Cómo estás? ¡Bien!") == 3


def test_count_syllables():
    assert count_syllables("casa") == 2
    assert count_syllables("sol") == 1


def test_document_counts(editor):
    editor.setPlainText("Hola mundo.\nEste es un ejemplo.")
    counts = counters.document_counts(editor)
    assert counts["words"] == 6
    assert counts["paragraphs"] >= 2


def test_readability_index():
    easy = "El gato come pan. El perro corre. La casa es grande."
    score, level = readability_index(easy)
    assert 0 <= score <= 100
    assert level in ("Fácil de leer", "Legible", "Difícil", "Muy difícil")


def test_average_word_length():
    assert average_word_length("hola mundo") == 4.5


def test_spell_checker_known_words(settings):
    checker = SpellChecker(settings)
    assert checker.is_known("casa")
    assert checker.is_known("perro")
    assert checker.is_known("123")
    assert checker.is_known("")


def test_spell_checker_unknown(settings):
    checker = SpellChecker(settings)
    assert not checker.is_known("xyzxyzxyz")


def test_spell_checker_user_words(settings):
    checker = SpellChecker(settings)
    checker.add_word("polivirtual")
    assert checker.is_known("Polivirtual")
    assert "polivirtual" in checker.user_words()
    assert checker.remove_word("polivirtual")
    assert not checker.is_known("polivirtual")


def test_spell_checker_misspelled_ranges(settings, editor):
    checker = SpellChecker(settings)
    editor.setPlainText("casa zzzperro malapalabra")
    ranges = checker.misspelled_ranges(editor)
    assert len(ranges) >= 2


def test_spell_checker_highlight(settings, editor):
    checker = SpellChecker(settings)
    editor.setPlainText("casa zzzpalabra")
    count = checker.highlight_misspelled(editor)
    assert count >= 1
    assert len(editor._spelling_selections) == count


def test_synonyms():
    assert "excelente" in synonyms("bueno")
    assert synonyms("inexistente") == []


def test_antonyms():
    assert "malo" in antonyms("bueno")
    assert antonyms("inexistente") == []


def test_suggest():
    result = suggest("grande")
    assert "enorme" in result["sinónimos"]
    assert "pequeño" in result["antónimos"]


def test_translate_word():
    assert translate_word("casa", "en") == "house"
    assert translate_word("house", "es") == "casa"
    assert translate_word("noexiste", "en") is None


def test_translate_text():
    assert translate_text("hola casa", "en") == "hello house"
    assert translate_text("la casa", "en") == "la house"


@pytest.fixture
def settings(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    qsettings = QSettings()
    qsettings.clear()
    yield qsettings
    qsettings.clear()

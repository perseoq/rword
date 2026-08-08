"""Capacidades de IA: escritura inteligente y corrección avanzada."""

from __future__ import annotations

from rword.core.ai.session import build_messages


def _chat(client, prompt: str, context: str = "", temperature: float = 0.7,
          max_tokens: int = 2048) -> str:
    messages = build_messages(prompt, context)
    return client.chat(messages, temperature=temperature, max_tokens=max_tokens)


# --- Escritura inteligente -------------------------------------------------

def redact(client, instruction: str, context: str = "") -> str:
    return _chat(client, f"Redacta un texto a partir de esta instrucción: {instruction}", context)


def continue_writing(client, text: str) -> str:
    return _chat(
        client,
        "Continúa el siguiente texto de forma natural y coherente:",
        text,
    )


def complete_sentence(client, text: str) -> str:
    return _chat(client, "Completa la frase de forma natural:", text)


def rewrite(client, text: str, instruction: str) -> str:
    return _chat(
        client,
        f"Reescribe el siguiente texto. {instruction} Devuelve solo el texto resultante.",
        text,
    )


def change_tone(client, text: str, tone: str) -> str:
    return rewrite(client, text, f"Cambia el tono a: {tone}.")


def summarize(client, text: str) -> str:
    return _chat(client, "Resume el siguiente texto en un párrafo claro y conciso:", text)


def expand(client, text: str) -> str:
    return _chat(client, "Expande el siguiente texto añadiendo detalles y ejemplos:", text)


def reduce_text(client, text: str) -> str:
    return _chat(client, "Reduce el siguiente texto conservando las ideas clave:", text)


def simplify(client, text: str) -> str:
    return _chat(client, "Simplifica el lenguaje del siguiente texto:", text)


def make_professional(client, text: str) -> str:
    return rewrite(client, text, "Haz el texto más profesional.")


def make_persuasive(client, text: str) -> str:
    return rewrite(client, text, "Haz el texto más persuasivo.")


def make_friendly(client, text: str) -> str:
    return rewrite(client, text, "Haz el texto más amigable.")


def make_neutral(client, text: str) -> str:
    return rewrite(client, text, "Haz el texto más neutral y objetivo.")


def adapt_audience(client, text: str, audience: str) -> str:
    return rewrite(client, text, f"Adapta el texto para {audience}.")


# --- Corrección avanzada ---------------------------------------------------

def correct(client, text: str) -> str:
    return _chat(
        client,
        "Corrige ortografía, gramática y puntuación. Devuelve únicamente el texto corregido.",
        text,
        temperature=0.2,
    )


def detect_redundancies(client, text: str) -> str:
    return _chat(
        client,
        "Detecta redundancias, muletillas y repeticiones. Devuelve una lista breve.",
        text,
        temperature=0.2,
    )


def suggest_better_words(client, text: str) -> str:
    return _chat(
        client,
        "Sugiere mejores palabras para el siguiente texto y explica brevemente.",
        text,
    )


def improve_fluidity(client, text: str) -> str:
    return rewrite(client, text, "Mejora la fluidez y cohesión del texto.")


def improve_clarity(client, text: str) -> str:
    return rewrite(client, text, "Mejora la claridad del texto.")


def detect_ambiguities(client, text: str) -> str:
    return _chat(
        client,
        "Detecta ambigüedades y frases demasiado largas. Devuelve una lista breve.",
        text,
    )


# --- Traducción ------------------------------------------------------------

def translate(client, text: str, target_language: str) -> str:
    return _chat(
        client,
        f"Traduce el siguiente texto a {target_language} manteniendo el significado. "
        "Devuelve únicamente la traducción:",
        text,
        temperature=0.2,
    )


def detect_language(client, text: str) -> str:
    return _chat(
        client,
        "Detecta el idioma del siguiente texto y responde con el nombre del idioma.",
        text,
        temperature=0.1,
        max_tokens=64,
    )


# --- Análisis del documento ------------------------------------------------

def main_ideas(client, text: str) -> str:
    return _chat(client, "Extrae las ideas principales del siguiente texto:", text)


def extract_conclusions(client, text: str) -> str:
    return _chat(client, "Extrae las conclusiones del siguiente texto:", text)


def detect_inconsistencies(client, text: str) -> str:
    return _chat(
        client,
        "Detecta inconsistencias, contradicciones e información faltante. "
        "Devuelve una lista breve.",
        text,
        temperature=0.2,
    )


def reading_difficulty(client, text: str) -> str:
    return _chat(
        client,
        "Calcula la dificultad de lectura del texto y explica brevemente.",
        text,
        temperature=0.2,
    )


def target_audience(client, text: str) -> str:
    return _chat(
        client,
        "Identifica el público objetivo del siguiente texto.",
        text,
        temperature=0.2,
    )


def classify_document(client, text: str) -> str:
    return _chat(
        client,
        "Clasifica el tipo de documento (informe, contrato, carta, artículo...) "
        "y justifica brevemente.",
        text,
        temperature=0.2,
    )


def executive_summary(client, text: str) -> str:
    return _chat(
        client,
        "Genera un resumen ejecutivo del siguiente texto.",
        text,
    )

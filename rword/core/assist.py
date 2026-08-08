"""Asistencia local: glosario, coherencia, plantillas y autocompletado."""

from __future__ import annotations

import re

from PySide6.QtWidgets import QTextEdit

from rword.core.ai.session import document_context

_WORD_RE = re.compile(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]{3,}")

SMART_TEMPLATES = {
    "Carta formal": {
        "fields": ["destinatario", "asunto", "cuerpo"],
        "template": (
            "Estimado/a {destinatario}:\n\n{asunto}\n\n{cuerpo}\n\n"
            "Atentamente,\n[Nombre del remitente]"
        ),
    },
    "Currículum": {
        "fields": ["nombre", "puesto", "experiencia", "educacion"],
        "template": (
            "CURRÍCULUM VITAE\n\nNombre: {nombre}\nPuesto deseado: {puesto}\n\n"
            "Experiencia:\n{experiencia}\n\nEducación:\n{educacion}"
        ),
    },
    "Contrato simple": {
        "fields": ["partes", "objeto", "duracion", "fecha"],
        "template": (
            "CONTRATO\n\nEntre {partes}.\n\nObjeto: {objeto}.\n"
            "Duración: {duracion}.\n\nFirmado el {fecha}."
        ),
    },
    "Informe": {
        "fields": ["titulo", "resumen", "conclusiones"],
        "template": (
            "INFORME\n\n{titulo}\n\nResumen:\n{resumen}\n\n"
            "Conclusiones:\n{conclusiones}"
        ),
    },
}


def generate_glossary(editor: QTextEdit) -> None:
    """Inserta un glosario con los términos técnicos repetidos."""
    text = editor.toPlainText()
    words = _WORD_RE.findall(text.lower())
    from collections import Counter

    counts = Counter(words)
    terms = sorted(
        (word for word, count in counts.items() if count >= 3),
        key=str.casefold,
    )
    cursor = editor.textCursor()
    cursor.movePosition(cursor.MoveOperation.End)
    cursor.insertBlock()
    cursor.insertText("Glosario\n")
    for term in terms:
        cursor.insertText(f"• {term}: \n")


def consistency_findings(editor: QTextEdit) -> list[tuple[str, str]]:
    """Detecta posibles incoherencias locales de nombres y cifras."""
    text = editor.toPlainText()
    findings: list[tuple[str, str]] = []
    words = _WORD_RE.findall(text)
    variants: dict[str, set[str]] = {}
    for word in words:
        variants.setdefault(word.lower(), set()).add(word)
    _stopwords = {"el", "la", "los", "las", "un", "una", "unos", "unas",
                  "del", "al", "en", "de", "y", "es", "se", "por", "para"}
    for base, forms in variants.items():
        if len(forms) > 1 and base not in _stopwords:
            findings.append(
                ("Nombres", f"«{base}» aparece como: {', '.join(sorted(forms))}.")
            )
    return findings


def fill_template(editor: QTextEdit, template_key: str, values: dict) -> None:
    """Inserta una plantilla con los valores rellenados."""
    template = SMART_TEMPLATES[template_key]["template"]
    for field, value in values.items():
        template = template.replace("{" + field + "}", value or f"[{field}]")
    editor.insertPlainText(template)


def completer_words(editor: QTextEdit) -> list[str]:
    """Palabras del documento para el autocompletado."""
    text = editor.toPlainText().lower()
    words = {word for word in _WORD_RE.findall(text) if len(word) >= 3}
    return sorted(words)


def style_sample_from_selection(editor: QTextEdit) -> str:
    cursor = editor.textCursor()
    if cursor.hasSelection():
        return cursor.selectedText().replace("\u2029", "\n")
    return document_context(editor)[:2000]


AGENTS = {
    "Abogado": "abogado especializado en derecho contractual",
    "Contador": "contador público experto en finanzas",
    "Médico": "profesional de la salud",
    "Profesor": "docente experto en pedagogía",
    "Programador": "desarrollador de software senior",
    "Analista": "analista de negocios",
}

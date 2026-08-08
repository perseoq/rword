"""Tesauro: sinónimos y antónimos."""

from __future__ import annotations

_SYNONYMS: dict[str, tuple[str, ...]] = {
    "bueno": (
        "excelente", "magnífico", "estupendo", "admirable",
        "bondadoso", "beneficioso", "favorable", "provechoso",
    ),
    "malo": ("pésimo", "deficiente", "deteriorado", "inadecuado"),
    "grande": ("enorme", "gigante", "colosal", "inmenso"),
    "pequeño": ("diminuto", "reducido", "menor", "mínimo"),
    "rápido": ("veloz", "ligero", "acelerado", "presuroso"),
    "lento": ("pausado", "tardío", "despacio", "parsimonioso"),
    "feliz": ("contento", "alegre", "satisfecho", "dichoso"),
    "triste": ("afligido", "abatido", "melancólico", "apenado"),
    "importante": ("relevante", "significativo", "trascendental", "destacado"),
    "fácil": ("sencillo", "simple", "cómodo", "ligero"),
    "difícil": ("complicado", "complejo", "arduo", "laborioso"),
    "trabajo": ("labor", "empleo", "ocupación", "tarea"),
    "casa": ("hogar", "domicilio", "vivienda", "residencia"),
    "hablar": ("conversar", "dialogar", "expresar", "comunicar"),
    "ver": ("observar", "contemplar", "mirar", "distinguir"),
    "comer": ("ingerir", "alimentarse", "tomar", "degustar"),
    "bondadoso": ("beneficioso", "favorable", "provechoso", "benevolente"),
    "bonito": ("hermoso", "bello", "lindo", "atractivo"),
    "feo": ("horrible", "desagradable", "deforme", "repulsivo"),
}

_ANTONYMS: dict[str, tuple[str, ...]] = {
    "bueno": ("malo", "pésimo", "deficiente"),
    "grande": ("pequeño", "diminuto", "reducido"),
    "rápido": ("lento", "pausado", "tardío"),
    "feliz": ("triste", "infeliz", "abatido"),
    "difícil": ("fácil", "sencillo", "simple"),
    "arriba": ("abajo", "inferior"),
    "primero": ("último", "postrero"),
    "siempre": ("nunca", "jamás"),
    "mucho": ("poco", "escaso"),
    "tener": ("carecer", "faltar"),
    "entrar": ("salir", "partir"),
    "abrir": ("cerrar", "clausurar"),
}


def synonyms(word: str) -> list[str]:
    return list(_SYNONYMS.get(word.lower().strip(), []))


def antonyms(word: str) -> list[str]:
    return list(_ANTONYMS.get(word.lower().strip(), []))


def suggest(word: str) -> dict[str, list[str]]:
    return {"sinónimos": synonyms(word), "antónimos": antonyms(word)}

"""Catálogo de documentos jurídicos extraído del archivo SKILL.md.

El archivo SKILL.md tiene una estructura irregular: unas fases enumeran los
documentos con encabezados ``##### N.N`` (con categorías ``#### N.``) y otras
usan encabezados planos ``###`` que además suelen repetir los mismos documentos
en dos catálogos. Este módulo normaliza ambas formas en una lista única.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

SKILL_FILENAME = "SKILL.md"

_PHASE_RE = re.compile(r"^# Skill:\s*(.+)$")
_CATALOG_RE = re.compile(
    r"^#+\s*(\d+(?:\.\d+)?[.)]?)?\s*Catálogo de documentos y requisitos"
)
_CATALOG_END_RE = re.compile(
    r"^#+\s*(?:Lectura de documentos|\d+\.\s*Reglas adicionales|"
    r"Reglas adicionales)"
)
_NUMBERED_DOC_RE = re.compile(r"^#####\s+\d+(?:\.\d+)?[.)]?\s+(.+)$")
_FLAT_DOC_RE = re.compile(r"^###\s+(.+)$")
_CATEGORY_RE = re.compile(r"^####\s+\d+\.?\s+(.+)$")
_HEADING_RE = re.compile(r"^#{1,6}\s+")
_META_RE = re.compile(r"^\*\*(.+?):\*\*\s?(.*)$")
_BULLET_RE = re.compile(r"^-\s+(.+)$")


@dataclass
class LegalDocument:
    """Un documento del catálogo: descripción, fundamento y requisitos."""

    phase: str
    name: str
    category: str = ""
    description: str = ""
    fundamento: str = ""
    requisitos: list[str] = field(default_factory=list)
    raw: str = ""


def default_skill_path() -> Path:
    """Ruta al SKILL.md: variable de entorno o junto al repositorio."""
    env = os.environ.get("RWORD_SKILL")
    if env:
        return Path(env)
    return Path(__file__).resolve().parents[3] / SKILL_FILENAME


@lru_cache(maxsize=4)
def load_skill(path: str | Path | None = None) -> tuple[str, list[LegalDocument]]:
    """Carga el SKILL.md y devuelve (sección base, lista de documentos)."""
    source = Path(path) if path else default_skill_path()
    return parse_skill(source.read_text(encoding="utf-8"))


def clear_skill_cache() -> None:
    """Limpia la caché de carga (útil en pruebas)."""
    load_skill.cache_clear()


def legal_documents(path: str | Path | None = None) -> list[LegalDocument]:
    """Devuelve la lista completa de documentos del catálogo."""
    return load_skill(path)[1]


def base_section(path: str | Path | None = None) -> str:
    """Devuelve la sección base con las reglas de formato forense."""
    return load_skill(path)[0]


def document_by_name(name: str) -> LegalDocument | None:
    """Busca un documento por su nombre exacto (primera coincidencia)."""
    target = name.strip().casefold()
    for document in legal_documents():
        if document.name.casefold() == target:
            return document
    return None


def _split_phases(text: str) -> list[tuple[str, list[str]]]:
    phases: list[tuple[str, list[str]]] = []
    current_name: str | None = None
    current_lines: list[str] = []
    for line in text.splitlines():
        match = _PHASE_RE.match(line)
        if match:
            if current_name is not None:
                phases.append((current_name, current_lines))
            current_name = match.group(1).strip()
            current_lines = []
        elif current_name is not None:
            current_lines.append(line)
    if current_name is not None:
        phases.append((current_name, current_lines))
    return phases


def _catalog_bounds(lines: list[str]) -> tuple[int | None, int]:
    start = None
    for index, line in enumerate(lines):
        if _CATALOG_RE.match(line):
            start = index
            break
    if start is None:
        return None, 0
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if _CATALOG_END_RE.match(lines[index]):
            end = index
            break
    return start, end


def _parse_document(
    phase: str, category: str, heading: str, body: list[str]
) -> LegalDocument:
    description = ""
    fundamento = ""
    inline_requisitos = ""
    requisitos: list[str] = []
    for line in body:
        meta = _META_RE.match(line)
        if meta:
            key, value = meta.group(1).strip(), meta.group(2).strip()
            if key.startswith("Descripción"):
                description = value
            elif key.startswith("Fundamento"):
                fundamento = value
            elif key.startswith("Requisitos"):
                inline_requisitos = value
            continue
        bullet = _BULLET_RE.match(line)
        if bullet:
            item = bullet.group(1).strip()
            if item:
                requisitos.append(item)
    if not requisitos and inline_requisitos:
        requisitos = [
            item.strip().rstrip(".")
            for item in inline_requisitos.split(",")
            if item.strip()
        ]
    raw = "\n".join([heading] + body).strip()
    return LegalDocument(
        phase=phase,
        name=heading,
        category=category,
        description=description,
        fundamento=fundamento,
        requisitos=requisitos,
        raw=raw,
    )


def parse_skill(text: str) -> tuple[str, list[LegalDocument]]:
    """Analiza el texto de SKILL.md y devuelve (base, documentos)."""
    documents: list[LegalDocument] = []
    base = ""
    phases = _split_phases(text)
    for index, (phase, lines) in enumerate(phases):
        start, end = _catalog_bounds(lines)
        if start is None:
            if index == 0:
                base = f"# Skill: {phase}\n" + "\n".join(lines)
            continue
        catalog = lines[start + 1 : end]
        numbered = any(_NUMBERED_DOC_RE.match(line) for line in catalog)
        doc_re = _NUMBERED_DOC_RE if numbered else _FLAT_DOC_RE

        category = ""
        seen: set[str] = set()
        for line_index, line in enumerate(catalog):
            category_match = _CATEGORY_RE.match(line)
            if category_match:
                category = category_match.group(1).strip()
                continue
            match = doc_re.match(line)
            if not match:
                continue
            name = match.group(1).strip()
            key = name.casefold()
            if key in seen:
                continue
            seen.add(key)
            body = []
            for following in catalog[line_index + 1 :]:
                if _HEADING_RE.match(following):
                    break
                body.append(following)
            documents.append(_parse_document(phase, category, name, body))
    return base, documents

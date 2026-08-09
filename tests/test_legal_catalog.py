from collections import Counter

from rword.core.legal.catalog import (
    default_skill_path,
    document_by_name,
    legal_documents,
    parse_skill,
)


def _load():
    return parse_skill(default_skill_path().read_text(encoding="utf-8"))


def test_parses_base_section():
    base, _docs = _load()
    assert "SECCIÓN BASE" in base
    assert "Formato Forense" in base


def test_parses_many_documents_and_phases():
    _base, docs = _load()
    assert len(docs) >= 700
    phases = {document.phase for document in docs}
    assert len(phases) >= 20


def test_no_duplicates_within_a_phase():
    _base, docs = _load()
    pairs = Counter((document.phase, document.name.casefold()) for document in docs)
    duplicates = {key for key, count in pairs.items() if count > 1}
    assert not duplicates


def test_flat_phase_duplicates_are_deduplicated():
    _base, docs = _load()
    amparo = [
        document
        for document in docs
        if document.phase == "Redactor de Documentos — Juicio de Amparo"
        and document.name == "Demanda de Amparo Indirecto"
    ]
    assert len(amparo) == 1


def test_numbered_document_fields():
    document = document_by_name("Demanda / Escrito Inicial de Demanda")
    assert document is not None
    assert document.fundamento
    assert len(document.requisitos) >= 10
    assert document.category


def test_flat_document_fields():
    document = document_by_name("Aviso de Incorporación al IMSS")
    assert document is not None
    assert document.fundamento
    assert any("NSS" in requisito for requisito in document.requisitos)


def test_document_by_name_returns_none_when_missing():
    assert document_by_name("No existe tal documento") is None


def test_parse_with_override(tmp_path):
    skill = tmp_path / "SKILL.md"
    skill.write_text(
        "# Skill: Redactor de Documentos — Prueba\n"
        "## 4. Catálogo de documentos y requisitos\n"
        "\n"
        "### Escrito de Prueba\n"
        "**Fundamento:** Ley de Pruebas Art. 1.\n"
        "**Requisitos:** nombre, domicilio, firma.\n",
        encoding="utf-8",
    )
    base, docs = parse_skill(skill.read_text(encoding="utf-8"))
    assert len(docs) == 1
    assert docs[0].name == "Escrito de Prueba"
    assert docs[0].requisitos == ["nombre", "domicilio", "firma"]


def test_legal_documents_returns_catalog():
    assert len(legal_documents()) >= 700

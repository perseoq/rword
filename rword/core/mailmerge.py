"""Combinación de correspondencia: orígenes de datos y generación."""

from __future__ import annotations

import csv
import re
import sqlite3
from pathlib import Path

from PySide6.QtWidgets import QTextEdit

RECORDS_KEY = "rword:mailmerge:records"
SOURCE_KEY = "rword:mailmerge:source"
FIELD_PATTERN = re.compile(r"\{(\w+)\}")


def load_csv(path: str | Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [dict(row) for row in reader]


def load_sqlite(path: str | Path, query: str) -> list[dict]:
    connection = sqlite3.connect(str(path))
    connection.row_factory = sqlite3.Row
    cursor = connection.execute(query)
    records = [dict(row) for row in cursor.fetchall()]
    connection.close()
    return records


def records_of(editor: QTextEdit) -> list[dict]:
    stored = editor.document().property(RECORDS_KEY)
    return list(stored) if stored else []


def set_records(editor: QTextEdit, records: list[dict], source: str = "") -> None:
    editor.document().setProperty(RECORDS_KEY, records)
    editor.document().setProperty(SOURCE_KEY, source)


def data_fields(records: list[dict]) -> list[str]:
    fields: list[str] = []
    for record in records:
        for key in record:
            if key not in fields:
                fields.append(key)
    return fields


def merge_template(template: str, record: dict) -> str:
    def _replace(match: re.Match) -> str:
        return str(record.get(match.group(1), match.group(0)))

    return FIELD_PATTERN.sub(_replace, template)


def merge_editor_template(editor: QTextEdit, record: dict) -> None:
    """Reemplaza los campos del documento por los valores de un registro."""
    cursor = editor.textCursor()
    cursor.select(cursor.SelectionType.Document)
    text = cursor.selectedText().replace("\u2029", "\n")
    merged = merge_template(text, record)
    cursor.insertText(merged)


def filter_records(records: list[dict], column: str, value: str) -> list[dict]:
    return [
        record for record in records if str(record.get(column, "")) == value
    ]


def sort_records(
    records: list[dict], column: str, ascending: bool = True
) -> list[dict]:
    return sorted(
        records,
        key=lambda record: str(record.get(column, "")),
        reverse=not ascending,
    )


def distinct_values(records: list[dict], column: str) -> list[str]:
    values = {str(record.get(column, "")) for record in records if record.get(column)}
    return sorted(values)


def generate_letters(editor: QTextEdit, records: list[dict]) -> str:
    """Genera las cartas combinadas separadas por saltos de página."""
    template_cursor = editor.textCursor()
    template_cursor.select(template_cursor.SelectionType.Document)
    template = template_cursor.selectedText().replace("\u2029", "\n")
    parts = []
    for record in records:
        parts.append(merge_template(template, record))
    return "\n".join(parts)


def generate_labels(
    records: list[dict],
    label_fields: list[str],
    columns_per_row: int = 3,
) -> str:
    """Genera texto de etiquetas de dirección dispuestas en filas."""
    blocks = []
    for record in records:
        lines = [
            str(record.get(field, "")).strip()
            for field in label_fields
            if str(record.get(field, "")).strip()
        ]
        blocks.append("\n".join(lines))
    rows = [
        blocks[i : i + columns_per_row]
        for i in range(0, len(blocks), columns_per_row)
    ]
    output = []
    for row in rows:
        output.append(" | ".join(cell for cell in row))
    return "\n\n".join(output)


def mailto_link(record: dict, subject: str = "") -> str:
    email = record.get("email", "")
    if not email:
        return ""
    import urllib.parse

    return f"mailto:{email}?subject={urllib.parse.quote(subject)}"


def generate_envelopes(editor: QTextEdit, records: list[dict], fields: list[str]) -> str:
    """Genera sobres con los datos de dirección de cada registro."""
    sections = []
    for record in records:
        lines = [
            str(record.get(field, "")).strip()
            for field in fields
            if str(record.get(field, "")).strip()
        ]
        sections.append("\n".join(lines))
    return "\n\n".join(sections)


def ensure_records_for(editor: QTextEdit) -> list[dict]:
    return records_of(editor)

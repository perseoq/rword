
from rword.core.mailmerge import (
    data_fields,
    distinct_values,
    filter_records,
    generate_envelopes,
    generate_labels,
    generate_letters,
    load_csv,
    load_sqlite,
    mailto_link,
    merge_editor_template,
    merge_template,
    records_of,
    set_records,
    sort_records,
)

RECORDS = [
    {"nombre": "Ana", "email": "ana@example.com", "ciudad": "Madrid"},
    {"nombre": "Luis", "email": "luis@example.com", "ciudad": "Barcelona"},
    {"nombre": "Sofía", "email": "sofia@example.com", "ciudad": "Madrid"},
]


def test_load_csv(tmp_path):
    path = tmp_path / "datos.csv"
    path.write_text("nombre,email\nAna,ana@example.com\n", encoding="utf-8")
    records = load_csv(path)
    assert records == [{"nombre": "Ana", "email": "ana@example.com"}]


def test_load_sqlite(tmp_path):
    import sqlite3

    path = tmp_path / "datos.db"
    connection = sqlite3.connect(path)
    connection.execute(
        "CREATE TABLE personas (nombre TEXT, email TEXT)"
    )
    connection.execute(
        "INSERT INTO personas VALUES (?, ?)", ("Ana", "ana@example.com")
    )
    connection.commit()
    connection.close()
    records = load_sqlite(path, "SELECT * FROM personas")
    assert records[0]["nombre"] == "Ana"


def test_set_and_get_records(editor):
    assert records_of(editor) == []
    set_records(editor, RECORDS)
    assert records_of(editor) == RECORDS


def test_data_fields():
    assert data_fields(RECORDS) == ["nombre", "email", "ciudad"]


def test_merge_template():
    result = merge_template("Hola {nombre}, escribe a {email}", RECORDS[0])
    assert result == "Hola Ana, escribe a ana@example.com"


def test_merge_template_missing_field_keeps_placeholder():
    result = merge_template("Valor: {inexistente}", RECORDS[0])
    assert "{inexistente}" in result


def test_merge_editor_template(editor):
    editor.setPlainText("Estimado {nombre}:")
    set_records(editor, RECORDS)
    merge_editor_template(editor, RECORDS[0])
    assert "Estimado Ana:" in editor.toPlainText()


def test_filter_records():
    filtered = filter_records(RECORDS, "ciudad", "Madrid")
    assert len(filtered) == 2
    assert all(r["ciudad"] == "Madrid" for r in filtered)


def test_sort_records():
    sorted_records = sort_records(RECORDS, "nombre")
    assert sorted_records[0]["nombre"] == "Ana"
    sorted_desc = sort_records(RECORDS, "nombre", ascending=False)
    assert sorted_desc[0]["nombre"] == "Sofía"


def test_distinct_values():
    assert distinct_values(RECORDS, "ciudad") == ["Barcelona", "Madrid"]


def test_generate_letters(editor):
    editor.setPlainText("Hola {nombre}.")
    set_records(editor, RECORDS)
    output = generate_letters(editor, RECORDS)
    assert "Hola Ana." in output
    assert "Hola Sofía." in output


def test_generate_labels():
    output = generate_labels(RECORDS, ["nombre"], columns_per_row=2)
    assert "Ana" in output
    assert "Luis" in output


def test_generate_envelopes():
    output = generate_envelopes(None, RECORDS, ["nombre", "ciudad"])
    assert "Ana\nMadrid" in output


def test_mailto_link():
    link = mailto_link(RECORDS[0], "Asunto prueba")
    assert link.startswith("mailto:ana@example.com")
    assert "Asunto" in link


def test_mailto_link_no_email():
    assert mailto_link({"nombre": "X"}, "Asunto") == ""


def test_main_window_data_fields(main_window):
    from rword.core.mailmerge import set_records

    set_records(main_window._editor, RECORDS)
    main_window._merge_fields = data_fields(RECORDS)
    assert "nombre" in main_window._merge_fields


def test_main_window_insert_field(main_window):
    from rword.core.mailmerge import set_records

    set_records(main_window._editor, RECORDS)
    main_window._insert_merge_field("nombre")
    assert "{nombre}" in main_window._editor.toPlainText()

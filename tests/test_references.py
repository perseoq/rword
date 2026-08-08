from PySide6.QtGui import QTextCursor

from rword.core.references import (
    _note_count,
    add_endnote,
    add_footnote,
    add_source,
    goto_anchor,
    insert_bibliography,
    insert_caption,
    insert_citation,
    insert_cross_reference,
    insert_index,
    insert_table_of_figures,
    insert_toc,
    mark_index_entry,
    sources,
    update_toc,
)
from rword.core.styles import Style, apply_style


def _heading(editor, text, size=26):
    editor.insertPlainText(text)
    editor.selectAll()
    apply_style(editor, Style("H", font_size=size, bold=True))
    editor.moveCursor(QTextCursor.MoveOperation.End)
    editor.insertPlainText("\n")


def test_insert_toc(editor):
    editor.setPlainText("")
    _heading(editor, "Introducción")
    _heading(editor, "Métodos", size=20)
    insert_toc(editor)
    text = editor.toPlainText()
    assert "Tabla de contenido" in text
    assert "Introducción" in text
    assert "Métodos" in text


def test_update_toc_replaces(editor):
    _heading(editor, "Capítulo A")
    insert_toc(editor)
    _heading(editor, "Capítulo B")
    update_toc(editor)
    assert "Capítulo B" in editor.toPlainText()


def test_toc_links_are_anchors(editor):
    _heading(editor, "Sección X")
    insert_toc(editor)
    found = False
    block = editor.document().begin()
    while block.isValid():
        iterator = block.begin()
        while not iterator.atEnd():
            fmt = iterator.fragment().charFormat()
            if fmt.isAnchor() and "Sección X" in iterator.fragment().text():
                found = True
            iterator += 1
        block = block.next()
    assert found


def test_goto_anchor(editor):
    _heading(editor, "Destino")
    insert_toc(editor)
    block_number = None
    block = editor.document().begin()
    while block.isValid():
        if block.text().strip() == "Destino":
            block_number = block.blockNumber()
            break
        block = block.next()
    assert block_number is not None
    assert goto_anchor(editor, f"rword-toc-{block_number}")


def test_add_footnote(editor):
    editor.insertPlainText("texto")
    add_footnote(editor, "nota explicativa")
    assert "[1]" in editor.toPlainText()
    assert "1. nota explicativa" in editor.toPlainText()
    assert _note_count(editor) == 1


def test_add_two_footnotes(editor):
    editor.insertPlainText("a")
    add_footnote(editor, "nota uno")
    add_footnote(editor, "nota dos")
    assert _note_count(editor) == 2
    assert "[2]" in editor.toPlainText()
    assert "2. nota dos" in editor.toPlainText()


def test_add_endnote(editor):
    editor.insertPlainText("texto")
    add_endnote(editor, "nota final")
    assert "[1]" in editor.toPlainText()
    assert "1. nota final" in editor.toPlainText()


def test_cross_reference(editor):
    editor.insertPlainText("véase ")
    insert_cross_reference(editor, "Apéndice A")
    assert "Apéndice A" in editor.toPlainText()


def test_sources_and_bibliography(editor):
    assert sources(editor) == []
    add_source(editor, "García", "2020", "El método")
    add_source(editor, "López", "2021", "Resultados")
    assert len(sources(editor)) == 2
    insert_bibliography(editor)
    text = editor.toPlainText()
    assert "Bibliografía" in text
    assert "García (2020). El método." in text
    assert "López (2021). Resultados." in text


def test_insert_citation(editor):
    editor.insertPlainText("según ")
    insert_citation(editor, "García", "2020")
    assert "(García, 2020)" in editor.toPlainText()


def test_caption_and_table_of_figures(editor):
    editor.insertPlainText("figura aquí\n")
    insert_caption(editor, "Gráfico de ventas")
    insert_caption(editor, "Gráfico de costes")
    insert_table_of_figures(editor)
    text = editor.toPlainText()
    assert "Figura 1: Gráfico de ventas" in text
    assert "Figura 2: Gráfico de costes" in text
    assert "Tabla de figuras" in text


def test_index_entries(editor):
    editor.insertPlainText("manzana pera")
    cursor = editor.textCursor()
    cursor.setPosition(0)
    cursor.setPosition(len("manzana"), cursor.MoveMode.KeepAnchor)
    editor.setTextCursor(cursor)
    mark_index_entry(editor, "manzana")
    cursor = editor.textCursor()
    cursor.setPosition(len("manzana ") + 4, cursor.MoveMode.MoveAnchor)
    editor.setTextCursor(cursor)
    insert_index(editor)
    assert "Índice analítico" in editor.toPlainText()
    assert "manzana" in editor.toPlainText()

from PySide6.QtGui import QColor, QTextTable

from rword.core.tables import (
    add_column_after,
    add_column_before,
    add_row_after,
    add_row_before,
    autofit,
    current_table,
    delete_column,
    delete_row,
    delete_table,
    insert_table,
    merge_cells,
    select_column,
    select_row,
    select_table,
    set_cell_shading,
    set_heading_row_repeat,
    set_table_style,
    sort_current_column,
    split_cell,
    table_formula,
    table_to_text,
    text_to_table,
)


def _cell_text(table, row, col):
    return table.cellAt(row, col).firstCursorPosition().block().text()


def _move_to(table, editor, row, col):
    editor.setTextCursor(table.cellAt(row, col).firstCursorPosition())


def test_insert_table(editor):
    table = insert_table(editor, 3, 4)
    assert isinstance(table, QTextTable)
    assert table.rows() == 3
    assert table.columns() == 4


def test_current_table(editor):
    insert_table(editor, 2, 2)
    table = current_table(editor)
    assert table is not None
    assert table.rows() == 2


def test_add_row_before_after(editor):
    table = insert_table(editor, 2, 2)
    _move_to(table, editor, 0, 0)
    add_row_before(editor)
    assert table.rows() == 3
    add_row_after(editor)
    assert table.rows() == 4


def test_add_column_before_after(editor):
    table = insert_table(editor, 2, 2)
    _move_to(table, editor, 0, 0)
    add_column_before(editor)
    assert table.columns() == 3
    add_column_after(editor)
    assert table.columns() == 4


def test_delete_row_column(editor):
    table = insert_table(editor, 3, 3)
    _move_to(table, editor, 1, 1)
    delete_row(editor)
    assert table.rows() == 2
    delete_column(editor)
    assert table.columns() == 2


def test_delete_table(editor):
    insert_table(editor, 2, 2)
    assert current_table(editor) is not None
    delete_table(editor)
    assert current_table(editor) is None


def test_merge_cells(editor):
    table = insert_table(editor, 3, 3)
    cursor = editor.textCursor()
    cursor.setPosition(table.cellAt(0, 0).firstPosition())
    cursor.setPosition(table.cellAt(1, 1).lastPosition(), cursor.MoveMode.KeepAnchor)
    editor.setTextCursor(cursor)
    merge_cells(editor)
    cell = table.cellAt(0, 0)
    assert cell.rowSpan() == 2
    assert cell.columnSpan() == 2


def test_split_cell(editor):
    table = insert_table(editor, 2, 2)
    _move_to(table, editor, 0, 0)
    split_cell(editor, 1, 2)
    assert table.columns() == 3


def test_select_row_column_table(editor):
    table = insert_table(editor, 3, 3)
    _move_to(table, editor, 1, 1)
    select_row(editor)
    assert editor.textCursor().hasSelection()
    select_column(editor)
    assert editor.textCursor().hasSelection()
    select_table(editor)
    assert editor.textCursor().hasSelection()


def test_set_cell_shading(editor):
    table = insert_table(editor, 2, 2)
    _move_to(table, editor, 0, 0)
    cursor = editor.textCursor()
    cursor.setPosition(table.cellAt(0, 0).firstPosition())
    cursor.setPosition(table.cellAt(0, 0).lastPosition(), cursor.MoveMode.KeepAnchor)
    editor.setTextCursor(cursor)
    set_cell_shading(editor, QColor("#ffffcc"))
    char_format = editor.textCursor().charFormat()
    assert char_format.background().color().name() == "#ffffcc"


def test_set_table_style(editor):
    table = insert_table(editor, 2, 2)
    set_table_style(editor, "Simple")
    assert table.format().borderStyle() != 0


def test_heading_repeat(editor):
    table = insert_table(editor, 3, 2)
    set_heading_row_repeat(editor, True)
    assert table.format().headerRowCount() == 1
    set_heading_row_repeat(editor, False)
    assert table.format().headerRowCount() == 0


def test_sort_table_numeric(editor):
    table = insert_table(editor, 4, 2)
    values = ["10", "5", "20", "15"]
    for r, value in enumerate(values):
        _cell_text(table, r, 0)
        table.cellAt(r, 0).firstCursorPosition().insertText(value)
    sort_current_column(editor, ascending=True)
    assert _cell_text(table, 0, 0) == "5"
    assert _cell_text(table, 3, 0) == "20"
    sort_current_column(editor, ascending=False)
    assert _cell_text(table, 0, 0) == "20"


def test_sort_table_text(editor):
    table = insert_table(editor, 3, 1)
    for r, value in enumerate(["naranja", "manzana", "banana"]):
        table.cellAt(r, 0).firstCursorPosition().insertText(value)
    sort_current_column(editor, ascending=True)
    assert _cell_text(table, 0, 0) == "banana"
    assert _cell_text(table, 1, 0) == "manzana"
    assert _cell_text(table, 2, 0) == "naranja"


def test_table_formula_sum(editor):
    table = insert_table(editor, 4, 2)
    for r, value in enumerate(["1", "2", "3", "6"]):
        table.cellAt(r, 0).firstCursorPosition().insertText(value)
    _move_to(table, editor, 3, 0)
    table_formula(editor, "SUM")
    assert _cell_text(table, 3, 0) == "6"


def test_table_formula_average(editor):
    table = insert_table(editor, 4, 2)
    for r, value in enumerate(["2", "4", "6", "9"]):
        table.cellAt(r, 0).firstCursorPosition().insertText(value)
    _move_to(table, editor, 3, 0)
    table_formula(editor, "AVERAGE")
    assert _cell_text(table, 3, 0) == "4"


def test_table_to_text(editor):
    table = insert_table(editor, 2, 2)
    table.cellAt(0, 0).firstCursorPosition().insertText("a")
    table.cellAt(0, 1).firstCursorPosition().insertText("b")
    table.cellAt(1, 0).firstCursorPosition().insertText("c")
    table.cellAt(1, 1).firstCursorPosition().insertText("d")
    editor.setTextCursor(table.cellAt(0, 0).firstCursorPosition())
    table_to_text(editor)
    assert current_table(editor) is None
    assert "a\tb\nc\td" in editor.toPlainText()


def test_text_to_table(editor):
    editor.setPlainText("a\tb\nc\td")
    editor.selectAll()
    text_to_table(editor, "\t")
    table = current_table(editor)
    assert table is not None
    assert table.rows() == 2
    assert table.columns() == 2
    assert _cell_text(table, 1, 1) == "d"


def test_autofit_sets_width_constraints(editor):
    table = insert_table(editor, 2, 4)
    autofit(editor)
    constraints = table.format().columnWidthConstraints()
    assert len(constraints) == 4

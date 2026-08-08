"""Operaciones sobre tablas del documento."""

from __future__ import annotations

from PySide6.QtGui import (
    QBrush,
    QColor,
    QTextBlockFormat,
    QTextCharFormat,
    QTextFrameFormat,
    QTextTable,
)
from PySide6.QtWidgets import QTextEdit

TABLE_STYLES = {
    "Básica": (QTextFrameFormat.BorderStyle.BorderStyle_Solid, "#000000"),
    "Simple": (QTextFrameFormat.BorderStyle.BorderStyle_Solid, "#d0d0d0"),
    "Grid claro": (QTextFrameFormat.BorderStyle.BorderStyle_Dashed, "#999999"),
}


def current_table(editor: QTextEdit) -> QTextTable | None:
    """La tabla que contiene el cursor, o None."""
    cursor = editor.textCursor()
    table = cursor.currentTable()
    if table is not None:
        return table
    frame = cursor.currentFrame()
    while frame is not None and not isinstance(frame, QTextTable):
        frame = frame.parentFrame()
    return frame if isinstance(frame, QTextTable) else None


def insert_table(
    editor: QTextEdit,
    rows: int,
    columns: int,
    style_name: str = "Básica",
) -> QTextTable:
    """Inserta una tabla en la posición del cursor."""
    cursor = editor.textCursor()
    table_format = _make_table_format(style_name)
    table = cursor.insertTable(rows, columns, table_format)
    editor.setTextCursor(table.cellAt(0, 0).firstCursorPosition())
    return table


def _make_table_format(style_name: str):
    from PySide6.QtGui import QTextTableFormat

    table_format = QTextTableFormat()
    style, color = TABLE_STYLES.get(style_name, TABLE_STYLES["Básica"])
    table_format.setBorderStyle(style)
    table_format.setBorderBrush(QBrush(QColor(color)))
    table_format.setBorder(1)
    table_format.setCellPadding(4)
    table_format.setCellSpacing(0)
    return table_format


def _cell_position(editor: QTextEdit) -> tuple[int, int] | None:
    table = current_table(editor)
    if table is None:
        return None
    cell = table.cellAt(editor.textCursor())
    return cell.row(), cell.column()


def _move_cursor_to(editor: QTextEdit, table: QTextTable, row: int, col: int) -> None:
    cell = table.cellAt(row, col)
    if cell.isValid():
        editor.setTextCursor(cell.firstCursorPosition())


def add_row_before(editor: QTextEdit) -> None:
    table = current_table(editor)
    position = _cell_position(editor)
    if table is None or position is None:
        return
    row, col = position
    table.insertRows(row, 1)
    _move_cursor_to(editor, table, row, col)


def add_row_after(editor: QTextEdit) -> None:
    table = current_table(editor)
    position = _cell_position(editor)
    if table is None or position is None:
        return
    row, col = position
    table.insertRows(row + 1, 1)
    _move_cursor_to(editor, table, row + 1, col)


def add_column_before(editor: QTextEdit) -> None:
    table = current_table(editor)
    position = _cell_position(editor)
    if table is None or position is None:
        return
    row, col = position
    table.insertColumns(col, 1)
    _move_cursor_to(editor, table, row, col)


def add_column_after(editor: QTextEdit) -> None:
    table = current_table(editor)
    position = _cell_position(editor)
    if table is None or position is None:
        return
    row, col = position
    table.insertColumns(col + 1, 1)
    _move_cursor_to(editor, table, row, col + 1)


def delete_row(editor: QTextEdit) -> None:
    table = current_table(editor)
    position = _cell_position(editor)
    if table is None or position is None or table.rows() == 1:
        return
    row, _ = position
    table.removeRows(row, 1)


def delete_column(editor: QTextEdit) -> None:
    table = current_table(editor)
    position = _cell_position(editor)
    if table is None or position is None or table.columns() == 1:
        return
    _, col = position
    table.removeColumns(col, 1)


def delete_table(editor: QTextEdit) -> None:
    table = current_table(editor)
    if table is None:
        return
    cursor = editor.textCursor()
    cursor.beginEditBlock()
    cursor.setPosition(table.firstPosition())
    cursor.setPosition(table.lastPosition() + 1, cursor.MoveMode.KeepAnchor)
    cursor.removeSelectedText()
    cursor.endEditBlock()
    editor.setTextCursor(cursor)


def merge_cells(editor: QTextEdit) -> None:
    table = current_table(editor)
    cursor = editor.textCursor()
    if table is None or not cursor.hasSelection():
        return
    first = table.cellAt(cursor.selectionStart())
    last = table.cellAt(cursor.selectionEnd())
    if not first.isValid() or not last.isValid():
        return
    rows = abs(last.row() - first.row()) + 1
    columns = abs(last.column() - first.column()) + 1
    table.mergeCells(first.row(), first.column(), rows, columns)


def split_cell(editor: QTextEdit, rows: int = 2, columns: int = 1) -> None:
    table = current_table(editor)
    position = _cell_position(editor)
    if table is None or position is None:
        return
    row, col = position
    cell = table.cellAt(row, col)
    if cell.rowSpan() > 1 or cell.columnSpan() > 1:
        table.splitCell(row, col, rows, columns)
    else:
        if columns > 1:
            table.insertColumns(col, columns - 1)
        if rows > 1:
            table.insertRows(row, rows - 1)


def split_table(editor: QTextEdit) -> None:
    table = current_table(editor)
    position = _cell_position(editor)
    if table is None or position is None:
        return
    row, _ = position
    cursor = editor.textCursor()
    cursor.setPosition(table.lastPosition())
    cursor.insertBlock()
    cursor.setPosition(table.cellAt(row, 0).firstPosition())


def select_row(editor: QTextEdit) -> None:
    table = current_table(editor)
    position = _cell_position(editor)
    if table is None or position is None:
        return
    row, _ = position
    _select_cells(editor, table, row, 0, 1, table.columns())


def select_column(editor: QTextEdit) -> None:
    table = current_table(editor)
    position = _cell_position(editor)
    if table is None or position is None:
        return
    _, col = position
    _select_cells(editor, table, 0, col, table.rows(), 1)


def select_table(editor: QTextEdit) -> None:
    table = current_table(editor)
    if table is None:
        return
    _select_cells(editor, table, 0, 0, table.rows(), table.columns())


def _select_cells(editor, table, row, col, rows, cols) -> None:
    cursor = editor.textCursor()
    cursor.setPosition(table.cellAt(row, col).firstPosition())
    cursor.setPosition(
        table.cellAt(row + rows - 1, col + cols - 1).lastPosition(),
        cursor.MoveMode.KeepAnchor,
    )
    editor.setTextCursor(cursor)


def autofit(editor: QTextEdit) -> None:
    """Ajusta las columnas para que tengan anchos proporcionales iguales."""
    table = current_table(editor)
    if table is None or table.columns() == 0:
        return
    from PySide6.QtGui import QTextLength

    width = editor.document().textWidth() / table.columns()
    table_format = table.format()
    constraints = [
        QTextLength(QTextLength.Type.FixedLength, width)
        for _ in range(table.columns())
    ]
    table_format.setColumnWidthConstraints(constraints)
    table.setFormat(table_format)


def set_column_width_equal(editor: QTextEdit) -> None:
    autofit(editor)


def set_row_height_equal(editor: QTextEdit) -> None:
    table = current_table(editor)
    if table is None:
        return
    block_fmt = QTextBlockFormat()
    block_fmt.setLineHeight(20.0, QTextBlockFormat.LineHeightTypes.FixedHeight.value)
    for row in range(table.rows()):
        for col in range(table.columns()):
            cell = table.cellAt(row, col)
            cell_cursor = cell.firstCursorPosition()
            cell_cursor.mergeBlockFormat(block_fmt)


def set_cell_shading(editor: QTextEdit, color: QColor) -> None:
    cursor = editor.textCursor()
    fmt = QTextCharFormat()
    fmt.setBackground(QBrush(color))
    block_fmt = QTextBlockFormat()
    block_fmt.setBackground(QBrush(color))
    if cursor.hasSelection():
        cursor.mergeCharFormat(fmt)
    cursor.mergeBlockFormat(block_fmt)
    editor.mergeCurrentCharFormat(fmt)


def set_table_style(editor: QTextEdit, style_name: str) -> None:
    table = current_table(editor)
    if table is None:
        return
    style, color = TABLE_STYLES.get(style_name, TABLE_STYLES["Básica"])
    table_format = table.format()
    table_format.setBorderStyle(style)
    table_format.setBorderBrush(QBrush(QColor(color)))
    table.setFormat(table_format)


def set_table_border(editor: QTextEdit, color: QColor, width: float) -> None:
    table = current_table(editor)
    if table is None:
        return
    table_format = table.format()
    table_format.setBorder(width)
    table_format.setBorderBrush(QBrush(color))
    table.setFormat(table_format)


def set_heading_row_repeat(editor: QTextEdit, enabled: bool) -> None:
    """Marca la primera fila como encabezado repetido al paginar."""
    table = current_table(editor)
    if table is None or table.rows() == 0:
        return
    table_format = table.format()
    table_format.setHeaderRowCount(1 if enabled else 0)
    table.setFormat(table_format)


def sort_table(editor: QTextEdit, column: int, ascending: bool) -> None:
    """Ordena las filas de la tabla por los valores de una columna."""
    table = current_table(editor)
    if table is None:
        return
    data = [
        [
            table.cellAt(row, col).firstCursorPosition().block().text()
            for col in range(table.columns())
        ]
        for row in range(table.rows())
    ]

    def key(values: list[str]):
        value = values[column].strip()
        try:
            return (0, float(value))
        except ValueError:
            return (1, value)

    data.sort(key=key, reverse=not ascending)
    for row, values in enumerate(data):
        for col in range(table.columns()):
            _set_cell_text(table, row, col, values[col])


def _set_cell_text(table: QTextTable, row: int, col: int, text: str) -> None:
    from PySide6.QtGui import QTextCursor

    block = table.cellAt(row, col).firstCursorPosition().block()
    cursor = QTextCursor(block)
    cursor.movePosition(
        cursor.MoveOperation.EndOfBlock, cursor.MoveMode.KeepAnchor
    )
    cursor.removeSelectedText()
    cursor.insertText(text)


def sort_current_column(editor: QTextEdit, ascending: bool) -> None:
    """Ordena la tabla por la columna que contiene el cursor."""
    position = _cell_position(editor)
    if position is None:
        return
    sort_table(editor, position[1], ascending)


def table_formula(editor: QTextEdit, function: str) -> None:
    """Calcula una fórmula sobre la columna actual e inserta el resultado."""
    table = current_table(editor)
    position = _cell_position(editor)
    if table is None or position is None:
        return
    row, col = position
    numbers: list[float] = []
    for r in range(table.rows()):
        if r == row:
            continue
        text = table.cellAt(r, col).firstCursorPosition().block().text().strip()
        try:
            numbers.append(float(text.replace(",", ".")))
        except ValueError:
            continue
    if not numbers:
        return
    if function == "SUM":
        result = sum(numbers)
    elif function == "AVERAGE":
        result = sum(numbers) / len(numbers)
    elif function == "COUNT":
        result = len(numbers)
    else:
        return
    _set_cell_text(table, row, col, f"{result:g}")


def table_to_text(editor: QTextEdit) -> None:
    """Convierte la tabla actual en texto con separadores tabuladores."""
    table = current_table(editor)
    if table is None:
        return
    lines = []
    for row in range(table.rows()):
        values = [
            table.cellAt(row, col).firstCursorPosition().block().text()
            for col in range(table.columns())
        ]
        lines.append("\t".join(values))
    cursor = editor.textCursor()
    cursor.setPosition(table.firstPosition())
    editor.setTextCursor(cursor)
    delete_table(editor)
    editor.insertPlainText("\n".join(lines))


def text_to_table(editor: QTextEdit, delimiter: str = "\t") -> None:
    """Convierte el texto seleccionado en una tabla."""
    cursor = editor.textCursor()
    if not cursor.hasSelection():
        return
    text = cursor.selectedText().replace("\u2029", "\n")
    lines = text.split("\n")
    rows = []
    max_cols = 0
    for line in lines:
        cells = line.split(delimiter)
        max_cols = max(max_cols, len(cells))
        rows.append(cells)
    if not rows:
        return
    table = cursor.insertTable(len(rows), max_cols)
    for r, cells in enumerate(rows):
        for c, cell_text in enumerate(cells):
            table.cellAt(r, c).firstCursorPosition().insertText(cell_text)
    editor.setTextCursor(table.cellAt(0, 0).firstCursorPosition())

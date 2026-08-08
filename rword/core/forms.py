"""Campos de formulario interactivos."""

from __future__ import annotations

from PySide6.QtGui import QColor, QTextCharFormat, QTextCursor
from PySide6.QtWidgets import QTextEdit

FORM_PREFIX = "rword:form:"
FORM_CHECKBOX = "rword:form:checkbox"
FORM_RADIO = "rword:form:radio"
FORM_DROPDOWN = "rword:form:dropdown"
FORM_DATE = "rword:form:date"
FORM_TEXT = "rword:form:text"
FORM_NUMBER = "rword:form:number"
FORM_HIDDEN = "rword:form:hidden"

CHECKED = "☑"
UNCHECKED = "☐"
RADIO_ON = "◉"
RADIO_OFF = "○"
DROPDOWN_DEFAULT = "▼ Elija una opción..."
DATE_DEFAULT = "DD/MM/AAAA"
TEXT_DEFAULT = "Haga clic para escribir…"
NUMBER_DEFAULT = "0"

ORIGINAL_KEY = "rword:form:original"


def _field_format(*names: str) -> QTextCharFormat:
    fmt = QTextCharFormat()
    fmt.setAnchorNames(list(names))
    return fmt


def _names_at(editor: QTextEdit, position: int) -> set[str]:
    limit = editor.document().characterCount() - 1
    if position < 0 or position >= limit:
        return set()
    cursor = QTextCursor(editor.document())
    cursor.setPosition(position + 1)
    return {
        name
        for name in cursor.charFormat().anchorNames()
        if name.startswith(FORM_PREFIX)
    }


def field_at(editor: QTextEdit, position: int) -> str | None:
    """Devuelve el tipo de campo en la posición dada, o None."""
    names = _names_at(editor, position)
    return next(iter(names)) if names else None


def _field_run(editor: QTextEdit, position: int):
    """Devuelve (inicio, fin, nombres) del campo en la posición."""
    names = _names_at(editor, position)
    if not names:
        return None
    limit = editor.document().characterCount() - 1
    start = position
    while start > 0 and _names_at(editor, start - 1) == names:
        start -= 1
    end = position
    while end < limit - 1 and _names_at(editor, end + 1) == names:
        end += 1
    return start, end + 1, names


def _replace_field(editor: QTextEdit, position: int, text: str, name: str) -> None:
    run = _field_run(editor, position)
    if run is None:
        return
    start, end, _ = run
    cursor = editor.textCursor()
    cursor.setPosition(start)
    cursor.setPosition(end, cursor.MoveMode.KeepAnchor)
    cursor.insertText(text, _field_format(name))
    editor.setTextCursor(cursor)


def insert_checkbox(editor: QTextEdit) -> None:
    editor.textCursor().insertText(UNCHECKED, _field_format(FORM_CHECKBOX))


def insert_radio(editor: QTextEdit) -> None:
    editor.textCursor().insertText(RADIO_OFF, _field_format(FORM_RADIO))


def insert_dropdown(editor: QTextEdit, options: list[str]) -> None:
    from PySide6.QtWidgets import QInputDialog

    if not options:
        return
    choice, ok = QInputDialog.getItem(
        editor, "Campo desplegable", "Opciones:", options, 0, False
    )
    if ok:
        name = f"{FORM_DROPDOWN}:{'|'.join(options)}"
        editor.textCursor().insertText(
            f"▼ {choice}", _field_format(name)
        )


def insert_date_field(editor: QTextEdit) -> None:
    editor.textCursor().insertText(DATE_DEFAULT, _field_format(FORM_DATE))


def insert_text_field(editor: QTextEdit) -> None:
    editor.textCursor().insertText(TEXT_DEFAULT, _field_format(FORM_TEXT))


def insert_number_field(editor: QTextEdit) -> None:
    editor.textCursor().insertText(NUMBER_DEFAULT, _field_format(FORM_NUMBER))


def insert_hidden_field(editor: QTextEdit, value: str = "") -> None:
    fmt = _field_format(FORM_HIDDEN)
    fmt.setForeground(QColor(0, 0, 0, 0))
    editor.textCursor().insertText(value or "\u200b", fmt)


def handle_field_click(editor: QTextEdit, position: int) -> bool:
    """Procesa un clic sobre un campo de formulario."""
    field = field_at(editor, position)
    if field is None:
        return False
    from PySide6.QtWidgets import QInputDialog

    if field == FORM_CHECKBOX:
        run = _field_run(editor, position)
        text = editor.document().toPlainText()[run[0]] if run else ""
        _replace_field(editor, position, CHECKED if text == UNCHECKED else UNCHECKED, field)
        return True
    if field == FORM_RADIO:
        run = _field_run(editor, position)
        text = editor.document().toPlainText()[run[0]] if run else ""
        _replace_field(editor, position, RADIO_ON if text == RADIO_OFF else RADIO_OFF, field)
        return True
    if field == FORM_DATE:
        date, ok = QInputDialog.getText(
            editor, "Campo de fecha", "Fecha (DD/MM/AAAA):", text=DATE_DEFAULT
        )
        if ok and date:
            _replace_field(editor, position, date, field)
        return True
    if field == FORM_TEXT:
        value, ok = QInputDialog.getText(editor, "Campo de texto", "Valor:")
        if ok:
            _replace_field(editor, position, value or TEXT_DEFAULT, field)
        return True
    if field == FORM_NUMBER:
        value, ok = QInputDialog.getDouble(editor, "Campo numérico", "Valor:")
        if ok:
            _replace_field(editor, position, str(value), field)
        return True
    if field.startswith(FORM_DROPDOWN):
        options = field.split(":", 1)[1].split("|")
        choice, ok = QInputDialog.getItem(editor, "Campo desplegable", "Elija:", options, 0, False)
        if ok:
            _replace_field(editor, position, f"▼ {choice}", field)
        return True
    return False


def protect_form(editor: QTextEdit, enabled: bool) -> None:
    """Activa o desactiva la protección del formulario."""
    if enabled:
        editor.setReadOnly(True)
        editor.setProperty(ORIGINAL_KEY, editor.toHtml())
    else:
        editor.setReadOnly(False)


def reset_form(editor: QTextEdit) -> None:
    original = editor.property(ORIGINAL_KEY)
    if original:
        editor.setHtml(original)

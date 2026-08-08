
from rword.core import forms
from rword.core.forms import (
    CHECKED,
    DATE_DEFAULT,
    RADIO_OFF,
    RADIO_ON,
    TEXT_DEFAULT,
    UNCHECKED,
    field_at,
    handle_field_click,
    insert_checkbox,
    insert_date_field,
    insert_hidden_field,
    insert_number_field,
    insert_radio,
    insert_text_field,
    protect_form,
    reset_form,
)


def test_insert_checkbox(editor):
    insert_checkbox(editor)
    assert editor.toPlainText() == UNCHECKED
    assert field_at(editor, 0) == forms.FORM_CHECKBOX


def test_insert_radio(editor):
    insert_radio(editor)
    assert editor.toPlainText() == RADIO_OFF


def test_insert_date_field(editor):
    insert_date_field(editor)
    assert editor.toPlainText() == DATE_DEFAULT
    assert field_at(editor, 0) == forms.FORM_DATE


def test_insert_text_field(editor):
    insert_text_field(editor)
    assert editor.toPlainText() == TEXT_DEFAULT


def test_insert_number_field(editor):
    insert_number_field(editor)
    assert editor.toPlainText() == "0"
    assert field_at(editor, 0) == forms.FORM_NUMBER


def test_insert_hidden_field(editor):
    insert_hidden_field(editor)
    assert field_at(editor, 0) == forms.FORM_HIDDEN


def test_checkbox_toggle(editor, monkeypatch):
    insert_checkbox(editor)
    monkeypatch.setattr(
        "PySide6.QtWidgets.QInputDialog", type("X", (), {})
    )
    assert handle_field_click(editor, 0)
    assert editor.toPlainText() == CHECKED
    assert handle_field_click(editor, 0)
    assert editor.toPlainText() == UNCHECKED


def test_radio_toggle(editor):
    insert_radio(editor)
    assert handle_field_click(editor, 0)
    assert editor.toPlainText() == RADIO_ON


def test_field_at_out_of_range(editor):
    editor.insertPlainText("abc")
    assert field_at(editor, -1) is None
    assert field_at(editor, 100) is None


def test_no_field_at_plain_text(editor):
    editor.insertPlainText("texto")
    assert field_at(editor, 0) is None


def test_protect_and_reset_form(editor):
    insert_checkbox(editor)
    original = editor.toHtml()
    protect_form(editor, True)
    assert editor.isReadOnly()
    protect_form(editor, False)
    assert not editor.isReadOnly()
    reset_form(editor)
    assert editor.toHtml() == original


def test_text_field_click_updates(editor, monkeypatch):
    insert_text_field(editor)
    calls = {"value": "Juan Pérez"}

    class FakeDialog:
        @staticmethod
        def getText(*args, **kwargs):
            return calls["value"], True

    monkeypatch.setattr("PySide6.QtWidgets.QInputDialog", FakeDialog)
    assert handle_field_click(editor, 0)
    assert editor.toPlainText() == "Juan Pérez"


def test_number_field_click_updates(editor, monkeypatch):
    insert_number_field(editor)

    class FakeDialog:
        @staticmethod
        def getDouble(*args, **kwargs):
            return 42.5, True

    monkeypatch.setattr("PySide6.QtWidgets.QInputDialog", FakeDialog)
    assert handle_field_click(editor, 0)
    assert editor.toPlainText() == "42.5"


def test_main_window_insert_actions(main_window):
    main_window._insert_checkbox()
    assert forms.field_at(main_window._editor, 0) == forms.FORM_CHECKBOX
    main_window._insert_date_field()
    assert forms.field_at(main_window._editor, 1) == forms.FORM_DATE


def test_main_window_protect(main_window):
    main_window.protect_form_action.setChecked(True)
    main_window._toggle_protect_form(True)
    assert main_window._editor.isReadOnly()
    main_window._toggle_protect_form(False)
    assert not main_window._editor.isReadOnly()

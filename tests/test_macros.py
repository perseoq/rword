import pytest
from PySide6.QtCore import QSettings, Qt
from PySide6.QtGui import QKeyEvent

from rword.core.macros import (
    MacroManager,
    MacroRecorder,
    document_variables,
    remove_variable,
    set_variable,
)


def _key_event(key, text=""):
    return QKeyEvent(QKeyEvent.Type.KeyPress, key, Qt.KeyboardModifier.NoModifier, text)


@pytest.fixture
def settings(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    qsettings = QSettings()
    qsettings.clear()
    yield qsettings
    qsettings.clear()


def test_macro_recorder_text(editor):
    recorder = MacroRecorder()
    recorder.key_pressed(_key_event(Qt.Key.Key_A, "a"))
    recorder.key_pressed(_key_event(Qt.Key.Key_B, "b"))
    script = recorder.script()
    assert "insertPlainText('a')" in script
    assert "insertPlainText('b')" in script


def test_macro_recorder_backspace(editor):
    recorder = MacroRecorder()
    recorder.key_pressed(_key_event(Qt.Key.Key_Backspace))
    assert "deletePreviousChar" in recorder.script()


def test_macro_recorder_enter(editor):
    recorder = MacroRecorder()
    recorder.key_pressed(_key_event(Qt.Key.Key_Return))
    assert "\\n" in recorder.script()


def test_macro_manager_crud(settings):
    manager = MacroManager(settings)
    manager.add("Saludar", "editor.insertPlainText('Hola')")
    assert "Saludar" in manager.names()
    assert "Hola" in manager.get("Saludar")
    assert manager.delete("Saludar")
    assert not manager.delete("NoExiste")


def test_macro_manager_persists(settings):
    manager = MacroManager(settings)
    manager.add("MiMacro", "editor.insertPlainText('x')")
    manager2 = MacroManager(settings)
    assert "MiMacro" in manager2.names()


def test_macro_run(editor, settings):
    manager = MacroManager(settings)
    manager.add("Escribir", "editor.insertPlainText('texto de macro')")
    assert manager.run(editor, "Escribir")
    assert "texto de macro" in editor.toPlainText()


def test_macro_run_missing(editor, settings):
    manager = MacroManager(settings)
    assert not manager.run(editor, "NoExiste")


def test_macro_shortcuts(settings):
    manager = MacroManager(settings)
    manager.assign_shortcut("A", "Ctrl+Shift+A")
    assert manager.shortcuts() == {"A": "Ctrl+Shift+A"}
    assert manager.validate_shortcut("Ctrl+Shift+A")
    manager.assign_shortcut("A", "")
    assert "A" not in manager.shortcuts()


def test_document_variables(editor):
    assert document_variables(editor) == {}
    set_variable(editor, "nombre", "rword")
    set_variable(editor, "anio", "2026")
    variables = document_variables(editor)
    assert variables["nombre"] == "rword"
    assert remove_variable(editor, "nombre")
    assert "nombre" not in document_variables(editor)
    assert not remove_variable(editor, "no-existe")


def test_recording_through_editor(editor, settings):
    manager = MacroManager(settings)
    recorder = MacroRecorder()
    editor.set_macro_recorder(recorder)
    from PySide6.QtTest import QTest

    editor.setFocus()
    QTest.keyClicks(editor, "hola")
    QTest.keyClick(editor, Qt.Key.Key_Backspace)
    editor.set_macro_recorder(None)
    manager.add("Grabada", recorder.script())
    assert "insertPlainText" in manager.get("Grabada")
    assert "deletePreviousChar" in manager.get("Grabada")


def test_main_window_record_flow(main_window, monkeypatch):
    monkeypatch.setattr(
        "PySide6.QtWidgets.QInputDialog.getText",
        staticmethod(lambda *a, **k: ("micromacro", True)),
    )
    main_window._record_macro()
    assert main_window._macro_recorder is not None
    from PySide6.QtTest import QTest

    main_window._editor.setFocus()
    QTest.keyClicks(main_window._editor, "abc")
    main_window._stop_recording()
    assert "insertPlainText('a')" in main_window._macro_manager_instance().get(
        "micromacro"
    )

import pytest
from PySide6.QtCore import QSettings

from rword.core.margin_templates import (
    STANDARD_TEMPLATES,
    MarginTemplateStore,
    apply_margins,
    current_margins,
)


@pytest.fixture
def settings(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    qsettings = QSettings()
    qsettings.clear()
    yield qsettings
    qsettings.clear()


def test_standard_presets():
    assert "Normal" in STANDARD_TEMPLATES
    assert "Estrecho" in STANDARD_TEMPLATES
    assert "Moderado" in STANDARD_TEMPLATES
    assert "Ancho" in STANDARD_TEMPLATES
    assert "Oficina 2003" in STANDARD_TEMPLATES
    assert STANDARD_TEMPLATES["Normal"] == (25.4, 25.4, 25.4, 25.4)


def test_store_roundtrip(settings):
    store = MarginTemplateStore(settings)
    store.save("Mi plantilla", 10, 20, 30, 40)
    assert "Mi plantilla" in store.names()
    assert store.get("Mi plantilla") == (10, 20, 30, 40)
    store2 = MarginTemplateStore(settings)
    assert store2.get("Mi plantilla") == (10, 20, 30, 40)


def test_store_replace(settings):
    store = MarginTemplateStore(settings)
    store.save("A", 1, 2, 3, 4)
    store.save("A", 5, 6, 7, 8)
    assert len(store.names()) == 1
    assert store.get("A") == (5, 6, 7, 8)


def test_store_rename(settings):
    store = MarginTemplateStore(settings)
    store.save("Antiguo", 1, 2, 3, 4)
    assert store.rename("Antiguo", "Nuevo")
    assert "Nuevo" in store.names()
    assert "Antiguo" not in store.names()
    assert not store.rename("NoExiste", "X")


def test_store_delete(settings):
    store = MarginTemplateStore(settings)
    store.save("Borrar", 1, 2, 3, 4)
    assert store.delete("Borrar")
    assert "Borrar" not in store.names()
    assert not store.delete("Borrar")


def test_apply_margins(editor):
    setup = apply_margins(editor, 10, 20, 30, 40)
    assert setup.left_margin_mm == 10
    assert setup.right_margin_mm == 20
    assert setup.top_margin_mm == 30
    assert setup.bottom_margin_mm == 40
    assert current_margins(editor) == (10, 20, 30, 40)


def test_apply_standard_template(editor):
    left, right, top, bottom = STANDARD_TEMPLATES["Estrecho"]
    apply_margins(editor, left, right, top, bottom)
    assert current_margins(editor) == (12.7, 12.7, 12.7, 12.7)


def test_main_window_margins_menu(main_window):
    main_window._rebuild_margins_menu()
    actions = main_window.margins_menu.actions()
    labels = [a.text() for a in actions]
    for preset in ("Normal", "Estrecho", "Moderado", "Ancho", "Oficina 2003"):
        assert preset in labels
    assert "Administrar plantillas de márgenes..." in labels


def test_apply_margin_from_ribbon(main_window):
    main_window._apply_margin_template(10, 10, 10, 10)
    assert current_margins(main_window._editor) == (10, 10, 10, 10)


def test_columns_more(main_window, monkeypatch):
    from PySide6.QtWidgets import QInputDialog

    monkeypatch.setattr(
        QInputDialog,
        "getInt",
        staticmethod(lambda *a, **k: (2, True)),
    )
    main_window._columns_more()

    table = None
    for frame in main_window._editor.document().rootFrame().childFrames():
        from PySide6.QtGui import QTextTable

        if isinstance(frame, QTextTable):
            table = frame
    assert table is not None and table.columns() == 2

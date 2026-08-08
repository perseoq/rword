
from rword.core.pages import PageSetup, apply_page_setup
from rword.ui.ruler import Ruler


def test_editor_zoom(editor):
    editor.set_zoom(150)
    assert editor.zoom() == 150
    editor.set_zoom(75)
    assert editor.zoom() == 75


def test_editor_grid_toggle(editor):
    assert not editor.grid_visible()
    editor.set_grid_visible(True)
    assert editor.grid_visible()


def test_editor_view_mode(editor):
    from PySide6.QtWidgets import QTextEdit

    assert editor.view_mode() == "print"
    editor.set_view_mode("web")
    assert editor.view_mode() == "web"
    assert editor.lineWrapMode().value == QTextEdit.LineWrapMode.NoWrap.value
    editor.set_view_mode("print")
    assert editor.lineWrapMode().value == QTextEdit.LineWrapMode.WidgetWidth.value


def test_zoom_actions(main_window):
    main_window._set_zoom(100)
    main_window._change_zoom(20)
    assert main_window._editor.zoom() == 120
    main_window._change_zoom(-20)
    assert main_window._editor.zoom() == 100


def test_fit_to_width(main_window):
    main_window._editor.resize(800, 600)
    apply_page_setup(main_window._editor, PageSetup())
    main_window._fit_to_width()
    assert 20 <= main_window._editor.zoom() <= 500


def test_fit_page(main_window):
    main_window._editor.resize(800, 600)
    apply_page_setup(main_window._editor, PageSetup())
    main_window._fit_page()
    assert 20 <= main_window._editor.zoom() <= 500


def test_enter_read_mode(main_window):
    main_window.show()
    main_window._enter_read_mode()
    assert not main_window.ribbon.isVisible()
    main_window._enter_print_mode()
    assert main_window.ribbon.isVisible()
    main_window.close()


def test_web_mode(main_window):
    main_window._enter_web_mode()
    assert main_window._editor.view_mode() == "web"


def test_outline_mode(main_window):
    main_window._enter_outline_mode()
    assert main_window._editor.view_mode() == "outline"
    assert main_window.toggle_navigation_action.isChecked()


def test_ruler_widget(main_window):
    ruler = main_window._ruler
    assert isinstance(ruler, Ruler)
    assert ruler.height() == 24


def test_vruler_widget(main_window):
    from rword.ui.ruler import VRuler

    assert isinstance(main_window._vruler, VRuler)
    assert main_window._vruler.width() == 24


def test_toggle_ruler(main_window):
    main_window.show()
    main_window._toggle_ruler(False)
    assert not main_window._ruler.isVisible()
    assert not main_window._vruler.isVisible()
    main_window._toggle_ruler(True)
    assert main_window._ruler.isVisible()
    assert main_window._vruler.isVisible()
    main_window.close()


def test_toggle_grid(main_window):
    main_window._toggle_grid(True)
    assert main_window._editor.grid_visible()


def test_split_window(main_window):
    main_window._split_window()
    assert main_window._splitter is not None
    assert main_window._second_editor is not None
    assert main_window._second_editor.document() is main_window._editor.document()

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QToolButton

from rword.ui.ribbon import RibbonGroup


def test_ribbon_tabs(main_window):
    titles = main_window.ribbon.tab_titles()
    assert "Edición" in titles
    assert "Insertar" in titles
    assert "Diseño de página" in titles
    assert "IA" in titles


def test_ribbon_groups(main_window):
    tab = main_window.ribbon._stack.widget(0)
    titles = [g.title for g in tab._groups]
    assert "Fuente" in titles
    assert "Párrafo" in titles


def test_ribbon_group_action(main_window):
    from PySide6.QtGui import QAction

    group = RibbonGroup("Prueba")
    action = QAction("Acción", None)
    button = group.add_action(action, large=False)
    assert isinstance(button, QToolButton)
    assert button.defaultAction() is action


def test_ribbon_group_large_button(main_window):
    from PySide6.QtGui import QAction

    group = RibbonGroup("Prueba")
    action = QAction("Grande", None)
    button = group.add_action(action, large=True)
    assert button.toolButtonStyle() == Qt.ToolButtonStyle.ToolButtonTextUnderIcon


def test_chevrons_scroll_without_menu(main_window):
    main_window.resize(400, 700)
    main_window.show()
    tab = main_window.ribbon._stack.widget(0)
    tab.resizeEvent(None)
    bar = tab._scroll.horizontalScrollBar()
    if bar.maximum() > bar.minimum():
        before = bar.value()
        tab._scroll_chevron("chevrons-right")
        assert bar.value() > before
        tab._scroll_chevron("chevrons-left")
        assert bar.value() == before
    main_window.close()


def test_chevrons_hidden_when_no_overflow(main_window):
    main_window.resize(1400, 800)
    main_window.show()
    tab = main_window.ribbon._stack.widget(0)
    tab.resizeEvent(None)
    assert not tab._chevrons_widget.isVisible()
    main_window.close()


def test_set_current_tab(main_window):
    main_window.ribbon.set_current_tab(1)
    assert main_window.ribbon.current_tab_index() == 1


def test_set_group_visible(main_window):
    main_window.ribbon.set_group_visible("Edición", "Párrafo", False)
    tab = main_window.ribbon._stack.widget(0)
    for group in tab._groups:
        if group.title == "Párrafo":
            assert not group.isVisible()
    main_window.ribbon.set_group_visible("Edición", "Párrafo", True)


def test_add_ribbon_action_plugin(main_window):
    from PySide6.QtGui import QAction

    action = QAction("Complemento", None)
    main_window.add_ribbon_action(action, "Insertar", "Complementos")
    tab_index = main_window.ribbon.tab_titles().index("Insertar")
    tab = main_window.ribbon._stack.widget(tab_index)
    titles = [g.title for g in tab._groups]
    assert "Complementos" in titles


def test_toggle_toolbar_hides_ribbon(main_window):
    main_window.show()
    main_window._toggle_toolbar(False)
    assert not main_window.ribbon.isVisible()
    main_window._toggle_toolbar(True)
    assert main_window.ribbon.isVisible()
    main_window.close()

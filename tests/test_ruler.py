import pytest
from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QMouseEvent, QTextOption

from rword.core import paragraph
from rword.core.pages import apply_page_setup, current_page_setup


def _press(widget, x, y=0, button=Qt.MouseButton.LeftButton):
    event = QMouseEvent(
        QMouseEvent.Type.MouseButtonPress,
        QPointF(x, y),
        button,
        Qt.MouseButton.NoButton,
        Qt.KeyboardModifier.NoModifier,
    )
    widget.mousePressEvent(event)


def _move(widget, x, y=0):
    event = QMouseEvent(
        QMouseEvent.Type.MouseMove,
        QPointF(x, y),
        Qt.MouseButton.NoButton,
        Qt.MouseButton.NoButton,
        Qt.KeyboardModifier.NoModifier,
    )
    widget.mouseMoveEvent(event)


def test_tab_stops_roundtrip(editor):
    assert paragraph.tab_stops(editor) == []
    tabs = [
        QTextOption.Tab(200.0, QTextOption.TabType.LeftTab),
        QTextOption.Tab(400.0, QTextOption.TabType.CenterTab),
    ]
    paragraph.set_tab_stops(editor, tabs)
    stored = paragraph.tab_stops(editor)
    assert len(stored) == 2
    assert stored[0].position == 200.0
    assert stored[1].position == 400.0


def test_add_remove_tab_stop(editor):
    paragraph.add_tab_stop(editor, 150.0)
    assert len(paragraph.tab_stops(editor)) == 1
    paragraph.add_tab_stop(editor, 150.0)
    assert len(paragraph.tab_stops(editor)) == 1
    paragraph.remove_tab_stop(editor, 150.0)
    assert paragraph.tab_stops(editor) == []


def test_current_indents(editor):
    editor.insertPlainText("párrafo")
    paragraph.set_left_indent(editor, 40)
    paragraph.set_right_indent(editor, 25)
    paragraph.set_first_line_indent(editor, 30)
    indents = paragraph.current_indents(editor)
    assert indents["left"] == 40
    assert indents["right"] == 25
    assert indents["first_line"] == 30


def test_hruler_drag_first_line(main_window):
    main_window.resize(1200, 800)
    main_window.show()
    ruler = main_window._ruler
    editor = main_window._editor
    editor.insertPlainText("texto")
    apply_page_setup(editor, current_page_setup(editor))
    main_window._page_view._relayout()
    from PySide6.QtWidgets import QApplication

    QApplication.processEvents()
    page_left = ruler._page_left()
    zoom = ruler._zoom()
    ruler._drag = ("first_line", page_left + 0)
    _move(ruler, page_left + 80 * zoom)
    indents = paragraph.current_indents(editor)
    assert indents["first_line"] == pytest.approx(80, abs=3)
    main_window.close()


def test_hruler_drag_left_indent(main_window):
    main_window.resize(1200, 800)
    main_window.show()
    ruler = main_window._ruler
    editor = main_window._editor
    editor.insertPlainText("texto")
    main_window._page_view._relayout()
    from PySide6.QtWidgets import QApplication

    QApplication.processEvents()
    page_left = ruler._page_left()
    zoom = ruler._zoom()
    ruler._drag = ("left", page_left + 0)
    _move(ruler, page_left + 60 * zoom)
    indents = paragraph.current_indents(editor)
    assert indents["left"] == pytest.approx(60, abs=3)
    main_window.close()


def test_hruler_drag_right_indent(main_window):
    main_window.resize(1200, 800)
    main_window.show()
    ruler = main_window._ruler
    editor = main_window._editor
    editor.insertPlainText("texto")
    main_window._page_view._relayout()
    from PySide6.QtWidgets import QApplication

    QApplication.processEvents()
    page_left = ruler._page_left()
    page_right = page_left + ruler._page_width()
    zoom = ruler._zoom()
    ruler._drag = ("right", page_right)
    _move(ruler, page_right - 50 * zoom)
    indents = paragraph.current_indents(editor)
    assert indents["right"] == pytest.approx(50, abs=3)
    main_window.close()


def test_hruler_margin_drag_emits(main_window):
    main_window.resize(1200, 800)
    main_window.show()
    ruler = main_window._ruler
    editor = main_window._editor
    apply_page_setup(editor, current_page_setup(editor))
    main_window._page_view._relayout()
    from PySide6.QtWidgets import QApplication

    QApplication.processEvents()
    page_left = ruler._page_left()
    mm_px = ruler._mm_px()
    emitted = []

    ruler.margins_changed.connect(lambda setup: emitted.append(setup))
    ruler._drag = ("margin_l", page_left)
    _move(ruler, page_left + 40 * mm_px)
    assert emitted
    setup = emitted[-1]
    assert setup.left_margin_mm == pytest.approx(40, abs=2)
    main_window.close()


def test_hruler_double_click_adds_tab(main_window):
    main_window.resize(1200, 800)
    main_window.show()
    ruler = main_window._ruler
    editor = main_window._editor
    main_window._page_view._relayout()
    from PySide6.QtWidgets import QApplication

    QApplication.processEvents()
    page_left = ruler._page_left()
    zoom = ruler._zoom()
    event = QMouseEvent(
        QMouseEvent.Type.MouseButtonDblClick,
        QPointF(page_left + 120 * zoom, 0),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.NoButton,
        Qt.KeyboardModifier.NoModifier,
    )
    ruler.mouseDoubleClickEvent(event)
    tabs = paragraph.tab_stops(editor)
    assert len(tabs) == 1
    assert tabs[0].position == pytest.approx(120, abs=3)
    main_window.close()


def test_hruler_right_click_removes_tab(main_window):
    main_window.resize(1200, 800)
    main_window.show()
    ruler = main_window._ruler
    editor = main_window._editor
    main_window._page_view._relayout()
    from PySide6.QtWidgets import QApplication

    QApplication.processEvents()
    page_left = ruler._page_left()
    zoom = ruler._zoom()
    paragraph.add_tab_stop(editor, 100.0)
    x = page_left + 100 * zoom
    event = QMouseEvent(
        QMouseEvent.Type.MouseButtonPress,
        QPointF(x, 0),
        Qt.MouseButton.RightButton,
        Qt.MouseButton.NoButton,
        Qt.KeyboardModifier.NoModifier,
    )
    ruler.mousePressEvent(event)
    assert paragraph.tab_stops(editor) == []
    main_window.close()


def test_vruler_margin_drag(main_window):
    main_window.resize(1200, 800)
    main_window.show()
    vruler = main_window._vruler
    editor = main_window._editor
    apply_page_setup(editor, current_page_setup(editor))
    main_window._page_view._relayout()
    from PySide6.QtWidgets import QApplication

    QApplication.processEvents()
    page_top = vruler._page_top()
    mm_px = vruler._mm_px()
    emitted = []
    vruler.margins_changed.connect(lambda setup: emitted.append(setup))
    vruler._drag = ("margin_top", page_top)
    _move(vruler, 0, page_top + 30 * mm_px)
    assert emitted
    assert emitted[-1].top_margin_mm == pytest.approx(30, abs=2)
    main_window.close()


def test_vruler_scroll_tracking(main_window):
    main_window.resize(1200, 800)
    main_window.show()
    vruler = main_window._vruler
    editor = main_window._editor
    editor.setPlainText("\n".join(f"Línea {i}" for i in range(200)))
    main_window._page_view._relayout()
    from PySide6.QtWidgets import QApplication

    QApplication.processEvents()
    page_top_before = vruler._page_top()
    main_window._page_view.verticalScrollBar().setValue(300)
    QApplication.processEvents()
    assert vruler._page_top() != page_top_before
    main_window.close()


def test_hruler_paint_smoke(main_window):
    main_window.resize(1200, 800)
    main_window.show()
    main_window._ruler.repaint()
    main_window._vruler.repaint()
    main_window.close()

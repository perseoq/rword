from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QScrollArea


def test_page_view_is_scroll_area(main_window):
    assert isinstance(main_window._page_view, QScrollArea)


def test_page_view_contains_editor(main_window):
    view = main_window._page_view
    assert view._editor is main_window._editor


def test_page_view_white_paper(main_window):
    palette = main_window._editor.palette()
    assert palette.color(QPalette.ColorRole.Base).name() == "#ffffff"


def test_page_view_gray_background(main_window):
    palette = main_window._page_view.palette()
    assert palette.color(QPalette.ColorRole.Window).name() == "#909090"


def test_editor_scrollbars_hidden(main_window):
    from PySide6.QtCore import Qt

    assert (
        main_window._editor.verticalScrollBarPolicy()
        == Qt.ScrollBarPolicy.ScrollBarAlwaysOff
    )
    assert (
        main_window._editor.horizontalScrollBarPolicy()
        == Qt.ScrollBarPolicy.ScrollBarAlwaysOff
    )


def test_page_view_centers_editor(main_window):
    main_window.resize(1200, 800)
    main_window.show()
    view = main_window._page_view
    editor = main_window._editor
    view._relayout()
    assert editor.x() > 0
    assert editor.x() + editor.width() <= view.viewport().width()
    main_window.close()


def test_page_view_page_width_cap(main_window):
    view = main_window._page_view
    editor = main_window._editor
    view.resize(2000, 800)
    view._relayout()
    assert editor.width() <= view._page_width
    assert editor.x() > 0


def test_page_view_small_window(main_window):
    view = main_window._page_view
    editor = main_window._editor
    view.resize(200, 300)
    view._relayout()
    assert editor.width() >= 120


def test_sheet_grows_with_content(main_window):
    view = main_window._page_view
    editor = main_window._editor
    view.resize(1000, 700)
    view._relayout()
    editor.setPlainText("")
    view._relayout()
    short_height = editor.height()
    editor.setPlainText("\n".join(f"Línea {i}" for i in range(300)))
    view._relayout()
    assert editor.height() > short_height


def test_update_paper_color(main_window):
    main_window._page_view.update_paper_color("#f4ecd8")
    palette = main_window._editor.palette()
    assert palette.color(QPalette.ColorRole.Base).name() == "#f4ecd8"
    main_window._page_view.update_paper_color("#ffffff")


def test_set_page_size(main_window):
    view = main_window._page_view
    view.set_page_size(500, 700)
    assert view._page_width == 500
    assert view._min_sheet_height == 700
    editor = main_window._editor
    view.resize(1600, 800)
    view._relayout()
    assert editor.width() <= 500


def test_theme_updates_paper(main_window):
    main_window._apply_theme("Sepia")
    palette = main_window._editor.palette()
    assert palette.color(QPalette.ColorRole.Base).name() == "#f4ecd8"
    main_window._apply_theme("Claro")


def test_zoom_scales_page(main_window):
    view = main_window._page_view
    editor = main_window._editor
    main_window.resize(2000, 900)
    main_window.show()
    from PySide6.QtWidgets import QApplication

    QApplication.processEvents()
    main_window._set_zoom(100)
    view._relayout()
    width_100 = editor.width()
    assert width_100 > 120
    main_window._set_zoom(150)
    view._relayout()
    assert editor.width() > width_100
    main_window._set_zoom(100)
    main_window.close()


def test_split_window_uses_page_view(main_window):
    main_window._split_window()
    assert main_window._second_editor is not None
    assert main_window._second_editor.parentWidget() is not main_window._editor.parentWidget()
    parent = main_window._second_editor.parentWidget()
    inside_page = False
    while parent is not None:
        if isinstance(parent, QScrollArea):
            inside_page = True
            break
        parent = parent.parentWidget()
    assert inside_page

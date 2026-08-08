from PySide6.QtGui import QPalette


def test_page_view_contains_editor(main_window):
    view = main_window._page_view
    assert view is not None
    assert view._editor is main_window._editor
    assert main_window._editor.parentWidget() is view


def test_page_view_white_paper(main_window):
    palette = main_window._editor.palette()
    assert palette.color(QPalette.ColorRole.Base).name() == "#ffffff"


def test_page_view_gray_background(main_window):
    palette = main_window._page_view.palette()
    assert palette.color(QPalette.ColorRole.Window).name() == "#909090"


def test_page_view_centers_editor(main_window):
    main_window.resize(1200, 800)
    main_window.show()
    view = main_window._page_view
    editor = main_window._editor
    view._layout_editor()
    assert editor.x() > 0
    assert editor.x() + editor.width() <= view.width()
    assert editor.width() <= view.width() - 2 * 28
    main_window.close()


def test_page_view_page_width_cap(main_window):
    view = main_window._page_view
    editor = main_window._editor
    view.resize(2000, 800)
    view._layout_editor()
    assert editor.width() <= view._page_width
    assert editor.x() > 0


def test_page_view_small_window(main_window):
    view = main_window._page_view
    editor = main_window._editor
    view.resize(200, 300)
    view._layout_editor()
    assert editor.width() >= 120


def test_update_paper_color(main_window):
    main_window._page_view.update_paper_color("#f4ecd8")
    palette = main_window._editor.palette()
    assert palette.color(QPalette.ColorRole.Base).name() == "#f4ecd8"
    main_window._page_view.update_paper_color("#ffffff")


def test_set_page_width(main_window):
    view = main_window._page_view
    view.set_page_width(500)
    assert view._page_width == 500
    editor = main_window._editor
    view.resize(1600, 800)
    view._layout_editor()
    assert editor.width() <= 500


def test_theme_updates_paper(main_window):
    main_window._apply_theme("Sepia")
    palette = main_window._editor.palette()
    assert palette.color(QPalette.ColorRole.Base).name() == "#f4ecd8"
    main_window._apply_theme("Claro")


def test_split_window_uses_page_view(main_window):
    main_window._split_window()
    assert main_window._second_editor is not None
    assert main_window._second_editor.parentWidget() is not main_window._editor.parentWidget()

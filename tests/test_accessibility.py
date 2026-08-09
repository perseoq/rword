from rword.core.themes import default_themes


def test_high_contrast_theme_available():
    names = [theme.name for theme in default_themes()]
    assert "Alto contraste" in names


def test_high_contrast_colors():
    theme = next(t for t in default_themes() if t.name == "Alto contraste")
    assert theme.page_color == "#000000"
    assert theme.text_color == "#ffffff"


def test_main_window_high_contrast(main_window):
    main_window._apply_high_contrast()
    assert main_window._theme_manager.current.name == "Alto contraste"

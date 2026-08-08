from PySide6.QtCore import QSettings, Qt
from PySide6.QtGui import QFont, QTextCharFormat

from rword.core.styles import (
    FormatPainter,
    Style,
    StyleManager,
    apply_style,
    default_styles,
)
from rword.core.themes import Theme, ThemeManager, apply_theme


def test_default_styles_include_expected():
    names = [style.name for style in default_styles()]
    assert "Normal" in names
    assert "Título 1" in names
    assert "Título 2" in names
    assert "Título 3" in names
    assert "Cita" in names
    assert "Código" in names


def test_apply_style_sets_formatting(editor):
    editor.insertPlainText("título")
    editor.selectAll()
    style = Style(
        "Mi estilo",
        font_family="Arial",
        font_size=18,
        bold=True,
        color="#ff0000",
        alignment="center",
    )
    apply_style(editor, style)
    fmt = editor.currentCharFormat()
    assert "Arial" in fmt.fontFamilies()
    assert fmt.fontPointSize() == 18
    assert fmt.fontWeight() >= QFont.Weight.Bold
    assert fmt.foreground().color().name() == "#ff0000"
    block_fmt = editor.textCursor().block().blockFormat()
    assert block_fmt.alignment() == Qt.AlignmentFlag.AlignCenter


def test_style_manager_add_get_remove(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    settings = QSettings()
    settings.clear()
    manager = StyleManager(settings)
    manager.add(Style("Personalizado", font_size=14))
    assert "Personalizado" in manager.names()
    assert manager.get("Personalizado").font_size == 14
    assert manager.remove("Personalizado")
    assert "Personalizado" not in manager.names()
    assert not manager.remove("No existe")
    settings.clear()


def test_style_manager_persists(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    settings = QSettings()
    settings.clear()
    manager = StyleManager(settings)
    manager.add(Style("Guardado", font_size=16, bold=True))
    manager2 = StyleManager(settings)
    assert "Guardado" in manager2.names()
    assert manager2.get("Guardado").font_size == 16
    assert manager2.get("Guardado").bold
    settings.clear()


def test_style_manager_rename(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    settings = QSettings()
    settings.clear()
    manager = StyleManager(settings)
    manager.add(Style("Antiguo"))
    assert manager.rename("Antiguo", "Nuevo")
    assert "Nuevo" in manager.names()
    assert "Antiguo" not in manager.names()
    settings.clear()


def test_format_painter_captures_and_applies(editor):
    painter = FormatPainter()
    editor.insertPlainText("formato")
    editor.selectAll()
    fmt = QTextCharFormat()
    fmt.setFontWeight(QFont.Weight.Bold)
    editor.mergeCurrentCharFormat(fmt)
    painter.capture(editor)
    assert painter.active

    editor.setPlainText("destino")
    cursor = editor.textCursor()
    cursor.setPosition(0)
    cursor.setPosition(len("destino"), cursor.MoveMode.KeepAnchor)
    editor.setTextCursor(cursor)
    assert painter.apply(editor)
    assert editor.currentCharFormat().fontWeight() >= QFont.Weight.Bold
    painter.clear()
    assert not painter.active


def test_theme_manager_defaults(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    settings = QSettings()
    settings.clear()
    manager = ThemeManager(settings)
    assert "Claro" in manager.names()
    assert "Oscuro" in manager.names()
    manager.set_current("Oscuro")
    assert manager.current.name == "Oscuro"
    settings.clear()


def test_theme_persists(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    settings = QSettings()
    settings.clear()
    manager = ThemeManager(settings)
    manager.set_current("Sepia")
    manager2 = ThemeManager(settings)
    assert manager2.current.name == "Sepia"
    settings.clear()


def test_apply_theme_changes_palette(editor):
    theme = Theme("Oscuro", page_color="#1e1e1e", text_color="#d4d4d4")
    apply_theme(editor, theme)
    from PySide6.QtGui import QPalette

    assert editor.palette().color(QPalette.ColorRole.Base).name() == "#1e1e1e"


def test_main_window_style_apply(main_window):
    main_window._editor.insertPlainText("texto")
    main_window._editor.selectAll()
    main_window._style_manager.add(
        Style("Título de prueba", font_size=24, bold=True)
    )
    main_window._apply_style("Título de prueba")
    fmt = main_window._editor.currentCharFormat()
    assert fmt.fontPointSize() == 24
    assert fmt.fontWeight() >= QFont.Weight.Bold


def test_main_window_theme_apply(main_window):
    main_window._apply_theme("Oscuro")
    assert main_window._theme_manager.current.name == "Oscuro"


def test_painter_action(main_window):
    main_window._editor.insertPlainText("origen")
    main_window._editor.selectAll()
    main_window.painter_action.trigger()
    assert main_window._format_painter.active
    main_window._on_painter_cursor_move()
    assert not main_window.painter_action.isChecked()

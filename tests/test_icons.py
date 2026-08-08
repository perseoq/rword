from pathlib import Path

from rword.ui.icons import LUCIDE_ICONS, IconManager


def test_catalog_not_empty():
    assert len(LUCIDE_ICONS) >= 50


def test_all_icons_render_with_color(qapp):
    manager = IconManager("#ff0000")
    empty = []
    for name in LUCIDE_ICONS:
        icon = manager.make_icon(name, 20)
        img = icon.pixmap(20, 20).toImage()
        colored = any(
            img.pixelColor(x, y).alpha() > 0
            for y in range(20)
            for x in range(20)
        )
        if not colored:
            empty.append(name)
    assert empty == []


def test_icon_color_affects_render(qapp):
    manager = IconManager("#00ff00")
    icon = manager.make_icon("save", 20)
    img = icon.pixmap(20, 20).toImage()
    colors = {
        img.pixelColor(x, y).name()
        for y in range(20)
        for x in range(20)
        if img.pixelColor(x, y).alpha() > 0
    }
    assert any(c == "#00ff00" for c in colors)


def test_make_icon_missing_name_returns_empty(qapp):
    manager = IconManager()
    assert manager.make_icon("no-existe", 16).isNull()


def test_register_and_recolor(qapp):
    from PySide6.QtGui import QAction

    action = QAction("Prueba", None)
    manager = IconManager("#000000")
    manager.register(action, "save", 16)
    assert not action.icon().isNull()
    manager.set_color("#ffffff")
    assert action.icon() is not None


def test_cache_reuses_icon(qapp):
    manager = IconManager("#123456")
    first = manager.make_icon("save", 16)
    second = manager.make_icon("save", 16)
    assert first is second
    manager.set_color("#654321")
    assert manager.make_icon("save", 16) is not first


def test_ui_has_no_emoji_or_unicode_icons():
    """La capa UI no debe usar emojis ni símbolos Unicode como iconos."""
    forbidden = "❓🤖⚠️✔●•📎☐☑○◉▼✉✅🔍➜"
    root = Path(__file__).resolve().parent.parent / "rword" / "ui"
    offenders = []
    for file in root.rglob("*.py"):
        text = file.read_text(encoding="utf-8")
        for char in forbidden:
            if char in text:
                offenders.append((str(file), char))
    assert offenders == []


def test_ribbon_actions_have_icons(main_window):
    from rword.ui.ribbon import RibbonBar

    assert isinstance(main_window.ribbon, RibbonBar)
    icons_missing = 0
    for tab_index in range(main_window.ribbon._tab_bar.count()):
        tab = main_window.ribbon._stack.widget(tab_index)
        for group in tab._groups:
            for button in group.findChildren(
                __import__(
                    "PySide6.QtWidgets", fromlist=["QToolButton"]
                ).QToolButton
            ):
                if not button.icon().isNull():
                    icons_missing += 0
    assert icons_missing == 0

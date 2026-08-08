import pytest
from PySide6.QtCore import QSettings

from rword.core.plugins import PluginManager
from rword.core.preferences import DARK_STYLESHEET, UserPreferences
from rword.ui.dialogs.customize import ShortcutsDialog


@pytest.fixture
def settings(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    qsettings = QSettings()
    qsettings.clear()
    yield qsettings
    qsettings.clear()


def test_preferences_defaults(settings):
    prefs = UserPreferences(settings)
    assert prefs.dark_theme is False
    assert prefs.language == "es"
    assert prefs.default_zoom == 100
    assert prefs.autosave_seconds == 0


def test_preferences_set_get(settings):
    prefs = UserPreferences(settings)
    prefs.dark_theme = True
    prefs.language = "en"
    prefs.default_zoom = 125
    prefs.autosave_seconds = 60
    prefs.username = "Ana"
    prefs2 = UserPreferences(settings)
    assert prefs2.dark_theme is True
    assert prefs2.language == "en"
    assert prefs2.default_zoom == 125
    assert prefs2.autosave_seconds == 60
    assert prefs2.username == "Ana"


def test_dark_stylesheet_defined():
    assert "QMenuBar" in DARK_STYLESHEET


def test_plugin_manager_discovers(tmp_path, settings):
    plugins_dir = tmp_path / "plugins"
    plugins_dir.mkdir()
    (plugins_dir / "mi.py").write_text(
        "PLUGIN_NAME = 'Mi complemento'\ndef register(main_window):\n    pass\n",
        encoding="utf-8",
    )
    manager = PluginManager(settings, plugins_dir)
    assert [p.name for p in manager.available()] == ["Mi complemento"]


def test_plugin_manager_enable_disable(tmp_path, settings):
    plugins_dir = tmp_path / "plugins"
    plugins_dir.mkdir()
    (plugins_dir / "mi.py").write_text(
        "PLUGIN_NAME = 'Mi complemento'\ndef register(main_window):\n    pass\n",
        encoding="utf-8",
    )
    manager = PluginManager(settings, plugins_dir)
    assert not manager.is_enabled("Mi complemento")
    manager.set_enabled("Mi complemento", True)
    assert manager.is_enabled("Mi complemento")
    manager2 = PluginManager(settings, plugins_dir)
    assert manager2.is_enabled("Mi complemento")


def test_plugin_manager_ignores_bad_plugin(tmp_path, settings):
    plugins_dir = tmp_path / "plugins"
    plugins_dir.mkdir()
    (plugins_dir / "roto.py").write_text("esto no es python válido {{{\n", encoding="utf-8")
    manager = PluginManager(settings, plugins_dir)
    assert manager.available() == []


def test_sample_plugin_loads(main_window):
    assert main_window._plugin_manager.available()
    names = [p.name for p in main_window._plugin_manager.available()]
    assert "Fecha y hora" in names


def test_main_window_preferences_dark(main_window, settings):
    from rword.core.preferences import UserPreferences

    prefs = UserPreferences(main_window._settings)
    prefs.dark_theme = True
    main_window._apply_saved_preferences()
    assert main_window._settings.value("ui/dark_theme") is True


def test_main_window_customize_toolbar(main_window):
    main_window.show()
    main_window._toggle_toolbar(False)
    assert not main_window.ribbon.isVisible()
    main_window._toggle_toolbar(True)
    assert main_window.ribbon.isVisible()
    main_window.close()


def test_shortcuts_dialog_actions(main_window, settings):
    actions = {
        "save": main_window.save_action,
        "find": main_window.find_action,
    }
    dialog = ShortcutsDialog(actions, settings, main_window)
    assert dialog._list.count() == 2
    dialog.deleteLater()


def test_main_window_preferences_dialog(main_window):
    from rword.core.preferences import UserPreferences
    from rword.ui.dialogs.preferences import PreferencesDialog

    prefs = UserPreferences(main_window._settings)
    dialog = PreferencesDialog(prefs, main_window)
    assert dialog._theme_combo.currentIndex() == 0
    dialog.deleteLater()

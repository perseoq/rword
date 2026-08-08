import pytest
from PySide6.QtCore import QSettings

from rword.core.collaboration import CollaborationManager


@pytest.fixture
def settings(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    qsettings = QSettings()
    qsettings.clear()
    yield qsettings
    qsettings.clear()


def test_username_default(editor, settings):
    manager = CollaborationManager(editor, settings)
    assert manager.username == "Usuario"


def test_set_username(editor, settings):
    manager = CollaborationManager(editor, settings)
    manager.set_username("Ana")
    assert CollaborationManager(editor, settings).username == "Ana"


def test_log_activity(editor, settings):
    manager = CollaborationManager(editor, settings)
    manager.log("Documento abierto", "informe.txt")
    manager.log("Guardado")
    activity = manager.activity()
    assert len(activity) == 2
    assert activity[0]["event"] == "Documento abierto"
    assert activity[0]["detail"] == "informe.txt"
    assert activity[0]["user"] == "Usuario"


def test_permissions(editor, settings):
    manager = CollaborationManager(editor, settings)
    assert manager.permission("Ana") == "write"
    manager.set_permission("Ana", "read")
    assert manager.permission("Ana") == "read"


def test_apply_permissions_read_only(editor, settings):
    manager = CollaborationManager(editor, settings)
    manager.set_username("Invitado")
    manager.set_permission("Invitado", "read")
    manager.apply_permissions()
    assert editor.isReadOnly()


def test_apply_permissions_write(editor, settings):
    manager = CollaborationManager(editor, settings)
    manager.set_username("Editor")
    manager.set_permission("Editor", "write")
    manager.apply_permissions()
    assert not editor.isReadOnly()


def test_track_authors(editor, settings):
    manager = CollaborationManager(editor, settings)
    assert manager.track_authors()
    manager.set_track_authors(False)
    assert not CollaborationManager(editor, settings).track_authors()


def test_share_link(editor, settings):
    manager = CollaborationManager(editor, settings)
    assert "compartido" in manager.share_link()


def test_share_link_with_path(editor, settings, tmp_path):
    editor.set_file_path(tmp_path / "doc.txt")
    manager = CollaborationManager(editor, settings)
    link = manager.share_link()
    assert link.startswith("file://")


def test_share_mailto(editor, settings):
    manager = CollaborationManager(editor, settings)
    url = manager.share_mailto("Asunto", "Cuerpo del mensaje")
    assert url.startswith("mailto:")
    assert "Asunto" in url


def test_activity_capped(editor, settings):
    manager = CollaborationManager(editor, settings)
    for i in range(250):
        manager.log("Evento", str(i))
    assert len(manager.activity()) <= 200


def test_main_window_presence(main_window):
    assert hasattr(main_window, "_presence_label")
    assert main_window._presence_label.text().startswith("●")


def test_main_window_log_on_new(main_window):
    main_window._new_document()
    assert len(main_window._collaboration_manager().activity()) >= 1


def test_main_window_track_authors(main_window):
    main_window.track_authors_action.setChecked(False)
    main_window._toggle_track_authors(False)
    assert not main_window._collaboration_manager().track_authors()

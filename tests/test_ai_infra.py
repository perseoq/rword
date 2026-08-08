import pytest
from PySide6.QtCore import QSettings

from rword.core.ai import AiError, DeepSeekClient
from rword.core.ai.config import DEFAULT_MODEL, ApiKeyManager
from rword.core.ai.session import ChatSession, build_messages, document_context


@pytest.fixture
def settings(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    qsettings = QSettings()
    qsettings.clear()
    yield qsettings
    qsettings.clear()


def test_api_key_manager(settings):
    manager = ApiKeyManager(settings)
    assert not manager.has_key()
    manager.set("sk-clave")
    assert manager.has_key()
    assert manager.get() == "sk-clave"
    assert ApiKeyManager(settings).get() == "sk-clave"
    manager.clear()
    assert not manager.has_key()


def test_client_requires_key():
    client = DeepSeekClient("")
    assert not client.configured
    with pytest.raises(AiError):
        client.chat([{"role": "user", "content": "hola"}])


def test_client_configured():
    client = DeepSeekClient("sk-test")
    assert client.configured


def test_chat_session_history():
    session = ChatSession("sistema")
    session.add("user", "pregunta")
    session.add("assistant", "respuesta")
    history = session.history()
    assert history[0] == {"role": "system", "content": "sistema"}
    assert history[-1] == {"role": "assistant", "content": "respuesta"}


def test_chat_session_reset():
    session = ChatSession("sistema")
    session.add("user", "x")
    session.reset("nuevo")
    assert session.is_empty
    assert session.history()[0]["content"] == "nuevo"


def test_document_context_selection(editor):
    editor.setPlainText("texto completo del documento")
    cursor = editor.textCursor()
    cursor.setPosition(0)
    cursor.setPosition(5, cursor.MoveMode.KeepAnchor)
    editor.setTextCursor(cursor)
    assert document_context(editor) == "texto"


def test_document_context_full(editor):
    editor.setPlainText("contenido total")
    assert document_context(editor) == "contenido total"


def test_build_messages_with_context():
    messages = build_messages("resume", "un documento")
    assert len(messages) == 2
    assert messages[1]["content"].startswith("Documento:")


def test_build_messages_without_context():
    messages = build_messages("hola")
    assert len(messages) == 1


def test_ai_error_message():
    error = AiError("fallo de red")
    assert str(error) == "fallo de red"


def test_main_window_api_key(main_window):
    from rword.ui.dialogs.api_key import ApiKeyDialog

    from rword.core.ai.config import ApiKeyManager

    dialog = ApiKeyDialog(ApiKeyManager(main_window._settings), main_window)
    assert dialog.windowTitle() == "Clave de API de DeepSeek"
    dialog.deleteLater()


def test_default_model():
    assert DEFAULT_MODEL == "deepseek-chat"


def test_ai_client_not_configured(main_window):
    client = main_window._ai_client()
    assert not client.configured

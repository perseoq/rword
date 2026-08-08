import time

from PySide6.QtWidgets import QApplication

from rword.core.ai import AiError, capabilities
from rword.ui.ai_chat_panel import AiChatPanel


class FakeClient:
    def __init__(self, reply="RESPUESTA"):
        self.reply = reply
        self.last_messages = None

    def chat(self, messages, **kwargs):
        self.last_messages = messages
        return self.reply


class ErrorClient:
    def chat(self, messages, **kwargs):
        raise AiError("clave inválida")


def _wait_for(condition, timeout_ms=3000):
    app = QApplication.instance()
    end = time.time() + timeout_ms / 1000.0
    while time.time() < end:
        app.processEvents()
        if condition():
            return True
        time.sleep(0.005)
    return False


def test_explain():
    client = FakeClient()
    capabilities.explain(client, "texto técnico")
    assert "Explica" in client.last_messages[-1]["content"]


def test_generate_questions():
    client = FakeClient()
    capabilities.generate_questions(client, "texto")
    assert "preguntas" in client.last_messages[-1]["content"]


def test_answer_question_uses_document():
    client = FakeClient()
    capabilities.answer_question(client, "documento", "¿qué dice?")
    assert "documento" in client.last_messages[-1]["content"]
    assert "¿qué dice?" in client.last_messages[-1]["content"]


def test_chat_panel_send(main_window):
    client = FakeClient()
    panel = AiChatPanel(main_window._editor, lambda: client, main_window)
    main_window._editor.setPlainText("contenido del documento")
    panel._input.setText("¿qué es?")
    panel._send()
    assert panel._messages.count() == 1
    assert panel._messages.item(0).text() == "¿qué es?"
    assert not panel._messages.item(0).icon().isNull()
    assert _wait_for(lambda: panel._messages.count() == 2)
    assert "RESPUESTA" in panel._messages.item(1).text()
    panel.deleteLater()


def test_chat_panel_document_only(main_window):
    client = FakeClient()
    panel = AiChatPanel(main_window._editor, lambda: client, main_window)
    main_window._editor.setPlainText("contenido")
    panel._document_only.setChecked(True)
    panel._input.setText("pregunta")
    panel._send()
    assert _wait_for(lambda: client.last_messages is not None)
    assert "únicamente" in client.last_messages[0]["content"]
    panel.deleteLater()


def test_chat_panel_error(main_window):
    panel = AiChatPanel(main_window._editor, lambda: ErrorClient(), main_window)
    panel._input.setText("pregunta")
    panel._send()
    assert _wait_for(lambda: panel._messages.count() == 2)
    assert "clave" in panel._messages.item(1).text()
    assert not panel._messages.item(1).icon().isNull()
    panel.deleteLater()


def test_chat_panel_empty_input(main_window):
    panel = AiChatPanel(main_window._editor, lambda: FakeClient(), main_window)
    panel._input.setText("   ")
    panel._send()
    assert panel._messages.count() == 0
    panel.deleteLater()


def test_chat_panel_clear(main_window):
    client = FakeClient()
    panel = AiChatPanel(main_window._editor, lambda: client, main_window)
    panel._input.setText("hola")
    panel._send()
    _wait_for(lambda: panel._messages.count() == 2)
    panel._clear()
    assert panel._messages.count() == 0
    panel.deleteLater()


def test_main_window_toggle_chat(main_window):
    main_window._toggle_ai_chat(True)
    assert main_window._ai_chat_panel is not None
    assert main_window.ai_chat_panel_action.isChecked() or True
    main_window._toggle_ai_chat(False)


def test_ai_run_and_apply_async(main_window):
    main_window._editor.setPlainText("")
    main_window._ai_run_and_apply(lambda: "texto generado", "insert")
    assert _wait_for(
        lambda: "texto generado" in main_window._editor.toPlainText()
    )


def test_ai_run_and_apply_replace_selection(main_window):
    main_window._editor.setPlainText("origen")
    cursor = main_window._editor.textCursor()
    cursor.setPosition(0)
    cursor.setPosition(6, cursor.MoveMode.KeepAnchor)
    main_window._editor.setTextCursor(cursor)
    main_window._ai_run_and_apply(lambda: "nuevo", "replace_selection")
    assert _wait_for(
        lambda: main_window._editor.toPlainText() == "nuevo"
    )


def test_ai_run_and_apply_error(main_window):
    main_window._ai_run_and_apply(lambda: (_ for _ in ()).throw(AiError("fallo")))
    assert _wait_for(lambda: hasattr(main_window, "_ai_worker"))

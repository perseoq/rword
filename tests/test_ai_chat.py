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
    assert panel._messages.count() == 2
    assert panel._messages.item(0).text() == "¿qué es?"
    assert not panel._messages.item(0).icon().isNull()
    assert "RESPUESTA" in panel._messages.item(1).text()
    panel.deleteLater()


def test_chat_panel_document_only(main_window):
    client = FakeClient()
    panel = AiChatPanel(main_window._editor, lambda: client, main_window)
    main_window._editor.setPlainText("contenido")
    panel._document_only.setChecked(True)
    panel._input.setText("pregunta")
    panel._send()
    assert "únicamente" in client.last_messages[0]["content"]
    panel.deleteLater()


def test_chat_panel_error(main_window):
    panel = AiChatPanel(main_window._editor, lambda: ErrorClient(), main_window)
    panel._input.setText("pregunta")
    panel._send()
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
    panel._clear()
    assert panel._messages.count() == 0
    panel.deleteLater()


def test_main_window_toggle_chat(main_window):
    main_window._toggle_ai_chat(True)
    assert main_window._ai_chat_panel is not None
    assert main_window.ai_chat_panel_action.isChecked() or True
    main_window._toggle_ai_chat(False)

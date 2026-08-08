
from rword.core.ai import capabilities


class FakeClient:
    def __init__(self, reply="RESPUESTA"):
        self.reply = reply
        self.last_messages = None

    def chat(self, messages, **kwargs):
        self.last_messages = messages
        return self.reply


def test_redact_builds_prompt():
    client = FakeClient()
    result = capabilities.redact(client, "una carta de presentación")
    assert result == "RESPUESTA"
    content = client.last_messages[-1]["content"]
    assert "carta de presentación" in content


def test_continue_writing_uses_context():
    client = FakeClient()
    capabilities.continue_writing(client, "El proyecto comenzó")
    system = client.last_messages[0]
    assert system["role"] == "system"
    assert "proyecto comenzó" in client.last_messages[1]["content"]


def test_rewrite_uses_instruction():
    client = FakeClient()
    capabilities.rewrite(client, "texto", "hazlo más técnico")
    assert "técnico" in client.last_messages[-1]["content"]


def test_change_tone_professional():
    client = FakeClient()
    capabilities.change_tone(client, "texto", "formal")
    assert "formal" in client.last_messages[-1]["content"]


def test_summarize_prompt():
    client = FakeClient()
    capabilities.summarize(client, "texto largo")
    assert "Resume" in client.last_messages[-1]["content"]


def test_correct_low_temperature():
    client = FakeClient()
    capabilities.correct(client, "texo con errras")
    assert "Corrige" in client.last_messages[-1]["content"]


def test_all_functions_return_string():
    client = FakeClient("ok")
    functions = [
        capabilities.continue_writing,
        capabilities.complete_sentence,
        capabilities.expand,
        capabilities.reduce_text,
        capabilities.simplify,
        capabilities.make_professional,
        capabilities.make_persuasive,
        capabilities.make_friendly,
        capabilities.make_neutral,
        capabilities.detect_redundancies,
        capabilities.suggest_better_words,
        capabilities.improve_fluidity,
        capabilities.improve_clarity,
        capabilities.detect_ambiguities,
    ]
    for function in functions:
        result = function(client, "algún texto")
        assert result == "ok", function.__name__


def test_adapt_audience():
    client = FakeClient()
    capabilities.adapt_audience(client, "texto", "niños")
    assert "niños" in client.last_messages[-1]["content"]


def test_ai_menu_actions(main_window):
    assert hasattr(main_window, "ai_redact_action")
    assert hasattr(main_window, "ai_correct_action")
    assert len(main_window.ai_tones) == 4


def test_ai_redact_no_instruction(main_window, monkeypatch):
    monkeypatch.setattr(
        "PySide6.QtWidgets.QInputDialog.getText",
        staticmethod(lambda *a, **k: ("", False)),
    )
    main_window._ai_redact()


def test_ai_rewrite_uses_selection(main_window, monkeypatch):
    monkeypatch.setattr(
        "PySide6.QtWidgets.QInputDialog.getText",
        staticmethod(lambda *a, **k: ("hazlo breve", True)),
    )
    main_window._editor.setPlainText("un texto muy largo")
    cursor = main_window._editor.textCursor()
    cursor.setPosition(0)
    cursor.setPosition(9, cursor.MoveMode.KeepAnchor)
    main_window._editor.setTextCursor(cursor)
    main_window._ai_rewrite()

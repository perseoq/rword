from rword.core.ai import capabilities


class FakeClient:
    def __init__(self, reply="RESPUESTA"):
        self.reply = reply
        self.last_messages = None
        self.last_kwargs = None

    def chat(self, messages, **kwargs):
        self.last_messages = messages
        self.last_kwargs = kwargs
        return self.reply


def test_translate_uses_target_language():
    client = FakeClient()
    result = capabilities.translate(client, "hola mundo", "inglés")
    assert result == "RESPUESTA"
    assert "inglés" in client.last_messages[-1]["content"]
    assert "hola mundo" in client.last_messages[-1]["content"]


def test_detect_language_low_tokens():
    client = FakeClient()
    capabilities.detect_language(client, "bonjour le monde")
    assert client.last_kwargs.get("max_tokens") == 64
    assert client.last_kwargs.get("temperature") == 0.1


def test_main_ideas():
    client = FakeClient()
    capabilities.main_ideas(client, "texto")
    assert "ideas principales" in client.last_messages[-1]["content"]


def test_conclusions():
    client = FakeClient()
    capabilities.extract_conclusions(client, "texto")
    assert "conclusiones" in client.last_messages[-1]["content"]


def test_inconsistencies():
    client = FakeClient()
    capabilities.detect_inconsistencies(client, "texto")
    assert "inconsistencias" in client.last_messages[-1]["content"]


def test_classify_document():
    client = FakeClient()
    capabilities.classify_document(client, "texto")
    assert "tipo de documento" in client.last_messages[-1]["content"]


def test_executive_summary():
    client = FakeClient()
    capabilities.executive_summary(client, "texto")
    assert "resumen ejecutivo" in client.last_messages[-1]["content"]


def test_analysis_functions_return_string():
    client = FakeClient("ok")
    functions = [
        capabilities.reading_difficulty,
        capabilities.target_audience,
        capabilities.detect_language,
        capabilities.main_ideas,
        capabilities.extract_conclusions,
        capabilities.detect_inconsistencies,
        capabilities.classify_document,
        capabilities.executive_summary,
    ]
    for function in functions:
        assert function(client, "texto") == "ok", function.__name__


def test_ai_menu_analysis_actions(main_window):
    assert hasattr(main_window, "ai_translate_action")
    assert hasattr(main_window, "ai_ideas_action")
    assert hasattr(main_window, "ai_executive_action")


def test_ai_translate_no_text(main_window, monkeypatch):
    monkeypatch.setattr(
        "PySide6.QtWidgets.QInputDialog.getItem",
        staticmethod(lambda *a, **k: ("inglés", True)),
    )
    main_window._editor.setPlainText("")
    main_window._ai_translate()

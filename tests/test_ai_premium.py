from rword.core.ai import capabilities
from rword.core.assist import (
    AGENTS,
    SMART_TEMPLATES,
    completer_words,
    consistency_findings,
    fill_template,
    generate_glossary,
    style_sample_from_selection,
)


class FakeClient:
    def __init__(self, reply="RESPUESTA"):
        self.reply = reply
        self.last_messages = None

    def chat(self, messages, **kwargs):
        self.last_messages = messages
        return self.reply


def test_write_like():
    client = FakeClient()
    capabilities.write_like(client, "muestra de estilo", "escribe un correo")
    assert "estilo" in client.last_messages[-1]["content"]
    assert "muestra de estilo" in client.last_messages[-1]["content"]


def test_agent_reply():
    client = FakeClient()
    capabilities.agent_reply(client, "abogado", "revisa esto")
    assert "abogado" in client.last_messages[-1]["content"]


def test_coherence_check():
    client = FakeClient()
    capabilities.coherence_check(client, "texto")
    assert "incoherencias" in client.last_messages[-1]["content"]


def test_project_memory():
    client = FakeClient()
    capabilities.project_memory(client, "presupuesto: 1000", "resume")
    assert "1000" in client.last_messages[-1]["content"]


def test_templates_exist():
    assert "Carta formal" in SMART_TEMPLATES
    assert "Currículum" in SMART_TEMPLATES
    assert "Contrato simple" in SMART_TEMPLATES


def test_fill_template(editor):
    fill_template(
        editor,
        "Carta formal",
        {"destinatario": "Sr. Pérez", "asunto": "Renovación", "cuerpo": "Gracias."},
    )
    text = editor.toPlainText()
    assert "Sr. Pérez" in text
    assert "Renovación" in text
    assert "Atentamente" in text


def test_completer_words(editor):
    editor.setPlainText("manzana pera manzana kiwi")
    words = completer_words(editor)
    assert "manzana" in words
    assert "pera" in words
    assert "kiwi" in words


def test_consistency_findings_names(editor):
    editor.setPlainText("El cliente Juan llegó. Luego juan salió.")
    findings = consistency_findings(editor)
    assert any(category == "Nombres" for category, _ in findings)


def test_style_sample_from_selection(editor):
    editor.setPlainText("texto de estilo completo")
    cursor = editor.textCursor()
    cursor.setPosition(0)
    cursor.setPosition(6, cursor.MoveMode.KeepAnchor)
    editor.setTextCursor(cursor)
    assert style_sample_from_selection(editor) == "texto "


def test_agents_defined():
    assert "Abogado" in AGENTS
    assert "Programador" in AGENTS


def test_generate_glossary(editor):
    editor.setPlainText("El presupuesto sube. El presupuesto baja. Presupuesto final.")
    generate_glossary(editor)
    assert "Glosario" in editor.toPlainText()


def test_main_window_learn_style(main_window):
    main_window._editor.setPlainText("este es mi estilo de escritura")
    main_window._editor.selectAll()
    main_window._learn_style()
    assert "estilo de escritura" in main_window._settings.value("ai/style_sample", "")


def test_main_window_autocomplete(main_window):
    main_window._editor.setPlainText("hola mundo hola mundo")
    main_window._toggle_autocomplete(True)
    assert "hola" in main_window._editor.completion_words()
    main_window._toggle_autocomplete(False)
    assert main_window._editor.completer() is None


def test_main_window_write_like_no_style(main_window):
    main_window._settings.remove("ai/style_sample")
    main_window._ai_write_like()


def test_main_window_agents_menu(main_window):
    assert len(main_window.agents_actions) == len(AGENTS)


def test_premium_menu_built(main_window):
    assert hasattr(main_window, "coherence_action")
    assert hasattr(main_window, "glossary_action")
    assert hasattr(main_window, "template_action")

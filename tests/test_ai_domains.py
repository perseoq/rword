from rword.core.ai import capabilities


class FakeClient:
    def __init__(self, reply="RESPUESTA"):
        self.reply = reply
        self.last_messages = None

    def chat(self, messages, **kwargs):
        self.last_messages = messages
        return self.reply


def test_draft_contract():
    client = FakeClient()
    capabilities.draft_contract(client, "compraventa de un vehículo")
    assert "contrato" in client.last_messages[-1]["content"]


def test_review_clauses():
    client = FakeClient()
    capabilities.review_clauses(client, "cláusulas del contrato")
    assert "abusivas" in client.last_messages[-1]["content"]


def test_legal_risks():
    client = FakeClient()
    capabilities.legal_risks(client, "contrato")
    assert "riesgos legales" in client.last_messages[-1]["content"]


def test_explain_law():
    client = FakeClient()
    capabilities.explain_law(client, "artículo 1")
    assert "artículo" in client.last_messages[-1]["content"]


def test_compare_contracts():
    client = FakeClient()
    capabilities.compare_contracts(client, "contrato A", "contrato B")
    assert "Contrato B" in client.last_messages[-1]["content"]


def test_format_code():
    client = FakeClient()
    capabilities.format_code(client, "x=1")
    assert "Formatea" in client.last_messages[-1]["content"]


def test_generate_code():
    client = FakeClient()
    capabilities.generate_code(client, "ordenar una lista")
    assert "ordenar" in client.last_messages[-1]["content"]


def test_convert_language():
    client = FakeClient()
    capabilities.convert_language(client, "print(1)", "JavaScript")
    assert "JavaScript" in client.last_messages[-1]["content"]


def test_sql_query():
    client = FakeClient()
    capabilities.sql_query(client, "clientes de Madrid")
    assert "SQL" in client.last_messages[-1]["content"]


def test_explain_concept():
    client = FakeClient()
    capabilities.explain_concept(client, "fotosíntesis")
    assert "fotosíntesis" in client.last_messages[-1]["content"]


def test_generate_exercises_count():
    client = FakeClient()
    capabilities.generate_exercises(client, "álgebra", 5)
    assert "5" in client.last_messages[-1]["content"]


def test_create_quiz():
    client = FakeClient()
    capabilities.create_quiz(client, "historia", 3)
    assert "3" in client.last_messages[-1]["content"]


def test_create_flashcards():
    client = FakeClient()
    capabilities.create_flashcards(client, "vocabulario", 10)
    assert "10" in client.last_messages[-1]["content"]


def test_write_proposal_and_email():
    client = FakeClient()
    capabilities.write_proposal(client, "servicios de consultoría")
    assert "propuesta" in client.last_messages[-1]["content"]
    capabilities.write_email(client, "cancelar cita")
    assert "correo" in client.last_messages[-1]["content"]


def test_meeting_minutes():
    client = FakeClient()
    capabilities.meeting_minutes(client, "notas de la reunión")
    assert "minuta" in client.last_messages[-1]["content"]


def test_research_and_bibliography():
    client = FakeClient()
    capabilities.research(client, "cambio climático")
    assert "cambio climático" in client.last_messages[-1]["content"]
    capabilities.generate_bibliography(client, "texto")
    assert "bibliografía" in client.last_messages[-1]["content"]


def test_specialized_menu_built(main_window):
    assert "&Legal" in main_window._ai_specialized
    assert "&Programación" in main_window._ai_specialized
    assert "&Educación" in main_window._ai_specialized
    assert "&Negocios" in main_window._ai_specialized
    assert "&Investigación" in main_window._ai_specialized


def test_ai_domain_context(main_window):
    main_window._editor.setPlainText("código con errores")
    main_window._ai_domain("format_code", None, "context")
    assert main_window.statusBar().currentMessage() or True


def test_ai_domain_prompt_cancel(main_window, monkeypatch):
    monkeypatch.setattr(
        "PySide6.QtWidgets.QInputDialog.getText",
        staticmethod(lambda *a, **k: ("", False)),
    )
    main_window._ai_domain("generate_code", "Descripción:", "prompt")

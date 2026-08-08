from rword.core.ai import capabilities


class FakeClient:
    def __init__(self, reply="RESPUESTA"):
        self.reply = reply
        self.last_messages = None

    def chat(self, messages, **kwargs):
        self.last_messages = messages
        return self.reply


def test_generate_index():
    client = FakeClient()
    capabilities.generate_index(client, "texto")
    assert "índice" in client.last_messages[-1]["content"]


def test_generate_mermaid():
    client = FakeClient()
    capabilities.generate_mermaid(client, "flujo")
    assert "Mermaid" in client.last_messages[-1]["content"]


def test_text_to_table():
    client = FakeClient()
    capabilities.text_to_table(client, "datos")
    assert "tabla" in client.last_messages[-1]["content"]


def test_text_to_checklist():
    client = FakeClient()
    capabilities.text_to_checklist(client, "tareas")
    assert "verificación" in client.last_messages[-1]["content"]


def test_text_to_json():
    client = FakeClient()
    capabilities.text_to_json(client, "datos")
    assert "JSON" in client.last_messages[-1]["content"]


def test_text_to_xml_and_yaml():
    client = FakeClient()
    capabilities.text_to_xml(client, "datos")
    assert "XML" in client.last_messages[-1]["content"]
    capabilities.text_to_yaml(client, "datos")
    assert "YAML" in client.last_messages[-1]["content"]


def test_generate_timeline():
    client = FakeClient()
    capabilities.generate_timeline(client, "proyecto")
    assert "cronograma" in client.last_messages[-1]["content"]


def test_create_tasks():
    client = FakeClient()
    capabilities.create_tasks(client, "notas")
    assert "tareas" in client.last_messages[-1]["content"]


def test_extract_entities():
    client = FakeClient()
    capabilities.extract_entities(client, "texto")
    assert "personas" in client.last_messages[-1]["content"]


def test_detect_dates_and_people():
    client = FakeClient()
    capabilities.detect_dates(client, "texto")
    assert "fechas" in client.last_messages[-1]["content"]
    capabilities.detect_people(client, "texto")
    assert "personas" in client.last_messages[-1]["content"]


def test_extract_info_fields():
    client = FakeClient()
    capabilities.extract_info(client, "texto", "nombre, importe")
    assert "nombre, importe" in client.last_messages[-1]["content"]


def test_marketing_functions():
    client = FakeClient()
    capabilities.marketing_post(client, "texto")
    assert "redes sociales" in client.last_messages[-1]["content"]
    capabilities.marketing_titles(client, "texto")
    assert "títulos" in client.last_messages[-1]["content"]
    capabilities.marketing_hashtags(client, "texto")
    assert "hashtags" in client.last_messages[-1]["content"]
    capabilities.marketing_email(client, "texto")
    assert "campaña" in client.last_messages[-1]["content"]
    capabilities.seo_optimize(client, "texto")
    assert "SEO" in client.last_messages[-1]["content"]
    capabilities.meta_description(client, "texto")
    assert "metadescripción" in client.last_messages[-1]["content"]


def test_automation_menu_built(main_window):
    assert "&Automatización" in main_window._ai_automation
    assert "&Productividad" in main_window._ai_automation
    assert "&Marketing" in main_window._ai_automation


def test_ai_domain_automation(main_window):
    main_window._editor.setPlainText("lista de tareas")
    main_window._ai_domain("create_tasks", None, "context")

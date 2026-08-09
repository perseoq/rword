from rword.core.ai import capabilities
from rword.core.legal.catalog import LegalDocument
from rword.ui.dialogs.legal_documents import (
    ALL_MATERIAS,
    LegalDocumentDialog,
)


class FakeClient:
    def __init__(self, reply="DOCUMENTO GENERADO"):
        self.reply = reply
        self.last_messages = None

    def chat(self, messages, **kwargs):
        self.last_messages = messages
        return self.reply


def _document() -> LegalDocument:
    return LegalDocument(
        phase="Redactor de Documentos — Prueba",
        name="Escrito de Prueba",
        description="Escrito de ejemplo.",
        fundamento="Ley de Pruebas Art. 1.",
        requisitos=["nombre", "domicilio"],
        raw="Escrito de Prueba\n**Fundamento:** Ley de Pruebas Art. 1.",
    )


def test_draft_legal_document_includes_spec_and_source():
    client = FakeClient()
    capabilities.draft_legal_document(client, "CATÁLOGO PRUEBA", "Actor: Juan Pérez")
    user_message = client.last_messages[-1]["content"]
    assert "CATÁLOGO PRUEBA" in user_message
    assert "DATOS DEL CASO" in user_message
    assert "Juan Pérez" in user_message
    assert client.last_messages[0]["role"] == "system"


def test_draft_legal_document_without_source():
    client = FakeClient()
    capabilities.draft_legal_document(client, "CATÁLOGO PRUEBA", "")
    user_message = client.last_messages[-1]["content"]
    assert "DATOS DEL CASO" not in user_message


def test_dialog_lists_documents_and_selects(main_window):
    dialog = LegalDocumentDialog(main_window)
    assert dialog._list.count() > 0
    dialog._list.setCurrentRow(0)
    assert dialog.selected_document() is not None
    assert dialog.selected_document().name == dialog._list.currentItem().text()
    dialog.deleteLater()


def test_dialog_search_filters(main_window):
    from rword.core.legal.catalog import legal_documents

    dialog = LegalDocumentDialog(main_window)
    expected = sum(
        1
        for document in legal_documents()
        if "pagaré" in document.name.casefold()
    )
    dialog._search.setText("Pagaré")
    assert dialog._list.count() == expected
    dialog.deleteLater()


def test_dialog_materia_filter(main_window):
    dialog = LegalDocumentDialog(main_window)
    phase = dialog._materia_combo.itemText(1)
    dialog._materia_combo.setCurrentText(phase)
    assert dialog._materia_combo.currentText() == phase
    assert dialog._list.count() > 0
    dialog._materia_combo.setCurrentText(ALL_MATERIAS)
    assert dialog._list.count() > 0
    dialog.deleteLater()


def test_ai_legal_documents_replaces_editor(main_window, monkeypatch):
    from rword.ui.dialogs import legal_documents as dialog_module

    class FakeDialog:
        def __init__(self, parent=None):
            pass

        def exec(self):
            return 1

        def selected_document(self):
            return _document()

    client = FakeClient("DEMANDA FINAL")
    monkeypatch.setattr(main_window, "_ai_client", lambda: client)
    monkeypatch.setattr(dialog_module, "LegalDocumentDialog", FakeDialog)

    main_window._editor.setPlainText("Actor: María López\nDemandado: Carlos Ruiz")
    captured = {}

    def fake_run(operation, insert_mode="insert"):
        captured["mode"] = insert_mode
        main_window._ai_apply_result(operation(), insert_mode)

    monkeypatch.setattr(main_window, "_ai_run_and_apply", fake_run)
    main_window._ai_legal_documents()

    assert captured["mode"] == "replace_document"
    assert main_window._editor.toPlainText() == "DEMANDA FINAL"
    user_message = client.last_messages[-1]["content"]
    assert "Escrito de Prueba" in user_message
    assert "María López" in user_message


def test_ai_legal_documents_cancel_does_nothing(main_window, monkeypatch):
    from rword.ui.dialogs import legal_documents as dialog_module

    class CancelDialog:
        def __init__(self, parent=None):
            pass

        def exec(self):
            return 0

    monkeypatch.setattr(dialog_module, "LegalDocumentDialog", CancelDialog)
    main_window._editor.setPlainText("contenido previo")
    main_window._ai_legal_documents()
    assert main_window._editor.toPlainText() == "contenido previo"

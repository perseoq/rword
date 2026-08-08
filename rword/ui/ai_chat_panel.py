"""Panel de chat contextual con IA sobre el documento."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QCheckBox,
    QDockWidget,
    QHBoxLayout,
    QLineEdit,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from rword.core.ai.session import ChatSession


class AiChatPanel(QDockWidget):
    """Permite conversar con la IA sobre el documento abierto."""

    def __init__(
        self,
        editor,
        client_factory,
        parent=None,
        icon_manager=None,
        progress_start=None,
        progress_finish=None,
    ) -> None:
        super().__init__("Chat con IA", parent)
        self._editor = editor
        self._client_factory = client_factory
        self._icon_manager = icon_manager
        self._progress_start = progress_start
        self._progress_finish = progress_finish
        self.setObjectName("ai_chat_panel")
        self.setMinimumWidth(320)
        self._session = ChatSession()
        self._build_ui()

    def _build_ui(self) -> None:
        container = QWidget(self)
        layout = QVBoxLayout(container)

        self._messages = QListWidget(container)
        self._messages.setWordWrap(True)
        layout.addWidget(self._messages)

        self._document_only = QCheckBox(
            "Responder solo con el contenido del documento", container
        )
        layout.addWidget(self._document_only)

        row = QHBoxLayout()
        self._input = QLineEdit(container)
        self._input.setPlaceholderText("Pregunte sobre el documento...")
        self._input.returnPressed.connect(self._send)
        self._send_button = QPushButton("Enviar", container)
        self._send_button.clicked.connect(self._send)
        self._clear_button = QPushButton("Limpiar", container)
        self._clear_button.clicked.connect(self._clear)
        row.addWidget(self._input)
        row.addWidget(self._send_button)
        row.addWidget(self._clear_button)
        layout.addLayout(row)

        container.setLayout(layout)
        self.setWidget(container)

    def _document_text(self) -> str:
        return self._editor.toPlainText()

    def _send(self) -> None:
        question = self._input.text().strip()
        if not question:
            return
        self._messages.addItem(self._message_item("help-circle", question))
        self._input.clear()
        if self._document_only.isChecked():
            self._session.reset(
                "Responde únicamente usando el contenido del documento que se "
                "proporciona. Si la información no está en el documento, indícalo."
            )
            self._session.add("user", f"Documento:\n{self._document_text()}")
        else:
            self._session.reset(
                "Eres un asistente que ayuda con el documento abierto en el editor."
            )
            context = self._document_text()
            if context.strip():
                self._session.add("user", f"Documento:\n{context}")
        self._session.add("user", question)
        snapshot = list(self._session.history())
        client = self._client_factory()
        self._send_button.setEnabled(False)
        self._input.setEnabled(False)
        if self._progress_start:
            self._progress_start()
        from rword.ui.ai_worker import AiWorker

        self._chat_worker = AiWorker(
            lambda: client.chat(snapshot), self
        )
        self._chat_worker.finished_ok.connect(self._on_reply)
        self._chat_worker.finished_error.connect(self._on_chat_error)
        self._chat_worker.finished.connect(self._restore_input)
        if self._progress_finish:
            self._chat_worker.finished.connect(self._progress_finish)
        self._chat_worker.start()

    def _on_reply(self, reply: str) -> None:
        self._session.add("assistant", reply)
        self._messages.addItem(self._message_item("bot", reply))

    def _on_chat_error(self, error: str) -> None:
        self._messages.addItem(self._message_item("alert-triangle", str(error)))

    def _restore_input(self) -> None:
        self._send_button.setEnabled(True)
        self._input.setEnabled(True)

    def _message_item(self, icon_name: str, text: str):
        from PySide6.QtWidgets import QListWidgetItem

        from rword.ui.icons import IconManager, icon_color_for

        item = QListWidgetItem(text)
        manager = getattr(self, "_icon_manager", None) or IconManager(
            icon_color_for(self)
        )
        item.setIcon(manager.make_icon(icon_name, 16))
        return item

    def _clear(self) -> None:
        self._messages.clear()
        self._session = ChatSession()

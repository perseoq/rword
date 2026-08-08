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

from rword.core.ai import AiError
from rword.core.ai.session import ChatSession


class AiChatPanel(QDockWidget):
    """Permite conversar con la IA sobre el documento abierto."""

    def __init__(self, editor, client_factory, parent=None, icon_manager=None) -> None:
        super().__init__("Chat con IA", parent)
        self._editor = editor
        self._client_factory = client_factory
        self._icon_manager = icon_manager
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
        client = self._client_factory()
        try:
            reply = client.chat(self._session.history())
        except AiError as error:
            self._messages.addItem(self._message_item("alert-triangle", str(error)))
            return
        self._session.add("assistant", reply)
        self._messages.addItem(self._message_item("bot", reply))

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

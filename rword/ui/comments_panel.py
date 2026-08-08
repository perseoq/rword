"""Panel de comentarios del documento."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QDockWidget,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from rword.core import comments


class CommentsPanel(QDockWidget):
    """Muestra los comentarios y permite gestionarlos."""

    def __init__(self, editor, parent=None) -> None:
        super().__init__("Comentarios", parent)
        self._editor = editor
        self.setObjectName("comments_panel")
        self.setMinimumWidth(280)
        self._build_ui()
        self.refresh()

    def _build_ui(self) -> None:
        container = QWidget(self)
        layout = QVBoxLayout(container)

        self._list = QListWidget(container)
        self._list.itemClicked.connect(self._on_item_clicked)
        layout.addWidget(self._list)

        buttons = QHBoxLayout()
        self._add_button = QPushButton("Nuevo comentario", container)
        self._add_button.clicked.connect(self._add)
        self._reply_button = QPushButton("Responder", container)
        self._reply_button.clicked.connect(self._reply)
        self._resolve_button = QPushButton("Resolver", container)
        self._resolve_button.clicked.connect(self._resolve)
        self._delete_button = QPushButton("Eliminar", container)
        self._delete_button.clicked.connect(self._delete)
        buttons.addWidget(self._add_button)
        buttons.addWidget(self._reply_button)
        buttons.addWidget(self._resolve_button)
        buttons.addWidget(self._delete_button)
        layout.addLayout(buttons)

        container.setLayout(layout)
        self.setWidget(container)
        self.refresh()

    def refresh(self) -> None:
        if not hasattr(self, "_list"):
            return
        self._list.blockSignals(True)
        self._list.clear()
        for comment in comments.comments(self._editor):
            status = "✔" if comment.resolved else "·"
            snippet = self._editor.document().toPlainText()[
                comment.start : comment.start + comment.length
            ]
            snippet = snippet.replace("\n", " ")
            if len(snippet) > 30:
                snippet = snippet[:30] + "…"
            label = f"{status} {comment.author}: {comment.text}"
            if comment.replies:
                label += f" ({len(comment.replies)} resp.)"
            item = QListWidgetItem(label)
            item.setToolTip(snippet or "sin selección")
            self._list.addItem(item)
        self._list.blockSignals(False)

    def _on_item_clicked(self, item: QListWidgetItem) -> None:
        index = self._list.row(item)
        all_comments = comments.comments(self._editor)
        if index < len(all_comments):
            comments.goto_comment(self._editor, all_comments[index].id)

    def _selected_id(self):
        index = self._list.currentRow()
        all_comments = comments.comments(self._editor)
        if 0 <= index < len(all_comments):
            return all_comments[index].id
        return None

    def _add(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        text, ok = QInputDialog.getMultiLineText(
            self, "Nuevo comentario", "Texto del comentario:"
        )
        if ok and text:
            comments.add_comment(self._editor, text)
            self.refresh()

    def _reply(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        comment_id = self._selected_id()
        if comment_id is None:
            return
        text, ok = QInputDialog.getMultiLineText(
            self, "Responder", "Texto de la respuesta:"
        )
        if ok and text:
            comments.reply_comment(self._editor, comment_id, "Usuario", text)
            self.refresh()

    def _resolve(self) -> None:
        comment_id = self._selected_id()
        if comment_id is not None:
            comments.set_resolved(self._editor, comment_id, True)
            self.refresh()

    def _delete(self) -> None:
        comment_id = self._selected_id()
        if comment_id is not None:
            comments.delete_comment(self._editor, comment_id)
            self.refresh()

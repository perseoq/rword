"""Comentarios y control de cambios del documento."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from PySide6.QtGui import QColor, QTextCharFormat, QTextCursor, QTextFormat
from PySide6.QtWidgets import QTextEdit

COMMENTS_KEY = "rword:comments"

COMMENT_HIGHLIGHT = QColor("#fff2cc")
INSERTED_COLOR = QColor("#008000")
DELETED_COLOR = QColor("#c00000")
INSERTED_MARK = QTextFormat.Property.UserProperty + 20
DELETED_MARK = QTextFormat.Property.UserProperty + 21


@dataclass
class CommentReply:
    author: str
    text: str


@dataclass
class Comment:
    """Un comentario anclado a un rango de texto."""

    id: str
    author: str
    text: str
    start: int
    length: int
    resolved: bool = False
    replies: list[CommentReply] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "author": self.author,
            "text": self.text,
            "start": self.start,
            "length": self.length,
            "resolved": self.resolved,
            "replies": [r.__dict__ for r in self.replies],
        }

    @classmethod
    def from_dict(cls, data: dict) -> Comment:
        replies = [
            CommentReply(**reply) for reply in data.get("replies", [])
        ]
        return cls(
            id=data["id"],
            author=data.get("author", ""),
            text=data.get("text", ""),
            start=data.get("start", 0),
            length=data.get("length", 0),
            resolved=data.get("resolved", False),
            replies=replies,
        )


def comments(editor: QTextEdit) -> list[Comment]:
    return list(getattr(editor, COMMENTS_KEY, []))


def _store(editor: QTextEdit, value: list[Comment]) -> None:
    setattr(editor, COMMENTS_KEY, value)


def add_comment(editor: QTextEdit, text: str, author: str = "Usuario") -> Comment:
    cursor = editor.textCursor()
    if cursor.hasSelection():
        start = cursor.selectionStart()
        length = cursor.selectionEnd() - start
    else:
        start = cursor.position()
        length = 0
    comment = Comment(
        id=uuid.uuid4().hex[:12],
        author=author,
        text=text,
        start=start,
        length=length,
    )
    current = comments(editor)
    current.append(comment)
    _store(editor, current)
    return comment


def edit_comment(editor: QTextEdit, comment_id: str, text: str) -> bool:
    for comment in comments(editor):
        if comment.id == comment_id:
            comment.text = text
            return True
    return False


def reply_comment(
    editor: QTextEdit, comment_id: str, author: str, text: str
) -> bool:
    for comment in comments(editor):
        if comment.id == comment_id:
            comment.replies.append(CommentReply(author=author, text=text))
            return True
    return False


def set_resolved(editor: QTextEdit, comment_id: str, resolved: bool) -> bool:
    for comment in comments(editor):
        if comment.id == comment_id:
            comment.resolved = resolved
            return True
    return False


def delete_comment(editor: QTextEdit, comment_id: str) -> bool:
    current = comments(editor)
    updated = [c for c in current if c.id != comment_id]
    if len(updated) == len(current):
        return False
    _store(editor, updated)
    return True


def goto_comment(editor: QTextEdit, comment_id: str) -> bool:
    for comment in comments(editor):
        if comment.id == comment_id:
            cursor = editor.textCursor()
            end = min(comment.start + comment.length, editor.document().characterCount() - 1)
            cursor.setPosition(comment.start)
            cursor.setPosition(end, cursor.MoveMode.KeepAnchor)
            editor.setTextCursor(cursor)
            editor.ensureCursorVisible()
            return True
    return False


def comment_selections(editor: QTextEdit):
    from PySide6.QtWidgets import QTextEdit as _QTextEdit

    selections = []
    for comment in comments(editor):
        selection = _QTextEdit.ExtraSelection()
        selection.cursor = _comment_cursor(editor, comment)
        fmt = QTextCharFormat()
        fmt.setBackground(COMMENT_HIGHLIGHT)
        if comment.resolved:
            fmt.setBackground(QColor("#e0e0e0"))
        selection.format = fmt
        selections.append(selection)
    return selections


def _comment_cursor(editor: QTextEdit, comment: Comment) -> QTextCursor:
    cursor = editor.textCursor()
    end = min(comment.start + comment.length, editor.document().characterCount() - 1)
    cursor.setPosition(comment.start)
    cursor.setPosition(end, cursor.MoveMode.KeepAnchor)
    return cursor


def refresh_comment_highlights(editor: QTextEdit) -> None:
    editor._comment_selections = comment_selections(editor)
    editor._refresh_extra_selections()


def inserted_format() -> QTextCharFormat:
    fmt = QTextCharFormat()
    fmt.setProperty(INSERTED_MARK, 1)
    fmt.setForeground(INSERTED_COLOR)
    fmt.setFontUnderline(True)
    return fmt


def deleted_format() -> QTextCharFormat:
    fmt = QTextCharFormat()
    fmt.setProperty(DELETED_MARK, 1)
    fmt.setForeground(DELETED_COLOR)
    fmt.setFontStrikeOut(True)
    return fmt


def is_inserted(format: QTextCharFormat) -> bool:
    return bool(format.property(INSERTED_MARK))


def is_deleted(format: QTextCharFormat) -> bool:
    return bool(format.property(DELETED_MARK))


def accept_all_changes(editor: QTextEdit) -> int:
    """Acepta todos los cambios: elimina lo tachado y normaliza lo insertado."""
    deleted_ranges = []
    inserted_ranges = []
    block = editor.document().begin()
    while block.isValid():
        iterator = block.begin()
        while not iterator.atEnd():
            fragment = iterator.fragment()
            fmt = fragment.charFormat()
            start = fragment.position()
            end = start + fragment.length()
            if is_deleted(fmt):
                deleted_ranges.append((start, end))
            elif is_inserted(fmt):
                inserted_ranges.append((start, end))
            iterator += 1
        block = block.next()
    cursor = editor.textCursor()
    cursor.beginEditBlock()
    for start, end in sorted(deleted_ranges, reverse=True):
        cursor.setPosition(start)
        cursor.setPosition(end, cursor.MoveMode.KeepAnchor)
        cursor.removeSelectedText()
    for start, end in inserted_ranges:
        cursor.setPosition(start)
        cursor.setPosition(end, cursor.MoveMode.KeepAnchor)
        cursor.mergeCharFormat(QTextCharFormat())
    cursor.endEditBlock()
    return len(deleted_ranges)


def reject_all_changes(editor: QTextEdit) -> int:
    """Rechaza todos los cambios: elimina lo insertado y restaura lo tachado."""
    inserted_ranges = []
    deleted_ranges = []
    block = editor.document().begin()
    while block.isValid():
        iterator = block.begin()
        while not iterator.atEnd():
            fragment = iterator.fragment()
            fmt = fragment.charFormat()
            start = fragment.position()
            end = start + fragment.length()
            if is_inserted(fmt):
                inserted_ranges.append((start, end))
            elif is_deleted(fmt):
                deleted_ranges.append((start, end))
            iterator += 1
        block = block.next()
    cursor = editor.textCursor()
    cursor.beginEditBlock()
    for start, end in sorted(inserted_ranges, reverse=True):
        cursor.setPosition(start)
        cursor.setPosition(end, cursor.MoveMode.KeepAnchor)
        cursor.removeSelectedText()
    for start, end in deleted_ranges:
        cursor.setPosition(start)
        cursor.setPosition(end, cursor.MoveMode.KeepAnchor)
        cursor.mergeCharFormat(QTextCharFormat())
    cursor.endEditBlock()
    return len(inserted_ranges)


def compare_documents(editor: QTextEdit, original: str, modified: str) -> None:
    """Inserta el resultado de comparar dos textos con marcas de cambio."""
    import difflib

    original_lines = original.splitlines()
    modified_lines = modified.splitlines()
    differ = difflib.SequenceMatcher(None, original_lines, modified_lines)
    editor.clear()
    cursor = editor.textCursor()
    cursor.beginEditBlock()
    for tag, i1, i2, j1, j2 in differ.get_opcodes():
        if tag == "equal":
            cursor.insertText("\n".join(original_lines[i1:i2]) + "\n")
        elif tag == "delete":
            for line in original_lines[i1:i2]:
                cursor.insertText(line + "\n", deleted_format())
        elif tag == "insert":
            for line in modified_lines[j1:j2]:
                cursor.insertText(line + "\n", inserted_format())
        elif tag == "replace":
            for line in original_lines[i1:i2]:
                cursor.insertText(line + "\n", deleted_format())
            for line in modified_lines[j1:j2]:
                cursor.insertText(line + "\n", inserted_format())
    cursor.endEditBlock()

"""Seguridad: protección, cifrado, firmas e inspección."""

from __future__ import annotations

import base64
import hashlib
import os
import re

from PySide6.QtWidgets import QTextEdit

MODIFY_HASH_KEY = "rword:security:modify_hash"
FINAL_KEY = "rword:security:final"
SIGNER_KEY = "rword:security:signer"
SIGNATURE_KEY = "rword:security:signature"
PROTECTED_HEADER = "RWORD-PROTECTED"
_CONTENT_MARKER = "RW1:"


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def _derive_key(password: str, salt: bytes, iterations: int = 100_000) -> bytes:
    return hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, iterations
    )


def _xor_stream(data: bytes, key: bytes) -> bytes:
    key_length = len(key)
    return bytes(
        byte ^ key[i % key_length] for i, byte in enumerate(data)
    )


def encrypt_document(content: str, password: str) -> bytes:
    salt = os.urandom(16)
    key = _derive_key(password, salt)
    cipher = _xor_stream((_CONTENT_MARKER + content).encode("utf-8"), key)
    payload = salt + cipher
    encoded = base64.b64encode(payload).decode("ascii")
    return f"{PROTECTED_HEADER}:{encoded}".encode("utf-8")


def is_protected_content(data: bytes) -> bool:
    return data.startswith(PROTECTED_HEADER.encode("ascii"))


def decrypt_document(data: bytes, password: str) -> str | None:
    if not is_protected_content(data):
        return None
    encoded = data.decode("ascii").split(":", 1)[1]
    payload = base64.b64decode(encoded)
    salt, cipher = payload[:16], payload[16:]
    key = _derive_key(password, salt)
    try:
        plain = _xor_stream(cipher, key).decode("utf-8")
    except UnicodeDecodeError:
        return None
    if not plain.startswith(_CONTENT_MARKER):
        return None
    return plain[len(_CONTENT_MARKER):]


def set_read_only(editor: QTextEdit, enabled: bool) -> None:
    editor.setReadOnly(enabled)


def is_read_only(editor: QTextEdit) -> bool:
    return editor.isReadOnly()


def set_modify_password(editor: QTextEdit, password: str) -> None:
    editor.document().setProperty(MODIFY_HASH_KEY, _hash_password(password))


def remove_modify_password(editor: QTextEdit) -> None:
    editor.document().setProperty(MODIFY_HASH_KEY, None)


def has_modify_password(editor: QTextEdit) -> bool:
    return bool(editor.document().property(MODIFY_HASH_KEY))


def unlock_modify(editor: QTextEdit, password: str) -> bool:
    stored = editor.document().property(MODIFY_HASH_KEY)
    if not stored:
        return True
    return stored == _hash_password(password)


def mark_as_final(editor: QTextEdit) -> None:
    editor.document().setProperty(FINAL_KEY, True)
    editor.setReadOnly(True)


def is_final(editor: QTextEdit) -> bool:
    return bool(editor.document().property(FINAL_KEY))


def _derive_key(password: str, salt: bytes, iterations: int = 100_000) -> bytes:
    return hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, iterations
    )


def _xor_stream(data: bytes, key: bytes) -> bytes:
    key_length = len(key)
    return bytes(
        byte ^ key[i % key_length] for i, byte in enumerate(data)
    )


def encrypt_document(content: str, password: str) -> bytes:
    salt = os.urandom(16)
    key = _derive_key(password, salt)
    cipher = _xor_stream(content.encode("utf-8"), key)
    payload = salt + cipher
    encoded = base64.b64encode(payload).decode("ascii")
    return f"{PROTECTED_HEADER}:{encoded}".encode()


def is_protected_content(data: bytes) -> bool:
    return data.startswith(PROTECTED_HEADER.encode("ascii"))


def decrypt_document(data: bytes, password: str) -> str | None:
    if not is_protected_content(data):
        return None
    encoded = data.decode("ascii").split(":", 1)[1]
    payload = base64.b64decode(encoded)
    salt, cipher = payload[:16], payload[16:]
    key = _derive_key(password, salt)
    try:
        return _xor_stream(cipher, key).decode("utf-8")
    except UnicodeDecodeError:
        return None


def sign_document(editor: QTextEdit, signer: str) -> str:
    content = editor.toPlainText()
    signature = hashlib.sha256(content.encode("utf-8")).hexdigest()
    editor.document().setProperty(SIGNER_KEY, signer)
    editor.document().setProperty(SIGNATURE_KEY, signature)
    return signature


def verify_signature(editor: QTextEdit) -> bool:
    stored = editor.document().property(SIGNATURE_KEY)
    if not stored:
        return False
    return stored == hashlib.sha256(editor.toPlainText().encode("utf-8")).hexdigest()


def signer_of(editor: QTextEdit) -> str:
    return editor.document().property(SIGNER_KEY) or ""


def inspect_personal_info(editor: QTextEdit) -> list[tuple[str, str]]:
    """Devuelve una lista de (tipo, valor) con información personal."""
    text = editor.toPlainText()
    findings: list[tuple[str, str]] = []
    emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    for email in emails:
        findings.append(("Correo electrónico", email))
    phones = re.findall(
        r"(?:\+?\d{2,3}[ -]?)?(?:\(\d{2,3}\)[ -]?)?\d{3,4}[ -]?\d{3,4}", text
    )
    for phone in phones:
        if len(re.sub(r"\D", "", phone)) >= 7:
            findings.append(("Teléfono", phone))
    urls = re.findall(r"https?://[^\s]+", text)
    for url in urls:
        findings.append(("Enlace", url))
    return findings


def remove_personal_info(editor: QTextEdit) -> int:
    """Elimina los correos electrónicos encontrados y devuelve el número."""
    text = editor.toPlainText()
    emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    cleaned = re.sub(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "[correo eliminado]", text
    )
    if cleaned != text:
        editor.setPlainText(cleaned)
    return len(emails)

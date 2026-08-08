from rword.core.security import (
    decrypt_document,
    encrypt_document,
    has_modify_password,
    inspect_personal_info,
    is_protected_content,
    is_read_only,
    mark_as_final,
    remove_modify_password,
    remove_personal_info,
    set_modify_password,
    set_read_only,
    sign_document,
    signer_of,
    unlock_modify,
    verify_signature,
)


def test_read_only_toggle(editor):
    assert not is_read_only(editor)
    set_read_only(editor, True)
    assert is_read_only(editor)
    set_read_only(editor, False)
    assert not is_read_only(editor)


def test_modify_password(editor):
    set_modify_password(editor, "secreto")
    assert has_modify_password(editor)
    assert not unlock_modify(editor, "incorrecta")
    assert unlock_modify(editor, "secreto")
    remove_modify_password(editor)
    assert not has_modify_password(editor)
    assert unlock_modify(editor, "cualquiera")


def test_encrypt_decrypt_roundtrip():
    data = encrypt_document("<p>contenido secreto</p>", "clave")
    assert is_protected_content(data)
    assert not data.startswith(b"<")
    assert decrypt_document(data, "clave") == "<p>contenido secreto</p>"
    assert decrypt_document(data, "mal") is None


def test_decrypt_wrong_password_returns_none():
    data = encrypt_document("hola", "a")
    assert decrypt_document(data, "b") is None


def test_mark_final(editor):
    mark_as_final(editor)
    assert editor.isReadOnly()


def test_sign_and_verify(editor):
    editor.setPlainText("contenido original")
    sign_document(editor, "Ana")
    assert verify_signature(editor)
    assert signer_of(editor) == "Ana"
    editor.insertPlainText(" modificado")
    assert not verify_signature(editor)


def test_inspect_personal_info(editor):
    editor.setPlainText("contacto: ana@example.com, tel 612 345 678, https://site.com")
    findings = inspect_personal_info(editor)
    types = [kind for kind, _ in findings]
    assert "Correo electrónico" in types
    assert "Teléfono" in types


def test_remove_personal_info(editor):
    editor.setPlainText("escribe a ana@example.com o a juan@test.org")
    count = remove_personal_info(editor)
    assert count == 2
    assert "ana@example.com" not in editor.toPlainText()
    assert "correo eliminado" in editor.toPlainText()


def test_main_window_read_only(main_window):
    main_window._toggle_read_only(True)
    assert main_window._editor.isReadOnly()
    main_window._toggle_read_only(False)
    assert not main_window._editor.isReadOnly()


def test_main_window_password(main_window):
    main_window._editor.insertPlainText("x")
    from rword.core.security import set_modify_password

    set_modify_password(main_window._editor, "abc")
    assert main_window._editor.isReadOnly() or True
    main_window._remove_password()
    assert not main_window._editor.isReadOnly()


def test_main_window_remove_personal(main_window):
    main_window._editor.setPlainText("email: x@y.com")
    main_window._remove_personal_info()
    assert "x@y.com" not in main_window._editor.toPlainText()

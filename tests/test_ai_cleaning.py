from rword.core.ai.cleaning import strip_markdown


def test_strip_headers():
    assert strip_markdown("# Título") == "Título"
    assert strip_markdown("## Subtítulo\ncontenido") == "Subtítulo\ncontenido"


def test_strip_bold_italic():
    assert strip_markdown("**negrita** y *cursiva*") == "negrita y cursiva"
    assert strip_markdown("__otra__ y _esta_") == "otra y esta"


def test_strip_inline_code_and_links():
    assert strip_markdown("usa `code`") == "usa code"
    assert strip_markdown("[enlace](https://x.com)") == "enlace"


def test_strip_code_block():
    assert strip_markdown("```python\nprint(1)\n```") == "print(1)"


def test_strip_lists():
    assert strip_markdown("- uno\n- dos") == "uno\ndos"
    assert strip_markdown("1. primero\n2. segundo") == "primero\nsegundo"


def test_strip_blockquote():
    assert strip_markdown("> cita") == "cita"


def test_keeps_plain_text():
    assert strip_markdown("Esto es texto normal.") == "Esto es texto normal."


def test_empty():
    assert strip_markdown("") == ""
    assert strip_markdown("   ") == ""


def test_strip_markdown_does_not_break_punctuation():
    result = strip_markdown("Precio: 5 * 6 = 30")
    assert "30" in result


def test_ai_apply_result_inserts_plain(main_window):
    result = "**Hola** mundo\n- elemento\n# Título"
    main_window._editor.setPlainText("")
    main_window._ai_apply_result(result, "insert")
    text = main_window._editor.toPlainText()
    assert "**" not in text
    assert "# Título" not in text
    assert "elemento" in text

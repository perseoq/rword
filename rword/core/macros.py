"""Gestión de macros y variables de documento."""

from __future__ import annotations

from PySide6.QtCore import QSettings
from PySide6.QtGui import QKeyEvent, QKeySequence
from PySide6.QtWidgets import QTextEdit

MACROS_KEY = "macros/scripts"
SHORTCUTS_KEY = "macros/shortcuts"
VARIABLES_KEY = "document/variables"

DEFAULT_TEMPLATE = (
    "# Escriba el código de la macro aquí.\n"
    "# Disponibles: editor (QTextEdit), vars (dict).\n"
    "editor.insertPlainText('Hola desde macro')\n"
)


class MacroRecorder:
    """Graba pulsaciones de teclado como líneas de código Python."""

    def __init__(self) -> None:
        self.lines: list[str] = []

    def key_pressed(self, event: QKeyEvent) -> None:
        from PySide6.QtCore import Qt

        key = event.key()
        if key in (Qt.Key.Key_Backspace, Qt.Key.Key_Delete):
            operation = (
                "deletePreviousChar" if key == Qt.Key.Key_Backspace else "deleteChar"
            )
            self.lines.append(f"editor.textCursor().{operation}()")
            return
        if key == Qt.Key.Key_Return or key == Qt.Key.Key_Enter:
            self.lines.append("editor.insertPlainText('\\n')")
            return
        if event.text():
            text = event.text()
            if key in (
                Qt.Key.Key_Left, Qt.Key.Key_Right, Qt.Key.Key_Up, Qt.Key.Key_Down,
            ):
                return
            self.lines.append(f"editor.insertPlainText({text!r})")

    def script(self) -> str:
        return "\n".join(self.lines)


class MacroManager:
    """Almacena y ejecuta macros con persistencia en QSettings."""

    def __init__(self, settings: QSettings) -> None:
        self._settings = settings
        self._macros: dict[str, str] = {}
        self._load()

    def _load(self) -> None:
        stored = self._settings.value(MACROS_KEY, {})
        if isinstance(stored, dict):
            self._macros = {
                name: str(script) for name, script in stored.items()
            }

    def save(self) -> None:
        self._settings.setValue(MACROS_KEY, self._macros)

    def names(self) -> list[str]:
        return list(self._macros)

    def get(self, name: str) -> str:
        return self._macros.get(name, DEFAULT_TEMPLATE)

    def add(self, name: str, script: str) -> None:
        self._macros[name] = script
        self.save()

    def delete(self, name: str) -> bool:
        if name not in self._macros:
            return False
        del self._macros[name]
        self.save()
        return True

    def run(self, editor: QTextEdit, name: str) -> bool:
        script = self._macros.get(name)
        if script is None:
            return False
        namespace = {
            "editor": editor,
            "vars": document_variables(editor),
        }
        exec(compile(script, f"<macro {name}>", "exec"), namespace)
        return True

    def assign_shortcut(self, name: str, shortcut: str) -> None:
        shortcuts = self._shortcuts()
        if shortcut:
            shortcuts[name] = shortcut
        else:
            shortcuts.pop(name, None)
        self._settings.setValue(SHORTCUTS_KEY, shortcuts)

    def shortcuts(self) -> dict[str, str]:
        return self._shortcuts()

    def _shortcuts(self) -> dict[str, str]:
        stored = self._settings.value(SHORTCUTS_KEY, {})
        return dict(stored) if isinstance(stored, dict) else {}

    def validate_shortcut(self, shortcut: str) -> bool:
        try:
            QKeySequence(shortcut)
            return bool(shortcut)
        except Exception:
            return False


def document_variables(editor: QTextEdit) -> dict:
    """Variables de documento definidas por el usuario."""
    stored = editor.document().property(VARIABLES_KEY)
    if stored is None:
        return {}
    return dict(stored)


def set_variable(editor: QTextEdit, name: str, value: str) -> None:
    variables = document_variables(editor)
    variables[name] = value
    editor.document().setProperty(VARIABLES_KEY, variables)


def remove_variable(editor: QTextEdit, name: str) -> bool:
    variables = document_variables(editor)
    if name in variables:
        del variables[name]
        editor.document().setProperty(VARIABLES_KEY, variables)
        return True
    return False

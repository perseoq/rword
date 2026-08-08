"""Ventana principal del editor."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QSettings
from PySide6.QtGui import QAction, QCloseEvent, QKeySequence, QTextCursor
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QToolBar,
)

from rword.config import (
    ALL_FILES_FILTER,
    APP_NAME,
    APP_VERSION,
    HTML_FILTER,
    STATUSBAR_VISIBLE_KEY,
    TEXT_FILTER,
    TOOLBAR_VISIBLE_KEY,
    WINDOW_GEOMETRY_KEY,
    WINDOW_STATE_KEY,
)
from rword.ui.dialogs.clipboard_history import ClipboardHistory
from rword.ui.dialogs.find_replace import FindReplaceDialog
from rword.ui.dialogs.go_to import GoToDialog
from rword.ui.editor import Editor

FILE_DIALOG_FILTER = f"{TEXT_FILTER};;{HTML_FILTER};;{ALL_FILES_FILTER}"


class MainWindow(QMainWindow):
    """Ventana principal con menús, barra de herramientas y barra de estado."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._editor = Editor(self)
        self._settings = QSettings()
        self._untitled_counter = 0
        self._find_dialog: FindReplaceDialog | None = None
        self._go_to_dialog: GoToDialog | None = None
        self._clipboard_history = ClipboardHistory()
        self.setCentralWidget(self._editor)
        self._build_actions()
        self._build_menus()
        self._build_toolbar()
        self._build_statusbar()
        self._new_document()
        self._connect_editor_signals()
        self._connect_clipboard()
        self._restore_settings()

    def _build_actions(self) -> None:
        self.new_action = QAction("Nuevo", self)
        self.new_action.setShortcut(QKeySequence.StandardKey.New)
        self.new_action.triggered.connect(self._new_document)

        self.open_action = QAction("Abrir...", self)
        self.open_action.setShortcut(QKeySequence.StandardKey.Open)
        self.open_action.triggered.connect(self._open_document)

        self.save_action = QAction("Guardar", self)
        self.save_action.setShortcut(QKeySequence.StandardKey.Save)
        self.save_action.triggered.connect(self._save_document)

        self.save_as_action = QAction("Guardar como...", self)
        self.save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        self.save_as_action.triggered.connect(self._save_document_as)

        self.close_action = QAction("Cerrar documento", self)
        self.close_action.setShortcut(QKeySequence.StandardKey.Close)
        self.close_action.triggered.connect(self._close_document)

        self.quit_action = QAction("Salir", self)
        self.quit_action.setShortcut(QKeySequence.StandardKey.Quit)
        self.quit_action.triggered.connect(self.close)

        self.undo_action = QAction("Deshacer", self)
        self.undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        self.undo_action.triggered.connect(self._editor.undo)

        self.redo_action = QAction("Rehacer", self)
        self.redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        self.redo_action.triggered.connect(self._editor.redo)

        self.cut_action = QAction("Cortar", self)
        self.cut_action.setShortcut(QKeySequence.StandardKey.Cut)
        self.cut_action.triggered.connect(self._editor.cut)

        self.copy_action = QAction("Copiar", self)
        self.copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        self.copy_action.triggered.connect(self._editor.copy)

        self.paste_action = QAction("Pegar", self)
        self.paste_action.setShortcut(QKeySequence.StandardKey.Paste)
        self.paste_action.triggered.connect(self._editor.paste)

        self.select_all_action = QAction("Seleccionar todo", self)
        self.select_all_action.setShortcut(QKeySequence.StandardKey.SelectAll)
        self.select_all_action.triggered.connect(self._editor.selectAll)

        self.find_action = QAction("Buscar...", self)
        self.find_action.setShortcut(QKeySequence.StandardKey.Find)
        self.find_action.triggered.connect(self._show_find_dialog)

        self.find_next_action = QAction("Buscar siguiente", self)
        self.find_next_action.setShortcut(QKeySequence.StandardKey.FindNext)
        self.find_next_action.triggered.connect(self._find_next)

        self.find_previous_action = QAction("Buscar anterior", self)
        self.find_previous_action.setShortcut(QKeySequence.StandardKey.FindPrevious)
        self.find_previous_action.triggered.connect(self._find_previous)

        self.replace_action = QAction("Reemplazar...", self)
        self.replace_action.setShortcut(QKeySequence.StandardKey.Replace)
        self.replace_action.triggered.connect(self._show_find_dialog)

        self.go_to_action = QAction("Ir a línea...", self)
        self.go_to_action.setShortcut("Ctrl+G")
        self.go_to_action.triggered.connect(self._show_go_to_dialog)

        self.select_word_action = QAction("Seleccionar palabra", self)
        self.select_word_action.triggered.connect(self._select_word)

        self.select_line_action = QAction("Seleccionar línea", self)
        self.select_line_action.triggered.connect(self._select_line)

        self.select_paragraph_action = QAction("Seleccionar párrafo", self)
        self.select_paragraph_action.triggered.connect(self._select_paragraph)

        self.paste_plain_action = QAction("Pegar texto sin formato", self)
        self.paste_plain_action.triggered.connect(self._paste_plain_text)

        self.clipboard_clear_action = QAction("Limpiar historial", self)
        self.clipboard_clear_action.triggered.connect(self._clear_clipboard)

        self.toggle_toolbar_action = QAction("Barra de herramientas", self)
        self.toggle_toolbar_action.setCheckable(True)
        self.toggle_toolbar_action.setChecked(True)
        self.toggle_toolbar_action.triggered.connect(self._toggle_toolbar)

        self.toggle_statusbar_action = QAction("Barra de estado", self)
        self.toggle_statusbar_action.setCheckable(True)
        self.toggle_statusbar_action.setChecked(True)
        self.toggle_statusbar_action.triggered.connect(self._toggle_statusbar)

        self.about_action = QAction("Acerca de rword", self)
        self.about_action.triggered.connect(self._show_about)

    def _build_menus(self) -> None:
        file_menu = self.menuBar().addMenu("&Archivo")
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(self.close_action)
        file_menu.addSeparator()
        file_menu.addAction(self.quit_action)

        edit_menu = self.menuBar().addMenu("&Edición")
        edit_menu.addAction(self.undo_action)
        edit_menu.addAction(self.redo_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.cut_action)
        edit_menu.addAction(self.copy_action)
        edit_menu.addAction(self.paste_action)
        self.clipboard_menu = edit_menu.addMenu("&Portapapeles")
        self._rebuild_clipboard_menu()
        edit_menu.addSeparator()
        edit_menu.addAction(self.find_action)
        edit_menu.addAction(self.find_next_action)
        edit_menu.addAction(self.find_previous_action)
        edit_menu.addAction(self.replace_action)
        edit_menu.addAction(self.go_to_action)
        edit_menu.addSeparator()
        select_menu = edit_menu.addMenu("&Seleccionar")
        select_menu.addAction(self.select_word_action)
        select_menu.addAction(self.select_line_action)
        select_menu.addAction(self.select_paragraph_action)
        select_menu.addAction(self.select_all_action)

        view_menu = self.menuBar().addMenu("&Ver")
        view_menu.addAction(self.toggle_toolbar_action)
        view_menu.addAction(self.toggle_statusbar_action)

        help_menu = self.menuBar().addMenu("&Ayuda")
        help_menu.addAction(self.about_action)

    def _build_toolbar(self) -> None:
        self.toolbar = QToolBar("Principal", self)
        self.toolbar.setObjectName("main_toolbar")
        self.toolbar.setMovable(False)
        self.toolbar.addAction(self.new_action)
        self.toolbar.addAction(self.open_action)
        self.toolbar.addAction(self.save_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.undo_action)
        self.toolbar.addAction(self.redo_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.cut_action)
        self.toolbar.addAction(self.copy_action)
        self.toolbar.addAction(self.paste_action)
        self.addToolBar(self.toolbar)

    def _build_statusbar(self) -> None:
        self.words_label = QLabel(self)
        self.chars_label = QLabel(self)
        self.modified_label = QLabel(self)
        self.statusBar().addPermanentWidget(self.words_label)
        self.statusBar().addPermanentWidget(self.chars_label)
        self.statusBar().addPermanentWidget(self.modified_label)

    def _connect_editor_signals(self) -> None:
        self._editor.document().modificationChanged.connect(
            self._on_modification_changed
        )
        self._editor.textChanged.connect(self._update_statusbar)
        self._editor.copyAvailable.connect(self.copy_action.setEnabled)
        self._editor.copyAvailable.connect(self.cut_action.setEnabled)
        self._editor.undoAvailable.connect(self.undo_action.setEnabled)
        self._editor.redoAvailable.connect(self.redo_action.setEnabled)

    def _connect_clipboard(self) -> None:
        self._clipboard = QApplication.clipboard()
        self._clipboard.dataChanged.connect(self._on_clipboard_changed)

    def _on_clipboard_changed(self) -> None:
        self._clipboard_history.add(self._clipboard.text())
        self._rebuild_clipboard_menu()

    def _rebuild_clipboard_menu(self) -> None:
        self.clipboard_menu.clear()
        items = self._clipboard_history.items
        if not items:
            action = self.clipboard_menu.addAction("(vacío)")
            action.setEnabled(False)
        else:
            for text in items:
                preview = text.replace("\n", " ").strip()
                if len(preview) > 40:
                    preview = preview[:40] + "…"
                action = self.clipboard_menu.addAction(f"Pegar: “{preview}”")
                action.triggered.connect(
                    lambda checked=False, t=text: self._paste_clipboard_item(t)
                )
        self.clipboard_menu.addSeparator()
        self.clipboard_menu.addAction(self.paste_plain_action)
        self.clipboard_menu.addAction(self.clipboard_clear_action)

    def _paste_clipboard_item(self, text: str) -> None:
        self._editor.insertPlainText(text)

    def _paste_plain_text(self) -> None:
        self._editor.insertPlainText(self._clipboard.text())

    def _clear_clipboard(self) -> None:
        self._clipboard_history.clear()
        self._rebuild_clipboard_menu()

    def _show_find_dialog(self) -> None:
        if self._find_dialog is None:
            self._find_dialog = FindReplaceDialog(self._editor, self)
        selected = self._editor.textCursor().selectedText()
        self._find_dialog.show_and_find(selected)

    def _show_go_to_dialog(self) -> None:
        if self._go_to_dialog is None:
            self._go_to_dialog = GoToDialog(self._editor, self)
        self._go_to_dialog.show()
        self._go_to_dialog.raise_()

    def _find_next(self) -> None:
        if self._find_dialog is None:
            self._show_find_dialog()
            return
        self._find_dialog.show()
        self._find_dialog._find_next()

    def _find_previous(self) -> None:
        if self._find_dialog is None:
            self._show_find_dialog()
            return
        self._find_dialog.show()
        self._find_dialog._find_previous()

    def _select_word(self) -> None:
        cursor = self._editor.textCursor()
        cursor.select(QTextCursor.SelectionType.WordUnderCursor)
        self._editor.setTextCursor(cursor)

    def _select_line(self) -> None:
        cursor = self._editor.textCursor()
        cursor.select(QTextCursor.SelectionType.LineUnderCursor)
        self._editor.setTextCursor(cursor)

    def _select_paragraph(self) -> None:
        cursor = self._editor.textCursor()
        cursor.select(QTextCursor.SelectionType.BlockUnderCursor)
        self._editor.setTextCursor(cursor)

    def _new_document(self) -> None:
        if not self._confirm_save_before_closing():
            return
        self._untitled_counter += 1
        self._editor.clear()
        self._editor.set_file_path(None)
        self._update_title()
        self._update_statusbar()

    def _open_document(self) -> None:
        if not self._confirm_save_before_closing():
            return
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Abrir documento", "", FILE_DIALOG_FILTER
        )
        if not file_name:
            return
        path = Path(file_name)
        try:
            self._editor.load_file(path)
        except (OSError, UnicodeDecodeError) as error:
            self._show_error(f"No se pudo abrir el archivo:\n{error}")
            return
        self._update_title()
        self._update_statusbar()

    def _save_document(self) -> None:
        if self._editor.file_path is None:
            self._save_document_as()
            return
        self._write_file(self._editor.file_path)

    def _save_document_as(self) -> None:
        default_name = self._suggested_name()
        file_name, selected_filter = QFileDialog.getSaveFileName(
            self, "Guardar documento como", default_name, FILE_DIALOG_FILTER
        )
        if not file_name:
            return
        path = Path(file_name)
        if path.suffix == "":
            if HTML_FILTER in selected_filter:
                path = path.with_suffix(".html")
            else:
                path = path.with_suffix(".txt")
        self._write_file(path)
        self._update_title()

    def _write_file(self, path: Path) -> None:
        try:
            self._editor.save_file(path)
        except OSError as error:
            self._show_error(f"No se pudo guardar el archivo:\n{error}")

    def _close_document(self) -> None:
        if not self._confirm_save_before_closing():
            return
        self._editor.clear()
        self._editor.set_file_path(None)
        self._untitled_counter = 0
        self._update_title()
        self._update_statusbar()

    def _suggested_name(self) -> str:
        if self._editor.file_path is not None:
            return self._editor.file_path.name
        return f"Sin título {self._untitled_counter}.txt"

    def _confirm_save_before_closing(self) -> bool:
        if not self._editor.document().isModified():
            return True
        answer = QMessageBox.question(
            self,
            "Cambios sin guardar",
            "El documento tiene cambios sin guardar. ¿Desea guardarlos?",
            QMessageBox.StandardButton.Save
            | QMessageBox.StandardButton.Discard
            | QMessageBox.StandardButton.Cancel,
        )
        if answer == QMessageBox.StandardButton.Save:
            self._save_document()
            return not self._editor.document().isModified()
        return answer != QMessageBox.StandardButton.Cancel

    def _show_error(self, message: str) -> None:
        QMessageBox.critical(self, APP_NAME, message)

    def _show_about(self) -> None:
        QMessageBox.about(
            self,
            f"Acerca de {APP_NAME}",
            f"{APP_NAME} {APP_VERSION}\n"
            "Procesador de texto profesional con integración de IA.",
        )

    def _toggle_toolbar(self, checked: bool) -> None:
        self.toolbar.setVisible(checked)

    def _toggle_statusbar(self, checked: bool) -> None:
        self.statusBar().setVisible(checked)

    def _update_title(self) -> None:
        name = self._editor.file_path.name if self._editor.file_path else "Sin título"
        modified = " *" if self._editor.document().isModified() else ""
        self.setWindowTitle(f"{name}{modified} - {APP_NAME}")

    def _on_modification_changed(self, modified: bool) -> None:
        self.modified_label.setText("Modificado" if modified else "")
        self._update_title()

    def _update_statusbar(self) -> None:
        self.words_label.setText(f"Palabras: {self._editor.word_count()}")
        self.chars_label.setText(f"Caracteres: {self._editor.character_count()}")

    def _restore_settings(self) -> None:
        geometry = self._settings.value(WINDOW_GEOMETRY_KEY)
        if geometry is not None:
            self.restoreGeometry(geometry)
        state = self._settings.value(WINDOW_STATE_KEY)
        if state is not None:
            self.restoreState(state)
        toolbar_visible = self._settings.value(TOOLBAR_VISIBLE_KEY, True, type=bool)
        self.toolbar.setVisible(toolbar_visible)
        self.toggle_toolbar_action.setChecked(toolbar_visible)
        statusbar_visible = self._settings.value(
            STATUSBAR_VISIBLE_KEY, True, type=bool
        )
        self.statusBar().setVisible(statusbar_visible)
        self.toggle_statusbar_action.setChecked(statusbar_visible)

    def closeEvent(self, event: QCloseEvent) -> None:
        if not self._confirm_save_before_closing():
            event.ignore()
            return
        self._settings.setValue(WINDOW_GEOMETRY_KEY, self.saveGeometry())
        self._settings.setValue(WINDOW_STATE_KEY, self.saveState())
        self._settings.setValue(
            TOOLBAR_VISIBLE_KEY, self.toolbar.isVisible()
        )
        self._settings.setValue(
            STATUSBAR_VISIBLE_KEY, self.statusBar().isVisible()
        )
        event.accept()

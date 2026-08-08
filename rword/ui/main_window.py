"""Ventana principal del editor."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QSettings, Qt
from PySide6.QtGui import QAction, QCloseEvent, QColor, QFont, QKeySequence, QTextCursor
from PySide6.QtWidgets import (
    QApplication,
    QColorDialog,
    QFileDialog,
    QFontDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QToolBar,
)

from rword.config import (
    ALL_FILES_FILTER,
    APP_NAME,
    APP_VERSION,
    FORMATBAR_VISIBLE_KEY,
    HTML_FILTER,
    PARAGRAPHBAR_VISIBLE_KEY,
    STATUSBAR_VISIBLE_KEY,
    TEXT_FILTER,
    TOOLBAR_VISIBLE_KEY,
    WINDOW_GEOMETRY_KEY,
    WINDOW_STATE_KEY,
)
from rword.core import formatting, paragraph
from rword.core.pages import apply_page_setup, current_page_setup
from rword.core.styles import FormatPainter, Style, StyleManager
from rword.core.tables import TABLE_STYLES
from rword.core.themes import ThemeManager, apply_theme
from rword.ui.comments_panel import CommentsPanel
from rword.ui.dialogs.clipboard_history import ClipboardHistory
from rword.ui.dialogs.find_replace import FindReplaceDialog
from rword.ui.dialogs.go_to import GoToDialog
from rword.ui.dialogs.header_footer import HeaderFooterDialog
from rword.ui.dialogs.image import AdjustDialog, CropDialog, ImageSizeDialog
from rword.ui.dialogs.insert_table import InsertTableDialog
from rword.ui.dialogs.page_setup import PageSetupDialog
from rword.ui.dialogs.paragraph import ParagraphDialog
from rword.ui.dialogs.shape import ShapeDialog, WordArtDialog
from rword.ui.dialogs.style import StyleDialog
from rword.ui.dialogs.style_organizer import StyleOrganizerDialog
from rword.ui.editor import Editor
from rword.ui.format_bar import FormatBar
from rword.ui.navigation_panel import NavigationPanel
from rword.ui.paragraph_bar import ParagraphBar

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
        self._paragraph_dialog: ParagraphDialog | None = None
        self._style_dialog: StyleDialog | None = None
        self._style_organizer: StyleOrganizerDialog | None = None
        self._clipboard_history = ClipboardHistory()
        self._style_manager = StyleManager(self._settings)
        self._theme_manager = ThemeManager(self._settings)
        self._format_painter = FormatPainter()
        self._navigation_panel: NavigationPanel | None = None
        self._comments_panel: CommentsPanel | None = None
        self.setCentralWidget(self._editor)
        self._build_actions()
        self._build_menus()
        self._build_toolbar()
        self._build_statusbar()
        self._new_document()
        self._connect_editor_signals()
        self._connect_clipboard()
        apply_theme(self._editor, self._theme_manager.current)
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

        self.font_action = QAction("Fuente...", self)
        self.font_action.triggered.connect(self._choose_font)

        self.bold_action = QAction("Negrita", self)
        self.bold_action.setShortcut(QKeySequence.StandardKey.Bold)
        self.bold_action.triggered.connect(
            lambda: formatting.toggle_bold(self._editor)
        )

        self.italic_action = QAction("Cursiva", self)
        self.italic_action.setShortcut(QKeySequence.StandardKey.Italic)
        self.italic_action.triggered.connect(
            lambda: formatting.toggle_italic(self._editor)
        )

        self.underline_action = QAction("Subrayado", self)
        self.underline_action.setShortcut(QKeySequence.StandardKey.Underline)
        self.underline_action.triggered.connect(
            lambda: formatting.toggle_underline(self._editor)
        )

        self.strike_action = QAction("Tachado", self)
        self.strike_action.triggered.connect(
            lambda: formatting.toggle_strikeout(self._editor)
        )

        self.superscript_action = QAction("Superíndice", self)
        self.superscript_action.triggered.connect(
            lambda: formatting.toggle_superscript(self._editor)
        )

        self.subscript_action = QAction("Subíndice", self)
        self.subscript_action.triggered.connect(
            lambda: formatting.toggle_subscript(self._editor)
        )

        self.grow_font_action = QAction("Aumentar tamaño", self)
        self.grow_font_action.setShortcut("Ctrl+Shift+>")
        self.grow_font_action.triggered.connect(
            lambda: formatting.change_font_size(self._editor, 1.0)
        )

        self.shrink_font_action = QAction("Disminuir tamaño", self)
        self.shrink_font_action.setShortcut("Ctrl+Shift+<")
        self.shrink_font_action.triggered.connect(
            lambda: formatting.change_font_size(self._editor, -1.0)
        )

        self.text_color_action = QAction("Color de texto...", self)
        self.text_color_action.triggered.connect(self._choose_text_color)

        self.highlight_action = QAction("Resaltado...", self)
        self.highlight_action.triggered.connect(self._choose_highlight)

        self.letter_spacing_normal_action = QAction("Espaciado normal", self)
        self.letter_spacing_normal_action.triggered.connect(
            lambda: formatting.set_letter_spacing(self._editor, 100)
        )

        self.letter_spacing_more_action = QAction("Aumentar espaciado", self)
        self.letter_spacing_more_action.triggered.connect(
            lambda: formatting.set_letter_spacing(self._editor, 120)
        )

        self.letter_spacing_less_action = QAction("Reducir espaciado", self)
        self.letter_spacing_less_action.triggered.connect(
            lambda: formatting.set_letter_spacing(self._editor, 80)
        )

        self.clear_format_action = QAction("Borrar formato", self)
        self.clear_format_action.triggered.connect(
            lambda: formatting.clear_formatting(self._editor)
        )

        self.case_sentence_action = QAction("Tipo oración", self)
        self.case_sentence_action.triggered.connect(
            lambda: formatting.apply_case(self._editor, "sentence")
        )

        self.case_lower_action = QAction("minúsculas", self)
        self.case_lower_action.triggered.connect(
            lambda: formatting.apply_case(self._editor, "lower")
        )

        self.case_upper_action = QAction("MAYÚSCULAS", self)
        self.case_upper_action.triggered.connect(
            lambda: formatting.apply_case(self._editor, "upper")
        )

        self.case_title_action = QAction("Tipo título", self)
        self.case_title_action.triggered.connect(
            lambda: formatting.apply_case(self._editor, "title")
        )

        self.case_toggle_action = QAction("Alternar mayúsculas", self)
        self.case_toggle_action.triggered.connect(
            lambda: formatting.apply_case(self._editor, "toggle")
        )

        self.paragraph_dialog_action = QAction("Párrafo...", self)
        self.paragraph_dialog_action.triggered.connect(self._show_paragraph_dialog)

        self.align_left_action = QAction("Alinear izquierda", self)
        self.align_left_action.setShortcut("Ctrl+L")
        self.align_left_action.triggered.connect(
            lambda: paragraph.set_alignment(self._editor, "left")
        )

        self.align_center_action = QAction("Centrar", self)
        self.align_center_action.setShortcut("Ctrl+E")
        self.align_center_action.triggered.connect(
            lambda: paragraph.set_alignment(self._editor, "center")
        )

        self.align_right_action = QAction("Alinear derecha", self)
        self.align_right_action.setShortcut("Ctrl+R")
        self.align_right_action.triggered.connect(
            lambda: paragraph.set_alignment(self._editor, "right")
        )

        self.align_justify_action = QAction("Justificar", self)
        self.align_justify_action.setShortcut("Ctrl+J")
        self.align_justify_action.triggered.connect(
            lambda: paragraph.set_alignment(self._editor, "justify")
        )

        self.indent_more_action = QAction("Aumentar sangría", self)
        self.indent_more_action.triggered.connect(
            lambda: paragraph.increase_indent(self._editor)
        )

        self.indent_less_action = QAction("Disminuir sangría", self)
        self.indent_less_action.triggered.connect(
            lambda: paragraph.decrease_indent(self._editor)
        )

        self.bullets_action = QAction("Viñetas", self)
        self.bullets_action.triggered.connect(
            lambda: paragraph.toggle_bullets(self._editor)
        )

        self.numbering_action = QAction("Numeración", self)
        self.numbering_action.triggered.connect(
            lambda: paragraph.toggle_numbering(self._editor)
        )

        self.spacing_single_action = QAction("Interlineado sencillo", self)
        self.spacing_single_action.triggered.connect(
            lambda: paragraph.set_line_spacing(self._editor, 1.0)
        )

        self.spacing_1_5_action = QAction("Interlineado 1,5", self)
        self.spacing_1_5_action.triggered.connect(
            lambda: paragraph.set_line_spacing(self._editor, 1.5)
        )

        self.spacing_double_action = QAction("Interlineado doble", self)
        self.spacing_double_action.triggered.connect(
            lambda: paragraph.set_line_spacing(self._editor, 2.0)
        )

        self.shading_clear_action = QAction("Sin sombreado", self)
        self.shading_clear_action.triggered.connect(self._clear_paragraph_shading)

        self.create_style_action = QAction("Nuevo estilo...", self)
        self.create_style_action.triggered.connect(self._create_style)

        self.modify_style_action = QAction("Modificar estilo actual...", self)
        self.modify_style_action.triggered.connect(self._modify_current_style)

        self.organizer_action = QAction("Organizador de estilos...", self)
        self.organizer_action.triggered.connect(self._show_style_organizer)

        self.painter_action = QAction("Pincel de formato", self)
        self.painter_action.setCheckable(True)
        self.painter_action.triggered.connect(self._toggle_format_painter)

        self.page_setup_action = QAction("Configurar página...", self)
        self.page_setup_action.triggered.connect(self._show_page_setup)

        self.page_break_action = QAction("Salto de página", self)
        self.page_break_action.setShortcut("Ctrl+Return")
        self.page_break_action.triggered.connect(self._insert_page_break)

        self.section_break_action = QAction("Salto de sección", self)
        self.section_break_action.triggered.connect(self._insert_section_break)

        self.columns_one_action = self._columns_action("Una columna", 1)
        self.columns_two_action = self._columns_action("Dos columnas", 2)
        self.columns_three_action = self._columns_action("Tres columnas", 3)

        self.line_numbers_action = QAction("Numeración de líneas", self)
        self.line_numbers_action.setCheckable(True)
        self.line_numbers_action.triggered.connect(self._toggle_line_numbers)

        self.watermark_action = QAction("Marca de agua...", self)
        self.watermark_action.triggered.connect(self._set_watermark)

        self._columns_action_labels = (
            self.columns_one_action,
            self.columns_two_action,
            self.columns_three_action,
        )

        self.insert_table_action = QAction("Insertar tabla...", self)
        self.insert_table_action.triggered.connect(self._insert_table)

        self.convert_text_to_table_action = QAction("Convertir texto en tabla", self)
        self.convert_text_to_table_action.triggered.connect(self._text_to_table)

        self.table_to_text_action = QAction("Convertir tabla en texto", self)
        self.table_to_text_action.triggered.connect(self._table_to_text)

        self.add_row_above_action = QAction("Agregar fila arriba", self)
        self.add_row_above_action.triggered.connect(self._add_row_above)

        self.add_row_below_action = QAction("Agregar fila abajo", self)
        self.add_row_below_action.triggered.connect(self._add_row_below)

        self.add_column_left_action = QAction("Agregar columna a la izquierda", self)
        self.add_column_left_action.triggered.connect(self._add_column_left)

        self.add_column_right_action = QAction("Agregar columna a la derecha", self)
        self.add_column_right_action.triggered.connect(self._add_column_right)

        self.delete_row_action = QAction("Eliminar fila", self)
        self.delete_row_action.triggered.connect(self._delete_row)

        self.delete_column_action = QAction("Eliminar columna", self)
        self.delete_column_action.triggered.connect(self._delete_column)

        self.delete_table_action = QAction("Eliminar tabla", self)
        self.delete_table_action.triggered.connect(self._delete_table)

        self.merge_cells_action = QAction("Combinar celdas", self)
        self.merge_cells_action.triggered.connect(self._merge_cells)

        self.split_cell_action = QAction("Dividir celda...", self)
        self.split_cell_action.triggered.connect(self._split_cell)

        self.split_table_action = QAction("Dividir tabla", self)
        self.split_table_action.triggered.connect(self._split_table)

        self.select_row_action = QAction("Seleccionar fila", self)
        self.select_row_action.triggered.connect(self._select_row)

        self.select_column_action = QAction("Seleccionar columna", self)
        self.select_column_action.triggered.connect(self._select_column)

        self.select_table_action = QAction("Seleccionar tabla", self)
        self.select_table_action.triggered.connect(self._select_table)

        self.autofit_action = QAction("Ajuste automático", self)
        self.autofit_action.triggered.connect(self._autofit)

        self.distribute_rows_action = QAction("Distribuir filas", self)
        self.distribute_rows_action.triggered.connect(self._distribute_rows)

        self.distribute_columns_action = QAction("Distribuir columnas", self)
        self.distribute_columns_action.triggered.connect(self._distribute_columns)

        self.sort_asc_action = QAction("Ordenar ascendente", self)
        self.sort_asc_action.triggered.connect(self._sort_table)

        self.sort_desc_action = QAction("Ordenar descendente", self)
        self.sort_desc_action.triggered.connect(self._sort_table_desc)

        self.sum_formula_action = QAction("Suma de columna", self)
        self.sum_formula_action.triggered.connect(
            lambda: self._table_formula("SUM")
        )

        self.average_formula_action = QAction("Promedio de columna", self)
        self.average_formula_action.triggered.connect(
            lambda: self._table_formula("AVERAGE")
        )

        self.count_formula_action = QAction("Contar celdas", self)
        self.count_formula_action.triggered.connect(
            lambda: self._table_formula("COUNT")
        )

        self.heading_repeat_action = QAction("Encabezado repetido", self)
        self.heading_repeat_action.setCheckable(True)
        self.heading_repeat_action.triggered.connect(self._toggle_heading_repeat)

        self.shade_cells_action = QAction("Sombreado de celdas...", self)
        self.shade_cells_action.triggered.connect(self._shade_cells)

        self.border_table_action = QAction("Bordes de tabla...", self)
        self.border_table_action.triggered.connect(self._set_table_border)

        self.table_styles_actions = {}
        for style_name in TABLE_STYLES:
            action = QAction(f"Estilo «{style_name}»", self)
            action.triggered.connect(
                lambda checked=False, s=style_name: self._set_table_style(s)
            )
            self.table_styles_actions[style_name] = action

        self.insert_image_action = QAction("Insertar imagen...", self)
        self.insert_image_action.triggered.connect(self._insert_image)

        self.image_size_action = QAction("Tamaño de imagen...", self)
        self.image_size_action.triggered.connect(self._image_size_dialog)

        self.image_crop_action = QAction("Recortar imagen...", self)
        self.image_crop_action.triggered.connect(self._crop_image)

        self.image_rotate_90_action = QAction("Girar 90°", self)
        self.image_rotate_90_action.triggered.connect(
            lambda: self._rotate_image(90)
        )

        self.image_rotate_180_action = QAction("Girar 180°", self)
        self.image_rotate_180_action.triggered.connect(
            lambda: self._rotate_image(180)
        )

        self.image_rotate_270_action = QAction("Girar 270°", self)
        self.image_rotate_270_action.triggered.connect(
            lambda: self._rotate_image(270)
        )

        self.image_flip_h_action = QAction("Voltear horizontal", self)
        self.image_flip_h_action.triggered.connect(
            lambda: self._flip_image(True)
        )

        self.image_flip_v_action = QAction("Voltear vertical", self)
        self.image_flip_v_action.triggered.connect(
            lambda: self._flip_image(False)
        )

        self.image_adjust_action = QAction("Brillo, contraste y saturación...", self)
        self.image_adjust_action.triggered.connect(self._adjust_image)

        self.image_grayscale_action = QAction("Escala de grises", self)
        self.image_grayscale_action.triggered.connect(self._grayscale_image)

        self.image_sepia_action = QAction("Efecto sepia", self)
        self.image_sepia_action.triggered.connect(self._sepia_image)

        self.image_replace_action = QAction("Reemplazar imagen...", self)
        self.image_replace_action.triggered.connect(self._replace_image)

        self.image_delete_action = QAction("Eliminar imagen", self)
        self.image_delete_action.triggered.connect(self._delete_image)

        self.shape_dialog_action = QAction("Insertar forma...", self)
        self.shape_dialog_action.triggered.connect(self._show_shape_dialog)

        self.text_box_action = QAction("Insertar cuadro de texto...", self)
        self.text_box_action.triggered.connect(self._insert_text_box)

        self.wordart_action = QAction("Insertar WordArt...", self)
        self.wordart_action.triggered.connect(self._show_wordart_dialog)

        self.shape_actions = {}
        for key, label in {
            "rectangle": "Rectángulo",
            "ellipse": "Círculo",
            "line": "Línea",
            "arrow": "Flecha",
        }.items():
            action = QAction(label, self)
            action.triggered.connect(
                lambda checked=False, k=key: self._insert_shape_quick(k)
            )
            self.shape_actions[key] = action

        self.insert_hyperlink_action = QAction("Hipervínculo...", self)
        self.insert_hyperlink_action.setShortcut("Ctrl+K")
        self.insert_hyperlink_action.triggered.connect(self._insert_hyperlink)

        self.remove_hyperlink_action = QAction("Eliminar hipervínculo", self)
        self.remove_hyperlink_action.triggered.connect(self._remove_hyperlink)

        self.add_bookmark_action = QAction("Marcador...", self)
        self.add_bookmark_action.triggered.connect(self._add_bookmark)

        self.go_to_bookmark_action = QAction("Ir a marcador...", self)
        self.go_to_bookmark_action.triggered.connect(self._goto_bookmark)

        self.delete_bookmark_action = QAction("Eliminar marcador...", self)
        self.delete_bookmark_action.triggered.connect(self._delete_bookmark)

        self.toggle_navigation_action = QAction("Panel de navegación", self)
        self.toggle_navigation_action.setCheckable(True)
        self.toggle_navigation_action.triggered.connect(
            self._toggle_navigation_panel
        )

        self.header_action = QAction("Encabezado...", self)
        self.header_action.triggered.connect(self._edit_header)

        self.footer_action = QAction("Pie de página...", self)
        self.footer_action.triggered.connect(self._edit_footer)

        self.page_number_action = QAction("Número de página", self)
        self.page_number_action.triggered.connect(
            lambda: self._insert_field("PAGE")
        )

        self.date_field_action = QAction("Fecha automática", self)
        self.date_field_action.triggered.connect(
            lambda: self._insert_field("DATE")
        )

        self.time_field_action = QAction("Hora automática", self)
        self.time_field_action.triggered.connect(
            lambda: self._insert_field("TIME")
        )

        self.file_field_action = QAction("Nombre del archivo", self)
        self.file_field_action.triggered.connect(
            lambda: self._insert_field("FILE")
        )

        self.path_field_action = QAction("Ruta del archivo", self)
        self.path_field_action.triggered.connect(
            lambda: self._insert_field("PATH")
        )

        self.refresh_fields_action = QAction("Actualizar campos", self)
        self.refresh_fields_action.triggered.connect(self._refresh_fields)

        self.remove_header_action = QAction("Eliminar encabezado", self)
        self.remove_header_action.triggered.connect(self._remove_header)

        self.remove_footer_action = QAction("Eliminar pie de página", self)
        self.remove_footer_action.triggered.connect(self._remove_footer)

        self.toc_action = QAction("Tabla de contenido", self)
        self.toc_action.triggered.connect(self._insert_toc)

        self.update_toc_action = QAction("Actualizar tabla de contenido", self)
        self.update_toc_action.triggered.connect(self._update_toc)

        self.footnote_action = QAction("Nota al pie...", self)
        self.footnote_action.triggered.connect(self._add_footnote)

        self.endnote_action = QAction("Nota al final...", self)
        self.endnote_action.triggered.connect(self._add_endnote)

        self.cross_reference_action = QAction("Referencia cruzada...", self)
        self.cross_reference_action.triggered.connect(self._insert_cross_reference)

        self.add_source_action = QAction("Nueva fuente...", self)
        self.add_source_action.triggered.connect(self._add_source)

        self.insert_citation_action = QAction("Insertar cita...", self)
        self.insert_citation_action.triggered.connect(self._insert_citation)

        self.bibliography_action = QAction("Bibliografía", self)
        self.bibliography_action.triggered.connect(self._insert_bibliography)

        self.caption_action = QAction("Leyenda...", self)
        self.caption_action.triggered.connect(self._insert_caption)

        self.table_of_figures_action = QAction("Tabla de ilustraciones", self)
        self.table_of_figures_action.triggered.connect(self._table_of_figures)

        self.mark_index_action = QAction("Marcar entrada de índice", self)
        self.mark_index_action.triggered.connect(self._mark_index)

        self.insert_index_action = QAction("Índice analítico", self)
        self.insert_index_action.triggered.connect(self._insert_index)

        self.add_comment_action = QAction("Nuevo comentario", self)
        self.add_comment_action.triggered.connect(self._add_comment)

        self.show_comments_action = QAction("Panel de comentarios", self)
        self.show_comments_action.setCheckable(True)
        self.show_comments_action.triggered.connect(
            self._toggle_comments_panel
        )

        self.track_changes_action = QAction("Control de cambios", self)
        self.track_changes_action.setCheckable(True)
        self.track_changes_action.triggered.connect(self._toggle_track_changes)

        self.accept_changes_action = QAction("Aceptar todos los cambios", self)
        self.accept_changes_action.triggered.connect(self._accept_all_changes)

        self.reject_changes_action = QAction("Rechazar todos los cambios", self)
        self.reject_changes_action.triggered.connect(self._reject_all_changes)

        self.compare_documents_action = QAction("Comparar documentos...", self)
        self.compare_documents_action.triggered.connect(self._compare_documents)

        self.toggle_toolbar_action = QAction("Barra de herramientas", self)
        self.toggle_toolbar_action.setCheckable(True)
        self.toggle_toolbar_action.setChecked(True)
        self.toggle_toolbar_action.triggered.connect(self._toggle_toolbar)

        self.toggle_formatbar_action = QAction("Barra de formato", self)
        self.toggle_formatbar_action.setCheckable(True)
        self.toggle_formatbar_action.setChecked(True)
        self.toggle_formatbar_action.triggered.connect(self._toggle_formatbar)

        self.toggle_paragraphbar_action = QAction("Barra de párrafo", self)
        self.toggle_paragraphbar_action.setCheckable(True)
        self.toggle_paragraphbar_action.setChecked(True)
        self.toggle_paragraphbar_action.triggered.connect(self._toggle_paragraphbar)

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

        format_menu = self.menuBar().addMenu("&Formato")
        format_menu.addAction(self.font_action)
        format_menu.addSeparator()
        format_menu.addAction(self.bold_action)
        format_menu.addAction(self.italic_action)
        format_menu.addAction(self.underline_action)
        format_menu.addAction(self.strike_action)
        format_menu.addAction(self.superscript_action)
        format_menu.addAction(self.subscript_action)
        format_menu.addSeparator()
        format_menu.addAction(self.grow_font_action)
        format_menu.addAction(self.shrink_font_action)
        format_menu.addSeparator()
        format_menu.addAction(self.text_color_action)
        format_menu.addAction(self.highlight_action)
        spacing_menu = format_menu.addMenu("Espaciado entre &caracteres")
        spacing_menu.addAction(self.letter_spacing_normal_action)
        spacing_menu.addAction(self.letter_spacing_more_action)
        spacing_menu.addAction(self.letter_spacing_less_action)
        case_menu = format_menu.addMenu("&Mayúsculas")
        case_menu.addAction(self.case_sentence_action)
        case_menu.addAction(self.case_lower_action)
        case_menu.addAction(self.case_upper_action)
        case_menu.addAction(self.case_title_action)
        case_menu.addAction(self.case_toggle_action)
        format_menu.addSeparator()
        format_menu.addAction(self.clear_format_action)
        paragraph_menu = format_menu.addMenu("&Párrafo")
        paragraph_menu.addAction(self.paragraph_dialog_action)
        paragraph_menu.addSeparator()
        paragraph_menu.addAction(self.align_left_action)
        paragraph_menu.addAction(self.align_center_action)
        paragraph_menu.addAction(self.align_right_action)
        paragraph_menu.addAction(self.align_justify_action)
        paragraph_menu.addSeparator()
        paragraph_menu.addAction(self.indent_more_action)
        paragraph_menu.addAction(self.indent_less_action)
        paragraph_menu.addSeparator()
        paragraph_menu.addAction(self.bullets_action)
        paragraph_menu.addAction(self.numbering_action)
        paragraph_menu.addSeparator()
        paragraph_menu.addAction(self.spacing_single_action)
        paragraph_menu.addAction(self.spacing_1_5_action)
        paragraph_menu.addAction(self.spacing_double_action)
        paragraph_menu.addSeparator()
        paragraph_menu.addAction(self.shading_clear_action)

        page_menu = format_menu.addMenu("&Página")
        page_menu.addAction(self.page_setup_action)
        page_menu.addSeparator()
        page_menu.addAction(self.page_break_action)
        page_menu.addAction(self.section_break_action)
        page_menu.addSeparator()
        columns_menu = page_menu.addMenu("&Columnas")
        columns_menu.addAction(self.columns_one_action)
        columns_menu.addAction(self.columns_two_action)
        columns_menu.addAction(self.columns_three_action)
        page_menu.addSeparator()
        page_menu.addAction(self.line_numbers_action)
        page_menu.addAction(self.watermark_action)

        styles_menu = self.menuBar().addMenu("&Estilos")
        self.styles_menu = styles_menu
        styles_menu.aboutToShow.connect(self._rebuild_styles_menu)
        styles_menu.addAction(self.create_style_action)
        styles_menu.addAction(self.modify_style_action)
        styles_menu.addAction(self.organizer_action)
        styles_menu.addSeparator()
        styles_menu.addAction(self.painter_action)

        table_menu = self.menuBar().addMenu("&Tabla")
        table_menu.addAction(self.insert_table_action)
        table_menu.addAction(self.convert_text_to_table_action)
        table_menu.addAction(self.table_to_text_action)
        table_menu.addSeparator()
        rows_menu = table_menu.addMenu("&Filas")
        rows_menu.addAction(self.add_row_above_action)
        rows_menu.addAction(self.add_row_below_action)
        rows_menu.addAction(self.delete_row_action)
        cols_menu = table_menu.addMenu("&Columnas")
        cols_menu.addAction(self.add_column_left_action)
        cols_menu.addAction(self.add_column_right_action)
        cols_menu.addAction(self.delete_column_action)
        cells_menu = table_menu.addMenu("&Celdas")
        cells_menu.addAction(self.merge_cells_action)
        cells_menu.addAction(self.split_cell_action)
        cells_menu.addAction(self.shade_cells_action)
        table_menu.addSeparator()
        table_menu.addAction(self.delete_table_action)
        table_menu.addAction(self.split_table_action)
        table_menu.addSeparator()
        select_menu = table_menu.addMenu("&Seleccionar")
        select_menu.addAction(self.select_row_action)
        select_menu.addAction(self.select_column_action)
        select_menu.addAction(self.select_table_action)
        table_menu.addSeparator()
        table_menu.addAction(self.autofit_action)
        table_menu.addAction(self.distribute_rows_action)
        table_menu.addAction(self.distribute_columns_action)
        table_menu.addAction(self.border_table_action)
        style_menu = table_menu.addMenu("&Estilos de tabla")
        for action in self.table_styles_actions.values():
            style_menu.addAction(action)
        table_menu.addSeparator()
        table_menu.addAction(self.sort_asc_action)
        table_menu.addAction(self.sort_desc_action)
        formula_menu = table_menu.addMenu("&Fórmula")
        formula_menu.addAction(self.sum_formula_action)
        formula_menu.addAction(self.average_formula_action)
        formula_menu.addAction(self.count_formula_action)
        table_menu.addSeparator()
        table_menu.addAction(self.heading_repeat_action)

        image_menu = self.menuBar().addMenu("&Imagen")
        image_menu.addAction(self.insert_image_action)
        image_menu.addSeparator()
        image_menu.addAction(self.image_size_action)
        image_menu.addAction(self.image_crop_action)
        rotate_menu = image_menu.addMenu("&Girar")
        rotate_menu.addAction(self.image_rotate_90_action)
        rotate_menu.addAction(self.image_rotate_180_action)
        rotate_menu.addAction(self.image_rotate_270_action)
        flip_menu = image_menu.addMenu("&Voltear")
        flip_menu.addAction(self.image_flip_h_action)
        flip_menu.addAction(self.image_flip_v_action)
        image_menu.addSeparator()
        image_menu.addAction(self.image_adjust_action)
        image_menu.addAction(self.image_grayscale_action)
        image_menu.addAction(self.image_sepia_action)
        image_menu.addSeparator()
        image_menu.addAction(self.image_replace_action)
        image_menu.addAction(self.image_delete_action)

        shapes_menu = self.menuBar().addMenu("&Formas")
        shapes_menu.addAction(self.shape_dialog_action)
        shapes_menu.addSeparator()
        for action in self.shape_actions.values():
            shapes_menu.addAction(action)
        shapes_menu.addSeparator()
        shapes_menu.addAction(self.text_box_action)
        shapes_menu.addAction(self.wordart_action)

        insert_menu = self.menuBar().addMenu("&Insertar")
        insert_menu.addAction(self.insert_table_action)
        insert_menu.addAction(self.insert_image_action)
        insert_menu.addAction(self.text_box_action)
        insert_menu.addAction(self.wordart_action)
        insert_menu.addSeparator()
        insert_menu.addAction(self.insert_hyperlink_action)
        bookmark_menu = insert_menu.addMenu("&Marcador")
        bookmark_menu.addAction(self.add_bookmark_action)
        bookmark_menu.addAction(self.go_to_bookmark_action)
        bookmark_menu.addAction(self.delete_bookmark_action)
        header_footer_menu = insert_menu.addMenu("&Encabezado y pie")
        header_footer_menu.addAction(self.header_action)
        header_footer_menu.addAction(self.footer_action)
        header_footer_menu.addSeparator()
        field_menu = header_footer_menu.addMenu("&Campos")
        field_menu.addAction(self.page_number_action)
        field_menu.addAction(self.date_field_action)
        field_menu.addAction(self.time_field_action)
        field_menu.addAction(self.file_field_action)
        field_menu.addAction(self.path_field_action)
        field_menu.addAction(self.refresh_fields_action)
        header_footer_menu.addSeparator()
        header_footer_menu.addAction(self.remove_header_action)
        header_footer_menu.addAction(self.remove_footer_action)

        references_menu = self.menuBar().addMenu("&Referencias")
        toc_menu = references_menu.addMenu("&Tabla de contenido")
        toc_menu.addAction(self.toc_action)
        toc_menu.addAction(self.update_toc_action)
        notes_menu = references_menu.addMenu("&Notas")
        notes_menu.addAction(self.footnote_action)
        notes_menu.addAction(self.endnote_action)
        references_menu.addAction(self.cross_reference_action)
        references_menu.addSeparator()
        citations_menu = references_menu.addMenu("&Citas y bibliografía")
        citations_menu.addAction(self.add_source_action)
        citations_menu.addAction(self.insert_citation_action)
        citations_menu.addAction(self.bibliography_action)
        references_menu.addSeparator()
        references_menu.addAction(self.caption_action)
        references_menu.addAction(self.table_of_figures_action)
        references_menu.addSeparator()
        references_menu.addAction(self.mark_index_action)
        references_menu.addAction(self.insert_index_action)

        review_menu = self.menuBar().addMenu("&Revisión")
        review_menu.addAction(self.add_comment_action)
        review_menu.addAction(self.show_comments_action)
        review_menu.addSeparator()
        review_menu.addAction(self.track_changes_action)
        review_menu.addAction(self.accept_changes_action)
        review_menu.addAction(self.reject_changes_action)
        review_menu.addSeparator()
        review_menu.addAction(self.compare_documents_action)

        view_menu = self.menuBar().addMenu("&Ver")
        view_menu.addAction(self.toggle_toolbar_action)
        view_menu.addAction(self.toggle_formatbar_action)
        view_menu.addAction(self.toggle_paragraphbar_action)
        view_menu.addAction(self.toggle_navigation_action)
        view_menu.addAction(self.toggle_statusbar_action)
        theme_menu = view_menu.addMenu("&Tema")
        self.theme_menu = theme_menu
        theme_menu.aboutToShow.connect(self._rebuild_theme_menu)

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
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.painter_action)
        self.addToolBar(self.toolbar)

        self.format_bar = FormatBar(self._editor, self)
        self.addToolBar(self.format_bar)

        self.paragraph_bar = ParagraphBar(self._editor, self)
        self.addToolBar(self.paragraph_bar)

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

    def _toggle_formatbar(self, checked: bool) -> None:
        self.format_bar.setVisible(checked)

    def _toggle_paragraphbar(self, checked: bool) -> None:
        self.paragraph_bar.setVisible(checked)

    def _show_paragraph_dialog(self) -> None:
        if self._paragraph_dialog is None:
            self._paragraph_dialog = ParagraphDialog(self._editor, self)
        self._paragraph_dialog._load_current()
        self._paragraph_dialog.show()
        self._paragraph_dialog.raise_()

    def _clear_paragraph_shading(self) -> None:
        from PySide6.QtGui import QColor

        paragraph.set_paragraph_shading(self._editor, QColor("transparent"))

    def _rebuild_styles_menu(self) -> None:
        styles_menu = self.styles_menu
        for action in styles_menu.actions():
            if action not in (
                self.create_style_action,
                self.modify_style_action,
                self.organizer_action,
                self.painter_action,
            ) and action.menu() is None:
                styles_menu.removeAction(action)
        for name in sorted(self._style_manager.names()):
            action = QAction(name, self)
            action.triggered.connect(
                lambda checked=False, n=name: self._apply_style(n)
            )
            styles_menu.insertAction(
                self.create_style_action, action
            )

    def _apply_style(self, name: str) -> None:
        style = self._style_manager.get(name)
        from rword.core.styles import apply_style

        apply_style(self._editor, style)

    def _create_style(self) -> None:
        dialog = StyleDialog(parent=self)
        if dialog.exec():
            style = dialog.style()
            if style.name and style.name not in self._style_manager.names():
                self._style_manager.add(style)
                self._apply_style(style.name)

    def _modify_current_style(self) -> None:
        current = self._editor.currentCharFormat()
        sample = Style(
            name="",
            font_family=current.fontFamilies()[0] if current.fontFamilies() else "Sans Serif",
            font_size=current.fontPointSize() or 12.0,
            bold=current.fontWeight() >= 700,
            italic=current.fontItalic(),
            color=current.foreground().color().name(),
        )
        dialog = StyleDialog(sample, self)
        if dialog.exec():
            style = dialog.style()
            if style.name and style.name not in self._style_manager.names():
                self._style_manager.add(style)
                self._apply_style(style.name)

    def _show_style_organizer(self) -> None:
        if self._style_organizer is None:
            self._style_organizer = StyleOrganizerDialog(
                self._style_manager, self
            )
        self._style_organizer._reload()
        self._style_organizer.show()
        self._style_organizer.raise_()

    def _toggle_format_painter(self, checked: bool) -> None:
        if checked:
            self._format_painter.capture(self._editor)
        else:
            self._format_painter.clear()

    def _columns_action(self, label, count):
        action = QAction(label, self)
        action.setCheckable(True)
        action.triggered.connect(lambda checked, n=count: self._set_columns(n))
        return action

    def _set_columns(self, count: int) -> None:
        from rword.core.pages import set_columns

        set_columns(self._editor, count)
        for action, index in zip(
            self._columns_action_labels, (1, 2, 3), strict=True
        ):
            action.setChecked(index == count)

    def _show_page_setup(self) -> None:
        setup = current_page_setup(self._editor)
        from PySide6.QtGui import QPalette

        setup.page_color = self._editor.palette().color(
            QPalette.ColorRole.Base
        ).name()
        dialog = PageSetupDialog(setup, self)
        if dialog.exec():
            new_setup = dialog.setup()
            apply_page_setup(self._editor, new_setup)
            palette = self._editor.palette()
            palette.setColor(QPalette.ColorRole.Base, QColor(new_setup.page_color))
            self._editor.setPalette(palette)
            self._editor.set_watermark(new_setup.watermark)

    def _insert_page_break(self) -> None:
        from rword.core.pages import insert_page_break

        insert_page_break(self._editor)

    def _insert_section_break(self) -> None:
        from rword.core.pages import insert_section_break

        insert_section_break(self._editor)

    def _toggle_line_numbers(self, checked: bool) -> None:
        self._editor.set_line_numbers_enabled(checked)

    def _set_watermark(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        current = self._editor.watermark()
        text, ok = QInputDialog.getText(
            self, "Marca de agua", "Texto de la marca de agua:", text=current
        )
        if ok:
            self._editor.set_watermark(text)

    def _insert_table(self) -> None:
        dialog = InsertTableDialog(self)
        if dialog.exec():
            from rword.core.tables import insert_table

            insert_table(self._editor, dialog.rows(), dialog.columns(), dialog.style_name())

    def _text_to_table(self) -> None:
        from rword.core.tables import text_to_table

        text_to_table(self._editor, "\t")

    def _table_to_text(self) -> None:
        from rword.core.tables import table_to_text

        table_to_text(self._editor)

    def _add_row_above(self) -> None:
        from rword.core.tables import add_row_before

        add_row_before(self._editor)

    def _add_row_below(self) -> None:
        from rword.core.tables import add_row_after

        add_row_after(self._editor)

    def _add_column_left(self) -> None:
        from rword.core.tables import add_column_before

        add_column_before(self._editor)

    def _add_column_right(self) -> None:
        from rword.core.tables import add_column_after

        add_column_after(self._editor)

    def _delete_row(self) -> None:
        from rword.core.tables import delete_row

        delete_row(self._editor)

    def _delete_column(self) -> None:
        from rword.core.tables import delete_column

        delete_column(self._editor)

    def _delete_table(self) -> None:
        from rword.core.tables import delete_table

        delete_table(self._editor)

    def _merge_cells(self) -> None:
        from rword.core.tables import merge_cells

        merge_cells(self._editor)

    def _split_cell(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        rows, ok = QInputDialog.getInt(self, "Dividir celda", "Número de filas:", 2, 1, 20)
        if not ok:
            return
        columns, ok = QInputDialog.getInt(self, "Dividir celda", "Número de columnas:", 2, 1, 20)
        if ok:
            from rword.core.tables import split_cell

            split_cell(self._editor, rows, columns)

    def _split_table(self) -> None:
        from rword.core.tables import split_table

        split_table(self._editor)

    def _select_row(self) -> None:
        from rword.core.tables import select_row

        select_row(self._editor)

    def _select_column(self) -> None:
        from rword.core.tables import select_column

        select_column(self._editor)

    def _select_table(self) -> None:
        from rword.core.tables import select_table

        select_table(self._editor)

    def _autofit(self) -> None:
        from rword.core.tables import autofit

        autofit(self._editor)

    def _distribute_rows(self) -> None:
        from rword.core.tables import set_row_height_equal

        set_row_height_equal(self._editor)

    def _distribute_columns(self) -> None:
        from rword.core.tables import set_column_width_equal

        set_column_width_equal(self._editor)

    def _sort_table(self) -> None:
        from rword.core.tables import sort_current_column

        sort_current_column(self._editor, ascending=True)

    def _sort_table_desc(self) -> None:
        from rword.core.tables import sort_current_column

        sort_current_column(self._editor, ascending=False)

    def _table_formula(self, function: str) -> None:
        from rword.core.tables import table_formula

        table_formula(self._editor, function)

    def _toggle_heading_repeat(self, checked: bool) -> None:
        from rword.core.tables import set_heading_row_repeat

        set_heading_row_repeat(self._editor, checked)

    def _shade_cells(self) -> None:
        from PySide6.QtGui import QColor
        from PySide6.QtWidgets import QColorDialog

        color = QColorDialog.getColor(QColor("#f2f2f2"), self, "Sombreado de celdas")
        if color.isValid():
            from rword.core.tables import set_cell_shading

            set_cell_shading(self._editor, color)

    def _set_table_border(self) -> None:
        from PySide6.QtGui import QColor
        from PySide6.QtWidgets import QColorDialog, QInputDialog

        color = QColorDialog.getColor(QColor("black"), self, "Color de borde")
        if not color.isValid():
            return
        width, ok = QInputDialog.getDouble(self, "Bordes de tabla", "Grosor:", 1.0, 0.0, 20.0, 1)
        if ok:
            from rword.core.tables import set_table_border

            set_table_border(self._editor, color, width)

    def _set_table_style(self, style_name: str) -> None:
        from rword.core.tables import set_table_style

        set_table_style(self._editor, style_name)

    def _insert_image(self) -> None:
        from rword.core.images import insert_image

        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Insertar imagen",
            "",
            "Imágenes (*.png *.jpg *.jpeg *.bmp *.gif *.svg);;Todos los archivos (*)",
        )
        if file_name and not insert_image(self._editor, file_name):
            self._show_error("No se pudo cargar la imagen.")

    def _image_size_dialog(self) -> None:
        from rword.core.images import current_image_size, set_image_size

        size = current_image_size(self._editor)
        if size is None:
            self._show_error("Coloque el cursor sobre una imagen.")
            return
        dialog = ImageSizeDialog(*size, self)
        if dialog.exec():
            set_image_size(self._editor, dialog.width(), dialog.height())

    def _crop_image(self) -> None:
        from rword.core.images import crop_image, current_image_size

        size = current_image_size(self._editor)
        if size is None:
            self._show_error("Coloque el cursor sobre una imagen.")
            return
        dialog = CropDialog(*size, self)
        if dialog.exec():
            crop_image(self._editor, dialog.rect())

    def _rotate_image(self, degrees: int) -> None:
        from rword.core.images import rotate_image

        rotate_image(self._editor, degrees)

    def _flip_image(self, horizontal: bool) -> None:
        from rword.core.images import flip_image

        flip_image(self._editor, horizontal)

    def _adjust_image(self) -> None:
        from rword.core.images import adjust_pixels

        dialog = AdjustDialog(self)
        if dialog.exec():
            brightness, contrast, saturation = dialog.values()
            adjust_pixels(self._editor, brightness, contrast, saturation)

    def _grayscale_image(self) -> None:
        from rword.core.images import adjust_pixels

        adjust_pixels(self._editor, grayscale=True)

    def _sepia_image(self) -> None:
        from rword.core.images import adjust_pixels

        adjust_pixels(self._editor, sepia=True)

    def _replace_image(self) -> None:
        from rword.core.images import replace_image

        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Reemplazar imagen",
            "",
            "Imágenes (*.png *.jpg *.jpeg *.bmp *.gif);;Todos los archivos (*)",
        )
        if file_name and not replace_image(self._editor, file_name):
            self._show_error("No se pudo reemplazar la imagen.")

    def _delete_image(self) -> None:
        from rword.core.images import delete_image

        delete_image(self._editor)

    def _show_shape_dialog(self) -> None:
        dialog = ShapeDialog(self)
        if dialog.exec():
            from rword.core.shapes import insert_shape

            values = dialog.values()
            insert_shape(
                self._editor,
                values["kind"],
                values["width"],
                values["height"],
                values["fill"],
                values["border"],
            )

    def _insert_shape_quick(self, kind: str) -> None:
        from rword.core.shapes import insert_shape

        insert_shape(self._editor, kind)

    def _insert_text_box(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        from rword.core.shapes import insert_text_box

        text, ok = QInputDialog.getText(
            self, "Cuadro de texto", "Texto del cuadro:"
        )
        if ok:
            insert_text_box(self._editor, text)

    def _show_wordart_dialog(self) -> None:
        dialog = WordArtDialog(self)
        if dialog.exec():
            from rword.core.shapes import insert_wordart

            text, style = dialog.values()
            if not insert_wordart(self._editor, text, style):
                self._show_error("Introduzca un texto para el WordArt.")

    def _insert_hyperlink(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        from rword.core.hyperlinks import insert_hyperlink

        selected = self._editor.textCursor().selectedText()
        text, ok = QInputDialog.getText(
            self, "Hipervínculo", "Texto a mostrar:", text=selected
        )
        if not ok:
            return
        url, ok = QInputDialog.getText(
            self, "Hipervínculo", "Dirección (https://, mailto: o #marcador):"
        )
        if ok and text:
            insert_hyperlink(self._editor, text, url)

    def _remove_hyperlink(self) -> None:
        from rword.core.hyperlinks import remove_hyperlink

        remove_hyperlink(self._editor)

    def _add_bookmark(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        from rword.core.hyperlinks import add_bookmark

        name, ok = QInputDialog.getText(self, "Marcador", "Nombre del marcador:")
        if ok:
            add_bookmark(self._editor, name)
            self._refresh_navigation()

    def _goto_bookmark(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        from rword.core.hyperlinks import bookmarks, goto_bookmark

        names = sorted(bookmarks(self._editor))
        if not names:
            self._show_error("No hay marcadores definidos.")
            return
        name, ok = QInputDialog.getItem(
            self, "Ir a marcador", "Marcador:", names, 0, False
        )
        if ok:
            goto_bookmark(self._editor, name)

    def _delete_bookmark(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        from rword.core.hyperlinks import bookmarks, remove_bookmark

        names = sorted(bookmarks(self._editor))
        if not names:
            self._show_error("No hay marcadores definidos.")
            return
        name, ok = QInputDialog.getItem(
            self, "Eliminar marcador", "Marcador:", names, 0, False
        )
        if ok:
            remove_bookmark(self._editor, name)
            self._refresh_navigation()

    def _toggle_navigation_panel(self, checked: bool) -> None:
        if self._navigation_panel is None:
            self._navigation_panel = NavigationPanel(self._editor, self)
            self.addDockWidget(
                Qt.DockWidgetArea.RightDockWidgetArea, self._navigation_panel
            )
        self._navigation_panel.setVisible(checked)

    def _refresh_navigation(self) -> None:
        if self._navigation_panel is not None:
            self._navigation_panel.refresh()

    def _edit_header(self) -> None:
        from rword.core.headers import apply_header, set_numbering_format

        dialog = HeaderFooterDialog("Encabezado de página", parent=self)
        if dialog.exec():
            apply_header(self._editor, dialog.template())
            set_numbering_format(self._editor, dialog.numbering_format())

    def _edit_footer(self) -> None:
        from rword.core.headers import apply_footer, set_numbering_format

        dialog = HeaderFooterDialog("Pie de página", parent=self)
        if dialog.exec():
            apply_footer(self._editor, dialog.template())
            set_numbering_format(self._editor, dialog.numbering_format())

    def _insert_field(self, kind: str) -> None:
        from rword.core.headers import insert_field

        insert_field(self._editor, kind)

    def _refresh_fields(self) -> None:
        from rword.core.headers import refresh_fields

        refresh_fields(self._editor)

    def _remove_header(self) -> None:
        from rword.core.headers import remove_header

        remove_header(self._editor)

    def _remove_footer(self) -> None:
        from rword.core.headers import remove_footer

        remove_footer(self._editor)

    def _insert_toc(self) -> None:
        from rword.core.references import insert_toc

        insert_toc(self._editor)

    def _update_toc(self) -> None:
        from rword.core.references import update_toc

        update_toc(self._editor)

    def _add_footnote(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        from rword.core.references import add_footnote

        text, ok = QInputDialog.getMultiLineText(
            self, "Nota al pie", "Texto de la nota:"
        )
        if ok and text:
            add_footnote(self._editor, text)

    def _add_endnote(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        from rword.core.references import add_endnote

        text, ok = QInputDialog.getMultiLineText(
            self, "Nota al final", "Texto de la nota:"
        )
        if ok and text:
            add_endnote(self._editor, text)

    def _insert_cross_reference(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        from rword.core.references import insert_cross_reference

        target, ok = QInputDialog.getText(
            self, "Referencia cruzada", "Título o marcador de destino:"
        )
        if ok and target:
            insert_cross_reference(self._editor, target)

    def _add_source(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        from rword.core.references import add_source

        author, ok = QInputDialog.getText(self, "Nueva fuente", "Autor:")
        if not ok:
            return
        year, ok = QInputDialog.getText(self, "Nueva fuente", "Año:")
        if not ok:
            return
        title, ok = QInputDialog.getText(self, "Nueva fuente", "Título:")
        if ok:
            add_source(self._editor, author, year, title)

    def _insert_citation(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        from rword.core.references import insert_citation, sources

        entries = sources(self._editor)
        if not entries:
            self._show_error("No hay fuentes guardadas. Añada una fuente primero.")
            return
        labels = [f"{s['author']} ({s['year']})" for s in entries]
        label, ok = QInputDialog.getItem(
            self, "Insertar cita", "Fuente:", labels, 0, False
        )
        if ok:
            author, year = label.rsplit(" (", 1)
            insert_citation(self._editor, author, year[:-1])

    def _insert_bibliography(self) -> None:
        from rword.core.references import insert_bibliography

        insert_bibliography(self._editor)

    def _insert_caption(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        from rword.core.references import insert_caption

        text, ok = QInputDialog.getText(
            self, "Leyenda", "Texto de la leyenda:"
        )
        if ok and text:
            insert_caption(self._editor, text)

    def _table_of_figures(self) -> None:
        from rword.core.references import insert_table_of_figures

        insert_table_of_figures(self._editor)

    def _mark_index(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        from rword.core.references import mark_index_entry

        entry, ok = QInputDialog.getText(
            self, "Marcar entrada de índice", "Entrada:"
        )
        if ok and entry:
            mark_index_entry(self._editor, entry)

    def _insert_index(self) -> None:
        from rword.core.references import insert_index

        insert_index(self._editor)

    def _add_comment(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        from rword.core import comments

        text, ok = QInputDialog.getMultiLineText(
            self, "Nuevo comentario", "Texto del comentario:"
        )
        if ok and text:
            comments.add_comment(self._editor, text)
            comments.refresh_comment_highlights(self._editor)
            self._refresh_comments_panel()

    def _toggle_comments_panel(self, checked: bool) -> None:
        if self._comments_panel is None:
            self._comments_panel = CommentsPanel(self._editor, self)
            self.addDockWidget(
                Qt.DockWidgetArea.RightDockWidgetArea, self._comments_panel
            )
        self._comments_panel.setVisible(checked)

    def _refresh_comments_panel(self) -> None:
        if self._comments_panel is not None:
            self._comments_panel.refresh()

    def _toggle_track_changes(self, checked: bool) -> None:
        self._editor.set_track_changes(checked)

    def _accept_all_changes(self) -> None:
        from rword.core.comments import accept_all_changes

        accept_all_changes(self._editor)

    def _reject_all_changes(self) -> None:
        from rword.core.comments import reject_all_changes

        reject_all_changes(self._editor)

    def _compare_documents(self) -> None:
        from rword.core.comments import compare_documents

        original_path, _ = QFileDialog.getOpenFileName(
            self, "Documento original", "", FILE_DIALOG_FILTER
        )
        if not original_path:
            return
        modified_path, _ = QFileDialog.getOpenFileName(
            self, "Documento modificado", "", FILE_DIALOG_FILTER
        )
        if not modified_path:
            return
        try:
            original = Path(original_path).read_text(encoding="utf-8")
            modified = Path(modified_path).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as error:
            self._show_error(f"No se pudieron leer los documentos:\n{error}")
            return
        compare_documents(self._editor, original, modified)

    def _rebuild_theme_menu(self) -> None:
        theme_menu = self.theme_menu
        for action in list(theme_menu.actions()):
            theme_menu.removeAction(action)
        for name in self._theme_manager.names():
            action = QAction(name, self)
            action.setCheckable(True)
            action.setChecked(name == self._theme_manager.current_name)
            action.triggered.connect(
                lambda checked=False, n=name: self._apply_theme(n)
            )
            theme_menu.addAction(action)

    def _apply_theme(self, name: str) -> None:
        theme = self._theme_manager.get(name)
        self._theme_manager.set_current(name)
        apply_theme(self._editor, theme)

    def _connect_editor_signals(self) -> None:
        self._editor.document().modificationChanged.connect(
            self._on_modification_changed
        )
        self._editor.textChanged.connect(self._update_statusbar)
        self._editor.copyAvailable.connect(self.copy_action.setEnabled)
        self._editor.copyAvailable.connect(self.cut_action.setEnabled)
        self._editor.undoAvailable.connect(self.undo_action.setEnabled)
        self._editor.redoAvailable.connect(self.redo_action.setEnabled)
        self._editor.cursorPositionChanged.connect(
            self._on_painter_cursor_move
        )
        self._editor.link_clicked.connect(self._on_link_clicked)

    def _on_link_clicked(self, href: str) -> None:
        if href.startswith("#"):
            from rword.core.hyperlinks import goto_bookmark

            goto_bookmark(self._editor, href[1:])
            return
        from PySide6.QtCore import QUrl
        from PySide6.QtGui import QDesktopServices

        QDesktopServices.openUrl(QUrl(href))

    def _on_painter_cursor_move(self) -> None:
        if self._format_painter.active:
            self._format_painter.apply(self._editor)
            self._format_painter.clear()
            self.painter_action.setChecked(False)

    def _choose_font(self) -> None:
        current = self._editor.currentCharFormat()
        family = current.fontFamilies()[0] if current.fontFamilies() else "Sans Serif"
        size = current.fontPointSize() or 12
        ok, font = QFontDialog.getFont(
            QFont(family, int(size)), self, "Fuente"
        )
        if ok:
            formatting.set_font_family(self._editor, font.family())
            formatting.set_font_size(self._editor, font.pointSizeF())
            if font.bold():
                formatting.toggle_bold(self._editor)

    def _choose_text_color(self) -> None:
        color = QColorDialog.getColor(QColor("black"), self, "Color de texto")
        if color.isValid():
            formatting.set_text_color(self._editor, color)

    def _choose_highlight(self) -> None:
        color = QColorDialog.getColor(QColor("#ffff00"), self, "Color de resaltado")
        if color.isValid():
            formatting.set_highlight(self._editor, color)

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
        formatbar_visible = self._settings.value(FORMATBAR_VISIBLE_KEY, True, type=bool)
        self.format_bar.setVisible(formatbar_visible)
        self.toggle_formatbar_action.setChecked(formatbar_visible)
        paragraphbar_visible = self._settings.value(
            PARAGRAPHBAR_VISIBLE_KEY, True, type=bool
        )
        self.paragraph_bar.setVisible(paragraphbar_visible)
        self.toggle_paragraphbar_action.setChecked(paragraphbar_visible)
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
            FORMATBAR_VISIBLE_KEY, self.format_bar.isVisible()
        )
        self._settings.setValue(
            PARAGRAPHBAR_VISIBLE_KEY, self.paragraph_bar.isVisible()
        )
        self._settings.setValue(
            STATUSBAR_VISIBLE_KEY, self.statusBar().isVisible()
        )
        event.accept()

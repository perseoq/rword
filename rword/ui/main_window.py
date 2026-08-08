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
    QGridLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMenu,
    QMessageBox,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from rword.config import (
    ALL_FILES_FILTER,
    APP_NAME,
    APP_VERSION,
    HTML_FILTER,
    RIBBON_VISIBLE_KEY,
    STATUSBAR_VISIBLE_KEY,
    TEXT_FILTER,
    WINDOW_GEOMETRY_KEY,
    WINDOW_STATE_KEY,
)
from rword.core import formatting, paragraph
from rword.core.assist import AGENTS
from rword.core.export import (
    export_epub,
    export_html,
    export_odt,
    export_pdf,
    export_rtf,
    export_text,
)
from rword.core.margin_templates import (
    STANDARD_TEMPLATES,
    MarginTemplateStore,
    apply_margins,
)
from rword.core.pages import apply_page_setup, current_page_setup
from rword.core.preferences import DARK_STYLESHEET
from rword.core.styles import FormatPainter, Style, StyleManager
from rword.core.tables import TABLE_STYLES
from rword.core.themes import ThemeManager, apply_theme
from rword.ui.comments_panel import CommentsPanel
from rword.ui.dialogs.clipboard_history import ClipboardHistory
from rword.ui.dialogs.count import CountDialog
from rword.ui.dialogs.find_replace import FindReplaceDialog
from rword.ui.dialogs.go_to import GoToDialog
from rword.ui.dialogs.header_footer import HeaderFooterDialog
from rword.ui.dialogs.image import AdjustDialog, CropDialog, ImageSizeDialog
from rword.ui.dialogs.insert_table import InsertTableDialog
from rword.ui.dialogs.margin_templates import (
    MarginTemplateManagerDialog,
    SaveMarginTemplateDialog,
)
from rword.ui.dialogs.objects import (
    ChartDialog,
    EquationDialog,
    SmartArtDialog,
    SymbolDialog,
)
from rword.ui.dialogs.page_setup import PageSetupDialog
from rword.ui.dialogs.paragraph import ParagraphDialog
from rword.ui.dialogs.shape import ShapeDialog, WordArtDialog
from rword.ui.dialogs.style import StyleDialog
from rword.ui.dialogs.style_organizer import StyleOrganizerDialog
from rword.ui.dialogs.thesaurus import ThesaurusDialog
from rword.ui.editor import Editor
from rword.ui.format_bar import FormatBar
from rword.ui.icons import IconManager, icon_color_for
from rword.ui.navigation_panel import NavigationPanel
from rword.ui.paragraph_bar import ParagraphBar
from rword.ui.ribbon import RibbonBar

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
        self._ai_chat_panel = None

        from rword.ui.page_view import PageView
        from rword.ui.ruler import HRuler, VRuler

        self._ruler = HRuler(self._editor, self)
        self._vruler = VRuler(self._editor, self)
        self._page_view = PageView(self._editor, self)

        self._corner = QWidget(self)
        self._corner.setFixedSize(24, 24)
        from PySide6.QtGui import QPalette as _Palette

        corner_palette = self._corner.palette()
        corner_palette.setColor(_Palette.ColorRole.Window, QColor("#eaeaea"))
        self._corner.setAutoFillBackground(True)
        self._corner.setPalette(corner_palette)

        self._central = QWidget(self)
        self._central_layout = QGridLayout(self._central)
        self._central_layout.setContentsMargins(0, 0, 0, 0)
        self._central_layout.setSpacing(0)
        self._central_layout.addWidget(self._corner, 0, 0)
        self._central_layout.addWidget(self._ruler, 0, 1)
        self._central_layout.addWidget(self._vruler, 1, 0)
        self._central_layout.addWidget(self._page_view, 1, 1)

        self._root = QWidget(self)
        self._root_layout = QVBoxLayout(self._root)
        self._root_layout.setContentsMargins(0, 0, 0, 0)
        self._root_layout.setSpacing(0)
        self._root_layout.addWidget(self._central, 1)
        self.setCentralWidget(self._root)
        self._splitter: QSplitter | None = None
        self._build_actions()
        self._icon_manager = IconManager(icon_color_for(self))
        self._margin_store = MarginTemplateStore(self._settings)
        self._build_ribbon()
        self._build_statusbar()
        self._new_document()
        self._connect_editor_signals()
        self._connect_clipboard()
        apply_theme(self._editor, self._theme_manager.current)
        self._page_view.update_paper_color(
            self._theme_manager.current.page_color
        )
        self._plugin_manager.load_enabled(self)
        self._apply_saved_preferences()
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

        self.print_action = QAction("Imprimir...", self)
        self.print_action.setShortcut(QKeySequence.StandardKey.Print)
        self.print_action.triggered.connect(self._print_document)

        self.print_preview_action = QAction("Vista previa de impresión...", self)
        self.print_preview_action.triggered.connect(self._print_preview)

        self.export_pdf_action = QAction("Exportar a PDF...", self)
        self.export_pdf_action.triggered.connect(
            lambda: self._export("PDF", "*.pdf", export_pdf)
        )

        self.export_html_action = QAction("Exportar a HTML...", self)
        self.export_html_action.triggered.connect(
            lambda: self._export("HTML", "*.html *.htm", export_html)
        )

        self.export_text_action = QAction("Exportar a texto...", self)
        self.export_text_action.triggered.connect(
            lambda: self._export("texto", "*.txt", export_text)
        )

        self.export_rtf_action = QAction("Exportar a RTF...", self)
        self.export_rtf_action.triggered.connect(
            lambda: self._export("RTF", "*.rtf", export_rtf)
        )

        self.export_odt_action = QAction("Exportar a ODT...", self)
        self.export_odt_action.triggered.connect(
            lambda: self._export("ODT", "*.odt", export_odt)
        )

        self.export_epub_action = QAction("Exportar a EPUB...", self)
        self.export_epub_action.triggered.connect(
            lambda: self._export("EPUB", "*.epub", export_epub)
        )

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
        self.columns_more_action = QAction("Más columnas...", self)
        self.columns_more_action.triggered.connect(self._columns_more)

        self.page_color_action = QAction("Color de página...", self)
        self.page_color_action.triggered.connect(self._choose_page_color)

        self.save_margin_template_action = QAction(
            "Guardar márgenes como plantilla...", self
        )
        self.save_margin_template_action.triggered.connect(
            self._save_margin_template
        )

        self.manage_margin_templates_action = QAction(
            "Administrar plantillas de márgenes...", self
        )
        self.manage_margin_templates_action.triggered.connect(
            self._manage_margin_templates
        )

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

        self.auto_date_field_action = QAction("Fecha automática", self)
        self.auto_date_field_action.triggered.connect(
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

        self.spell_check_action = QAction("Revisar ortografía", self)
        self.spell_check_action.triggered.connect(self._check_spelling)

        self.add_dictionary_action = QAction("Añadir palabra al diccionario", self)
        self.add_dictionary_action.triggered.connect(self._add_dictionary_word)

        self.manage_dictionary_action = QAction("Diccionario personalizado...", self)
        self.manage_dictionary_action.triggered.connect(self._manage_dictionary)

        self.thesaurus_action = QAction("Sinónimos y antónimos...", self)
        self.thesaurus_action.triggered.connect(self._show_thesaurus)

        self.count_action = QAction("Contar palabras...", self)
        self.count_action.triggered.connect(self._show_count)

        self.translate_action = QAction("Traducir selección...", self)
        self.translate_action.triggered.connect(self._translate_selection)

        self.symbol_action = QAction("Símbolo...", self)
        self.symbol_action.triggered.connect(self._show_symbol_dialog)

        self.equation_action = QAction("Ecuación...", self)
        self.equation_action.triggered.connect(self._show_equation_dialog)

        self.chart_action = QAction("Gráfico...", self)
        self.chart_action.triggered.connect(self._show_chart_dialog)

        self.smartart_action = QAction("SmartArt...", self)
        self.smartart_action.triggered.connect(self._show_smartart_dialog)

        self.date_insert_action = QAction("Insertar fecha", self)
        self.date_insert_action.triggered.connect(self._insert_date)

        self.time_insert_action = QAction("Insertar hora", self)
        self.time_insert_action.triggered.connect(self._insert_time)

        self.file_insert_action = QAction("Insertar archivo...", self)
        self.file_insert_action.triggered.connect(self._insert_file)

        self.attachment_action = QAction("Adjuntar archivo (PDF/video/audio)...", self)
        self.attachment_action.triggered.connect(self._insert_attachment)

        self.zoom_in_action = QAction("Acercar", self)
        self.zoom_in_action.setShortcut("Ctrl++")
        self.zoom_in_action.triggered.connect(lambda: self._change_zoom(10))

        self.zoom_out_action = QAction("Alejar", self)
        self.zoom_out_action.setShortcut("Ctrl+-")
        self.zoom_out_action.triggered.connect(lambda: self._change_zoom(-10))

        self.zoom_reset_action = QAction("100%", self)
        self.zoom_reset_action.triggered.connect(lambda: self._set_zoom(100))

        self.zoom_fit_width_action = QAction("Ajustar al ancho de página", self)
        self.zoom_fit_width_action.triggered.connect(self._fit_to_width)

        self.zoom_fit_page_action = QAction("Página completa", self)
        self.zoom_fit_page_action.triggered.connect(self._fit_page)

        self.read_mode_action = QAction("Modo lectura", self)
        self.read_mode_action.triggered.connect(self._enter_read_mode)

        self.print_mode_action = QAction("Diseño de impresión", self)
        self.print_mode_action.triggered.connect(self._enter_print_mode)

        self.web_mode_action = QAction("Diseño web", self)
        self.web_mode_action.triggered.connect(self._enter_web_mode)

        self.draft_mode_action = QAction("Borrador", self)
        self.draft_mode_action.triggered.connect(self._enter_draft_mode)

        self.outline_mode_action = QAction("Esquema", self)
        self.outline_mode_action.triggered.connect(self._enter_outline_mode)

        self.ruler_action = QAction("Regla", self)
        self.ruler_action.setCheckable(True)
        self.ruler_action.triggered.connect(self._toggle_ruler)

        self.grid_action = QAction("Cuadrícula", self)
        self.grid_action.setCheckable(True)
        self.grid_action.triggered.connect(self._toggle_grid)

        self.fullscreen_action = QAction("Pantalla completa", self)
        self.fullscreen_action.setShortcut("F11")
        self.fullscreen_action.triggered.connect(self._toggle_fullscreen)

        self.split_window_action = QAction("Dividir ventana", self)
        self.split_window_action.triggered.connect(self._split_window)

        self.new_window_action = QAction("Nueva ventana", self)
        self.new_window_action.triggered.connect(self._new_window)

        self.checkbox_action = QAction("Casilla de verificación", self)
        self.checkbox_action.triggered.connect(self._insert_checkbox)

        self.radio_action = QAction("Botón de opción", self)
        self.radio_action.triggered.connect(self._insert_radio)

        self.dropdown_action = QAction("Lista desplegable...", self)
        self.dropdown_action.triggered.connect(self._insert_dropdown)

        self.date_field_action = QAction("Selector de fecha", self)
        self.date_field_action.triggered.connect(self._insert_date_field)

        self.text_field_action = QAction("Campo de texto", self)
        self.text_field_action.triggered.connect(self._insert_text_field)

        self.number_field_action = QAction("Campo numérico", self)
        self.number_field_action.triggered.connect(self._insert_number_field)

        self.hidden_field_action = QAction("Campo oculto", self)
        self.hidden_field_action.triggered.connect(self._insert_hidden_field)

        self.protect_form_action = QAction("Proteger formulario", self)
        self.protect_form_action.setCheckable(True)
        self.protect_form_action.triggered.connect(self._toggle_protect_form)

        self.reset_form_action = QAction("Restablecer formulario", self)
        self.reset_form_action.triggered.connect(self._reset_form)

        self.read_only_action = QAction("Solo lectura", self)
        self.read_only_action.setCheckable(True)
        self.read_only_action.triggered.connect(self._toggle_read_only)

        self.password_modify_action = QAction("Contraseña para modificar...", self)
        self.password_modify_action.triggered.connect(self._set_modify_password)

        self.remove_password_action = QAction("Quitar contraseña", self)
        self.remove_password_action.triggered.connect(self._remove_password)

        self.unlock_action = QAction("Desbloquear edición...", self)
        self.unlock_action.triggered.connect(self._unlock_edition)

        self.save_protected_action = QAction("Guardar con contraseña...", self)
        self.save_protected_action.triggered.connect(self._save_protected)

        self.final_action = QAction("Marcar como final", self)
        self.final_action.triggered.connect(self._mark_final)

        self.sign_action = QAction("Firmar documento...", self)
        self.sign_action.triggered.connect(self._sign_document)

        self.verify_sign_action = QAction("Verificar firma", self)
        self.verify_sign_action.triggered.connect(self._verify_signature)

        self.inspect_action = QAction("Inspeccionar documento...", self)
        self.inspect_action.triggered.connect(self._inspect_document)

        self.remove_personal_action = QAction("Eliminar información personal", self)
        self.remove_personal_action.triggered.connect(self._remove_personal_info)

        self.record_macro_action = QAction("Grabar macro", self)
        self.record_macro_action.triggered.connect(self._record_macro)

        self.stop_recording_action = QAction("Detener grabación", self)
        self.stop_recording_action.triggered.connect(self._stop_recording)

        self.manage_macros_action = QAction("Administrar macros...", self)
        self.manage_macros_action.triggered.connect(self._manage_macros)

        self.assign_shortcut_action = QAction("Asignar macro a teclado...", self)
        self.assign_shortcut_action.triggered.connect(self._assign_macro_shortcut)

        self.variables_action = QAction("Variables de documento...", self)
        self.variables_action.triggered.connect(self._edit_variables)

        self._macro_manager = None
        self._macro_recorder = None
        self._macro_shortcut_actions: list = []

        from rword.core.plugins import PluginManager

        self._plugin_manager = PluginManager(
            self._settings, Path(__file__).resolve().parent.parent.parent / "plugins"
        )

        self.data_source_action = QAction("Seleccionar origen de datos...", self)
        self.data_source_action.triggered.connect(self._select_data_source)

        self.insert_field_action = QAction("Insertar campo", self)
        self.insert_field_action.triggered.connect(self._insert_merge_field)

        self.preview_merge_action = QAction("Vista previa de resultados...", self)
        self.preview_merge_action.triggered.connect(self._preview_merge)

        self.filter_merge_action = QAction("Filtrar destinatarios...", self)
        self.filter_merge_action.triggered.connect(self._filter_records)

        self.sort_merge_action = QAction("Ordenar destinatarios...", self)
        self.sort_merge_action.triggered.connect(self._sort_records)

        self.generate_letters_action = QAction("Generar cartas...", self)
        self.generate_letters_action.triggered.connect(self._generate_letters)

        self.generate_labels_action = QAction("Generar etiquetas...", self)
        self.generate_labels_action.triggered.connect(self._generate_labels)

        self.generate_envelopes_action = QAction("Generar sobres...", self)
        self.generate_envelopes_action.triggered.connect(self._generate_envelopes)

        self.email_merge_action = QAction("Enviar por correo...", self)
        self.email_merge_action.triggered.connect(self._send_email)

        self.collab_dialog_action = QAction("Colaboración...", self)
        self.collab_dialog_action.triggered.connect(self._show_collaboration)

        self.set_username_action = QAction("Nombre de usuario...", self)
        self.set_username_action.triggered.connect(self._set_username)

        self.track_authors_action = QAction("Seguimiento de autores", self)
        self.track_authors_action.setCheckable(True)
        self.track_authors_action.triggered.connect(self._toggle_track_authors)

        self.presence_action = QAction("Estado en línea", self)
        self.presence_action.setCheckable(True)
        self.presence_action.setChecked(True)
        self.presence_action.triggered.connect(self._toggle_presence)

        self.check_accessibility_action = QAction("Comprobar accesibilidad...", self)
        self.check_accessibility_action.triggered.connect(self._check_accessibility)

        self.alt_text_action = QAction("Texto alternativo de imagen...", self)
        self.alt_text_action.triggered.connect(self._set_alt_text)

        self.read_aloud_action = QAction("Leer en voz alta", self)
        self.read_aloud_action.triggered.connect(self._read_aloud)

        self.stop_reading_action = QAction("Detener lectura", self)
        self.stop_reading_action.triggered.connect(self._stop_reading)

        self.high_contrast_action = QAction("Tema de alto contraste", self)
        self.high_contrast_action.triggered.connect(self._apply_high_contrast)

        self.immersive_action = QAction("Enfoque inmersivo", self)
        self.immersive_action.setCheckable(True)
        self.immersive_action.triggered.connect(self._toggle_immersive)

        self.preferences_action = QAction("Preferencias...", self)
        self.preferences_action.triggered.connect(self._show_preferences)


        self.shortcuts_action = QAction("Atajos de teclado...", self)
        self.shortcuts_action.triggered.connect(self._show_shortcuts)

        self.manage_plugins_action = QAction("Administrar complementos...", self)
        self.manage_plugins_action.triggered.connect(self._manage_plugins)

        self.api_key_action = QAction("Configurar clave de API...", self)
        self.api_key_action.triggered.connect(self._configure_api_key)

        self.ai_about_action = QAction("Acerca de la IA...", self)
        self.ai_about_action.triggered.connect(self._ai_about)

        self.ai_redact_action = QAction("Redactar desde instrucción...", self)
        self.ai_redact_action.triggered.connect(self._ai_redact)

        self.ai_continue_action = QAction("Continuar escribiendo", self)
        self.ai_continue_action.triggered.connect(
            lambda: self._ai_context("continue_writing")
        )

        self.ai_complete_action = QAction("Completar frase", self)
        self.ai_complete_action.triggered.connect(
            lambda: self._ai_context("complete_sentence")
        )

        self.ai_rewrite_action = QAction("Reescribir...", self)
        self.ai_rewrite_action.triggered.connect(self._ai_rewrite)

        self.ai_summarize_action = QAction("Resumir", self)
        self.ai_summarize_action.triggered.connect(
            lambda: self._ai_context("summarize")
        )

        self.ai_expand_action = QAction("Expandir texto", self)
        self.ai_expand_action.triggered.connect(
            lambda: self._ai_context("expand")
        )

        self.ai_reduce_action = QAction("Reducir texto", self)
        self.ai_reduce_action.triggered.connect(
            lambda: self._ai_context("reduce_text")
        )

        self.ai_simplify_action = QAction("Simplificar lenguaje", self)
        self.ai_simplify_action.triggered.connect(
            lambda: self._ai_context("simplify")
        )

        self.ai_correct_action = QAction("Corregir ortografía y gramática", self)
        self.ai_correct_action.triggered.connect(
            lambda: self._ai_context("correct", "replace_selection")
        )

        self.ai_redundancies_action = QAction("Detectar redundancias", self)
        self.ai_redundancies_action.triggered.connect(
            lambda: self._ai_context("detect_redundancies", "insert")
        )

        self.ai_suggest_words_action = QAction("Sugerir mejores palabras", self)
        self.ai_suggest_words_action.triggered.connect(
            lambda: self._ai_context("suggest_better_words", "insert")
        )

        self.ai_fluidity_action = QAction("Mejorar fluidez y cohesión", self)
        self.ai_fluidity_action.triggered.connect(
            lambda: self._ai_context("improve_fluidity", "replace_selection")
        )

        self.ai_clarity_action = QAction("Mejorar claridad", self)
        self.ai_clarity_action.triggered.connect(
            lambda: self._ai_context("improve_clarity", "replace_selection")
        )

        self.ai_ambiguity_action = QAction("Detectar ambigüedades", self)
        self.ai_ambiguity_action.triggered.connect(
            lambda: self._ai_context("detect_ambiguities", "insert")
        )

        self.ai_tones = {}
        for label, function in {
            "Formal": "make_professional",
            "Persuasivo": "make_persuasive",
            "Amigable": "make_friendly",
            "Neutral": "make_neutral",
        }.items():
            action = QAction(label, self)
            action.triggered.connect(
                lambda checked=False, fn=function: self._ai_context(fn, "replace_selection")
            )
            self.ai_tones[label] = action

        self.ai_translate_action = QAction("Traducir...", self)
        self.ai_translate_action.triggered.connect(self._ai_translate)

        self.ai_detect_language_action = QAction("Detectar idioma", self)
        self.ai_detect_language_action.triggered.connect(
            lambda: self._ai_context("detect_language", "insert")
        )

        self.ai_ideas_action = QAction("Ideas principales", self)
        self.ai_ideas_action.triggered.connect(
            lambda: self._ai_context("main_ideas", "insert")
        )

        self.ai_conclusions_action = QAction("Conclusiones", self)
        self.ai_conclusions_action.triggered.connect(
            lambda: self._ai_context("extract_conclusions", "insert")
        )

        self.ai_inconsistencies_action = QAction("Inconsistencias y contradicciones", self)
        self.ai_inconsistencies_action.triggered.connect(
            lambda: self._ai_context("detect_inconsistencies", "insert")
        )

        self.ai_difficulty_action = QAction("Dificultad de lectura", self)
        self.ai_difficulty_action.triggered.connect(
            lambda: self._ai_context("reading_difficulty", "insert")
        )

        self.ai_audience_action = QAction("Público objetivo", self)
        self.ai_audience_action.triggered.connect(
            lambda: self._ai_context("target_audience", "insert")
        )

        self.ai_classify_action = QAction("Clasificar documento", self)
        self.ai_classify_action.triggered.connect(
            lambda: self._ai_context("classify_document", "insert")
        )

        self.ai_executive_action = QAction("Resumen ejecutivo", self)
        self.ai_executive_action.triggered.connect(
            lambda: self._ai_context("executive_summary", "insert")
        )

        self.ai_explain_action = QAction("Explicar selección", self)
        self.ai_explain_action.triggered.connect(
            lambda: self._ai_context("explain", "insert")
        )

        self.ai_selection_summary_action = QAction("Resumir selección", self)
        self.ai_selection_summary_action.triggered.connect(
            lambda: self._ai_context("summarize", "insert")
        )

        self.ai_selection_translate_action = QAction("Traducir selección...", self)
        self.ai_selection_translate_action.triggered.connect(self._ai_translate)

        self.ai_selection_improve_action = QAction("Mejorar selección", self)
        self.ai_selection_improve_action.triggered.connect(
            lambda: self._ai_context("improve_fluidity", "replace_selection")
        )

        self.ai_selection_errors_action = QAction("Detectar errores en la selección", self)
        self.ai_selection_errors_action.triggered.connect(
            lambda: self._ai_context("correct", "replace_selection")
        )

        self.ai_selection_questions_action = QAction("Generar preguntas", self)
        self.ai_selection_questions_action.triggered.connect(
            lambda: self._ai_context("generate_questions", "insert")
        )

        self.ai_chat_panel_action = QAction("Chat con IA", self)
        self.ai_chat_panel_action.setCheckable(True)
        self.ai_chat_panel_action.triggered.connect(self._toggle_ai_chat)

        self._ai_specialized = {}
        for menu_name, items in {
            "&Legal": [
                ("Redactar contrato...", "draft_contract",
                    "Instrucción del contrato:", "prompt_context"),
                ("Revisar cláusulas abusivas", "review_clauses", None, "context"),
                ("Detectar riesgos legales", "legal_risks", None, "context"),
                ("Explicar artículo...", "explain_law", "Artículo o norma:", "prompt"),
                ("Comparar contratos...", "compare_contracts",
                    "Texto del segundo contrato:", "prompt_compare"),
                ("Resumir contrato", "summarize_contract", None, "context"),
            ],
            "&Investigación": [
                ("Investigar tema...", "research", "Tema:", "prompt"),
                ("Generar bibliografía", "generate_bibliography", None, "context"),
            ],
        }.items():
            submenu_actions = {}
            for label, function, prompt, style in items:
                action = QAction(label, self)
                action.triggered.connect(
                    lambda checked=False, f=function, p=prompt, s=style: self._ai_domain(f, p, s)
                )
                submenu_actions[label] = action
            self._ai_specialized[menu_name] = submenu_actions

        self._ai_automation = {}
        for menu_name, items in {
            "&Automatización": [
                ("Generar índice", "generate_index", None, "context"),
                ("Generar diagrama Mermaid", "generate_mermaid", None, "context"),
                ("Texto en tabla", "text_to_table", None, "context"),
                ("Texto en lista", "text_to_list", None, "context"),
                ("Texto en lista de verificación", "text_to_checklist", None, "context"),
                ("Generar cronograma", "generate_timeline", None, "context"),
                ("Crear tareas", "create_tasks", None, "context"),
                ("Texto a JSON", "text_to_json", None, "context"),
                ("Texto a XML", "text_to_xml", None, "context"),
                ("Texto a YAML", "text_to_yaml", None, "context"),
            ],
            "&Productividad": [
                ("Extraer entidades", "extract_entities", None, "context"),
                ("Detectar fechas", "detect_dates", None, "context"),
                ("Detectar personas", "detect_people", None, "context"),
                ("Extraer información...", "extract_info",
                    "Campos a extraer (p. ej. nombre, importe):", "prompt_context"),
            ],
            "&Marketing": [
                ("Publicación para redes", "marketing_post", None, "context"),
                ("Sugerir títulos", "marketing_titles", None, "context"),
                ("Generar hashtags", "marketing_hashtags", None, "context"),
                ("Campaña de correo", "marketing_email", None, "context"),
                ("Optimizar SEO", "seo_optimize", None, "context"),
                ("Metadescripción", "meta_description", None, "context"),
            ],
        }.items():
            submenu_actions = {}
            for label, function, prompt, style in items:
                action = QAction(label, self)
                action.triggered.connect(
                    lambda checked=False, f=function, p=prompt, s=style: self._ai_domain(f, p, s)
                )
                submenu_actions[label] = action
            self._ai_automation[menu_name] = submenu_actions

        self.write_like_action = QAction("Escribir como yo...", self)
        self.write_like_action.triggered.connect(self._ai_write_like)

        self.set_style_memory_action = QAction("Aprender mi estilo", self)
        self.set_style_memory_action.triggered.connect(self._learn_style)

        self.project_memory_action = QAction("Usar memoria del proyecto...", self)
        self.project_memory_action.triggered.connect(self._ai_project_memory)

        self.template_action = QAction("Plantillas inteligentes...", self)
        self.template_action.triggered.connect(self._show_smart_templates)

        self.autocomplete_action = QAction("Activar autocompletado", self)
        self.autocomplete_action.setCheckable(True)
        self.autocomplete_action.setChecked(False)
        self.autocomplete_action.triggered.connect(self._toggle_autocomplete)

        self.coherence_action = QAction("Inspector de coherencia", self)
        self.coherence_action.triggered.connect(self._coherence_check)

        self.glossary_action = QAction("Generar glosario", self)
        self.glossary_action.triggered.connect(self._generate_glossary)

        self.agents_actions = {}
        for label, role in AGENTS.items():
            action = QAction(label, self)
            action.triggered.connect(
                lambda checked=False, r=role, lbl=label: self._ai_agent(r, lbl)
            )
            self.agents_actions[label] = action

        self.toggle_toolbar_action = QAction("Cinta de opciones", self)
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

    def _ribbon_button(self, group, action, icon_name, large=False):
        self._icon_manager.register(action, icon_name, 32 if large else 16)
        return group.add_action(action, large=large)

    def _ribbon_dropdown(self, group, label, icon_name, menu):
        action = QAction(label, self)
        self._icon_manager.register(action, icon_name, 16)
        return group.add_dropdown(action, menu)

    def _build_ribbon(self) -> None:
        self.ribbon = RibbonBar(self._icon_manager, self)
        self._root_layout.insertWidget(0, self.ribbon)
        self._build_dynamic_menus()
        self._build_tabs_edicion_archivo()
        self._build_tab_insertar()
        self._build_tab_diseno()
        self._build_tab_referencias()
        self._build_tab_revision()
        self._build_tab_vista()
        self._build_tab_correspondencia()
        self._build_tab_automatizacion()
        self._build_tab_colab_seguridad()
        self._build_tab_accesibilidad()
        self._build_tab_ia()
        self._build_tab_ayuda()
        self.ribbon.set_current_tab(0)

    def _build_dynamic_menus(self) -> None:
        self.clipboard_menu = QMenu("Portapapeles", self)
        self._rebuild_clipboard_menu()
        self.styles_menu = QMenu("Estilos", self)
        self.styles_menu.aboutToShow.connect(self._rebuild_styles_menu)
        self.theme_menu = QMenu("Tema", self)
        self.theme_menu.aboutToShow.connect(self._rebuild_theme_menu)
        self.automation_menu = QMenu("Macros", self)
        self.automation_menu.aboutToShow.connect(self._rebuild_macro_shortcuts)
        self.field_menu = QMenu("Insertar campo", self)
        self.field_menu.aboutToShow.connect(self._rebuild_field_menu)
        self.margins_menu = QMenu("Márgenes", self)
        self.margins_menu.aboutToShow.connect(self._rebuild_margins_menu)
        self.export_menu = QMenu("Exportar", self)
        for action in (
            self.export_pdf_action,
            self.export_html_action,
            self.export_rtf_action,
            self.export_odt_action,
            self.export_epub_action,
            self.export_text_action,
        ):
            self.export_menu.addAction(action)

        self.shapes_menu = QMenu("Formas", self)
        for action in self.shape_actions.values():
            self.shapes_menu.addAction(action)
        self.shapes_menu.addSeparator()
        self.shapes_menu.addAction(self.text_box_action)
        self.shapes_menu.addAction(self.wordart_action)

        self.tone_menu = QMenu("Cambiar tono", self)
        for action in self.ai_tones.values():
            self.tone_menu.addAction(action)

        self.agents_menu = QMenu("Agentes especializados", self)
        for action in self.agents_actions.values():
            self.agents_menu.addAction(action)

        self.ai_domain_menus = {}
        for menu_name, submenu_actions in self._ai_specialized.items():
            menu = QMenu(menu_name.replace("&", ""), self)
            for action in submenu_actions.values():
                menu.addAction(action)
            self.ai_domain_menus[menu_name] = menu

        self.ai_automation_menus = {}
        for menu_name, submenu_actions in self._ai_automation.items():
            menu = QMenu(menu_name.replace("&", ""), self)
            for action in submenu_actions.values():
                menu.addAction(action)
            self.ai_automation_menus[menu_name] = menu

        self.ai_premium_menu = QMenu("Premium", self)
        for action in (
            self.write_like_action,
            self.set_style_memory_action,
            self.project_memory_action,
            self.template_action,
            self.autocomplete_action,
            self.coherence_action,
            self.glossary_action,
        ):
            self.ai_premium_menu.addAction(action)

    def _build_tabs_edicion_archivo(self) -> None:
        tab = self.ribbon.add_tab("Edición")

        self.format_bar = FormatBar(self._editor, tab, self._icon_manager)
        fuente = tab.add_group("Fuente")
        fuente.add_widget(self.format_bar)

        self.paragraph_bar = ParagraphBar(self._editor, tab, self._icon_manager)
        parrafo = tab.add_group("Párrafo")
        parrafo.add_widget(self.paragraph_bar)

        estilos = tab.add_group("Estilos")
        self._ribbon_dropdown(estilos, "Estilos", "type", self.styles_menu)
        estilos.add_separator()
        self._ribbon_button(estilos, self.create_style_action, "sparkles")
        self._ribbon_button(estilos, self.organizer_action, "layers")

        archivo_tab = self.ribbon.add_tab("Archivo")

        archivo = archivo_tab.add_group("Archivo")
        self._ribbon_button(archivo, self.new_action, "file-plus", large=True)
        self._ribbon_button(archivo, self.open_action, "folder-open", large=True)
        self._ribbon_button(archivo, self.save_action, "save", large=True)
        self._ribbon_button(archivo, self.save_as_action, "files", large=True)
        archivo.add_separator()
        self._ribbon_button(archivo, self.close_action, "x")
        self._ribbon_button(archivo, self.print_action, "printer")
        self._ribbon_button(archivo, self.print_preview_action, "eye")
        self._ribbon_dropdown(archivo, "Exportar", "file-text", self.export_menu)

        portapapeles = archivo_tab.add_group("Portapapeles")
        self._ribbon_button(portapapeles, self.cut_action, "scissors")
        self._ribbon_button(portapapeles, self.copy_action, "copy")
        self._ribbon_button(portapapeles, self.paste_action, "clipboard")
        self._ribbon_button(portapapeles, self.painter_action, "paintbrush")
        self._ribbon_dropdown(portapapeles, "Portapapeles", "clipboard", self.clipboard_menu)

        edicion = archivo_tab.add_group("Edición")
        self._ribbon_button(edicion, self.undo_action, "undo-2")
        self._ribbon_button(edicion, self.redo_action, "redo-2")
        edicion.add_separator()
        self._ribbon_button(edicion, self.find_action, "search")
        self._ribbon_button(edicion, self.replace_action, "replace")
        self._ribbon_button(edicion, self.go_to_action, "corner-down-right")
        self._ribbon_dropdown(edicion, "Seleccionar", "check-square", self._selection_menu())


    def _selection_menu(self) -> QMenu:
        menu = QMenu(self)
        menu.addAction(self.select_word_action)
        menu.addAction(self.select_line_action)
        menu.addAction(self.select_paragraph_action)
        menu.addAction(self.select_all_action)
        return menu

    def _build_tab_insertar(self) -> None:
        tab = self.ribbon.add_tab("Insertar")

        tablas = tab.add_group("Tablas")
        self._ribbon_button(tablas, self.insert_table_action, "table", large=True)
        tablas.add_separator()
        self._ribbon_button(tablas, self.convert_text_to_table_action, "list")
        self._ribbon_button(tablas, self.table_to_text_action, "align-justify")

        ilustraciones = tab.add_group("Ilustraciones")
        self._ribbon_button(ilustraciones, self.insert_image_action, "image", large=True)
        self._ribbon_dropdown(ilustraciones, "Formas", "shapes", self.shapes_menu)
        self._ribbon_button(ilustraciones, self.wordart_action, "type")
        self._ribbon_button(ilustraciones, self.smartart_action, "network")
        self._ribbon_button(ilustraciones, self.chart_action, "bar-chart")

        simbolos = tab.add_group("Símbolos")
        self._ribbon_button(simbolos, self.symbol_action, "sigma", large=True)
        self._ribbon_button(simbolos, self.equation_action, "function-square")

        enlaces = tab.add_group("Enlaces")
        self._ribbon_button(enlaces, self.insert_hyperlink_action, "link", large=True)
        bookmark_menu = QMenu(self)
        bookmark_menu.addAction(self.add_bookmark_action)
        bookmark_menu.addAction(self.go_to_bookmark_action)
        bookmark_menu.addAction(self.delete_bookmark_action)
        self._ribbon_dropdown(enlaces, "Marcador", "bookmark", bookmark_menu)

        encabezado = tab.add_group("Encabezado y pie")
        self._ribbon_button(encabezado, self.header_action, "heading", large=True)
        self._ribbon_button(encabezado, self.footer_action, "heading")
        self._ribbon_button(encabezado, self.page_number_action, "hash")
        self._ribbon_button(encabezado, self.auto_date_field_action, "calendar")
        self._ribbon_button(encabezado, self.time_field_action, "clock")
        self._ribbon_button(encabezado, self.refresh_fields_action, "refresh-cw")

        texto = tab.add_group("Texto")
        self._ribbon_button(texto, self.text_box_action, "square")
        self._ribbon_button(texto, self.file_insert_action, "file-text")
        self._ribbon_button(texto, self.attachment_action, "paperclip")

    def _build_tab_diseno(self) -> None:
        tab = self.ribbon.add_tab("Diseño de página")

        configurar = tab.add_group("Configurar página")
        self._ribbon_button(configurar, self.page_setup_action, "settings", large=True)
        configurar.add_separator()
        self._ribbon_button(configurar, self.page_break_action, "file-output")
        self._ribbon_button(configurar, self.section_break_action, "split")
        self._ribbon_button(configurar, self.line_numbers_action, "hash")

        columnas = tab.add_group("Columnas")
        self._ribbon_button(columnas, self.columns_one_action, "columns-2")
        self._ribbon_button(columnas, self.columns_two_action, "columns-3")
        self._ribbon_button(columnas, self.columns_three_action, "columns-3")
        self._ribbon_button(columnas, self.columns_more_action, "columns-3", large=True)

        margenes = tab.add_group("Márgenes")
        self._ribbon_dropdown(margenes, "Márgenes", "ruler", self.margins_menu)
        margenes.add_separator()
        self._ribbon_button(margenes, self.save_margin_template_action, "bookmark-plus")
        self._ribbon_button(margenes, self.manage_margin_templates_action, "settings")

        fondo = tab.add_group("Fondo")
        self._ribbon_button(fondo, self.watermark_action, "type")
        self._ribbon_button(fondo, self.page_color_action, "palette")

        temas = tab.add_group("Temas")
        self._ribbon_dropdown(temas, "Tema", "palette", self.theme_menu)
        temas.add_separator()
        self._ribbon_button(temas, self.high_contrast_action, "contrast")
        self._ribbon_button(temas, self.create_style_action, "sparkles")
        self._ribbon_button(temas, self.modify_style_action, "wand")

    def _build_tab_referencias(self) -> None:
        tab = self.ribbon.add_tab("Referencias")

        toc = tab.add_group("Tabla de contenido")
        self._ribbon_button(toc, self.toc_action, "list", large=True)
        self._ribbon_button(toc, self.update_toc_action, "refresh-cw")

        notas = tab.add_group("Notas")
        self._ribbon_button(notas, self.footnote_action, "superscript")
        self._ribbon_button(notas, self.endnote_action, "subscript")

        citas = tab.add_group("Citas y bibliografía")
        self._ribbon_button(citas, self.add_source_action, "book-open")
        self._ribbon_button(citas, self.insert_citation_action, "quote")
        self._ribbon_button(citas, self.bibliography_action, "file-text")

        leyendas = tab.add_group("Leyendas")
        self._ribbon_button(leyendas, self.caption_action, "type")
        self._ribbon_button(leyendas, self.table_of_figures_action, "image")

        indice = tab.add_group("Índice")
        self._ribbon_button(indice, self.mark_index_action, "bookmark-plus")
        self._ribbon_button(indice, self.insert_index_action, "list-ordered")
        self._ribbon_button(indice, self.cross_reference_action, "link")

    def _build_tab_revision(self) -> None:
        tab = self.ribbon.add_tab("Revisión")

        comentarios = tab.add_group("Comentarios")
        self._ribbon_button(comentarios, self.add_comment_action, "message-square", large=True)
        self._ribbon_button(comentarios, self.show_comments_action, "message-square")

        cambios = tab.add_group("Cambios")
        self._ribbon_button(cambios, self.track_changes_action, "file-check")
        self._ribbon_button(cambios, self.accept_changes_action, "check")
        self._ribbon_button(cambios, self.reject_changes_action, "x")
        self._ribbon_button(cambios, self.compare_documents_action, "copy")

        correccion = tab.add_group("Corrección")
        self._ribbon_button(correccion, self.spell_check_action, "spell-check", large=True)
        self._ribbon_button(correccion, self.add_dictionary_action, "book-open")
        self._ribbon_button(correccion, self.manage_dictionary_action, "book-open")
        self._ribbon_button(correccion, self.thesaurus_action, "languages")
        self._ribbon_button(correccion, self.count_action, "calculator")

    def _build_tab_vista(self) -> None:
        tab = self.ribbon.add_tab("Vista")

        vistas = tab.add_group("Vistas")
        self._ribbon_button(vistas, self.read_mode_action, "eye")
        self._ribbon_button(vistas, self.print_mode_action, "layout")
        self._ribbon_button(vistas, self.web_mode_action, "globe")
        self._ribbon_button(vistas, self.draft_mode_action, "file-text")
        self._ribbon_button(vistas, self.outline_mode_action, "list")

        zoom = tab.add_group("Zoom")
        self._ribbon_button(zoom, self.zoom_in_action, "zoom-in")
        self._ribbon_button(zoom, self.zoom_out_action, "zoom-out")
        self._ribbon_button(zoom, self.zoom_reset_action, "percent")
        self._ribbon_button(zoom, self.zoom_fit_width_action, "maximize")
        self._ribbon_button(zoom, self.zoom_fit_page_action, "scan")

        mostrar = tab.add_group("Mostrar")
        self._ribbon_button(mostrar, self.ruler_action, "ruler")
        self._ribbon_button(mostrar, self.grid_action, "grid")
        self._ribbon_button(mostrar, self.toggle_navigation_action, "panel-left")
        self._ribbon_button(mostrar, self.toggle_statusbar_action, "layout")

        ventana = tab.add_group("Ventana")
        self._ribbon_button(ventana, self.split_window_action, "split")
        self._ribbon_button(ventana, self.new_window_action, "copy-plus")
        self._ribbon_button(ventana, self.fullscreen_action, "maximize-2")

        cinta = tab.add_group("Cinta")
        self._ribbon_button(cinta, self.toggle_toolbar_action, "panel-top")
        self._ribbon_button(cinta, self.toggle_formatbar_action, "type")
        self._ribbon_button(cinta, self.toggle_paragraphbar_action, "align-left")

    def _build_tab_correspondencia(self) -> None:
        tab = self.ribbon.add_tab("Correspondencia")

        iniciar = tab.add_group("Iniciar")
        self._ribbon_button(iniciar, self.data_source_action, "database", large=True)
        self._ribbon_dropdown(iniciar, "Insertar campo", "type", self.field_menu)
        self._ribbon_button(iniciar, self.preview_merge_action, "eye")

        filtrar = tab.add_group("Filtrar")
        self._ribbon_button(filtrar, self.filter_merge_action, "filter")
        self._ribbon_button(filtrar, self.sort_merge_action, "sort-asc")

        generar = tab.add_group("Generar")
        self._ribbon_button(generar, self.generate_letters_action, "file-text", large=True)
        self._ribbon_button(generar, self.generate_labels_action, "list")
        self._ribbon_button(generar, self.generate_envelopes_action, "send")
        self._ribbon_button(generar, self.email_merge_action, "mail")

    def _build_tab_automatizacion(self) -> None:
        tab = self.ribbon.add_tab("Automatización")

        macros = tab.add_group("Macros")
        self._ribbon_button(macros, self.record_macro_action, "play", large=True)
        self._ribbon_button(macros, self.stop_recording_action, "square-stop")
        self._ribbon_button(macros, self.manage_macros_action, "settings")
        self._ribbon_button(macros, self.assign_shortcut_action, "keyboard")
        self._ribbon_dropdown(macros, "Macros asignadas", "play", self.automation_menu)

        variables = tab.add_group("Variables")
        self._ribbon_button(variables, self.variables_action, "variable", large=True)

        formularios = tab.add_group("Formularios")
        self._ribbon_button(formularios, self.checkbox_action, "check-square")
        self._ribbon_button(formularios, self.radio_action, "circle")
        self._ribbon_button(formularios, self.dropdown_action, "list")
        self._ribbon_button(formularios, self.date_field_action, "calendar")
        self._ribbon_button(formularios, self.text_field_action, "type")
        self._ribbon_button(formularios, self.number_field_action, "hash")
        self._ribbon_button(formularios, self.hidden_field_action, "eye-off")
        self._ribbon_button(formularios, self.protect_form_action, "lock")
        self._ribbon_button(formularios, self.reset_form_action, "refresh-cw")

        config = tab.add_group("Configuración")
        self._ribbon_button(config, self.preferences_action, "settings")
        self._ribbon_button(config, self.shortcuts_action, "keyboard")
        self._ribbon_button(config, self.manage_plugins_action, "puzzle")

    def _build_tab_colab_seguridad(self) -> None:
        tab = self.ribbon.add_tab("Colaboración y seguridad")

        colaboracion = tab.add_group("Colaboración")
        self._ribbon_button(colaboracion, self.collab_dialog_action, "users", large=True)
        self._ribbon_button(colaboracion, self.set_username_action, "user")
        self._ribbon_button(colaboracion, self.presence_action, "activity")
        self._ribbon_button(colaboracion, self.track_authors_action, "users")

        seguridad = tab.add_group("Seguridad")
        self._ribbon_button(seguridad, self.read_only_action, "lock")
        self._ribbon_button(seguridad, self.password_modify_action, "lock")
        self._ribbon_button(seguridad, self.remove_password_action, "unlock")
        self._ribbon_button(seguridad, self.unlock_action, "unlock")
        self._ribbon_button(seguridad, self.save_protected_action, "shield")
        self._ribbon_button(seguridad, self.final_action, "check-circle-2")
        self._ribbon_button(seguridad, self.sign_action, "fingerprint")
        self._ribbon_button(seguridad, self.verify_sign_action, "shield")
        self._ribbon_button(seguridad, self.inspect_action, "search")
        self._ribbon_button(seguridad, self.remove_personal_action, "eraser")

    def _build_tab_accesibilidad(self) -> None:
        tab = self.ribbon.add_tab("Accesibilidad")

        comprobar = tab.add_group("Comprobar")
        self._ribbon_button(comprobar, self.check_accessibility_action, "accessibility", large=True)
        self._ribbon_button(comprobar, self.alt_text_action, "image")

        leer = tab.add_group("Leer")
        self._ribbon_button(leer, self.read_aloud_action, "volume-2", large=True)
        self._ribbon_button(leer, self.stop_reading_action, "square-stop")

        ayuda = tab.add_group("Ayuda visual")
        self._ribbon_button(ayuda, self.high_contrast_action, "contrast")
        self._ribbon_button(ayuda, self.immersive_action, "maximize")
        self._ribbon_button(ayuda, self.toggle_navigation_action, "panel-left")

    def _build_tab_ia(self) -> None:
        tab = self.ribbon.add_tab("IA")

        chat = tab.add_group("Chat")
        self._ribbon_button(chat, self.ai_chat_panel_action, "bot", large=True)
        self._ribbon_button(chat, self.api_key_action, "key")

        escritura = tab.add_group("Escritura")
        self._ribbon_button(escritura, self.ai_redact_action, "sparkles")
        self._ribbon_button(escritura, self.ai_continue_action, "play")
        self._ribbon_button(escritura, self.ai_complete_action, "type")
        self._ribbon_button(escritura, self.ai_rewrite_action, "refresh-cw")
        self._ribbon_button(escritura, self.ai_summarize_action, "list")
        self._ribbon_button(escritura, self.ai_expand_action, "maximize")
        self._ribbon_button(escritura, self.ai_reduce_action, "minimize")
        self._ribbon_button(escritura, self.ai_simplify_action, "type")
        self._ribbon_dropdown(escritura, "Tono", "palette", self.tone_menu)

        correccion = tab.add_group("Corrección IA")
        self._ribbon_button(correccion, self.ai_correct_action, "spell-check")
        self._ribbon_button(correccion, self.ai_redundancies_action, "repeat")
        self._ribbon_button(correccion, self.ai_suggest_words_action, "languages")
        self._ribbon_button(correccion, self.ai_fluidity_action, "waves")
        self._ribbon_button(correccion, self.ai_clarity_action, "lightbulb")
        self._ribbon_button(correccion, self.ai_ambiguity_action, "help-circle")

        traduccion = tab.add_group("Traducción")
        self._ribbon_button(traduccion, self.ai_translate_action, "languages", large=True)
        self._ribbon_button(traduccion, self.ai_detect_language_action, "globe")

        analisis = tab.add_group("Análisis")
        self._ribbon_button(analisis, self.ai_ideas_action, "lightbulb")
        self._ribbon_button(analisis, self.ai_conclusions_action, "list-ordered")
        self._ribbon_button(analisis, self.ai_inconsistencies_action, "alert-triangle")
        self._ribbon_button(analisis, self.ai_difficulty_action, "book-open")
        self._ribbon_button(analisis, self.ai_audience_action, "users")
        self._ribbon_button(analisis, self.ai_classify_action, "file-text")
        self._ribbon_button(analisis, self.ai_executive_action, "file-check")

        seleccion = tab.add_group("Selección")
        self._ribbon_button(seleccion, self.ai_explain_action, "help-circle")
        self._ribbon_button(seleccion, self.ai_selection_summary_action, "list")
        self._ribbon_button(seleccion, self.ai_selection_translate_action, "languages")
        self._ribbon_button(seleccion, self.ai_selection_improve_action, "wand")
        self._ribbon_button(seleccion, self.ai_selection_errors_action, "spell-check")
        self._ribbon_button(seleccion, self.ai_selection_questions_action, "help-circle")

        dominios = tab.add_group("Dominios")
        for label in ("Legal", "Investigación"):
            key = f"&{label}"
            menu = self.ai_domain_menus.get(key)
            if menu is not None:
                self._ribbon_dropdown(dominios, label, "scale", menu)

        automatizacion = tab.add_group("Automatización IA")
        for label in ("Automatización", "Productividad", "Marketing"):
            menu = self.ai_automation_menus.get(f"&{label}")
            if menu is not None:
                self._ribbon_dropdown(automatizacion, label, "zap", menu)

        premium = tab.add_group("Premium")
        self._ribbon_dropdown(premium, "Premium", "star", self.ai_premium_menu)
        self._ribbon_dropdown(premium, "Agentes", "bot", self.agents_menu)

    def _build_tab_ayuda(self) -> None:
        tab = self.ribbon.add_tab("Ayuda")
        ayuda = tab.add_group("Ayuda")
        self._ribbon_button(ayuda, self.about_action, "help-circle", large=True)

    def add_ribbon_action(self, action, tab_title: str, group_title: str,
                          large: bool = False) -> None:
        """Hook para que los complementos añadan acciones a la cinta."""
        tabs = {t: i for i, t in enumerate(self.ribbon.tab_titles())}
        index = tabs.get(tab_title)
        if index is None:
            index = self.ribbon.add_tab(tab_title)
        tab_widget = self.ribbon._stack.widget(index)
        group = None
        for existing in tab_widget._groups:
            if existing.title == group_title:
                group = existing
                break
        if group is None:
            group = tab_widget.add_group(group_title)
        self._ribbon_button(group, action, "sparkles", large=large)
        return group


    def _build_statusbar(self) -> None:
        self.words_label = QLabel(self)
        self.chars_label = QLabel(self)
        self.modified_label = QLabel(self)
        self._presence_label = QLabel(self)
        self._presence_user_label = QLabel(self)
        self.statusBar().addPermanentWidget(self._presence_label)
        self.statusBar().addPermanentWidget(self._presence_user_label)
        self.statusBar().addPermanentWidget(self.words_label)
        self.statusBar().addPermanentWidget(self.chars_label)
        self.statusBar().addPermanentWidget(self.modified_label)
        self._update_presence_label()

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
        apply_page_setup(self._editor, current_page_setup(self._editor))
        self._editor.document().setModified(False)
        self._page_view.refresh()
        self._update_title()
        self._update_statusbar()
        self._log_activity("Nuevo documento")

    def _open_document(self) -> None:
        if not self._confirm_save_before_closing():
            return
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Abrir documento", "", FILE_DIALOG_FILTER
        )
        if not file_name:
            return
        path = Path(file_name)
        if self._try_open_protected(path):
            return
        try:
            self._editor.load_file(path)
        except (OSError, UnicodeDecodeError) as error:
            self._show_error(f"No se pudo abrir el archivo:\n{error}")
            return
        self._update_title()
        self._update_statusbar()

    def _try_open_protected(self, path: Path) -> bool:
        from PySide6.QtWidgets import QInputDialog

        from rword.core.security import decrypt_document, is_protected_content

        try:
            data = path.read_bytes()
        except OSError:
            return False
        if not is_protected_content(data):
            return False
        password, ok = QInputDialog.getText(
            self, "Documento protegido", "Contraseña:",
            echo=QLineEdit.EchoMode.Password,
        )
        if not ok:
            return True
        content = decrypt_document(data, password)
        if content is None:
            self._show_error("No se pudo desbloquear el documento.")
            return True
        self._editor.setHtml(content)
        self._editor.set_file_path(path)
        self._editor.document().setModified(False)
        self._update_title()
        self._update_statusbar()
        self._log_activity("Documento abierto", path.name)
        return True

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
            return
        self._log_activity("Documento guardado", path.name)

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
        self.ribbon.setVisible(checked)

    def _toggle_formatbar(self, checked: bool) -> None:
        self.ribbon.set_group_visible("Edición", "Fuente", checked)

    def _toggle_paragraphbar(self, checked: bool) -> None:
        self.ribbon.set_group_visible("Edición", "Párrafo", checked)

    def _print_document(self) -> None:
        from rword.core.export import print_document

        if not print_document(self._editor, self):
            return

    def _print_preview(self) -> None:
        from rword.core.export import print_preview

        print_preview(self._editor, self)

    def _export(self, label: str, file_filter: str, exporter) -> None:
        default = self._suggested_name()
        base = Path(default).stem or "documento"
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            f"Exportar a {label}",
            f"{base}.{file_filter.replace('*', '').split()[0].lstrip('.')}",
            f"Archivo {label} ({file_filter});;Todos los archivos (*)",
        )
        if not file_name:
            return
        try:
            exporter(self._editor, file_name)
        except OSError as error:
            self._show_error(f"No se pudo exportar:\n{error}")
            return
        self.statusBar().showMessage(
            f"Documento exportado a {label}.", 5000
        )

    def _show_symbol_dialog(self) -> None:
        dialog = SymbolDialog(self._editor, self)
        dialog.exec()

    def _show_equation_dialog(self) -> None:
        dialog = EquationDialog(self._editor, self)
        dialog.exec()

    def _show_chart_dialog(self) -> None:
        dialog = ChartDialog(self)
        if dialog.exec():
            from rword.core.inserts import insert_chart

            values = dialog.values()
            if not values:
                self._show_error("Introduzca al menos un valor.")
                return
            if not insert_chart(self._editor, values, dialog.labels()):
                self._show_error("No se pudo insertar el gráfico.")

    def _show_smartart_dialog(self) -> None:
        dialog = SmartArtDialog(self)
        if dialog.exec():
            from rword.core.inserts import insert_smartart

            items = dialog.items()
            if not items:
                self._show_error("Introduzca al menos un elemento.")
                return
            if not insert_smartart(self._editor, items):
                self._show_error("No se pudo insertar el diagrama.")

    def _insert_date(self) -> None:
        from rword.core.inserts import insert_date

        insert_date(self._editor)

    def _insert_time(self) -> None:
        from rword.core.inserts import insert_time

        insert_time(self._editor)

    def _insert_file(self) -> None:
        from rword.core.inserts import insert_file_contents

        file_name, _ = QFileDialog.getOpenFileName(
            self, "Insertar archivo", "", "Documentos de texto (*.txt *.md *.rst)"
        )
        if file_name and not insert_file_contents(self._editor, file_name):
            self._show_error("No se pudo insertar el archivo.")

    def _insert_attachment(self) -> None:
        from rword.core.inserts import insert_attachment

        file_name, _ = QFileDialog.getOpenFileName(
            self, "Adjuntar archivo", "",
            "Archivos (*.pdf *.mp4 *.mp3 *.wav *.zip *.pdf)"
        )
        if file_name:
            insert_attachment(self._editor, file_name)

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
        self.styles_menu.clear()
        for name in sorted(self._style_manager.names()):
            action = self.styles_menu.addAction(name)
            action.triggered.connect(
                lambda checked=False, n=name: self._apply_style(n)
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

    def _columns_more(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        count, ok = QInputDialog.getInt(
            self, "Más columnas", "Número de columnas:", 3, 1, 8
        )
        if ok:
            self._set_columns(count)

    def _rebuild_margins_menu(self) -> None:
        self.margins_menu.clear()
        for name, (left, right, top, bottom) in STANDARD_TEMPLATES.items():
            action = self.margins_menu.addAction(name)
            action.triggered.connect(
                lambda checked=False, lm=left, rm=right, tm=top, bm=bottom:
                self._apply_margin_template(lm, rm, tm, bm)
            )
        self.margins_menu.addSeparator()
        for name in sorted(self._margin_store.names()):
            margins = self._margin_store.get(name)
            action = self.margins_menu.addAction(name)
            action.triggered.connect(
                lambda checked=False, lm=margins[0], rm=margins[1],
                tm=margins[2], bm=margins[3]:
                self._apply_margin_template(lm, rm, tm, bm)
            )
        self.margins_menu.addSeparator()
        self.margins_menu.addAction(self.save_margin_template_action)
        self.margins_menu.addAction(self.manage_margin_templates_action)
        self.margins_menu.addAction(self.page_setup_action)

    def _apply_margin_template(self, left, right, top, bottom) -> None:
        setup = apply_margins(self._editor, left, right, top, bottom)
        page = setup.page_size_px()
        self._page_view.set_page_size(int(page.width()), int(page.height()))
        self._page_view.update_paper_color(setup.page_color)
        self._refresh_rulers()

    def _save_margin_template(self) -> None:
        dialog = SaveMarginTemplateDialog(self._editor, self._margin_store, self)
        dialog.exec()

    def _manage_margin_templates(self) -> None:
        dialog = MarginTemplateManagerDialog(self._editor, self._margin_store, self)
        dialog.exec()

    def _choose_page_color(self) -> None:
        from PySide6.QtWidgets import QColorDialog

        setup = current_page_setup(self._editor)
        color = QColorDialog.getColor(
            QColor(setup.page_color), self, "Color de página"
        )
        if color.isValid():
            setup.page_color = color.name()
            apply_page_setup(self._editor, setup)
            self._page_view.update_paper_color(color.name())
            self._refresh_rulers()

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
            self._page_view.update_paper_color(new_setup.page_color)
            page = new_setup.page_size_px()
            self._page_view.set_page_size(int(page.width()), int(page.height()))
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
            self._navigation_panel = NavigationPanel(self._editor, self, self._icon_manager)
            self.addDockWidget(
                Qt.DockWidgetArea.RightDockWidgetArea, self._navigation_panel
            )
        self._navigation_panel.setVisible(checked)

    def _change_zoom(self, delta: int) -> None:
        self._set_zoom(self._editor.zoom() + delta)

    def _set_zoom(self, percent: int) -> None:
        self._editor.set_zoom(percent)
        self._page_view.refresh()
        self._refresh_rulers()

    def _fit_to_width(self) -> None:
        from rword.core.pages import current_page_setup

        setup = current_page_setup(self._editor)
        page_width = setup.page_size_px().width()
        viewport_width = max(1, self._editor.viewport().width())
        percent = int(viewport_width / page_width * 100)
        self._set_zoom(max(20, min(500, percent)))

    def _fit_page(self) -> None:
        from rword.core.pages import current_page_setup

        setup = current_page_setup(self._editor)
        page = setup.page_size_px()
        viewport = self._editor.viewport()
        percent = int(
            min(viewport.width() / page.width(), viewport.height() / page.height())
            * 100
        )
        self._set_zoom(max(20, min(500, percent)))

    def _enter_read_mode(self) -> None:
        self._editor.set_view_mode("read")
        self.ribbon.hide()
        self.statusBar().hide()

    def _exit_read_mode(self) -> None:
        self.ribbon.show()
        self.statusBar().show()
        self._editor.set_view_mode("print")

    def _enter_print_mode(self) -> None:
        self._exit_read_mode()
        self._editor.set_view_mode("print")

    def _enter_web_mode(self) -> None:
        self._exit_read_mode()
        self._editor.set_view_mode("web")

    def _enter_draft_mode(self) -> None:
        self._exit_read_mode()
        self._editor.set_view_mode("draft")

    def _enter_outline_mode(self) -> None:
        self._exit_read_mode()
        self._editor.set_view_mode("outline")
        self.toggle_navigation_action.setChecked(True)
        self._toggle_navigation_panel(True)

    def _toggle_ruler(self, checked: bool) -> None:
        self._ruler.setVisible(checked)
        self._vruler.setVisible(checked)
        self._corner.setVisible(checked)

    def _toggle_grid(self, checked: bool) -> None:
        self._editor.set_grid_visible(checked)

    def _toggle_fullscreen(self) -> None:
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def _split_window(self) -> None:
        if self._splitter is None:
            from rword.ui.page_view import PageView

            self._splitter = QSplitter(Qt.Orientation.Vertical, self)
            self._splitter.setObjectName("splitter")
            self._splitter.addWidget(self._editor)
            self._second_editor = Editor(self._splitter)
            self._second_editor.setDocument(self._editor.document())
            second_page = PageView(self._second_editor, self._splitter)
            second_page.update_paper_color(
                self._theme_manager.current.page_color
            )
            self._splitter.addWidget(second_page)
            self.setCentralWidget(self._splitter)
        else:
            self._splitter.setVisible(not self._splitter.isVisible())

    def _new_window(self) -> None:
        window = MainWindow()
        window._editor.setDocument(self._editor.document())
        window.show()

    def _insert_checkbox(self) -> None:
        from rword.core.forms import insert_checkbox

        insert_checkbox(self._editor)

    def _insert_radio(self) -> None:
        from rword.core.forms import insert_radio

        insert_radio(self._editor)

    def _insert_dropdown(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        from rword.core.forms import insert_dropdown

        text, ok = QInputDialog.getText(
            self, "Lista desplegable", "Opciones separadas por coma:"
        )
        if ok:
            options = [opt.strip() for opt in text.split(",") if opt.strip()]
            if options:
                insert_dropdown(self._editor, options)
            else:
                self._show_error("Introduzca al menos una opción.")

    def _insert_date_field(self) -> None:
        from rword.core.forms import insert_date_field

        insert_date_field(self._editor)

    def _insert_text_field(self) -> None:
        from rword.core.forms import insert_text_field

        insert_text_field(self._editor)

    def _insert_number_field(self) -> None:
        from rword.core.forms import insert_number_field

        insert_number_field(self._editor)

    def _insert_hidden_field(self) -> None:
        from rword.core.forms import insert_hidden_field

        insert_hidden_field(self._editor)

    def _toggle_protect_form(self, checked: bool) -> None:
        from rword.core.forms import protect_form

        protect_form(self._editor, checked)

    def _reset_form(self) -> None:
        from rword.core.forms import reset_form

        reset_form(self._editor)

    def _toggle_read_only(self, checked: bool) -> None:
        from rword.core.security import set_read_only

        set_read_only(self._editor, checked)

    def _set_modify_password(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        from rword.core.security import set_modify_password

        password, ok = QInputDialog.getText(
            self, "Contraseña para modificar", "Nueva contraseña:",
            echo=QLineEdit.EchoMode.Password,
        )
        if ok and password:
            set_modify_password(self._editor, password)
            from rword.core.security import set_read_only

            set_read_only(self._editor, True)

    def _remove_password(self) -> None:
        from rword.core.security import remove_modify_password, set_read_only

        remove_modify_password(self._editor)
        set_read_only(self._editor, False)

    def _unlock_edition(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        from rword.core.security import (
            has_modify_password,
            set_read_only,
            unlock_modify,
        )

        if not has_modify_password(self._editor):
            set_read_only(self._editor, False)
            return
        password, ok = QInputDialog.getText(
            self, "Desbloquear edición", "Contraseña:",
            echo=QLineEdit.EchoMode.Password,
        )
        if ok and unlock_modify(self._editor, password):
            set_read_only(self._editor, False)

    def _save_protected(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        from rword.core.security import encrypt_document

        password, ok = QInputDialog.getText(
            self, "Guardar con contraseña", "Contraseña:",
            echo=QLineEdit.EchoMode.Password,
        )
        if not ok or not password:
            return
        default = Path(self._suggested_name()).stem or "documento"
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Guardar con contraseña", f"{default}.rword",
            "Documento protegido (*.rword)",
        )
        if not file_name:
            return
        content = self._editor.toHtml()
        data = encrypt_document(content, password)
        Path(file_name).write_bytes(data)

    def _mark_final(self) -> None:
        from rword.core.security import mark_as_final

        mark_as_final(self._editor)

    def _sign_document(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        from rword.core.security import sign_document

        signer, ok = QInputDialog.getText(self, "Firmar documento", "Firmante:")
        if ok and signer:
            signature = sign_document(self._editor, signer)
            self.statusBar().showMessage(f"Firma: {signature[:12]}…", 6000)

    def _verify_signature(self) -> None:
        from rword.core.security import signer_of, verify_signature

        if verify_signature(self._editor):
            QMessageBox.information(
                self, "Firma", f"Firma válida de: {signer_of(self._editor)}"
            )
        else:
            QMessageBox.warning(
                self, "Firma", "La firma no es válida o el documento fue modificado."
            )

    def _inspect_document(self) -> None:
        from rword.core.security import inspect_personal_info

        findings = inspect_personal_info(self._editor)
        if not findings:
            QMessageBox.information(
                self, "Inspección", "No se encontró información personal."
            )
            return
        lines = [f"{kind}: {value}" for kind, value in findings]
        QMessageBox.information(
            self, "Inspección", "Información encontrada:\n" + "\n".join(lines)
        )

    def _remove_personal_info(self) -> None:
        from rword.core.security import remove_personal_info

        count = remove_personal_info(self._editor)
        self.statusBar().showMessage(
            f"Se eliminaron {count} elementos de información personal.", 5000
        )

    def _macro_manager_instance(self):
        from rword.core.macros import MacroManager

        if self._macro_manager is None:
            self._macro_manager = MacroManager(self._settings)
        return self._macro_manager

    def _record_macro(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        from rword.core.macros import MacroRecorder

        name, ok = QInputDialog.getText(self, "Grabar macro", "Nombre de la macro:")
        if not ok or not name.strip():
            return
        self._macro_recorder = MacroRecorder()
        self._editor.set_macro_recorder(self._macro_recorder)
        self._recording_name = name
        self.record_macro_action.setEnabled(False)
        self.stop_recording_action.setEnabled(True)
        self.statusBar().showMessage("Grabando macro...", 0)

    def _stop_recording(self) -> None:
        self._editor.set_macro_recorder(None)
        self.record_macro_action.setEnabled(True)
        self.stop_recording_action.setEnabled(False)
        if self._macro_recorder is not None:
            manager = self._macro_manager_instance()
            manager.add(self._recording_name, self._macro_recorder.script())
            self._macro_recorder = None
        self.statusBar().showMessage("Grabación finalizada.", 3000)

    def _manage_macros(self) -> None:
        from rword.ui.dialogs.macro import MacroDialog

        dialog = MacroDialog(self._macro_manager_instance(), self._editor, self)
        dialog.exec()

    def _assign_macro_shortcut(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        manager = self._macro_manager_instance()
        names = sorted(manager.names())
        if not names:
            self._show_error("No hay macros definidas.")
            return
        name, ok = QInputDialog.getItem(
            self, "Asignar macro a teclado", "Macro:", names, 0, False
        )
        if not ok:
            return
        shortcut, ok = QInputDialog.getText(
            self, "Asignar macro a teclado",
            "Atajo (p. ej. Ctrl+Shift+M):",
            text=manager.shortcuts().get(name, ""),
        )
        if ok:
            manager.assign_shortcut(name, shortcut)

    def _rebuild_macro_shortcuts(self) -> None:
        menu = self.automation_menu
        for action in self._macro_shortcut_actions:
            menu.removeAction(action)
        self._macro_shortcut_actions = []
        manager = self._macro_manager_instance()
        for name, shortcut in manager.shortcuts().items():
            if not shortcut or name not in manager.names():
                continue
            action = QAction(f"Ejecutar: {name}", self)
            action.setShortcut(shortcut)
            action.triggered.connect(
                lambda checked=False, n=name: manager.run(self._editor, n)
            )
            menu.addAction(action)
            self._macro_shortcut_actions.append(action)

    def _edit_variables(self) -> None:
        from PySide6.QtWidgets import (
            QDialog,
            QDialogButtonBox,
            QHBoxLayout,
            QLineEdit,
            QListWidget,
            QPushButton,
        )

        from rword.core.macros import (
            document_variables,
        )

        dialog = QDialog(self)
        dialog.setWindowTitle("Variables de documento")
        layout = QVBoxLayout(dialog)
        var_list = QListWidget(dialog)
        var_list.addItems(sorted(document_variables(self._editor)))
        layout.addWidget(var_list)
        row = QHBoxLayout()
        name_input = QLineEdit(dialog)
        name_input.setPlaceholderText("Nombre")
        value_input = QLineEdit(dialog)
        value_input.setPlaceholderText("Valor")
        row.addWidget(name_input)
        row.addWidget(value_input)
        layout.addLayout(row)
        add_button = QPushButton("Añadir/Actualizar", dialog)
        add_button.clicked.connect(
            lambda: self._add_variable(
                dialog, name_input, value_input, var_list
            )
        )
        remove_button = QPushButton("Eliminar", dialog)
        remove_button.clicked.connect(
            lambda: self._remove_variable(dialog, var_list)
        )
        layout.addWidget(add_button)
        layout.addWidget(remove_button)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close, dialog)
        buttons.rejected.connect(dialog.accept)
        layout.addWidget(buttons)
        dialog.exec()

    def _add_variable(self, dialog, name_input, value_input, var_list) -> None:
        from rword.core.macros import document_variables, set_variable

        if name_input.text().strip():
            set_variable(self._editor, name_input.text().strip(), value_input.text())
            var_list.clear()
            var_list.addItems(sorted(document_variables(self._editor)))

    def _remove_variable(self, dialog, var_list) -> None:
        from rword.core.macros import remove_variable

        item = var_list.currentItem()
        if item is not None and remove_variable(self._editor, item.text()):
            var_list.takeItem(var_list.row(item))

    def _select_data_source(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        from rword.core.mailmerge import (
            data_fields,
            load_csv,
            load_sqlite,
            set_records,
        )

        file_name, _ = QFileDialog.getOpenFileName(
            self, "Origen de datos", "",
            "CSV (*.csv);;Base de datos SQLite (*.db *.sqlite);;Todos los archivos (*)",
        )
        if not file_name:
            return
        try:
            if file_name.endswith(".csv"):
                records = load_csv(file_name)
            else:
                query, ok = QInputDialog.getText(
                    self, "Base de datos",
                    "Consulta SQL (p. ej. SELECT * FROM contactos):",
                    text="SELECT * FROM contactos",
                )
                if not ok:
                    return
                records = load_sqlite(file_name, query)
        except Exception as error:
            self._show_error(f"No se pudieron cargar los datos:\n{error}")
            return
        if not records:
            self._show_error("El origen de datos no contiene registros.")
            return
        set_records(self._editor, records, file_name)
        self._merge_fields = data_fields(records)
        self.statusBar().showMessage(
            f"Origen de datos cargado: {len(records)} registros.", 5000
        )

    def _rebuild_field_menu(self) -> None:
        self.field_menu.clear()
        fields = getattr(self, "_merge_fields", [])
        if not fields:
            action = self.field_menu.addAction("(sin origen de datos)")
            action.setEnabled(False)
            return
        for field in fields:
            action = self.field_menu.addAction(f"{{{field}}}")
            action.triggered.connect(
                lambda checked=False, f=field: self._insert_merge_field(f)
            )

    def _insert_merge_field(self, field: str | None = None) -> None:
        if field is None:
            from PySide6.QtWidgets import QInputDialog

            from rword.core.mailmerge import data_fields, records_of

            fields = data_fields(records_of(self._editor))
            if not fields:
                self._show_error("Seleccione primero un origen de datos.")
                return
            field, ok = QInputDialog.getItem(
                self, "Insertar campo", "Campo:", fields, 0, False
            )
            if not ok:
                return
        self._editor.insertPlainText("{" + field + "}")

    def _preview_merge(self) -> None:
        from rword.core.mailmerge import records_of
        from rword.ui.dialogs.mailmerge import MailMergePreviewDialog

        records = records_of(self._editor)
        if not records:
            self._show_error("Seleccione primero un origen de datos.")
            return
        dialog = MailMergePreviewDialog(self._editor, records, self)
        dialog.exec()

    def _filter_records(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        from rword.core.mailmerge import (
            data_fields,
            distinct_values,
            filter_records,
            records_of,
            set_records,
        )

        records = records_of(self._editor)
        fields = data_fields(records)
        if not fields:
            return
        field, ok = QInputDialog.getItem(
            self, "Filtrar destinatarios", "Columna:", fields, 0, False
        )
        if not ok:
            return
        values = distinct_values(records, field)
        value, ok = QInputDialog.getItem(
            self, "Filtrar destinatarios", "Valor:", values, 0, False
        )
        if ok:
            filtered = filter_records(records, field, value)
            set_records(self._editor, filtered)
            self.statusBar().showMessage(f"{len(filtered)} destinatarios.", 4000)

    def _sort_records(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        from rword.core.mailmerge import (
            data_fields,
            records_of,
            set_records,
            sort_records,
        )

        records = records_of(self._editor)
        fields = data_fields(records)
        if not fields:
            return
        field, ok = QInputDialog.getItem(
            self, "Ordenar destinatarios", "Columna:", fields, 0, False
        )
        if ok:
            set_records(self._editor, sort_records(records, field))

    def _generate_letters(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        from rword.core.mailmerge import records_of

        records = records_of(self._editor)
        if not records:
            self._show_error("Seleccione primero un origen de datos.")
            return
        count, ok = QInputDialog.getInt(
            self, "Generar cartas", "Número de cartas a generar:", len(records),
            1, len(records),
        )
        if not ok:
            return
        from rword.core.mailmerge import generate_letters

        combined = generate_letters(self._editor, records[:count])
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Guardar cartas combinadas", "cartas.txt", "Texto (*.txt)"
        )
        if file_name:
            Path(file_name).write_text(combined, encoding="utf-8")

    def _generate_labels(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        from rword.core.mailmerge import (
            data_fields,
            generate_labels,
            records_of,
        )

        records = records_of(self._editor)
        fields = data_fields(records)
        if not fields:
            return
        chosen, ok = QInputDialog.getItem(
            self, "Generar etiquetas", "Campo de la etiqueta:", fields, 0, False
        )
        if not ok:
            return
        columns, ok = QInputDialog.getInt(
            self, "Generar etiquetas", "Columnas por fila:", 3, 1, 6
        )
        if ok:
            output = generate_labels(records, [chosen], columns)
            self._editor.insertPlainText(output)

    def _generate_envelopes(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        from rword.core.mailmerge import (
            data_fields,
            generate_envelopes,
            records_of,
        )

        records = records_of(self._editor)
        fields = data_fields(records)
        if not fields:
            return
        chosen, ok = QInputDialog.getItem(
            self, "Generar sobres", "Campo de dirección:", fields, 0, False
        )
        if ok:
            output = generate_envelopes(self._editor, records, [chosen])
            self._editor.insertPlainText(output)

    def _send_email(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        from rword.core.mailmerge import mailto_link, records_of

        records = records_of(self._editor)
        if not records:
            self._show_error("Seleccione primero un origen de datos.")
            return
        subject, ok = QInputDialog.getText(
            self, "Enviar por correo", "Asunto:", text="Comunicación"
        )
        if not ok:
            return
        from PySide6.QtCore import QUrl
        from PySide6.QtGui import QDesktopServices

        for record in records[:10]:
            link = mailto_link(record, subject)
            if link:
                QDesktopServices.openUrl(QUrl(link))

    def _collaboration_manager(self):
        from rword.core.collaboration import CollaborationManager

        if not hasattr(self, "_collab_manager"):
            self._collab_manager = CollaborationManager(self._editor, self._settings)
        return self._collab_manager

    def _show_collaboration(self) -> None:
        from rword.ui.dialogs.collaboration import CollaborationDialog

        dialog = CollaborationDialog(self._collaboration_manager(), self)
        dialog.exec()

    def _set_username(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        manager = self._collaboration_manager()
        name, ok = QInputDialog.getText(
            self, "Nombre de usuario", "Nombre:", text=manager.username
        )
        if ok and name.strip():
            manager.set_username(name.strip())
            self._update_presence_label()
            self._collaboration_manager().log(
                "Cambió el nombre de usuario", name.strip()
            )

    def _toggle_track_authors(self, checked: bool) -> None:
        self._collaboration_manager().set_track_authors(checked)

    def _toggle_presence(self, checked: bool) -> None:
        self._presence_label.setVisible(checked)
        self._collaboration_manager().log(
            "Conectado" if checked else "Desconectado"
        )

    def _update_presence_label(self) -> None:
        if not hasattr(self, "_presence_label"):
            return
        self._presence_label.setStyleSheet(
            "background: #22c55e; border-radius: 4px;"
        )
        self._presence_label.setFixedSize(8, 8)
        self._presence_user_label.setText(
            self._collaboration_manager().username
        )

    def _log_activity(self, event: str, detail: str = "") -> None:
        if hasattr(self, "_collab_manager"):
            self._collab_manager.log(event, detail)

    def _check_accessibility(self) -> None:
        from rword.core.accessibility import check_accessibility

        issues = check_accessibility(self._editor)
        if not issues:
            QMessageBox.information(
                self, "Accesibilidad", "El documento supera la comprobación."
            )
            return
        lines = [f"- {category}: {problem}" for category, problem in issues]
        QMessageBox.information(
            self,
            "Comprobador de accesibilidad",
            f"Se encontraron {len(issues)} problemas:\n\n" + "\n".join(lines[:20]),
        )

    def _set_alt_text(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        from rword.core.accessibility import (
            image_alt_text_at_cursor,
            set_image_alt_text,
        )

        if not hasattr(self._editor, "file_path"):
            return
        current = image_alt_text_at_cursor(self._editor)
        alt_text, ok = QInputDialog.getText(
            self, "Texto alternativo", "Descripción de la imagen:", text=current
        )
        if ok and not set_image_alt_text(self._editor, alt_text):
            self._show_error("Coloque el cursor sobre una imagen.")

    def _read_aloud(self) -> None:
        from rword.core.accessibility import SpeechReader

        if not hasattr(self, "_speech"):
            self._speech = SpeechReader(self)
        cursor = self._editor.textCursor()
        text = cursor.selectedText().replace("\u2029", "\n")
        if not text:
            text = self._editor.toPlainText()
        self._speech.speak(text)

    def _stop_reading(self) -> None:
        if hasattr(self, "_speech"):
            self._speech.stop()

    def _apply_high_contrast(self) -> None:
        self._apply_theme("Alto contraste")

    def _toggle_immersive(self, checked: bool) -> None:
        if checked:
            self.ribbon.hide()
            self.statusBar().hide()
        else:
            self.ribbon.show()
            self.statusBar().show()

    def _apply_saved_preferences(self) -> None:
        from rword.core.preferences import UserPreferences

        preferences = UserPreferences(self._settings)
        self._set_zoom(preferences.default_zoom)
        if preferences.dark_theme:
            QApplication.instance().setStyleSheet(DARK_STYLESHEET)

    def _show_preferences(self) -> None:
        from rword.core.preferences import UserPreferences
        from rword.ui.dialogs.preferences import PreferencesDialog

        preferences = UserPreferences(self._settings)
        dialog = PreferencesDialog(preferences, self)
        if dialog.exec():
            if preferences.dark_theme:
                QApplication.instance().setStyleSheet(DARK_STYLESHEET)
            else:
                QApplication.instance().setStyleSheet("")
            self._collaboration_manager().set_username(preferences.username)
            self._update_presence_label()
            self._icon_manager.set_color(icon_color_for(self))
            self._refresh_rulers()

    def _show_shortcuts(self) -> None:
        from rword.ui.dialogs.customize import ShortcutsDialog

        actions = {
            "new": self.new_action,
            "open": self.open_action,
            "save": self.save_action,
            "save_as": self.save_as_action,
            "find": self.find_action,
            "replace": self.replace_action,
            "bold": self.bold_action,
            "italic": self.italic_action,
            "underline": self.underline_action,
        }
        dialog = ShortcutsDialog(actions, self._settings, self)
        dialog.exec()

    def _manage_plugins(self) -> None:
        from PySide6.QtWidgets import (
            QCheckBox,
            QDialog,
            QDialogButtonBox,
        )

        dialog = QDialog(self)
        dialog.setWindowTitle("Administrar complementos")
        layout = QVBoxLayout(dialog)
        checkboxes = {}
        for plugin in self._plugin_manager.available():
            check = QCheckBox(plugin.name, dialog)
            check.setChecked(self._plugin_manager.is_enabled(plugin.name))
            checkboxes[plugin.name] = check
            layout.addWidget(check)
        if not checkboxes:
            from PySide6.QtWidgets import QLabel

            layout.addWidget(QLabel("No se encontraron complementos.", dialog))
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close, dialog)
        buttons.rejected.connect(dialog.accept)
        layout.addWidget(buttons)
        dialog.exec()
        for name, check in checkboxes.items():
            self._plugin_manager.set_enabled(name, check.isChecked())

    def _configure_api_key(self) -> None:
        from rword.core.ai.config import ApiKeyManager
        from rword.ui.dialogs.api_key import ApiKeyDialog

        dialog = ApiKeyDialog(ApiKeyManager(self._settings), self)
        dialog.exec()

    def _ai_about(self) -> None:
        from rword.core.ai.config import DEFAULT_MODEL

        QMessageBox.information(
            self,
            "Acerca de la IA",
            f"Integración con DeepSeek ({DEFAULT_MODEL}).\n"
            "Las funciones de IA se ejecutan a través de la API oficial. "
            "Consulte la documentación de privacidad de DeepSeek.",
        )

    def _ai_client(self):
        from rword.core.ai import DeepSeekClient
        from rword.core.ai.config import ApiKeyManager

        manager = ApiKeyManager(self._settings)
        return DeepSeekClient(manager.get())

    def _ai_error(self, error) -> None:
        self._show_error(f"Error de IA:\n{error}")

    def _ai_run_and_apply(self, operation, insert_mode: str = "insert") -> None:
        """Ejecuta una operación de IA y aplica el resultado al editor."""
        from rword.core.ai import AiError

        try:
            result = operation()
        except AiError as error:
            self._ai_error(error)
            return
        if insert_mode == "replace_selection":
            cursor = self._editor.textCursor()
            if cursor.hasSelection():
                cursor.insertText(result)
            else:
                self._editor.insertPlainText(result)
        elif insert_mode == "replace_document":
            self._editor.setPlainText(result)
        else:
            self._editor.insertPlainText(result)
        self.statusBar().showMessage("Operación de IA completada.", 3000)

    def _ai_context(self, function: str, insert_mode: str = "insert") -> None:
        from rword.core.ai import capabilities
        from rword.core.ai.session import document_context

        client = self._ai_client()
        context = document_context(self._editor)
        operation = getattr(capabilities, function)
        self._ai_run_and_apply(
            lambda fn=operation, c=context: fn(client, c),
            insert_mode,
        )

    def _ai_redact(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        from rword.core.ai import capabilities

        instruction, ok = QInputDialog.getText(
            self, "Redactar con IA", "Instrucción:"
        )
        if not ok or not instruction.strip():
            return
        client = self._ai_client()
        self._ai_run_and_apply(
            lambda: capabilities.redact(client, instruction.strip())
        )

    def _ai_rewrite(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        from rword.core.ai import capabilities
        from rword.core.ai.session import document_context

        instruction, ok = QInputDialog.getText(
            self, "Reescribir con IA", "Indicación (p. ej. hazlo más técnico):"
        )
        if not ok:
            return
        client = self._ai_client()
        context = document_context(self._editor)
        self._ai_run_and_apply(
            lambda: capabilities.rewrite(client, context, instruction.strip()),
            "replace_selection",
        )

    def _ai_translate(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        from rword.core.ai import capabilities
        from rword.core.ai.session import document_context

        target, ok = QInputDialog.getItem(
            self,
            "Traducir con IA",
            "Idioma de destino:",
            ["inglés", "español", "francés", "alemán", "portugués", "italiano"],
            0,
            False,
        )
        if not ok:
            return
        client = self._ai_client()
        context = document_context(self._editor)
        if not context.strip():
            self._show_error("No hay texto para traducir.")
            return
        insert_mode = (
            "replace_selection"
            if self._editor.textCursor().hasSelection()
            else "insert"
        )
        self._ai_run_and_apply(
            lambda: capabilities.translate(client, context, target),
            insert_mode,
        )

    def _toggle_ai_chat(self, checked: bool) -> None:
        from rword.ui.ai_chat_panel import AiChatPanel

        if self._ai_chat_panel is None:
            self._ai_chat_panel = AiChatPanel(
                self._editor, self._ai_client, self, self._icon_manager
            )
            self.addDockWidget(
                Qt.DockWidgetArea.RightDockWidgetArea, self._ai_chat_panel
            )
        self._ai_chat_panel.setVisible(checked)

    def _ai_domain(self, function: str, prompt_label: str | None, style: str) -> None:
        from PySide6.QtWidgets import QInputDialog

        from rword.core.ai import capabilities
        from rword.core.ai.session import document_context

        client = self._ai_client()
        context = document_context(self._editor)
        fn = getattr(capabilities, function)

        if style == "context":
            self._ai_run_and_apply(lambda c=context: fn(client, c))
            return

        value, ok = QInputDialog.getText(self, "IA", prompt_label or "Instrucción:")
        if not ok or not value.strip():
            return
        value = value.strip()

        if style == "prompt":
            self._ai_run_and_apply(lambda v=value: fn(client, v))
        elif style == "prompt_context":
            self._ai_run_and_apply(lambda v=value, c=context: fn(client, v, c))
        elif style == "prompt_compare":
            self._ai_run_and_apply(
                lambda v=value, c=context: fn(client, c, v)
            )
        elif style == "prompt_count":
            count, ok = QInputDialog.getInt(
                self, "IA", "Cantidad:", 5, 1, 50
            )
            if ok:
                self._ai_run_and_apply(
                    lambda v=value, n=count: fn(client, v, n)
                )

    def _ai_write_like(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        from rword.core.ai import capabilities

        sample = self._settings.value("ai/style_sample", "")
        if not sample:
            self._show_error(
                "Primero aprenda su estilo con «Aprender mi estilo»."
            )
            return
        instruction, ok = QInputDialog.getText(
            self, "Escribir como yo", "¿Qué quiere que escriba?"
        )
        if not ok or not instruction.strip():
            return
        client = self._ai_client()
        self._ai_run_and_apply(
            lambda: capabilities.write_like(client, sample, instruction.strip())
        )

    def _learn_style(self) -> None:
        from rword.core.assist import style_sample_from_selection

        sample = style_sample_from_selection(self._editor)
        if not sample.strip():
            self._show_error("Seleccione texto para aprender su estilo.")
            return
        self._settings.setValue("ai/style_sample", sample[:4000])
        self.statusBar().showMessage("Estilo aprendido correctamente.", 4000)

    def _ai_project_memory(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        from rword.core.ai import capabilities
        from rword.core.macros import document_variables

        memory = "\n".join(
            f"{key}: {value}" for key, value in document_variables(self._editor).items()
        )
        if not memory:
            self._show_error("No hay variables de proyecto definidas.")
            return
        instruction, ok = QInputDialog.getText(
            self, "Memoria del proyecto", "Instrucción:"
        )
        if not ok or not instruction.strip():
            return
        client = self._ai_client()
        self._ai_run_and_apply(
            lambda: capabilities.project_memory(client, memory, instruction.strip())
        )

    def _show_smart_templates(self) -> None:
        from rword.ui.dialogs.smart_template import SmartTemplateDialog

        dialog = SmartTemplateDialog(self._editor, self)
        dialog.exec()

    def _toggle_autocomplete(self, checked: bool) -> None:
        if checked:
            from rword.core.assist import completer_words

            words = completer_words(self._editor)
            self._editor.set_completion_words(words)
        else:
            self._editor.setCompleter(None)

    def _coherence_check(self) -> None:
        from rword.core.ai import capabilities
        from rword.core.ai.session import document_context
        from rword.core.assist import consistency_findings

        local = consistency_findings(self._editor)
        lines = [f"- {category}: {detail}" for category, detail in local]
        if self._ai_client().configured:
            context = document_context(self._editor)
            client = self._ai_client()
            self._ai_run_and_apply(
                lambda: capabilities.coherence_check(client, context),
                "insert",
            )
        elif lines:
            QMessageBox.information(
                self, "Inspector de coherencia", "\n".join(lines)
            )
        else:
            QMessageBox.information(
                self, "Inspector de coherencia", "Sin incoherencias detectadas."
            )

    def _generate_glossary(self) -> None:
        from rword.core.assist import generate_glossary

        generate_glossary(self._editor)

    def _ai_agent(self, role: str, label: str) -> None:
        from PySide6.QtWidgets import QInputDialog

        from rword.core.ai import capabilities

        instruction, ok = QInputDialog.getText(
            self, f"Agente: {label}", "Su consulta:"
        )
        if not ok or not instruction.strip():
            return
        client = self._ai_client()
        self._ai_run_and_apply(
            lambda: capabilities.agent_reply(client, role, instruction.strip())
        )

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
            self._comments_panel = CommentsPanel(self._editor, self, self._icon_manager)
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

    def _check_spelling(self) -> None:
        from rword.core.spelling import SpellChecker

        if not hasattr(self, "_spell_checker"):
            self._spell_checker = SpellChecker(self._settings)
        count = self._spell_checker.highlight_misspelled(self._editor)
        if count:
            self.statusBar().showMessage(
                f"Revisión ortográfica: {count} palabras desconocidas.", 5000
            )
        else:
            self.statusBar().showMessage("Revisión ortográfica: sin errores.", 5000)

    def _add_dictionary_word(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        from rword.core.spelling import SpellChecker

        word, ok = QInputDialog.getText(
            self, "Añadir al diccionario", "Palabra:"
        )
        if ok and word:
            checker = getattr(
                self, "_spell_checker", SpellChecker(self._settings)
            )
            self._spell_checker = checker
            checker.add_word(word)

    def _manage_dictionary(self) -> None:
        from PySide6.QtWidgets import (
            QDialog,
            QDialogButtonBox,
            QListWidget,
            QPushButton,
        )

        from rword.core.spelling import SpellChecker

        checker = getattr(self, "_spell_checker", SpellChecker(self._settings))
        self._spell_checker = checker
        dialog = QDialog(self)
        dialog.setWindowTitle("Diccionario personalizado")
        layout = QVBoxLayout(dialog)
        word_list = QListWidget(dialog)
        word_list.addItems(checker.user_words())
        layout.addWidget(word_list)
        remove_button = QPushButton("Quitar seleccionada", dialog)
        remove_button.clicked.connect(
            lambda: self._remove_dictionary_word(checker, word_list)
        )
        layout.addWidget(remove_button)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close, dialog)
        buttons.rejected.connect(dialog.accept)
        layout.addWidget(buttons)
        dialog.exec()

    def _remove_dictionary_word(self, checker, word_list) -> None:
        item = word_list.currentItem()
        if item is not None and checker.remove_word(item.text()):
            word_list.takeItem(word_list.row(item))

    def _show_thesaurus(self) -> None:
        dialog = ThesaurusDialog(self._editor, self)
        dialog.exec()

    def _show_count(self) -> None:
        dialog = CountDialog(self._editor, self)
        dialog.exec()

    def _translate_selection(self) -> None:
        from PySide6.QtWidgets import QInputDialog

        from rword.core.translate import translate_text

        selected = self._editor.textCursor().selectedText().replace("\u2029", "\n")
        if not selected:
            self._show_error("Seleccione texto para traducir.")
            return
        target, ok = QInputDialog.getItem(
            self,
            "Traducir",
            "Idioma de destino:",
            ["Inglés (en)", "Español (es)"],
            0,
            False,
        )
        if not ok:
            return
        code = "en" if target.startswith("Inglés") else "es"
        translation = translate_text(selected, code)
        self._editor.insertPlainText(translation)

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
        self._page_view.update_paper_color(theme.page_color)
        self._icon_manager.set_color(icon_color_for(self))

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
        self._editor.cursorPositionChanged.connect(self._refresh_rulers)
        self._editor.document().contentsChange.connect(
            lambda *_: self._refresh_rulers()
        )
        self._page_view.verticalScrollBar().valueChanged.connect(
            lambda *_: self._refresh_rulers()
        )
        self._page_view.layout_changed.connect(self._refresh_rulers)
        self._ruler.margins_changed.connect(self._on_ruler_margins_changed)
        self._vruler.margins_changed.connect(self._on_ruler_margins_changed)

    def _refresh_rulers(self) -> None:
        self._ruler.update()
        self._vruler.update()

    def _on_ruler_margins_changed(self, setup) -> None:
        from rword.core.pages import apply_page_setup

        apply_page_setup(self._editor, setup)
        page = setup.page_size_px()
        self._page_view.set_page_size(int(page.width()), int(page.height()))
        self._page_view.update_paper_color(setup.page_color)
        self._refresh_rulers()

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
        ribbon_visible = self._settings.value(RIBBON_VISIBLE_KEY, True, type=bool)
        self.ribbon.setVisible(ribbon_visible)
        self.toggle_toolbar_action.setChecked(ribbon_visible)
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
            RIBBON_VISIBLE_KEY, self.ribbon.isVisible()
        )
        self._settings.setValue(
            STATUSBAR_VISIBLE_KEY, self.statusBar().isVisible()
        )
        event.accept()

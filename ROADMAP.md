# ROADMAP de rword

Procesador de texto profesional con integración de IA (DeepSeek), construido con
PySide6 (Qt for Python).

## Plan de fases

| # | Fase | Alcance principal | Estado |
|---|------|-------------------|--------|
| 1 | **Base y arquitectura** | Ventana principal, menús, toolbar, editor, gestión de documentos (nuevo/abrir/guardar), barra de estado, preferencias | ✅ Implementada |
| 2 | **Edición de texto** | Selección, cortar/copiar/pegar, portapapeles múltiple, buscar/reemplazar (avanzado), ir a página/sección/marcador, arrastrar y soltar | ✅ Implementada |
| 3 | **Formato de fuente** | Fuente/tamaño, negrita/cursiva/subrayado/tachado, superíndice/subíndice, color/resaltado, mayúsculas, espaciado de caracteres, efectos | ✅ Implementada |
| 4 | **Formato de párrafo** | Alineación, sangrías, interlineado, espaciado, viñetas/numeración/multinivel, tabulaciones, bordes y sombreado, control de página | Pendiente |
| 5 | **Estilos y temas** | Aplicar/crear/modificar/eliminar estilos, organizador, títulos, tema (colores/fuentes/efectos) | Pendiente |
| 6 | **Diseño de página** | Márgenes, orientación, tamaño, columnas, saltos, fondo/marca de agua, numeración de líneas, guiones | Pendiente |
| 7 | **Tablas** | Insertar/dibujar, filas/columnas, combinar/dividir, bordes/sombreado, ordenar, fórmulas, convertir texto↔tabla | Pendiente |
| 8 | **Imágenes** | Insertar, redimensionar/recortar, girar/voltear, ajuste de texto, brillo/contraste, efectos, agrupar/ordenar | Pendiente |
| 9 | **Formas, cuadros y WordArt** | Formas, relleno/contorno, cuadros de texto, WordArt, efectos de texto, agrupar/alinear | Pendiente |
| 10 | **Hipervínculos y navegación** | Enlaces, marcadores, panel de navegación por títulos/páginas | Pendiente |
| 11 | **Encabezados y pies** | Insertar/editar encabezado y pie, número de página, primera página diferente, campos automáticos | Pendiente |
| 12 | **Referencias** | Tabla de contenido, notas al pie/final, citas y bibliografía, leyendas, índice analítico | Pendiente |
| 13 | **Comentarios y revisión** | Comentarios anidados, control de cambios, aceptar/rechazar, comparar/combinar documentos | Pendiente |
| 14 | **Corrección y recuento** | Corrector ortográfico/gramatical, diccionario, sinónimos/antónimos, contar palabras/caracteres, idioma, legibilidad | Pendiente |
| 15 | **Objetos insertados y dibujo** | Iconos/SVG/gráficos/ecuaciones/símbolos, PDF/video/audio, lápiz/pluma/resaltador/borrador, tinta→texto | Pendiente |
| 16 | **Vista y zoom** | Modos de vista, zoom, regla, cuadrícula, miniaturas, pantalla completa, dividir ventana | Pendiente |
| 17 | **Impresión y exportación** | Vista previa, imprimir (rangos/doble cara/por hoja), exportar PDF/HTML/ODT/RTF/TXT/EPUB | Pendiente |
| 18 | **Formularios** | Casillas, botones, listas, campos de texto/número/fecha, protección de formulario | Pendiente |
| 19 | **Seguridad** | Solo lectura, contraseñas, restricciones, firmas digitales, inspección, marcar como final | Pendiente |
| 20 | **Automatización y macros** | Grabar/editar/ejecutar macros, asignar a botón/teclado, campos automáticos | Pendiente |
| 21 | **Combinación de correspondencia** | Origen de datos, campos, vista previa, filtros, cartas/etiquetas/sobres | Pendiente |
| 22 | **Colaboración** | Edición colaborativa, compartir, presencia, historial, permisos, resolución de conflictos | Pendiente |
| 23 | **Accesibilidad** | Comprobador, texto alternativo, teclado, lectores de pantalla, dictado, lectura en voz alta | Pendiente |
| 24 | **Personalización** | Cinta, barra rápida, temas visuales, modo oscuro, atajos, preferencias de usuario | Pendiente |
| 25 | **IA — Infraestructura** | Cliente DeepSeek, gestión de API key, gestión de errores/tiempos, seguridad | Pendiente |
| 26 | **IA — Escritura y corrección** | Redactar/continuar, resumir, reescribir, tono, expandir/reducir, ortografía/gramática avanzada, redundancias | Pendiente |
| 27 | **IA — Traducción y análisis** | Traducir documento/selección (con formato), detección de idioma, ideas, conclusiones, legibilidad, público | Pendiente |
| 28 | **IA — Selección y chat** | Preguntas sobre selección, chat contextual sobre el documento ("pregúntale al documento") | Pendiente |
| 29 | **IA — Dominios especializados** | Legal, programación, educación, negocios, investigación (bibliografía), comparación de documentos | Pendiente |
| 30 | **IA — Automatización y productividad** | Índices, tablas/listas, Mermaid, JSON/XML/YAML, detección de fechas/personas/datos, marketing, tareas | Pendiente |
| 31 | **IA — Premium y pulido final** | Agentes especializados, estilo del usuario, OCR, extracción PDF, generación de imágenes, "escribir como", inspector de coherencia, anexos | Pendiente |

**Total: 31 fases** (1 completada, 30 pendientes).

## Metodología de ejecución

Cada fase sigue el flujo definido en `build_rules.md`:

1. Implementación completa de la fase.
2. Validación técnica: compilar, tests, linters.
3. Validación funcional: endpoints, casos de éxito/error, flujos completos.
4. Pruebas de regresión de fases anteriores.
5. Revisión de calidad (sin TODO, código muerto, secretos o errores).
6. Confirmación de la fase.
7. Commit atómico (Conventional Commits) y push.
8. Inicio inmediato de la siguiente fase.

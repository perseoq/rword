# TODO de rword

Lista de trabajo del proyecto, organizada por versiones. Todo plan nuevo se
registra aquí (marcado `[ ]`) **antes** de implementarse, y se marca `[x]` en
el commit correspondiente cuando queda terminado y validado.

## v0.1.x — Base del editor (implementado)

- [x] Las 31 fases del editor completo + IA (ver `ROADMAP.md`).
- [x] Vista de página tipo Word: hoja blanca centrada sobre fondo gris, con
      el scroll en el área gris (no dentro de la hoja).
- [x] Reglas estilo Word: regla superior + lateral, arrastre de sangrías,
      tabulaciones y márgenes, numeración en centímetros.
- [x] `requirements.txt`, `requirements-dev.txt` y `.gitignore`.
- [x] Documentación del plan de fases en `ROADMAP.md`.

## v0.2.0 — Cinta de opciones + Iconografía (implementado)

- [x] **Iconos Lucide en toda la UI** (`rword/ui/icons.py`): catálogo SVG
      incrustado, `make_icon(name, color, size)`, `apply_action_icons`,
      `recolor_icons()` al cambiar de tema (claro/oscuro).
- [x] **Cinta de opciones estilo Word** (`rword/ui/ribbon.py`): pestañas y
      grupos con título al pie; botón `«`/`»` (chevrons) que desplaza las
      cintillas ocultas por desbordamiento **sin menú emergente**.
- [x] Sustituir los 20 menús y las 4 barras de herramientas por pestañas y
      grupos de la cinta (Inicio, Insertar, Diseño de página, Referencias,
      Revisión, Vista, Correspondencia, Automatización, Colaboración y
      seguridad, Accesibilidad, IA, Ayuda).
- [x] Refactor de `FormatBar`, `ParagraphBar` y `DrawingBar` a widgets
      embebibles (mantienen su sincronización con el cursor).
- [x] **Columnas** en «Diseño de página»: Una / Dos / Tres / Más columnas….
- [x] **Márgenes y plantillas de márgenes**: presets estándar (Normal,
      Estrecho, Moderado, Ancho, Oficina 2003) + plantillas personalizadas
      con nombre (guardar/renombrar/eliminar), persistidas en QSettings.
- [x] Limpieza de emojis/símbolos-icono (chat de IA, comentarios, panel de
      navegación, presencia, adjunto).
- [x] Integración en `main_window.py`: toggle único «Cinta de opciones»,
      modo lectura/enfoque inmersivo, plugin hook `add_ribbon_action`,
      `RIBBON_VISIBLE_KEY` y tests.
- [x] **Soporte de formato .docx** (Word) como formato por defecto: abrir y
      guardar con `python-docx` (texto con formato, listas, tablas e
      imágenes), filtro por defecto en Archivo y nombre sugerido `.docx`.
      El HTML completo del editor se incrusta en el `.docx` para conservar
      el formato exacto al reabrir en la app.

## v0.3.0 — Futuro (pendientes)

- [ ] Rediseño visual inspirado en shadcn/ui (fuera del alcance actual).
- [ ] (Aquí se añadirán los nuevos pedidos antes de implementarlos.)

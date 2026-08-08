# rword

Procesador de texto profesional con integración de IA (DeepSeek), construido con
PySide6 (Qt for Python).

## Estado

**31 fases completadas** de 31. Consulte `ROADMAP.md` para el detalle de cada fase.

Resumen de capacidades:

- **Editor**: gestión de documentos, edición, formato de fuente y párrafo,
  estilos y temas, diseño de página, tablas, imágenes, formas, WordArt,
  hipervínculos y marcadores, encabezados y pies, referencias (TOC, notas,
  citas, bibliografía), comentarios y control de cambios, corrector y
  diccionario, símbolos/gráficos/SmartArt/ecuaciones, dibujo a mano alzada,
  vistas y zoom, impresión y exportación (PDF/HTML/ODT/RTF/TXT/EPUB),
  formularios interactivos, seguridad y cifrado, macros, combinación de
  correspondencia, colaboración, accesibilidad y personalización.
- **IA (DeepSeek)**: escritura inteligente, corrección avanzada, traducción y
  análisis, chat contextual sobre el documento, dominios especializados
  (legal, programación, educación, negocios, investigación), automatización,
  productividad, marketing y funciones premium (estilo del usuario, agentes,
  coherencia, glosario, autocompletado).

Para usar las funciones de IA necesita una clave de API de DeepSeek, que se
configura en el menú **IA → Configurar clave de API**.

## Requisitos

- Python >= 3.10
- PySide6 >= 6.6

## Instalación

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt          # solo ejecución
.venv/bin/pip install -r requirements-dev.txt      # ejecución + desarrollo
```

O bien, instalación en modo editable con las dependencias de desarrollo:

```bash
.venv/bin/pip install -e ".[dev]"
```

## Ejecución

```bash
.venv/bin/rword
```

o:

```bash
.venv/bin/python -m rword
```

## Pruebas

```bash
.venv/bin/pytest
```

Los tests se ejecutan en modo *offscreen* (sin necesidad de pantalla).

## Estructura

```
rword/
├── rword/
│   ├── app.py            # Bootstrap de la aplicación
│   ├── config.py         # Constantes de la aplicación
│   ├── core/             # Lógica de dominio (formato, tablas, IA, etc.)
│   │   └── ai/           # Cliente DeepSeek y capacidades de IA
│   └── ui/               # Widgets, barras, paneles y diálogos
├── plugins/              # Complementos opcionales
├── tests/
└── pyproject.toml
```

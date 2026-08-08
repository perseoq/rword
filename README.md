# rword

Procesador de texto profesional con integración de IA (DeepSeek), construido con
PySide6 (Qt for Python).

## Estado

- **Fase 1 — Implementada**: arquitectura base, ventana principal, gestión de
  documentos (nuevo/abrir/guardar/guardar como/cerrar), edición básica
  (deshacer/rehacer/cortar/copiar/pegar/seleccionar todo), barra de estado con
  recuento de palabras y persistencia de preferencias.

## Requisitos

- Python >= 3.10
- PySide6 >= 6.6

## Instalación

```bash
python3 -m venv .venv
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
│   ├── core/
│   │   └── document.py   # Modelo de documento
│   └── ui/
│       ├── main_window.py
│       ├── editor.py
│       └── ...
├── tests/
└── pyproject.toml
```

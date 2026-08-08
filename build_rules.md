# Instrucciones de ejecución (Obligatorias)

Implementa las fases del proyecto **una por una y en orden**, comenzando por la **Fase 1**. Está **prohibido** comenzar una fase nueva hasta que la fase actual haya sido implementada, verificada, corregida y validada completamente.

## Para cada fase deberás ejecutar el siguiente flujo sin excepciones:

### 1. Implementación

* Implementa todos los requisitos de la fase.
* No dejes funcionalidades parcialmente implementadas.
* Mantén la arquitectura y el estilo de código existente.
* Evita introducir deuda técnica innecesaria.

### 2. Validación técnica obligatoria

Antes de considerar la fase terminada deberás:

* Compilar el proyecto.
* Ejecutar todos los tests existentes.
* Ejecutar los linters.
* Verificar que no existan errores de compilación.
* Verificar que no existan warnings críticos.
* Corregir cualquier error encontrado.

Si alguna validación falla, **está prohibido continuar** hasta corregirla.

### 3. Validación funcional obligatoria

Probar exhaustivamente:

* Todos los endpoints implementados.
* Todos los métodos HTTP correspondientes.
* Casos exitosos.
* Casos de error.
* Validaciones.
* Manejo de excepciones.
* Permisos y autenticación.
* Formularios.
* Vistas.
* Navegación.
* Flujos completos.
* Procesos en segundo plano.
* Integraciones.
* Base de datos.
* Migraciones.
* Seeds si existen.

Corregir cualquier problema encontrado y repetir todas las pruebas.

### 4. Pruebas de regresión

Verificar que las funcionalidades implementadas en fases anteriores continúan funcionando correctamente.

Si detectas una regresión:

* Corrígela.
* Repite todas las pruebas necesarias.
* No avances hasta eliminar completamente la regresión.

### 5. Revisión de calidad

Antes de finalizar la fase verifica que:

* No existan TODO, FIXME o código temporal.
* No exista código muerto.
* No existan archivos innecesarios.
* No existan credenciales.
* No existan secretos.
* No existan errores conocidos.
* No existan funcionalidades incompletas.
* La documentación correspondiente haya sido actualizada si aplica.

### 6. Confirmación de la fase

Una fase solo puede considerarse terminada cuando:

* Todas las pruebas pasan satisfactoriamente.
* No existen errores conocidos.
* No existen regresiones.
* Todas las funcionalidades cumplen los requisitos.
* El proyecto permanece estable.

Hasta entonces **está prohibido iniciar la siguiente fase**.

### 7. Control de versiones

Una vez validada completamente la fase:

* Crear un commit atómico.
* Utilizar un mensaje descriptivo siguiendo Conventional Commits.
* Hacer push al repositorio remoto.

Verificar que el push fue exitoso antes de continuar.

### 8. Continuación

Después del push:

* Iniciar inmediatamente la siguiente fase.
* Repetir exactamente el mismo procedimiento.

## Regla absoluta

No solicites confirmación entre fases.

No omitas pruebas para ahorrar tiempo.

No des una fase por terminada si existe cualquier error, prueba fallida, advertencia crítica, funcionalidad incompleta o comportamiento inesperado.

Continúa automáticamente fase por fase hasta completar el 100 % del proyecto. El trabajo solo finaliza cuando todas las fases hayan sido implementadas, verificadas, corregidas, validadas, documentadas (si aplica), comprometidas mediante commit y publicadas mediante push al repositorio remoto.


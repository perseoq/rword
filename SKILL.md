# Skill: Redactor de Documentos Jurídicos (Multimateria)
**23 fases | ~800 tipos de documentos**
Fuentes: Las indicadas en cada fase.

---

## SECCIÓN BASE — Formato Forense Mexicano Unificado

Esta sección contiene las reglas de formato, exportación y flujo de trabajo que aplican a TODAS las fases. Cada fase solo añade su catálogo específico y reglas sustantivas de la materia.

### 1. Formato de presentación judicial

| Elemento | Formato |
|----------|---------|
| **Encabezado** | Alineación **derecha**. **MAYÚSCULAS**. |
| – Actor / Promovente | `NOMBRE DEL ACTOR` |
| – `VS` | `VS` |
| – Demandado / Contraparte | `NOMBRE DEL DEMANDADO` |
| – Tipo de juicio + expediente | `JUICIO [TIPO], EXP. 123/2026` (puede omitirse "ASUNTO") |
| **Autoridad** | `C. JUEZ [NÚMERO] DE LO [MATERIA]` — alineación **derecha** |
| – Ciudad | Alineación derecha |
| – `P R E S E N T E` | Con espacios entre letras |
| **Cuerpo** | **Justificado**. Cada párrafo inicia con **tabulador** (sangría 1.27 cm). |
| **Secciones principales** | `HECHOS`, `DERECHO`, `PRUEBAS`, etc. — **centradas**, **MAYÚSCULAS** |
| **Petitorio** | Ver "Equivalencias de la sección petitoria" abajo |
| **Cierre** | `PROTESTO LO NECESARIO` + nombre completo + lugar y fecha, alineado **izquierda** |

### 2. Equivalencias de la sección petitoria

Distintas materias usan distinta nomenclatura para la sección de peticiones al juez. Todas son equivalentes funcionales y deben producir peticiones enumeradas con `PRIMERO.`, `SEGUNDO.`, etc.:

| Materia | Denominación usada en los escritos |
|---------|-----------------------------------|
| Mercantil | **PUNTOS PETITORIOS** (encabezado explícito) |
| Laboral | **PIDO** |
| Civil / Familiar / Agrario | **pido se sirva** / **a Usted C. Juez atentamente pido** |
| Desahucio / Ejecutivo | **solicito** / **PIDO SE SIRVA** |
| Convenios extrajudiciales | **CLÁUSULAS** (no hay petitorio al juez) |

### 3. Uso de tablas en documentos

Las demandas ejecutivas (desahucio, mercantil, liquidaciones) suelen incluir **tablas** con:
- Resumen de montos adeudados (rentas, penalizaciones, totales)
- Períodos de adeudo y tasas de interés
- Relación de contratos con fechas, partes y montos

Generar con `python-docx`: `doc.add_table(rows, cols)`. Formato: Times New Roman 12.

### 4. Placeholders y versionado

- Los documentos pueden contener placeholders: `[____]`, `[NOMBRE]`, `[DOMICILIO]`, `[FECHA]`, `[EXPEDIENTE]`
- Versiones iterativas: `_v2`, `_vf` (versión final), `_v3` (borrador 3)
- Flujo de trabajo: `plantilla → borrador → revisión → exportación final`

### 5. Exportación a .docx

- Biblioteca: `python-docx` o `docxtpl`
- Configuración técnica:
  ```python
  from docx.shared import Cm, Pt
  from docx.enum.text import WD_ALIGN_PARAGRAPH
  paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT  # o LEFT, CENTER, JUSTIFY
  paragraph.paragraph_format.first_line_indent = Cm(1.27)
  ```
- Fuente: **Times New Roman 12**
- Interlineado: **1.5**
- Estilos: unificar a **"No Spacing"** (escritos forenses) o **"Normal"** (contratos)
- Exportar como `.docx`

### 6. Flujo conversacional genérico

1. **Identificar:** "¿Qué documento necesita redactar? (Demanda, contestación, recurso, contrato, convenio...)"
2. **Recibir adjuntos:** "Puede adjuntar documentos relacionados (contratos, actas, resoluciones, identificaciones). Los analizaré para extraer datos."
3. **Confirmar datos:** "He identificado: [datos extraídos según la materia]. ¿Confirma?"
4. **Solicitar datos faltantes** según los requisitos del catálogo de la fase correspondiente.
5. **Generar borrador** con el formato forense unificado (base + materia).
6. **Revisar:** "¿Desea modificar hechos, agregar pruebas, cambiar el petitorio o ajustar montos?"
7. **Exportar a .docx** con Times New Roman 12, interlineado 1.5.

### 7. Reglas de estilo generales

- Encabezado y autoridad: **MAYÚSCULAS**, alineación **derecha**.
- Cuerpo: **justificado**, sangría 1.27 cm por párrafo.
- Secciones (HECHOS, DERECHO, PRUEBAS, CAPÍTULO DE PRUEBAS, EXCEPCIONES): **centradas**, **MAYÚSCULAS**, sin sangría.
- Petitorio: `PRIMERO.`, `SEGUNDO.`… con sangría francesa (alineación izquierda).
- Cierre: `PROTESTO LO NECESARIO` + nombre completo + lugar y fecha, alineado **izquierda**.
- Sin viñetas ni listas en el cuerpo; redactar en **párrafos**.
- No incluir corchetes ni instrucciones de diseño en el documento final.
- Permitir **tablas** para resúmenes financieros, relación de contratos, o cálculos de prestaciones.
- Fuente: **Times New Roman 12**, interlineado **1.5**.

### 8. Citación de fundamentos legales (sección DERECHO)

No usar rangos de artículos (ej: `Arts. 685–722`). Listar artículos individualmente separados por coma (ej: `1, 2, 3, 4, 5`). Máximo **5 artículos por código** como regla general. No hay límite en la cantidad de leyes o códigos que se citen (sustantivos, adjetivos, supletorios, federales o locales); pueden incluirse todos los que sean relevantes para el caso. Si se requieren más de 5 artículos de un mismo código por su relevancia, pueden incluirse algunos adicionales, siempre que **no sea una lista extensa ni se vacíen artículos del código**. Ejemplo:

> *"Son aplicables los artículos 1, 14, 16 y 17 de la Constitución Política de los Estados Unidos Mexicanos; 2.1, 2.6, 2.7, 2.31, 2.115 del Código de Procedimientos Civiles del Estado de México; 18, 23, 25 de la Ley Agraria."*

---


### 9. Excepciones de formato por tipo de documento

| Tipo de documento | Formato de encabezado | Estructura del cuerpo |
|------------------|----------------------|----------------------|
| **Escritos forenses** (demandas, contestaciones, recursos) | Encabezado y autoridad: alineación **derecha**, MAYÚSCULAS | Secciones centradas, petitorio con ordinales, cierre: PROTESTO LO NECESARIO |
| **Contratos** (civiles, mercantiles, laborales) | Título del contrato: **centrado**, MAYÚSCULAS. Comparecientes: justificado. | DECLARACIONES + CLÁUSULAS (PRIMERA, SEGUNDA...) sin PROTESTO LO NECESARIO |
| **Instrumentos notariales** (escrituras, poderes, testamentos) | Número de instrumento + notaría: **derecha**. | ANTECEDENTES + DECLARACIONES + CLÁUSULAS. Cierre con fe de notario y firmas |
| **Convenios extrajudiciales** | Título centrado o derecha según la materia | DECLARACIONES + CLÁUSULAS. Sin petitorio al juez |

---


# Skill: Redactor de Documentos — Derecho Procesal Civil y Familiar
**Fase 1 | 169 tipos de documentos**
Fuentes: CNPCF, Código Civil para el DF/CDMX, Código Civil del Estado de México (codvig001), Código de Procedimientos Civiles del Estado de México (codvig003).

---

## 1. Nombre
**"Redactor de documentos de derecho procesal civil y familiar"**
(Formato forense mexicano — alineaciones, mayúsculas, tabuladores, justificación)

## 2. Objetivo
A partir de documentos adjuntos por el usuario (PDF/Word) y de instrucciones conversacionales, generar cualquier escrito, resolución, recurso o documento procesal dentro del Derecho Procesal Civil y Familiar que cumpla exactamente con las normas de presentación judicial:
- Encabezado alineado a la derecha (demandante, vs, demandado, tipo de juicio, folio, asunto)
- Autoridad y ciudad alineadas a la derecha, con viñeta "PRESENTE"
- Cuerpo justificado, con sangría (tabulador) al inicio de cada párrafo
- Puntos petitorios enumerados y sangrados (alineación izquierda)
- Exportación final a Word (.docx) con el formato exacto

## 3. Entradas del usuario
- **Documentos subidos** (opcional): PDF o Word (contratos, escrituras, notificaciones, actas, etc.)
- **Indicación del tipo de documento**: demanda, contestación, incidente, recurso, etc.
- **Datos específicos** (solicitados en conversación si no están en los documentos):
  - Nombres completos (demandante, demandado, terceros)
  - Tipo de juicio y número de folio
  - Asunto
  - Autoridad a quien va dirigido (juzgado, tribunal)
  - Ciudad
  - Hechos relevantes en lenguaje narrativo
  - Pretensiones concretas
  - Capítulo de pruebas
  - Fundamento legal
  - Lugar y fecha

### 4.3 Catálogo de documentos y requisitos

---

#### 1. ESCRITOS DE PARTE (LITIGANTES)

---

##### 1.1 Demanda / Escrito Inicial de Demanda
**Descripción:** Escrito con el que el actor inicia el juicio.
**Fundamento:** CNPCF Arts. 224–244; CPC Edomex Arts. 2.1–2.10.
**Requisitos:**
- Nombre completo y domicilio del demandante
- Nombre completo y domicilio del demandado
- Tipo de juicio y vía procesal
- Número de folio / expediente (si existe)
- Autoridad a quien se dirige
- Hechos numerados y narrados cronológicamente
- Prestaciones reclamadas (petitorio claro)
- Fundamento legal
- Capítulo de pruebas
- Valor de lo demandado (si aplica cuantía)
- Lugar y fecha de presentación
- Firma del promovente o representante legal
- Documentos anexos

##### 1.2 Contestación a la Demanda
**Descripción:** Respuesta formal del demandado.
**Fundamento:** CNPCF Arts. 245–260; CPC Edomex Arts. 2.11–2.20.
**Requisitos:**
- Nombre y domicilio del demandado
- Número de expediente y juzgado
- Referencia expresa a cada hecho (se admite, se niega, se desconoce)
- Excepciones y defensas (procesales y de fondo)
- Reconvención (si se ejerce)
- Fundamento legal de las excepciones
- Capítulo de pruebas
- Firma

##### 1.3 Reconvención
**Descripción:** Demanda del demandado contra el actor dentro del mismo juicio.
**Fundamento:** CNPCF Arts. 261–265.
**Requisitos:** Mismos que la demanda. Debe presentarse junto con la contestación o dentro del plazo legal. Prestaciones reconvencionales separadas de las excepciones. Fundamento legal autónomo.

##### 1.4 Contestación a la Reconvención
**Descripción:** Respuesta del actor-reconvenido.
**Fundamento:** CNPCF Art. 265.
**Requisitos:** Número de expediente. Referencia expresa a cada hecho de la reconvención. Excepciones. Capítulo de pruebas. Firma.

##### 1.5 Escrito de Réplica
**Descripción:** Respuesta del actor a la contestación.
**Requisitos:** Número de expediente. Refutación punto a punto. Argumentos adicionales. Pruebas supervenientes. Firma.

##### 1.6 Escrito de Contrarréplica
**Descripción:** Respuesta del demandado a la réplica.
**Requisitos:** Número de expediente. Refutación. Firma.

##### 1.7 Escrito de Agravios / Expresión de Agravios
**Descripción:** Escrito de apelación expresando errores del fallo recurrido.
**Fundamento:** CNPCF Arts. 495–510.
**Requisitos:** Número de expediente y juzgado de origen. Tribunal de alzada. Identificación de la resolución impugnada. Agravios numerados (norma violada + razonamiento + perjuicio). Fundamento legal. Firma.

##### 1.8 Escrito de Aclaración
**Descripción:** Solicitud para aclarar puntos oscuros de una resolución.
**Fundamento:** CNPCF Arts. 474–476.
**Requisitos:** Número de expediente. Identificación de la resolución. Señalamiento preciso del punto oscuro. Lo que se solicita aclarar. Firma.

##### 1.9 Escrito de Oposición
**Descripción:** Oposición a una actuación procesal o medida.
**Requisitos:** Número de expediente. Actuación impugnada. Fundamentos. Firma.

##### 1.10 Escrito de Ofrecimiento de Pruebas
**Descripción:** Ofrecimiento formal de medios de prueba.
**Fundamento:** CNPCF Arts. 293–360.
**Requisitos:** Número de expediente. Listado de pruebas con tipo. Relación con hechos a probar. Datos de testigos. Puntos de peritaje. Documentos anexos. Firma.

##### 1.11 Escrito de Desahogo de Vista
**Descripción:** Respuesta a una vista o traslado.
**Requisitos:** Número de expediente. Referencia al acuerdo que ordena la vista. Manifestación sobre el contenido. Argumentos. Firma.

##### 1.12 Pliego de Posiciones (Absolución de Posiciones)
**Descripción:** Cuestionario para confesión bajo protesta.
**Fundamento:** CNPCF Arts. 322–333.
**Requisitos:** Número de expediente. Identificación del absolvente. Posiciones afirmativas, claras, concisas. Numeradas. Firma.

##### 1.13 Pliego de Preguntas para Testigos
**Descripción:** Cuestionario para interrogatorio de testigos.
**Fundamento:** CNPCF Arts. 334–350.
**Requisitos:** Número de expediente. Nombre del testigo. Preguntas numeradas y claras. Firma.

##### 1.14 Alegatos de Bien Probado (por escrito)
**Descripción:** Exposición escrita del valor probatorio de las pruebas.
**Fundamento:** CNPCF Arts. 428–430.
**Requisitos:** Número de expediente. Síntesis de hechos probados. Análisis de cada prueba. Conclusiones. Fundamento. Solicitud de sentencia favorable. Firma.

##### 1.15 Alegatos Orales (en audiencia)
**Descripción:** Exposición verbal al cierre del desahogo de pruebas.
**Requisitos:** Síntesis de hechos probados. Valoración de pruebas desahogadas. Conclusiones sobre el fondo. Solicitud concreta.

##### 1.16 Conclusiones
**Descripción:** Resumen escrito de argumentos finales antes de la sentencia.
**Requisitos:** Número de expediente. Síntesis de hechos y derecho. Referencia a pruebas. Solicitud concreta. Firma.

##### 1.17 Escrito de Interposición de Recurso
**Descripción:** Escrito genérico para interponer cualquier recurso.
**Requisitos:** Número de expediente. Tipo de recurso. Resolución impugnada. Agravios. Fundamento legal. Firma.

##### 1.18 Escrito de Queja
**Descripción:** Impugnación contra actuaciones del juez sin otro recurso.
**Fundamento:** CNPCF Arts. 516–525.
**Requisitos:** Número de expediente. Tribunal al que se dirige. Acto reclamado. Agravios. Fundamento. Firma.

##### 1.19 Escrito de Recusación
**Descripción:** Solicitud para apartar a un juez por causa legal.
**Fundamento:** CNPCF Arts. 54–68.
**Requisitos:** Número de expediente. Nombre del juez recusado. Causa legal. Hechos que la configuran. Pruebas. Firma.

##### 1.20 Promoción / Petición / Memorial / Escrito de Solicitud
**Descripción:** Escritos genéricos para solicitar actuaciones.
**Requisitos:** Número de expediente. Lo que se solicita. Fundamento legal (si aplica). Firma.

---

#### 2. RESOLUCIONES JUDICIALES

---

##### 2.1 Sentencia Definitiva
**Descripción:** Resolución que pone fin al juicio resolviendo el fondo.
**Fundamento:** CNPCF Arts. 453–473.
**Elementos:**
- Lugar y fecha
- Tribunal que resuelve y número de expediente
- Nombre de las partes y tipo de juicio
- Resultando (antecedentes procesales)
- Considerando (análisis de hechos, pruebas y derecho)
- Puntos resolutivos (PRIMERO, SEGUNDO…)
- Firma del juez y secretario

##### 2.2 Sentencia Interlocutoria
**Descripción:** Resuelve un incidente sin decidir el fondo.
**Elementos:** Mismos que sentencia definitiva, limitados a la cuestión incidental.

##### 2.3 Resolución / Acuerdo / Decreto
**Descripción:** Determinaciones judiciales de trámite o fondo menor.
**Elementos:** Número de expediente. Fecha. Antecedente que la motiva. Determinación. Fundamento legal. Firma.

##### 2.4 Laudo Arbitral
**Descripción:** Resolución del tribunal arbitral que decide el conflicto.
**Fundamento:** CNPCF Arts. 1169–1186.
**Elementos:** Lugar y fecha. Nombre de las partes. Cuestión sometida a arbitraje. Consideraciones. Puntos resolutivos. Firma de los árbitros.

##### 2.5 Autos (tipos)
**Descripción:** Resoluciones de trámite que impulsan el procedimiento.
**Tipos:** Auto de admisión de demanda, auto de radicación, auto de ejecución, auto de embargo, auto de requerimiento y embargo, auto de discernimiento de tutela, auto de depuración, auto de tramitación inmediata, auto de tramitación conjunta con la definitiva, auto de mandamiento en forma, auto de exequendo, auto de inicio del proceso concursal, auto de inicio al procedimiento ordinario de ejecución.
**Elementos comunes:** Número de expediente. Fecha y lugar. Partes. Antecedente procesal. Determinación concreta. Fundamento legal. Firma del juez y secretario.

---

#### 3. RECURSOS

---

##### 3.1 Recurso de Apelación
**Descripción:** Medio ordinario contra sentencias definitivas e interlocutorias.
**Fundamento:** CNPCF Arts. 495–515.
**Requisitos:** Número de expediente y juzgado de origen. Tribunal de alzada. Resolución impugnada. Efecto (devolutivo o ambos efectos). Agravios numerados. Fundamento. Firma.

##### 3.2 Recurso de Revocación
**Descripción:** Impugna autos de trámite ante el mismo juez.
**Fundamento:** CNPCF Arts. 490–494.
**Requisitos:** Número de expediente. Auto impugnado. Motivos de revocación. Lo que se solicita. Fundamento. Firma.

##### 3.3 Recurso de Queja
**Descripción:** Impugna actos del juez no recurribles por apelación.
**Fundamento:** CNPCF Arts. 516–525.
**Requisitos:** Número de expediente. Acto impugnado. Agravios. Fundamento. Firma.

##### 3.4 Recurso de Revisión
**Descripción:** Revisión de resoluciones en casos específicos.
**Requisitos:** Mismos que apelación, con precepto que admite la revisión.

##### 3.5 Recurso de Reconsideración
**Descripción:** Solicitud al mismo juzgado para reconsidere un acuerdo.
**Requisitos:** Número de expediente. Acuerdo a reconsiderar. Fundamentos. Firma.

##### 3.6 Recurso de Inconformidad
**Descripción:** Impugnación específica en procedimientos especiales.
**Requisitos:** Variables según el procedimiento: acto impugnado, agravios, fundamento, firma.

---

#### 4. JUICIOS NOMINADOS

---

##### 4.1 Juicio Ordinario Civil
**Descripción:** Procedimiento de mayor amplitud probatoria.
**Fundamento:** CNPCF Arts. 213 ss.
**Documentos propios:** Demanda, auto de admisión, emplazamiento, contestación, audiencia preliminar, audiencia de juicio, sentencia.
**Requisitos adicionales:** Indicar vía ordinaria. Valor del negocio si determina competencia.

##### 4.2 Juicio Ejecutivo Civil
**Descripción:** Procedimiento para títulos con aparejada ejecución.
**Fundamento:** CNPCF Arts. 767 ss.
**Requisitos:** Título ejecutivo (escritura, cheque, pagaré, etc.). Nombre y domicilio del deudor. Monto líquido exigible. Solicitud de mandamiento de ejecución, requerimiento y embargo.

##### 4.3 Juicio Hipotecario
**Descripción:** Ejecución de garantía hipotecaria.
**Fundamento:** CNPCF Arts. 826 ss.
**Requisitos:** Escritura de hipoteca inscrita en RPP. Certificado de gravámenes. Monto del crédito. Datos del inmueble. Solicitud de requerimiento, embargo y remate.

##### 4.4 Vía de Apremio
**Descripción:** Procedimiento ejecutivo especial para créditos fiscales o garantizados.
**Requisitos:** Título que trae aparejada ejecución. Determinación líquida del adeudo. Solicitud de mandamiento de ejecución.

##### 4.5 Juicio Testamentario
**Descripción:** Sucesión por testamento.
**Fundamento:** CC DF Arts. 1281–1367.
**Requisitos:** Testamento (original o copia certificada). Acta de defunción del autor de la herencia. Identificación de herederos y legatarios. Inventario de bienes.

##### 4.6 Juicio de Intestado (Ab Intestato)
**Descripción:** Sucesión legítima sin testamento.
**Fundamento:** CC DF Arts. 1368–1455.
**Requisitos:** Acta de defunción. Parentesco con el difunto. Declaración de no existencia de testamento. Inventario de bienes. Solicitud de declaratoria de herederos.

##### 4.7 Juicio Sucesorio (Testamentario e Intestamentario)
**Descripción:** Procedimiento unificado para sucesiones.
**Requisitos:** Actas de defunción y de estado civil. Testamento o declaratoria. Inventario y avalúo. Solicitud de nombramiento de albacea. Plan de partición.

##### 4.8 Juicio Sumario de Usucapión
**Descripción:** Adquisición de propiedad por prescripción.
**Fundamento:** CC DF Arts. 1152–1164; CNPCF Arts. 637 ss.
**Requisitos:** Descripción del inmueble. Tiempo de posesión (5 años con justo título; 10 años sin). Prueba de posesión pública, pacífica, continua. Certificado de libertad de gravámenes. Testigos. Plano.

##### 4.9 Juicio Oral Civil
**Descripción:** Procedimiento oral para asuntos de menor cuantía.
**Fundamento:** CNPCF Arts. 1080 ss.
**Requisitos:** Demanda verbal o escrita. Identificación de la vía oral. Pretensiones claras y concretas. Pruebas ofrecidas desde el inicio.

##### 4.10 Juicio Patrimonial
**Descripción:** Controversia sobre derechos patrimoniales.
**Requisitos:** Según la materia: títulos de propiedad, contratos, comprobantes de pago, etc.

##### 4.11 Juicio Contencioso Administrativo
**Descripción:** Impugnación de actos administrativos.
**Requisitos:** Acto administrativo impugnado. Agravios. Fundamento legal. Pruebas documentales.

##### 4.12 Procedimiento Contencioso Familiar
**Descripción:** Controversias del orden familiar.
**Fundamento:** CNPCF Arts. 578 ss.
**Requisitos:** Relación familiar acreditada. Hechos controvertidos. Pretensiones. Medidas provisionales.

##### 4.13 Juicio de Nulidad de Acto Jurídico
**Descripción:** Declaración de ineficacia de un acto jurídico.
**Fundamento:** CC DF Arts. 1795–1803; CC Edomex Arts. 7.22–7.25.
**Requisitos:** Identificación del acto impugnado. Causa de nulidad. Pruebas. Efectos solicitados.

##### 4.14 Juicio de Nulidad de Matrimonio
**Descripción:** Disolución por causa legal preexistente.
**Fundamento:** CC DF Arts. 235–250.
**Requisitos:** Acta de matrimonio. Causa de nulidad. Hechos. Petitorio: declaración, efectos sobre hijos, bienes y alimentos.

##### 4.15 Juicio de Nulidad de Asamblea (Agrario/Societario)
**Descripción:** Impugnación de acuerdos de asamblea.
**Requisitos:** Acta de asamblea impugnada. Causa de nulidad (convocatoria irregular, falta de quórum, etc.). Calidad de socio o ejidatario.

##### 4.16 Juicio de Nulidad de Resolución Administrativa
**Descripción:** Impugnación de actos administrativos definitivos.
**Requisitos:** Resolución impugnada. Agravios. Fundamento legal. Pruebas.

##### 4.17 Juicio de Divorcio Contencioso
**Descripción:** Disolución del vínculo matrimonial sin acuerdo.
**Fundamento:** CC DF Arts. 266–291; CC Edomex Arts. 4.88–4.106.
**Requisitos:** Acta de matrimonio. Actas de nacimiento de hijos. Régimen patrimonial. Hechos que motivan el divorcio. Propuesta sobre guarda, visitas, alimentos, liquidación.

##### 4.18 Juicio de Alimentos
**Descripción:** Exigir cumplimiento de obligación alimentaria.
**Fundamento:** CC DF Arts. 301–323.
**Requisitos:** Nombre y parentesco. Acta que acredite parentesco. Necesidades del acreedor. Capacidad del deudor. Monto solicitado. Medidas cautelares.

##### 4.19 Juicio de Guarda y Custodia
**Descripción:** Determinación de guarda y custodia de hijos.
**Fundamento:** CC DF Arts. 416–416 Ter.
**Requisitos:** Actas de nacimiento. Hechos justificantes. Propuesta de visitas. Propuesta de alimentos. Opinión del menor (si procede).

##### 4.20 Juicio de Patria Potestad
**Descripción:** Modificación, suspensión o extinción de patria potestad.
**Fundamento:** CC DF Arts. 444–448.
**Requisitos:** Actas de nacimiento. Causa legal. Hechos. Pruebas documentales, testimoniales, periciales.

##### 4.21 Juicio de Adopción
**Descripción:** Constitución del vínculo adoptivo.
**Fundamento:** CC DF Arts. 390–410.
**Requisitos:** Solicitud de adoptantes. Acta de nacimiento del adoptado. Consentimientos. Estudio socioeconómico. Informe del DIF.

##### 4.22 Juicio de Interdicción
**Descripción:** Declaración de incapacidad y nombramiento de tutor.
**Fundamento:** CC DF Arts. 450–466.
**Requisitos:** Nombre y domicilio del presunto incapaz. Causa de incapacidad. Dictamen médico. Propuesta de tutor y curador. Inventario de bienes.

##### 4.23 Juicio de Ausencia
**Descripción:** Declaración de ausencia y presunción de muerte.
**Fundamento:** CC DF Arts. 648–724.
**Requisitos:** Último domicilio y noticias del ausente. Parentesco del promovente. Bienes dejados. Tiempo transcurrido. Solicitud de representante provisional.

##### 4.24 Juicio de Desahucio / Terminación de Arrendamiento
**Descripción:** Recuperación de posesión de inmueble arrendado.
**Fundamento:** CC DF Arts. 2478–2497.
**Requisitos:** Contrato de arrendamiento. Identificación del inmueble. Causa de terminación. Rentas adeudadas. Solicitud de entrega y pago.

##### 4.25 Juicio de Oposición
**Descripción:** Oposición a actos judiciales o administrativos.
**Requisitos:** Acto al que se opone. Interés jurídico. Hechos y fundamentos. Pruebas.

##### 4.26 Juicio de Inmatriculación
**Descripción:** Primera inscripción de inmueble en el RPP.
**Requisitos:** Descripción del inmueble. Título de propiedad o posesión. Certificado de no inscripción. Testigos. Plano.

##### 4.27 Juicio de Petición de Herencia
**Descripción:** Acción del heredero para obtener bienes hereditarios.
**Fundamento:** CC DF Arts. 1281–1290.
**Requisitos:** Documento que acredite la calidad de heredero. Bienes. Identificación del poseedor. Fundamento de posesión del demandado.

##### 4.28 Juicio de Rendición de Cuentas
**Descripción:** Exigencia de cuentas a administrador, tutor, albacea.
**Fundamento:** CNPCF Arts. 1011–1014.
**Requisitos:** Relación jurídica. Período. Hechos de incumplimiento. Solicitud concreta.

##### 4.29 Juicio de Responsabilidad Civil
**Descripción:** Reparación del daño por hecho ilícito.
**Fundamento:** CC DF Arts. 1910–1934.
**Requisitos:** Hecho dañoso. Identificación del responsable. Daños y perjuicios (monto). Pruebas. Fundamento.

##### 4.30 Controversia de Orden Familiar
**Descripción:** Conflictos entre miembros de una familia.
**Fundamento:** CNPCF Arts. 578 ss.
**Requisitos:** Relación familiar. Hechos controvertidos. Pretensiones. Medidas provisionales.

---

#### 5. TERCERÍAS

---

##### 5.1 Demanda de Tercería Coadyuvante
**Descripción:** El tercero apoya a una parte.
**Fundamento:** CNPCF Arts. 488–491.
**Requisitos:** Número de expediente. Interés jurídico y vinculación. Hechos y fundamentos de la parte coadyuvada. Pruebas propias.

##### 5.2 Demanda de Tercería Excluyente de Dominio
**Descripción:** El tercero reclama propiedad sobre bienes embargados.
**Fundamento:** CNPCF Arts. 492, 494–497.
**Requisitos:** Número de expediente. Título de fecha cierta de propiedad. Descripción de bienes. Título anterior al embargo. Inscripción en RPP (si inmueble).

##### 5.3 Demanda de Tercería Excluyente de Preferencia
**Descripción:** Mejor derecho a ser pagado.
**Fundamento:** CNPCF Arts. 493–495, 497.
**Requisitos:** Título que acredite crédito preferente. Demostración de preferencia legal. Monto del crédito.

##### 5.4 Demanda de Tercería Excluyente de Crédito Hipotecario
**Descripción:** Variante con hipoteca inscrita.
**Fundamento:** CNPCF Art. 496.
**Requisitos:** Escritura de hipoteca inscrita. Certificado de inscripción. Monto del crédito. Solicitud de inscripción en RPP.

##### 5.5 Contestación a la Demanda de Tercería
**Descripción:** Oposición del ejecutante o ejecutado.
**Requisitos:** Número de expediente. Excepciones. Pruebas. Fundamento.

##### 5.6 Sentencia de Tercería
**Descripción:** Resolución que declara fundada o infundada la tercería.
**Elementos:** Mismos que sentencia interlocutoria. Determinación sobre el derecho del tercero. Condena en costas si procede.

---

#### 6. ACCIONES NOMINADAS

---

##### 6.1 Acción Reivindicatoria
**Descripción:** Propietario no poseedor contra poseedor no propietario.
**Fundamento:** CC DF Arts. 830 ss.
**Requisitos:** Título de propiedad. Identificación del bien. Identificación del poseedor. Prueba de posesión sin título. Solicitud de restitución, frutos y daños.

##### 6.2 Acción Plenaria de Posesión (Publiciana)
**Descripción:** Recuperación de posesión por mejor derecho.
**Fundamento:** CC DF Arts. 806–827.
**Requisitos:** Prueba del derecho a poseer. Identificación del bien. Poseedor actual. Cómo se perdió la posesión.

##### 6.3 Acción Negatoria de Servidumbre
**Descripción:** El propietario niega la existencia de una servidumbre sobre su predio.
**Fundamento:** CC DF Arts. 1054–1058.
**Requisitos:** Título de propiedad del predio sirviente. Hechos que configuran el gravamen. Prueba de inexistencia de la servidumbre. Solicitud de declaración de libertad del predio.

##### 6.4 Acción Confesoria de Servidumbre
**Descripción:** El titular de una servidumbre reclama su reconocimiento.
**Fundamento:** CC DF Arts. 1054–1058.
**Requisitos:** Título constitutivo de la servidumbre. Identificación de los predios dominante y sirviente. Hechos de perturbación. Solicitud de restitución y daños.

##### 6.5 Acción de Nulidad (Absoluta, Relativa, Parcial)
**Descripción:** Declaración de nulidad de un acto jurídico.
**Tipos:** Absoluta (ley, orden público, buenas costumbres); Relativa/Anulabilidad (incapacidad, error, dolo, violencia, lesión); Parcial.
**Requisitos:** Identificación del acto impugnado. Causa específica de nulidad. Pruebas. Efectos solicitados.

##### 6.6 Acción Rescisoria
**Descripción:** Dejar sin efectos un contrato por incumplimiento.
**Fundamento:** CC DF Arts. 1949.
**Requisitos:** Contrato base. Obligación incumplida. Daños y perjuicios. Solicitud de rescisión y restitución.

##### 6.7 Acción Pauliana / Revocatoria
**Descripción:** Revocar actos fraudulentos del deudor.
**Fundamento:** CC DF Arts. 2163–2180.
**Requisitos:** Crédito del actor. Acto fraudulento. Prueba del fraude. Tercero interviniente.

##### 6.8 Acción de Simulación
**Descripción:** Declaración de simulación de un acto jurídico.
**Fundamento:** CC DF Arts. 2180–2184.
**Requisitos:** Acto simulado. Tipo (absoluta o relativa). Hechos y pruebas. Efectos solicitados.

##### 6.9 Acción de Nulidad de Juicio Concluido
**Descripción:** Nulidad de juicio por dolo, colusión o cosa juzgada fraudulenta.
**Fundamento:** CC DF Arts. 2185–2192.
**Requisitos:** Juicio cuya nulidad se demanda. Causa de nulidad. Pruebas del dolo, colusión o fraude.

##### 6.10 Acción de Petición de Herencia
**Descripción:** Heredero reclama bienes hereditarios.
**Fundamento:** CC DF Arts. 1281–1290.
**Requisitos:** Calidad de heredero. Bienes reclamados. Poseedor demandado.

##### 6.11 Acción de Revocación
**Descripción:** Revocación de actos jurídicos por causas legales.
**Requisitos:** Acto a revocar. Causa legal. Hechos y pruebas.

##### 6.12 Acción de Responsabilidad Civil
**Descripción:** Reparación del daño extracontractual.
**Fundamento:** CC DF Arts. 1910–1934.
**Requisitos:** Hecho ilícito. Daño. Relación causal. Monto indemnizatorio. Pruebas.

##### 6.13 Acción de Posesión
**Descripción:** Protección de la posesión.
**Requisitos:** Identificación del bien. Prueba de posesión. Acto de desposesión o turbación.

##### 6.14 Acción de Ausencia / Posesión Definitiva
**Descripción:** Declaración de ausencia y posesión provisional o definitiva de bienes.
**Requisitos:** Últimas noticias del ausente. Tiempo transcurrido. Parentesco. Inventario de bienes.

##### 6.15 Acción de Revalidación de Venta de Cosa Ajena
**Descripción:** El verdadero propietario ratifica una venta hecha por quien no era dueño.
**Requisitos:** Título de propiedad. Contrato de compraventa a revalidar. Manifestación expresa de ratificación.

##### 6.16 Acción Derivada de Teoría de la Imprevisión
**Descripción:** Revisión de contrato por acontecimientos extraordinarios e imprevisibles.
**Fundamento:** CC DF Arts. 1796, 1797; teoría general.
**Requisitos:** Contrato vigente. Acontecimiento extraordinario. Desequilibrio de prestaciones. Solicitud de revisión o rescisión.

##### 6.17 Acción Colectiva (Demanda Colectiva)
**Descripción:** Acción ejercida por un grupo de personas con un interés común.
**Fundamento:** CNPCF Arts. 595 ss.
**Requisitos:** Identificación del grupo o colectividad. Interés común. Hechos y fundamentos comunes. Representante del grupo. Pruebas.

##### 6.18 Acción de Responsabilidad por Servicios Profesionales
**Descripción:** Contra profesionista por negligencia, impericia o dolo.
**Fundamento:** CC DF Art. 2615.
**Requisitos:** Contrato o relación de servicios. Daño causado. Vínculo causal. Prueba del daño. Monto indemnizatorio.

---

#### 7. INCIDENTES Y PROCEDIMIENTOS ESPECIALES

---

##### 7.1 Incidente de Previo y Especial Pronunciamiento
**Descripción:** Cuestión a resolver antes de continuar el principal.
**Fundamento:** CNPCF Arts. 279–292.
**Tipos:** Falta de personalidad, incompetencia, litispendencia, cosa juzgada.
**Requisitos:** Número de expediente. Tipo de incidente. Hechos y fundamentos. Pruebas. Firma.

##### 7.2 Incidente de Liquidación
**Descripción:** Cuantificación de condena no determinada en sentencia.
**Requisitos:** Número de expediente y sentencia ejecutoriada. Liquidación detallada. Documentos de soporte. Firma.

##### 7.3 Incidente de Liquidación de Sentencia
**Descripción:** Cuantificación del monto de condena líquida.
**Fundamento:** CNPCF Arts. 1000–1010.
**Requisitos:** Mismos que incidente de liquidación. Cálculos de capital, intereses, daños. Tablas y soportes.

##### 7.4 Diligencias de Jurisdicción Voluntaria
**Descripción:** Actuaciones judiciales sin controversia que requieren intervención judicial.
**Fundamento:** CNPCF Arts. 77–117; CPC Edomex Libro Sexto.
**Tipos:** Autorización para vender bienes de menores, información testimonial, consignación, apeo y deslinde, etc.
**Requisitos:** Exposición del objeto. Documentos de soporte. Solicitud concreta. Justificación de la necesidad de intervención judicial.

##### 7.5 Diligencias de Mera Ejecución
**Descripción:** Actuaciones para hacer cumplir resoluciones firmes.
**Requisitos:** Resolución ejecutoriada. Solicitud de ejecución. Identificación de bienes o personas objeto.

##### 7.6 Rendición de Cuentas (Solicitud / Incidente)
**Descripción:** Exigencia de cuentas a un obligado.
**Requisitos:** Relación jurídica. Período. Hechos de incumplimiento.

##### 7.7 Plan de Partición (Proyecto Partitorio)
**Descripción:** Proyecto de división de herencia o bienes comunes.
**Requisitos:** Inventario de bienes. Avalúo. Propuesta de adjudicación por heredero o partícipe. Colacion de bienes si aplica.

##### 7.8 Denuncia de Juicio Sucesorio
**Descripción:** Noticia al juez del fallecimiento de una persona para iniciar la sucesión.
**Requisitos:** Acta de defunción. Parentesco o interés del denunciante. Bienes conocidos. Testamento (si existe).

##### 7.9 Declaración de Ausencia por Desaparición
**Descripción:** Declaración judicial de ausencia.
**Requisitos:** Nombre del ausente. Últimas noticias. Tiempo. Parentesco del promovente. Bienes.

##### 7.10 Nombramiento de Tutor / Curador
**Descripción:** Designación judicial de tutor o curador.
**Requisitos:** Causa de la tutela. Identificación del incapaz. Propuesta de tutor. Inventario de bienes. Dictamen médico.

##### 7.11 Consignación (Pago por Consignación)
**Descripción:** Liberación del deudor que no puede pagar directamente.
**Fundamento:** CNPCF Arts. 700–709.
**Requisitos:** Nombre del acreedor. Obligación que se cumple. Causa de la imposibilidad. Depósito. Solicitud de liberación.

##### 7.12 Impugnación de Falsedad de Documento
**Descripción:** Declaración de falsedad de un documento exhibido en juicio.
**Fundamento:** CNPCF Art. 321.
**Requisitos:** Número de expediente. Documento impugnado. Tipo de falsedad (material o ideológica). Hechos y pruebas (peritaje grafoscópico).

##### 7.13 Cotejo de Documentos
**Descripción:** Verificación de autenticidad por comparación con documento indubitado.
**Fundamento:** CNPCF Arts. 325–332.
**Requisitos:** Documento cuestionado. Documento indubitado. Solicitud de perito grafoscópico.

---

#### 8. NOTIFICACIONES Y COMUNICACIONES JUDICIALES

---

##### 8.1 Notificación
**Descripción:** Acto de hacer saber una resolución judicial.
**Tipos:** Personal, por lista, por cédula, por correo electrónico, por estrados, por edictos.
**Elementos:** Número de expediente. Resolución que se notifica. Nombre del notificado. Forma de notificación. Acuse o constancia.

##### 8.2 Emplazamiento
**Descripción:** Notificación al demandado del inicio del juicio y plazo para contestar.
**Elementos:** Copia de demanda y anexos. Auto de admisión. Apercibimiento. Plazo para contestar.

##### 8.3 Citatorio
**Descripción:** Documento que cita a una persona para que comparezca en día y hora determinados.
**Elementos:** Autoridad que cita. Nombre del citado. Día, hora y lugar. Objeto de la citación. Apercibimiento.

##### 8.4 Exhorto
**Descripción:** Comunicación entre jueces de distinta jurisdicción.
**Elementos:** Juez exhortante y exhortado. Número de expediente. Diligencia solicitada. Documentos anexos. Firma y sello.

##### 8.5 Requisitoria
**Descripción:** Comunicación a autoridad no judicial para práctica de diligencia.
**Elementos:** Autoridad requirente y requerida. Diligencia. Plazo. Fundamento.

##### 8.6 Mandamiento
**Descripción:** Orden judicial dirigida a autoridad administrativa o fedatario.
**Elementos:** Autoridad emisora. Destinatario. Determinación. Fundamento.

##### 8.7 Acta de Notificación
**Descripción:** Documento que da fe de la realización de una notificación.
**Elementos:** Fecha, hora y lugar. Notificador. Notificado. Resolución notificada. Forma de notificación. Constancia de entrega o negativa.

##### 8.8 Acta Circunstanciada
**Descripción:** Registro detallado de una diligencia practicada por el actuario.
**Elementos:** Fecha, hora y lugar. Funcionario actuante. Personas que intervinieron. Descripción de lo ocurrido. Firmas.

##### 8.9 Carta Rogatoria Internacional
**Descripción:** Exhorto a autoridad judicial extranjera.
**Fundamento:** CNPCF Arts. 1162–1168.
**Requisitos:** Mismos que exhorto. Traducción al idioma del país destinatario. Legalización o apostilla.

---

#### 9. MEDIDAS CAUTELARES Y DE APREMIO

---

##### 9.1 Medida Cautelar / Medidas Provisionales / Medidas Precautorias
**Descripción:** Medidas para asegurar el resultado del juicio.
**Fundamento:** CNPCF Arts. 382–395.
**Tipos:** Radicación de persona, retención de bienes, embargo precautorio, secuestro.
**Requisitos:** Fumus boni iuris. Periculum in mora. Garantía/fianza (salvo exención). Descripción de bienes o persona.

##### 9.2 Medida de Apremio
**Descripción:** Medidas coercitivas para hacer cumplir determinaciones judiciales.
**Requisitos:** Resolución que se ejecuta. Tipo de apremio (multa, arresto, uso de la fuerza pública). Fundamento.

##### 9.3 Medidas de Protección (Materia Familiar)
**Descripción:** Medidas urgentes contra violencia familiar.
**Fundamento:** CNPCF Arts. 2.355 Ter–Quinquies (CPC Edomex); LGAMVLV.
**Tipos:** Emergentes, preventivas, de naturaleza civil.
**Requisitos:** Exposición de hechos de violencia. Medida específica. Prueba sumaria del riesgo.

##### 9.4 Providencia Precautoria
**Descripción:** Radicación de persona o retención de bienes antes o durante el juicio.
**Requisitos:** Prueba del derecho. Peligro en la demora. Garantía. Descripción del objeto.

##### 9.5 Embargo / Secuestro de Bienes / Diligencia de Embargo
**Descripción:** Afectación de bienes del deudor.
**Requisitos:** Mandamiento o auto. Identificación de bienes. Acta de diligencia. Designación de depositario.

---

#### 10. PRUEBAS

---

##### 10.1 Prueba Documental
**Descripción:** Documentos públicos o privados aportados como prueba.
**Requisitos:** Identificación del documento. Tipo (público o privado). Relación con los hechos. Objeción de falsedad si aplica.

##### 10.2 Prueba Instrumental
**Descripción:** Instrumentos públicos y privados con relevancia probatoria.
**Requisitos:** Exhibición del instrumento. Solicitud de tenerlo por recibido. Relación con los hechos.

##### 10.3 Dictamen Pericial / Peritaje / Informe Pericial
**Descripción:** Opinión técnica de un experto.
**Fundamento:** CNPCF Arts. 351–370.
**Requisitos:** Nombre y cédula del perito. Puntos de dictamen. Metodología. Conclusiones. Firma.

##### 10.4 Prueba Testimonial (Declaración de Testigo)
**Descripción:** Deposición de quien conoce los hechos.
**Fundamento:** CNPCF Arts. 334–350.
**Requisitos:** Nombre, domicilio y ocupación. Relación con las partes. Hechos sobre los que declarará. Pliego de preguntas.

##### 10.5 Confesión / Declaración de Parte / Posiciones
**Descripción:** Declaración bajo protesta de decir verdad.
**Fundamento:** CNPCF Arts. 322–333.
**Requisitos:** Pliego de posiciones. Apertura bajo protesta. Respuesta afirmativa o negativa.

##### 10.6 Declaración
**Descripción:** Manifestación de parte o tercero sobre hechos del juicio.
**Requisitos:** Identificación del declarante. Calidad procesal. Contenido de la declaración.

##### 10.7 Inspección Judicial
**Descripción:** Examen directo por el juez de personas, lugares o cosas.
**Fundamento:** CNPCF Arts. 371–381.
**Requisitos:** Descripción del objeto. Lugar. Puntos a verificar. Solicitud de peritos si aplica.

##### 10.8 Reconocimiento de Documentos
**Descripción:** Acto de examinar y cotejar documentos ante el juez.
**Requisitos:** Documentos a reconocer. Partes que intervienen. Manifestación sobre autenticidad.

---

#### 11. DILIGENCIAS DE EJECUCIÓN

---

##### 11.1 Diligencia de Requerimiento de Pago y Embargo
**Descripción:** Actuación del actuario para requerir pago y trabar embargo.
**Elementos:** Mandamiento o auto de ejecución. Requerimiento de pago (capital + intereses + costas). Señalamiento de bienes. Acta circunstanciada. Depositario.

##### 11.2 Diligencia de Embargo
**Descripción:** Traba de embargo sobre bienes específicos.
**Elementos:** Mandamiento. Identificación de bienes. Acta. Depositario.

##### 11.3 Diligencia de Deslinde (Apeo y Deslinde)
**Descripción:** Fijación de linderos entre predios colindantes.
**Elementos:** Solicitud del interesado. Títulos de propiedad. Plano. Citación a colindantes. Acta de la diligencia.

##### 11.4 Diligencia de Ejecución / Diligencias de Ocupación
**Descripción:** Actuaciones para hacer efectiva una resolución (lanzamiento, ocupación, etc.).
**Elementos:** Resolución ejecutoriada. Mandamiento. Acta de la diligencia. Fuerza pública si es necesaria.

##### 11.5 Remate (Subasta Pública)
**Descripción:** Venta judicial de bienes embargados al mejor postor.
**Fundamento:** CNPCF Arts. 1082–1090.
**Requisitos:** Auto que ordena el remate. Avalúo. Convocatoria. Posturas (mínimo 2/3 del avalúo). Acta de remate. Auto de finca.

##### 11.6 Postura (en Subasta Pública / Remate)
**Descripción:** Oferta de compra en remate judicial.
**Requisitos:** Identificación del postor. Depósito. Bien por el que se postula. Monto de la postura.

##### 11.7 Orden de Remate o Transferencia
**Descripción:** Resolución que adjudica el bien al mejor postor.
**Requisitos:** Acta de remate. Verificación de postura legal. Auto de finca. Orden de escrituración.

##### 11.8 Escritura de Adjudicación (en Ejecución de Sentencia)
**Descripción:** Instrumento notarial que formaliza la adjudicación.
**Fundamento:** CNPCF Arts. 1092, 1101.
**Requisitos:** Auto de finca ejecutoriado. Identificación del adjudicatario. Descripción del bien. Precio y constancia de pago. Firma del juez (si el deudor se niega).

##### 11.9 Inventario
**Descripción:** Relación detallada de bienes (en embargo, administración o sucesión).
**Elementos:** Identificación de cada bien. Descripción. Valor estimado. Estado de conservación.

---

### Lectura de documentos
- Extraer texto de PDF o Word
- Identificar: nombres de partes, fechas, montos, tipo de juicio y expediente
- Identificar autoridad judicial y materia
- Usar los datos extraídos para prellenar la plantilla

## 5. Reglas adicionales

- Demanda: debe contener las prestaciones claras y determinadas; si son genéricas, el juez prevendrá.
- Contestación: debe referirse expresamente a cada hecho (se admite, se niega, se desconoce).
- Acción reivindicatoria: requiere título de propiedad inscrito en el RPP.
- Acción plenaria de posesión: requiere justo título y posesión material.
- Desahucio: procede por falta de pago de 2 o más mensualidades (CPC Edomex Art. 2.309).
- Divorcio incausado: no requiere expresar causa; basta la solicitud unilateral.
- Excepciones procesales: deben oponerse como previo y especial pronunciamiento.
- Prueba pericial: ofrecerse con cuestionario y datos del perito; de lo contrario se tiene por no ofrecida.
- Sentencia: debe ser congruente con la litis planteada (principio de congruencia).
- Costas: se imponen a la parte que litigue con temeridad o mala fe.
- Juicio ejecutivo mercantil: el título debe tener aparejada ejecución (pagaré, cheque, escritura).
- Reconvención: debe presentarse junto con la contestación; si no, precluye el derecho.

# Skill: Redactor de Documentos — Derecho del Trabajo
**Fase 2 | 121 tipos de documentos**
Fuentes: Ley Federal del Trabajo (LFT), Ley Federal de los Trabajadores al Servicio del Estado (LFTSE), Ley del Seguro Social (LSS), CODEX/LFT.txt.

---

## 1. Nombre
**"Redactor de documentos laborales"**
(Formato forense mexicano — alineaciones, mayúsculas, tabuladores, justificación)

## 2. Objetivo
A partir de documentos adjuntos por el usuario (PDF/Word) y de instrucciones conversacionales, generar cualquier escrito, demanda, contrato, convenio o documento procesal laboral que cumpla exactamente con las normas de presentación judicial:
- Encabezado alineado a la derecha (actor, vs, demandado, tipo de procedimiento, expediente, asunto)
- Autoridad y ciudad alineadas a la derecha, con viñeta "PRESENTE"
- Cuerpo justificado, con sangría (tabulador) al inicio de cada párrafo
- Puntos petitorios enumerados y sangrados (alineación izquierda)
- Exportación final a Word (.docx) con el formato exacto

## 3. Entradas del usuario
- **Documentos subidos** (opcional): PDF o Word (contratos, recibos, cartas de despido, liquidaciones, etc.)
- **Indicación del tipo de documento**: demanda, contestación, contrato, convenio, pliego de peticiones, etc.
- **Datos específicos** (solicitados en conversación si no están en los documentos):
  - Nombres completos (trabajador, patrón, sindicato)
  - Tipo de procedimiento y número de expediente
  - Asunto (despido injustificado, reinstalación, cobro de prestaciones, etc.)
  - Autoridad a quien va dirigido (Tribunal Laboral, Centro de Conciliación, CFCRL)
  - Ciudad
  - Hechos relevantes en lenguaje narrativo (fechas, puestos, salarios)
  - Pretensiones concretas con montos estimados
  - Capítulo de pruebas
  - Fundamento legal
  - Lugar y fecha

### 4.3 Catálogo de documentos y requisitos

---

#### 1. PROCEDIMIENTOS LABORALES NOMINADOS

---

##### 1.1 Procedimiento Ordinario Laboral
**Descripción:** Juicio principal para controversias entre trabajadores y patrones sobre derechos laborales individuales o colectivos.
**Fundamento:** LFT Arts. 685–722.
**Requisitos:**
- Nombre y domicilio del trabajador (actor) o sindicato
- Nombre y domicilio del patrón (demandado)
- Centro de trabajo (nombre, dirección, municipio, entidad)
- Tipo de relación laboral (empleado, confianza, sindicalizado)
- Hechos en orden cronológico con fechas precisas
- Prestaciones reclamadas con montos estimados
- Fundamento legal de cada prestación
- Ofrecimiento de pruebas (documentales, testimoniales, periciales, inspección)
- Anexos (contratos, recibos, liquidaciones, constancias)

##### 1.2 Juicio Individual Ordinario Laboral
**Descripción:** Procedimiento ordinario promovido por un trabajador individual.
**Fundamento:** LFT Arts. 685–722.
**Requisitos:** Mismos que 1.1, más:
- Antigüedad del trabajador (fecha de ingreso y separación)
- Salario diario integrado (SDI): cuota diaria + proporcional de aguinaldo, vacaciones, prima vacacional
- Tipo de separación: despido injustificado, renuncia, rescisión imputable al patrón

##### 1.3 Procedimiento Especial Laboral
**Descripción:** Vía rápida para conflictos ≤ 3 meses de salario, designación de beneficiarios y prestaciones de seguridad social.
**Fundamento:** LFT Arts. 723–733.
**Requisitos:**
- Tipo de conflicto (cuantía menor / beneficiarios / seguridad social)
- Para beneficiarios: nombre del trabajador fallecido, NSS, vínculos familiares, documentos de identidad y parentesco
- Para cuantía menor: monto de la prestación y fundamento

##### 1.4 Procedimiento Especial Colectivo
**Descripción:** Disputas sobre titularidad de CCT, recuento de trabajadores, elecciones sindicales ante el CFCRL.
**Fundamento:** LFT Arts. 388-bis, 390-bis, 931–933.
**Requisitos:**
- Nombre del sindicato solicitante y número de registro
- Sindicato contrario (titular actual si aplica)
- Empresa y centro de trabajo objeto del conflicto
- Número de trabajadores en padrón
- Contrato colectivo en disputa (si lo hay)
- Fundamento y causa de la solicitud

##### 1.5 Procedimiento de Conflictos Colectivos de Naturaleza Económica
**Descripción:** Modificación de condiciones de trabajo por causas económicas.
**Fundamento:** LFT Arts. 900–919.
**Requisitos:**
- Sindicato o trabajadores promoventes
- Causas económicas detalladas
- Condiciones actuales y solicitadas
- Documentos financieros de la empresa

##### 1.6 Procedimiento de Huelga
**Descripción:** Tramitación del derecho de huelga: pliego de peticiones hasta declaración de existencia e ilicitud.
**Fundamento:** LFT Arts. 440–469, 920–938.
**Requisitos:**
- Nombre del sindicato emplazante y número de registro
- Nombre y domicilio del patrón
- Objeto de la huelga (celebrar/revisar CCT, solidaridad, pago de salarios)
- Peticiones concretas
- Fecha propuesta de estallamiento
- Número de trabajadores que estallan la huelga

##### 1.7 Procedimiento de Ejecución de Sentencias y Convenios Laborales
**Descripción:** Etapa para hacer cumplir la sentencia o convenio ratificado.
**Fundamento:** LFT Arts. 939–956.
**Requisitos:**
- Número de expediente y tribunal
- Partes y datos de la sentencia o convenio
- Monto de la condena
- Bienes o cuentas del patrón (si se solicitará embargo)

##### 1.8 Procedimiento de Conciliación Prejudicial
**Descripción:** Etapa obligatoria previa al juicio ante el Centro de Conciliación.
**Fundamento:** LFT Arts. 684-A–684-J.
**Requisitos:**
- Datos del trabajador y del patrón
- Descripción del conflicto y prestaciones reclamadas
- Documentos que acreditan la relación laboral
- Pretensión conciliatoria

##### 1.9 Procedimiento de Registro Sindical
**Descripción:** Solicitud ante el CFCRL para obtener registro de sindicato.
**Fundamento:** LFT Arts. 364–366, 364-bis–365-bis.
**Requisitos:**
- Nombre del sindicato y tipo (gremial, empresa, industrial, nacional, oficios varios)
- Acta constitutiva y estatutos aprobados en asamblea
- Padrón de socios con firmas
- Acta de elección de directiva
- Constancia de voto personal, libre, directo y secreto

##### 1.10 Procedimiento de Registro de Contrato Colectivo Inicial
**Descripción:** Registro y depósito del primer CCT ante el CFCRL.
**Fundamento:** LFT Arts. 386–391.
**Requisitos:**
- Nombre del sindicato titular y número de registro
- Nombre y RFC del patrón
- Texto completo del CCT
- Constancia de consulta a trabajadores
- Resultado del proceso de legitimación

##### 1.11 Procedimiento de Revisión de Contrato Colectivo de Trabajo
**Descripción:** Revisión de cláusulas económicas o integrales del CCT.
**Fundamento:** LFT Arts. 399–399-bis.
**Requisitos:**
- CCT vigente (número de registro y fecha)
- Cláusulas a modificar
- Nuevas condiciones económicas propuestas
- Resultado de consulta a trabajadores

##### 1.12 Procedimiento de Revisión de Contrato-Ley
**Descripción:** Revisión de las condiciones del contrato-ley en una rama industrial.
**Fundamento:** LFT Arts. 404–418.
**Requisitos:**
- Rama industrial y ámbito de aplicación territorial
- Sindicatos y patrones suscribientes
- Condiciones actuales y propuestas de modificación

##### 1.13 Procedimiento de Preferencia de Créditos Laborales
**Descripción:** Hacer valer la preferencia del crédito laboral sobre otros adeudos.
**Fundamento:** LFT Art. 113.
**Requisitos:**
- Sentencia o laudo con crédito laboral reconocido
- Bienes del patrón en disputa con otros acreedores
- Monto del crédito laboral y de los demás créditos

---

#### 2. DEMANDAS Y ACCIONES ESPECÍFICAS

---

##### 2.1 Demanda Laboral (Escrito de Demanda)
**Descripción:** Escrito inicial que inicia el procedimiento ordinario o especial.
**Fundamento:** LFT Arts. 685, 871–878.
**Requisitos:**
- Nombre completo, CURP y domicilio del trabajador
- Nombre, denominación social y domicilio del patrón
- Número de seguridad social del trabajador
- Fecha de inicio y fin de la relación laboral
- SDI (cuota diaria + proporcionales)
- Tipo de separación y circunstancias del despido
- Prestaciones reclamadas con montos o bases de cálculo
- Fundamento legal de cada prestación
- Ofrecimiento de pruebas

##### 2.2 Demanda de Reinstalación en el Empleo
**Descripción:** Acción del trabajador despedido injustificadamente que opta por reinstalación.
**Fundamento:** LFT Arts. 48–50; Const. Art. 123 Ap. A Fr. XXII.
**Requisitos:**
- Manifestación expresa de la opción por reinstalación
- Descripción del despido (lugar, fecha, persona, forma)
- Puesto, categoría y condiciones originales
- Salarios caídos desde el despido hasta la reinstalación

##### 2.3 Demanda de Pago de Indemnización Constitucional
**Descripción:** Acción del trabajador despedido que opta por indemnización (3 meses de salario).
**Fundamento:** LFT Arts. 48–50.
**Requisitos:**
- Manifestación expresa de la opción por indemnización
- SDI para cálculo de 3 meses (90 días)
- 20 días de SDI por año de servicios
- Partes proporcionales de aguinaldo, vacaciones, prima vacacional
- Prima de antigüedad (12 días por año, máximo 2 salarios mínimos)

##### 2.4 Demanda de Pago de Salarios Caídos / Vencidos
**Descripción:** Reclamación de salarios no percibidos desde el despido hasta la resolución.
**Fundamento:** LFT Art. 48 (limitado a 12 meses + intereses 2 % mensual).
**Requisitos:**
- Fecha exacta del despido
- SDI
- Cálculo de 12 meses de SDI (o plazo menor)
- Intereses del 2 % mensual sobre los siguientes 15 meses

##### 2.5 Demanda de Pago de Prestaciones Laborales
**Descripción:** Reclamación de aguinaldo, vacaciones, prima vacacional, prima de antigüedad, horas extras, etc.
**Fundamento:** LFT Arts. 76–80, 87, 162, 68–75.
**Requisitos:**
- Tipo de prestación reclamada
- Período de la reclamación
- SDI o salario ordinario según la prestación
- Cálculo estimado del monto

##### 2.6 Demanda de Designación de Beneficiarios de Trabajador Fallecido
**Descripción:** Beneficiarios reclaman prestaciones del trabajador fallecido.
**Fundamento:** LFT Arts. 501–502, 723–733.
**Requisitos:**
- Nombre y datos del trabajador fallecido
- Acta de defunción
- Documentos que acrediten parentesco o dependencia económica
- Prestaciones pendientes al momento del fallecimiento

##### 2.7 Demanda de Prestaciones de Seguridad Social
**Descripción:** Acción para obtener prestaciones del IMSS/INFONAVIT omitidas o negadas.
**Fundamento:** LFT Arts. 723–733; LSS arts. aplicables.
**Requisitos:**
- Prestación reclamada (incapacidad, pensión, crédito INFONAVIT, guardería)
- Acreditación de relación laboral y cotización
- Resolución o negativa del instituto (si existe)

##### 2.8 Demanda de Titularidad de Contrato Colectivo de Trabajo
**Descripción:** Acción sindical para obtener la titularidad del CCT.
**Fundamento:** LFT Arts. 388–391, 931–933.
**Requisitos:**
- Nombre y registro del sindicato promovente
- Empresa y centro de trabajo
- CCT en disputa (número de registro, patrón, sindicato actual)
- Afiliación mayoritaria (documentos de consulta/recuento)

##### 2.9 Demanda de Celebración de Contrato Colectivo de Trabajo
**Descripción:** Acción del sindicato mayoritario para obligar al patrón a celebrar CCT.
**Fundamento:** LFT Arts. 386–391.
**Requisitos:**
- Nombre del sindicato, registro y constancia de representatividad
- Nombre y domicilio del patrón
- Proyecto de CCT propuesto
- Constancia de notificación al patrón y negativa

##### 2.10 Demanda de Revisión de Contrato Colectivo de Trabajo
**Descripción:** Acción para revisar condiciones del CCT.
**Fundamento:** LFT Arts. 399–399-bis.
**Requisitos:**
- CCT vigente y cláusulas a revisar
- Cláusulas económicas nuevas con montos
- Resultado de consulta a trabajadores

##### 2.11 Demanda de Nulidad de Convenio o Liquidación
**Descripción:** Anulación de convenios con renuncia de derechos irrenunciables.
**Fundamento:** LFT Arts. 5, 33.
**Requisitos:**
- Texto del convenio o liquidación impugnado
- Derechos renunciados
- Circunstancias de la firma (coacción, vicio del consentimiento)
- Prestaciones que legalmente corresponden

##### 2.12 Demanda en Conflictos Colectivos de Naturaleza Económica
**Descripción:** Escrito de parte para iniciar el conflicto económico.
**Fundamento:** LFT Arts. 900–919.
**Requisitos:**
- Parte promovente (sindicato o patrón)
- Causas económicas (documentación financiera)
- Condiciones actuales y propuestas

##### 2.13 Demanda de Reconvención Laboral
**Descripción:** Demanda del patrón contra el trabajador dentro del mismo juicio.
**Fundamento:** LFT Art. 878 Fr. V.
**Requisitos:**
- Prestaciones reconvencionales con montos y fundamento
- Hechos que sustentan la reconvención

##### 2.14 Solicitud de Declaración de Inexistencia de Huelga
**Descripción:** Petición del patrón para declarar huelga inexistente.
**Fundamento:** LFT Arts. 459–462.
**Requisitos:**
- Datos del emplazamiento (sindicato, fecha, objeto)
- Causas de inexistencia
- Fundamento legal

##### 2.15 Solicitud de Calificación de Ilicitud de Huelga
**Descripción:** Petición del patrón para declarar huelga ilícita.
**Fundamento:** LFT Arts. 445–447.
**Requisitos:**
- Actos de violencia o hechos constitutivos de ilicitud
- Testigos y pruebas documentales
- Daños ocasionados

---

#### 3. TIPOS DE ALEGATOS

---

##### 3.1 Alegatos Orales (en Audiencia de Juicio)
**Descripción:** Exposición oral al concluir el desahogo de pruebas.
**Fundamento:** LFT Art. 884.
**Requisitos:**
- Resumen de hechos probados con indicación de pruebas
- Valor probatorio de cada prueba
- Conclusión sobre prestaciones procedentes o improcedentes

##### 3.2 Alegatos por Escrito (Procedimiento Especial)
**Descripción:** Escrito de alegatos dentro de los 5 días siguientes al cierre de instrucción.
**Fundamento:** LFT Art. 733.
**Requisitos:**
- Número de expediente y autoridad
- Síntesis de hechos y pruebas desahogadas
- Fundamentos legales de las pretensiones

##### 3.3 Alegatos Orales en Conflictos Colectivos de Naturaleza Económica
**Descripción:** Exposición oral en el procedimiento de conflicto económico.
**Fundamento:** LFT Art. 916.
**Requisitos:**
- Resumen de la situación económica probada
- Propuesta de condiciones a modificar

---

#### 4. ACTOS PROCESALES Y DOCUMENTOS DEL PROCESO LABORAL

---

##### 4.1 Conciliación Prejudicial — Escrito de Solicitud
**Descripción:** Escrito que inicia la conciliación prejudicial obligatoria.
**Fundamento:** LFT Arts. 684-A–684-J.
**Requisitos:**
- Nombre y domicilio del trabajador
- Nombre y domicilio del patrón
- Centro de trabajo
- Descripción del conflicto y prestaciones
- Documentos probatorios

##### 4.2 Conciliación Prejudicial — Citatorio a Audiencia
**Descripción:** Citación a las partes para la audiencia de conciliación.
**Elementos:**
- Centro de Conciliación que cita
- Nombre de las partes citadas
- Día, hora y lugar de la audiencia
- Apercibimiento por inasistencia

##### 4.3 Conciliación Prejudicial — Acta de Audiencia
**Descripción:** Registro del desarrollo y resultado de la audiencia.
**Fundamento:** LFT Art. 684-E.
**Requisitos:**
- Datos de las partes asistentes
- Postura de cada parte
- Acuerdos o constancia de fracaso

##### 4.4 Conciliación Prejudicial — Constancia de No Conciliación
**Descripción:** Documento que acredita el agotamiento de la etapa prejudicial.
**Fundamento:** LFT Art. 684-J.
**Requisitos:**
- Folio de la solicitud de conciliación
- Fecha de la audiencia y resultado

##### 4.5 Conciliación Prejudicial — Convenio de Conciliación
**Descripción:** Acuerdo con efectos de cosa juzgada.
**Fundamento:** LFT Arts. 684-G, 987.
**Requisitos:**
- Prestaciones y montos acordados
- Forma y plazos de pago
- Declaraciones sobre terminación de la relación
- Firmas de partes y conciliador

##### 4.6 Procedimiento Ordinario — Auto Admisorio de la Demanda
**Descripción:** Resolución que admite la demanda y ordena el emplazamiento.
**Elementos:**
- Número de expediente y fecha
- Demanda que se admite
- Plazo para contestar
- Apercibimientos

##### 4.7 Procedimiento Ordinario — Emplazamiento a Juicio
**Descripción:** Notificación al patrón de la demanda y plazo para contestar.
**Elementos:**
- Copia de la demanda y auto admisorio
- Plazo para contestar (15 días hábiles)
- Apercibimiento de rebeldía

##### 4.8 Procedimiento Ordinario — Contestación de Demanda
**Descripción:** Respuesta del patrón demandado.
**Fundamento:** LFT Arts. 878–880.
**Requisitos:**
- Número de expediente y tribunal
- Respuesta a cada hecho (se admite / se niega / se desconoce)
- Excepciones procesales y de fondo
- Fundamento legal
- Ofrecimiento de pruebas

##### 4.9 Procedimiento Ordinario — Escrito de Réplica
**Descripción:** Respuesta del actor a la contestación.
**Requisitos:**
- Número de expediente
- Refutación de las excepciones opuestas
- Argumentos adicionales

##### 4.10 Procedimiento Ordinario — Escrito de Contrarréplica
**Descripción:** Respuesta del demandado a la réplica.
**Requisitos:**
- Número de expediente
- Refutación de los argumentos de la réplica

##### 4.11 Procedimiento Ordinario — Reconvención
**Descripción:** Demanda del patrón contra el trabajador.
**Fundamento:** LFT Art. 878 Fr. V.
**Requisitos:**
- Prestaciones reconvencionales con montos
- Hechos y fundamento legal

##### 4.12 Procedimiento Ordinario — Contestación a la Reconvención
**Descripción:** Respuesta del trabajador a la reconvención.
**Requisitos:**
- Referencia expresa a cada hecho de la reconvención
- Excepciones y defensas
- Pruebas

##### 4.13 Audiencia Preliminar — Auto de Radicación
**Descripción:** Resolución que radica el expediente en el tribunal.
**Elementos:**
- Número de expediente
- Fecha de radicación
- Juez o tribunal instructor

##### 4.14 Audiencia Preliminar — Resolución sobre Excepciones Procesales
**Descripción:** Resolución que dirime las excepciones previas.
**Fundamento:** LFT Art. 879.
**Requisitos:**
- Excepciones opuestas y argumentos
- Pruebas ofrecidas

##### 4.15 Audiencia Preliminar — Auto de Admisión / Desechamiento de Pruebas
**Descripción:** Resolución que admite o desecha los medios de prueba ofrecidos.
**Elementos:**
- Listado de pruebas admitidas
- Pruebas desechadas y fundamento
- Fecha para audiencia de juicio

##### 4.16 Audiencia Preliminar — Auto Resolutorio de Incidente
**Descripción:** Resolución de incidente (falta de personalidad, nulidad, incompetencia).
**Elementos:**
- Incidente planteado
- Alegatos de las partes
- Resolución y fundamento

##### 4.17 Audiencia de Juicio — Dictamen Pericial
**Descripción:** Opinión técnica del perito.
**Fundamento:** LFT Arts. 822–825.
**Requisitos:**
- Puntos periciales a dictaminar
- Nombre y cédula profesional del perito
- Disciplina y especialidad

##### 4.18 Audiencia de Juicio — Declaración Testimonial
**Descripción:** Deposición de testigos en la audiencia.
**Requisitos:**
- Nombre, domicilio y ocupación del testigo
- Relación con las partes
- Hechos sobre los que declarará

##### 4.19 Audiencia de Juicio — Confesión / Absolución de Posiciones
**Descripción:** Declaración de parte bajo protesta.
**Requisitos:**
- Pliego de posiciones
- Apertura bajo protesta de decir verdad

##### 4.20 Audiencia de Juicio — Certificación de Cierre de Instrucción
**Descripción:** Acta que certifica el cierre del desahogo de pruebas.
**Elementos:**
- Pruebas desahogadas
- Pruebas pendientes (si las hay)
- Fecha de cierre

##### 4.21 Audiencia de Juicio — Sentencia Laboral
**Descripción:** Resolución definitiva del tribunal.
**Fundamento:** LFT Arts. 840–843.
**Requisitos:**
- Prestaciones procedentes / improcedentes
- Bases de cálculo de la condena
- Costas (si se imponen)
- Plazo de cumplimiento voluntario

---

#### 5. RECURSOS

---

##### 5.1 Recurso de Reconsideración
**Descripción:** Impugnación contra acuerdos del secretario instructor.
**Fundamento:** LFT Art. 856-bis.
**Requisitos:**
- Acuerdo impugnado (fecha, contenido)
- Agravios (razones de ilegalidad)
- Pruebas ofrecidas en apoyo

##### 5.2 Resolución del Recurso de Reconsideración
**Descripción:** Resolución que confirma, revoca o modifica el acuerdo impugnado.
**Elementos:**
- Acuerdo recurrido
- Agravios del recurrente
- Determinación fundada

---

#### 6. DOCUMENTOS DERIVADOS DE LA HUELGA

---

##### 6.1 Pliego de Peticiones con Emplazamiento a Huelga
**Descripción:** Demandas del sindicato al patrón con anuncio de huelga.
**Fundamento:** LFT Arts. 440, 920–921.
**Requisitos:**
- Nombre y registro del sindicato
- Nombre y domicilio del patrón
- Peticiones concretas
- Objeto de la huelga
- Fecha de estallamiento (mín. 6 días / 10 días servicio público)
- Número de trabajadores que suscriben

##### 6.2 Contestación del Patrón al Pliego de Peticiones
**Descripción:** Respuesta formal del patrón al sindicato.
**Fundamento:** LFT Art. 926.
**Requisitos:**
- Referencia a cada petición
- Oferta (aceptación, rechazo, contrapropuesta)
- Fundamento del rechazo

##### 6.3 Aviso de Suspensión de Labores (Estallamiento)
**Descripción:** Comunicación al tribunal del inicio de la huelga.
**Fundamento:** LFT Arts. 443, 930.
**Requisitos:**
- Fecha y hora exacta del estallamiento
- Trabajadores adheridos
- Medidas de servicios mínimos

##### 6.4 Constancia de Representatividad Sindical (CFCRL)
**Descripción:** Documento que acredita la representación de un sindicato.
**Elementos:**
- Nombre y registro del sindicato
- Ámbito de representación
- Número de trabajadores representados

##### 6.5 Acta de Recuento de Trabajadores
**Descripción:** Documento del recuento de afiliación mayoritaria.
**Fundamento:** LFT Art. 931.
**Requisitos:**
- Total de trabajadores de la empresa
- Votos por cada sindicato
- Resultado del recuento
- Incidencias

##### 6.6 Resolución de Existencia / Inexistencia Legal de Huelga
**Descripción:** Declaración sobre el cumplimiento de requisitos legales.
**Fundamento:** LFT Arts. 459–462.
**Requisitos:**
- Datos del emplazamiento
- Argumentos de las partes
- Resultado del recuento (si se realizó)

##### 6.7 Resolución de Calificación de Ilicitud de Huelga
**Descripción:** Declaración de huelga ilícita por violencia u otros motivos.
**Fundamento:** LFT Arts. 445–447.
**Requisitos:**
- Hechos de violencia acreditados
- Consecuencias legales

##### 6.8 Declaración de Huelga Justificada
**Descripción:** Resolución que declara justificada la huelga.
**Elementos:**
- Causas que la justifican
- Efectos legales

##### 6.9 Fijación del Número de Trabajadores de Servicios Mínimos
**Descripción:** Determinación del personal necesario durante la huelga.
**Elementos:**
- Número y puestos de trabajadores
- Fundamento
- Notificación a las partes

---

#### 7. DOCUMENTOS DE EJECUCIÓN LABORAL

---

##### 7.1 Solicitud de Ejecución de Sentencia / Convenio
**Descripción:** Solicitud para hacer cumplir la sentencia o convenio.
**Fundamento:** LFT Art. 939.
**Requisitos:**
- Número de expediente y datos de la sentencia
- Monto actualizado de la condena
- Bienes del patrón (si se conocen)

##### 7.2 Auto de Requerimiento y Embargo
**Descripción:** Auto que requiere el pago y ordena el embargo.
**Fundamento:** LFT Arts. 941–945.
**Requisitos:**
- Monto de la condena
- Bienes embargables del patrón
- Actuario o ejecutor designado

##### 7.3 Acta de Embargo (Bienes, Cuentas, Inmuebles)
**Descripción:** Formalización del embargo de bienes.
**Fundamento:** LFT Arts. 943–949.
**Requisitos:**
- Descripción detallada de los bienes
- Depositario designado
- Valor estimado

##### 7.4 Avalúo de Bienes Embargados
**Descripción:** Determinación del valor de los bienes embargados.
**Elementos:**
- Identificación del bien
- Valor del avalúo
- Perito avaluador

##### 7.5 Convocatoria / Anuncio de Remate
**Descripción:** Convocatoria a postores para el remate.
**Fundamento:** LFT Arts. 950–956.
**Requisitos:**
- Descripción de los bienes
- Valor base (2/3 del avalúo)
- Fecha, hora y lugar
- Requisitos para postores

##### 7.6 Acta / Diligencia de Remate
**Descripción:** Documento que formaliza el remate y adjudicación.
**Fundamento:** LFT Arts. 950–956.
**Requisitos:**
- Posturas presentadas
- Postura ganadora y adjudicatario
- Monto pagado y saldo cubierto

##### 7.7 Auto de Finca de Remate
**Descripción:** Declaración del mejor postor como adjudicatario.
**Elementos:**
- Postura ganadora
- Bien adjudicado
- Orden de escrituración

##### 7.8 Liquidación de Sentencia / Incidente de Liquidación
**Descripción:** Cálculo pormenorizado del monto adeudado.
**Fundamento:** LFT Art. 843.
**Requisitos:**
- Sentencia con bases de cálculo
- SDI, antigüedad, período de salarios caídos
- Cálculo detallado de cada prestación

##### 7.9 Exhorto de Ejecución (a otro Tribunal)
**Descripción:** Comunicación a otro tribunal para ejecutar la sentencia.
**Elementos:**
- Tribunal exhortante y exhortado
- Sentencia a ejecutar
- Diligencias solicitadas

##### 7.10 Auto de Cumplimiento de Sentencia
**Descripción:** Resolución que declara cumplida la sentencia.
**Elementos:**
- Actuaciones de cumplimiento realizadas
- Declaración de cumplimiento
- Archivo del expediente

##### 7.11 Resolución de Tercería Excluyente de Dominio (Laboral)
**Descripción:** Resolución sobre propiedad de bienes embargados.
**Fundamento:** LFT Arts. 976–980.
**Requisitos:**
- Documentos de propiedad del tercero
- Fecha de adquisición (anterior al embargo)
- Inscripción en RPP (inmuebles)

##### 7.12 Resolución de Tercería de Preferencia / Preferencia de Crédito
**Descripción:** Resolución sobre orden de prelación de créditos.
**Fundamento:** LFT Arts. 113, 981–987.
**Requisitos:**
- Créditos en concurso (laboral, fiscal, hipotecario)
- Documentos de cada crédito y fechas
- Producto del remate disponible

##### 7.13 Providencia Cautelar (Medida Cautelar Laboral)
**Descripción:** Medida cautelar antes o durante el juicio.
**Elementos:**
- Riesgo de incumplimiento
- Bienes a asegurar
- Garantía si procede

##### 7.14 Constancia de Pago y Cancelación de Embargo
**Descripción:** Documento que acredita el pago total y ordena levantar el embargo.
**Elementos:**
- Monto pagado
- Bienes desembargados
- Orden de cancelación

---

#### 8. CONTRATOS Y CONVENIOS LABORALES

---

##### 8.1 Contrato Individual de Trabajo por Tiempo Indeterminado
**Descripción:** Contrato sin fecha fija de término (regla general).
**Fundamento:** LFT Arts. 20–39.
**Requisitos:**
- Nombre y CURP del trabajador; denominación del patrón
- Puesto, categoría y actividades
- Lugar y horario de trabajo
- Salario ordinario y prestaciones (aguinaldo, vacaciones, prima vacacional)
- Cláusulas de confidencialidad o no competencia (opcional)

##### 8.2 Contrato Individual de Trabajo por Tiempo Determinado
**Descripción:** Contrato con fecha de término justificada.
**Fundamento:** LFT Arts. 35–39.
**Requisitos:** Mismos que 8.1. Causa justificada. Fecha de inicio y término.

##### 8.3 Contrato Individual de Trabajo por Obra Determinada
**Descripción:** Contrato para obra específica.
**Fundamento:** LFT Arts. 36–39.
**Requisitos:** Descripción de la obra. Lugar de ejecución. Salario y forma de pago.

##### 8.4 Contrato Individual de Trabajo por Temporada
**Descripción:** Contrato para actividad estacional.
**Fundamento:** LFT Art. 39-F.
**Requisitos:** Actividad estacional. Períodos de temporada. Salario y prestaciones.

##### 8.5 Contrato con Período a Prueba
**Descripción:** Contrato con período de prueba (máx. 30 días general / 180 días dirección).
**Fundamento:** LFT Arts. 39-A–39-B.
**Requisitos:** Duración. Criterios de evaluación. Condiciones del contrato definitivo.

##### 8.6 Contrato de Capacitación Inicial
**Descripción:** Contrato para adquisición de habilidades (máx. 3 meses / 6 meses dirección).
**Fundamento:** LFT Arts. 39-C–39-D.
**Requisitos:** Duración. Plan de capacitación. Evaluación.

##### 8.7 Contrato de Subcontratación de Servicios Especializados
**Descripción:** Contrato con contratista REPSE para servicios no esenciales.
**Fundamento:** LFT Arts. 12–15-D (reforma 2021).
**Requisitos:**
- Nombre, RFC de contratante y contratista
- Descripción precisa de los servicios
- Número de trabajadores y condiciones
- Número de registro REPSE del contratista
- Período del contrato

##### 8.8 Contrato de Trabajo para el Extranjero
**Descripción:** Contrato para prestar servicios fuera del país.
**Requisitos:**
- País de destino y condiciones migratorias
- Salario y prestaciones aplicables
- Gastos de traslado y repatriación
- Vigencia y causas de terminación

##### 8.9 Contrato de Trabajo para Explotación de Minas
**Descripción:** Contrato especial para la industria minera.
**Requisitos:**
- Tipo de explotación
- Medidas de seguridad e higiene específicas
- Jornadas y salarios conforme a la industria

##### 8.10 Contrato Colectivo de Trabajo
**Descripción:** Convenio entre sindicato titular y patrón.
**Fundamento:** LFT Arts. 386–403.
**Requisitos:**
- Nombre y registro del sindicato titular
- Nombre, RFC y domicilio del patrón
- Cláusulas de ingreso, categorías, salarios tabulados
- Prestaciones superiores a la ley
- Cláusula de exclusión (si se pacta)
- Vigencia y revisión

##### 8.11 Contrato-Ley (Rama Industrial)
**Descripción:** CCT obligatorio para toda una rama industrial.
**Fundamento:** LFT Arts. 404–418.
**Requisitos:**
- Rama industrial y ámbito territorial
- Sindicatos y patrones suscribientes
- Condiciones de trabajo y tablas salariales
- Procedimiento de revisión y duración

##### 8.12 Convenio de Revisión del Contrato Colectivo de Trabajo
**Descripción:** Acuerdo de modificación del CCT vigente.
**Requisitos:**
- CCT vigente
- Cláusulas modificadas
- Nuevas condiciones acordadas
- Resultado de consulta a trabajadores

##### 8.13 Convenio de Terminación de la Relación Laboral
**Descripción:** Acuerdo de terminación bilateral de la relación de trabajo.
**Requisitos:**
- Causa de la terminación (mutuo acuerdo)
- Prestaciones pagadas (desglose)
- Declaración del trabajador de recibir conforme

##### 8.14 Convenio de Liquidación de Trabajador (Ratificado)
**Descripción:** Acuerdo de pago total de prestaciones, ratificado ante autoridad.
**Fundamento:** LFT Arts. 33, 987.
**Requisitos:**
- Causa de terminación (renuncia, mutuo acuerdo, despido reconocido)
- Desglose detallado de prestaciones pagadas
- Monto total y forma de pago
- Declaración de conformidad del trabajador

##### 8.15 Reglamento Interior de Trabajo
**Descripción:** Disposiciones sobre organización y disciplina en el centro de trabajo.
**Fundamento:** LFT Arts. 422–425.
**Requisitos:**
- Nombre del patrón y centro de trabajo
- Horarios por turno
- Lugar y tiempo para alimentos
- Días y lugar de pago
- Normas de seguridad e higiene
- Sanciones disciplinarias y procedimiento

##### 8.16 Estatutos Sindicales
**Descripción:** Norma interna del sindicato.
**Fundamento:** LFT Arts. 371–373.
**Requisitos:**
- Nombre y tipo de sindicato
- Domicilio social
- Objeto y actividades
- Admisión, separación y expulsión
- Estructura orgánica
- Procedimiento de elección (voto personal, libre, directo, secreto)
- Patrimonio y manejo de cuotas

##### 8.17 Solicitud de Registro Sindical
**Descripción:** Solicitud formal ante el CFCRL.
**Requisitos:**
- Acta constitutiva
- Estatutos
- Padrón de socios
- Acta de elección

##### 8.18 Tabulador de Salarios
**Descripción:** Tabla de salarios por puesto, categoría y turno.
**Elementos:**
- Puestos y categorías
- Salario base por jornada
- Prestaciones en especie (si aplican)

##### 8.19 Padrón de Socios del Sindicato
**Descripción:** Lista de miembros del sindicato.
**Elementos:**
- Nombre y firma de cada socio
- Puesto y área de trabajo
- Fecha de afiliación

---

#### 9. DOCUMENTOS LABORALES ADMINISTRATIVOS

---

##### 9.1 Liquidación Laboral
**Descripción:** Cálculo detallado de prestaciones adeudadas al terminar la relación.
**Fundamento:** LFT Arts. 48–50, 76–80, 87, 162.
**Requisitos:**
- Fechas de ingreso y separación
- Salario diario ordinario y SDI
- Motivo de terminación
- Desglose: indemnización, 20 días por año, prima de antigüedad, proporcionales

##### 9.2 Finiquito
**Descripción:** Documento que acredita el pago total al trabajador que renuncia o termina su contrato.
**Fundamento:** LFT Arts. 53–55, 76–80, 87.
**Requisitos:** Mismos que liquidación. Declaración del trabajador de recibir conforme.

##### 9.3 Constancia de Trabajo
**Descripción:** Certificación del patrón sobre servicios prestados.
**Fundamento:** LFT Art. 804.
**Requisitos:**
- Nombre del trabajador
- Puesto desempeñado
- Período de servicios
- Salario vigente

##### 9.4 Recibo de Nómina / Recibo de Pago de Salario
**Descripción:** Comprobante de pago de salario.
**Fundamento:** LFT Arts. 101, 804.
**Requisitos:**
- Nombre y RFC del trabajador
- Período de pago
- Salario, horas extras, bonos y deducciones
- Firma o acuse de recibo

##### 9.5 Aviso de Huelga
**Descripción:** Notificación del inicio de huelga al patrón y autoridad.
**Fundamento:** LFT Arts. 443, 920.
**Requisitos:**
- Nombre y registro del sindicato
- Nombre y domicilio del patrón
- Fecha y hora del estallamiento

##### 9.6 Cédula de Notificación (Laboral)
**Descripción:** Constancia de notificación de una resolución.
**Fundamento:** LFT Arts. 739–752.
**Requisitos:**
- Autoridad que ordena la notificación
- Notificado (nombre y domicilio)
- Resolución notificada
- Fecha, hora y lugar
- Actuario o notificador

##### 9.7 Exhorto (Laboral)
**Descripción:** Comunicación entre tribunales para practicar diligencias.
**Fundamento:** LFT Arts. 753–756.
**Requisitos:**
- Tribunal exhortante y expediente
- Diligencias a practicar
- Datos del notificado o lugar a inspeccionar

##### 9.8 Despacho (Exhorto Internacional Laboral)
**Descripción:** Comunicación a autoridad extranjera.
**Requisitos:**
- Autoridad extranjera y tratado aplicable
- Diligencias solicitadas
- Traducción y legalización

---

### Lectura de documentos
- Extraer texto de PDF o Word
- Identificar: nombre del trabajador, patrón, SDI, antigüedad, prestaciones
- Identificar tipo de separación (despido, renuncia, terminación)
- Calcular SDI integrando aguinaldo, vacaciones y prima vacacional


## 6. Reglas adicionales

- En demandas, siempre calcular SDI integrando aguinaldo (15/365), vacaciones (proporcional LFT Art. 76) y prima vacacional (25 % de vacaciones).
- Salarios caídos: limitados a 12 meses + intereses del 2 % mensual por los 15 meses siguientes (LFT Art. 48 reforma 2019).
- Todo convenio no ratificado ante autoridad no tiene efectos de cosa juzgada (LFT Art. 33).
- El trabajador de confianza no puede afiliarse al sindicato de la empresa (LFT Art. 183).
- Subcontratación: verificar registro vigente en REPSE (obligatorio desde 2021).


# Skill: Redactor de Documentos — Derecho Notarial y Registro Civil
**Fase 3 | 73 tipos de documentos**
Fuentes: Ley del Notariado (CDMX y Estado de México), Ley Registral del RPP, Código Civil Federal, Código Civil para el DF/CDMX, Código Civil del Estado de México (codvig001), Ley Orgánica del Registro Civil.

---

## 1. Nombre
**"Redactor de instrumentos notariales, registrales y actas del registro civil"**
(Formato notarial/forense — alineaciones, mayúsculas, fe de conocimiento, cláusulas)

## 2. Objetivo
A partir de documentos adjuntos por el usuario (PDF/Word) y de instrucciones conversacionales, generar cualquier instrumento notarial, documento registral, testamento, poder o acta del registro civil que cumpla con las formalidades legales y de presentación:
- Encabezado notarial (número de instrumento, notaría, notario) alineado a la derecha
- Comparecientes y fe de conocimiento en mayúsculas
- Cuerpo justificado (ANTECEDENTES, DECLARACIONES, CLÁUSULAS)
- Cierre notarial con lugar, fecha, firmas y fe del notario
- Exportación a Word (.docx) con formato exacto

## 3. Entradas del usuario
- **Documentos subidos** (opcional): escrituras previas, actas, certificados, identificaciones
- **Indicación del tipo de instrumento**: escritura, poder, testamento, acta, certificado, etc.
- **Datos específicos** (solicitados en conversación):
  - Datos de los comparecientes/otorgantes (nombre, RFC, CURP, estado civil, domicilio)
  - Naturaleza del acto jurídico
  - Bienes involucrados (descripción, valor, datos registrales)
  - Cláusulas y condiciones pactadas
  - Lugar y fecha de otorgamiento

### 4.3 Catálogo de documentos y requisitos

---

#### 1. INSTRUMENTOS NOTARIALES

---

##### 1.1 Escritura Pública
**Descripción:** Instrumento notarial que da fe de un acto jurídico celebrado ante notario.
**Fundamento:** CC DF Arts. 1516–1520; Ley del Notariado CDMX/Edomex.
**Requisitos:**
- Número de instrumento y notaría
- Nombre, estado civil, RFC, CURP, domicilio de comparecientes
- Representantes legales (escritura de poder y notaría de origen)
- Objeto y naturaleza del acto jurídico
- Declaraciones de las partes
- Cláusulas acordadas
- Documentos previos relacionados (antecedentes registrales)
- Pago de impuestos y derechos
- Lugar y fecha de firma

##### 1.2 Escritura Constitutiva (de Sociedad)
**Descripción:** Formaliza la constitución de una sociedad mercantil o civil.
**Fundamento:** LGSM Arts. 5–6; CC DF Arts. 2688–2736.
**Requisitos:**
- Tipo de sociedad (SA, SA de CV, SRL, SC, AC, etc.)
- Denominación social
- Domicilio social y duración
- Objeto social
- Capital social e integración (acciones/partes, valor nominal)
- Socios fundadores: nombre, RFC, domicilio, aportación
- Órganos de administración y vigilancia
- Cláusulas de transmisión de acciones
- RFC del notario para inscripción SAT

##### 1.3 Escritura de Compraventa
**Descripción:** Transmisión de dominio de bien inmueble.
**Fundamento:** CC DF Arts. 2248–2322.
**Requisitos:**
- Datos del vendedor y comprador (nombre, RFC, CURP, estado civil, domicilio)
- Descripción del inmueble (superficie, medidas, colindancias, clave catastral, folio real)
- Antecedentes de propiedad (escritura anterior)
- Precio y forma de pago (contado, crédito hipotecario, INFONAVIT, FOVISSSTE)
- Avalúo catastral y valor comercial
- Estado fiscal (predial, agua)
- Certificado de libertad de gravámenes
- ISR del enajenante e ISAI del adquirente

##### 1.4 Escritura de Donación
**Descripción:** Transmisión gratuita de un bien.
**Fundamento:** CC DF Arts. 2332–2383.
**Requisitos:**
- Datos del donante y donatario
- Descripción del bien donado
- Causa de la donación (liberal, remuneratoria, con carga)
- Avalúo del bien
- Declaración sobre inoficiosidad
- ISR (si aplica) o exención

##### 1.5 Escritura de Arrendamiento (Protocolización)
**Descripción:** Formalización de contrato de arrendamiento.
**Fundamento:** CC DF Arts. 2398–2496.
**Requisitos:**
- Datos del arrendador y arrendatario
- Inmueble arrendado
- Renta y plazo
- Depósito en garantía
- Prórroga, desahucio y penalidades

##### 1.6 Escritura de Hipoteca
**Descripción:** Constitución de gravamen hipotecario.
**Fundamento:** CC DF Arts. 2893–2943.
**Requisitos:**
- Datos del deudor hipotecante y acreedor
- Inmueble en garantía (folio real)
- Monto del crédito, tasa de interés y plazo
- Vencimiento anticipado
- Cédula hipotecaria (Edomex)

##### 1.7 Escritura de Fideicomiso
**Descripción:** Constitución de fideicomiso ante notario.
**Fundamento:** LGTOC Arts. 381–407.
**Requisitos:**
- Fideicomitente, fiduciario, fideicomisario(s)
- Objeto y fin (garantía, administración, traslativo)
- Bienes fideicomitidos
- Facultades del fiduciario
- Duración y causas de extinción

##### 1.8 Escritura de Protocolización
**Descripción:** Incorporación al protocolo de documento privado.
**Fundamento:** Ley del Notariado CDMX/Edomex.
**Requisitos:**
- Tipo de documento (acta de asamblea, contrato privado, resolución judicial)
- Fecha y lugar del documento
- Partes que comparecen a ratificar
- Propósito de la protocolización

##### 1.9 Escritura de Fusión de Sociedades
**Descripción:** Unión de dos o más sociedades en una sola.
**Fundamento:** LGSM Arts. 222–226.
**Requisitos:**
- Sociedades fusionantes y fusionada/resultante
- Acuerdos de asamblea de cada sociedad
- Balance de fusión y activos/pasivos transferidos
- Canje de acciones
- Plazo de oposición de acreedores

##### 1.10 Escritura de Escisión de Sociedad
**Descripción:** División de una sociedad en dos o más.
**Fundamento:** LGSM Art. 228-bis.
**Requisitos:**
- Sociedad escindente y escindidas
- Activos y pasivos transmitidos a cada escindida
- Acuerdo de asamblea
- Tratamiento fiscal

##### 1.11 Escritura de Disolución de Sociedad
**Descripción:** Acuerdo de disolución de la sociedad.
**Fundamento:** LGSM Arts. 229–244.
**Requisitos:**
- Sociedad disuelta y acuerdo de asamblea
- Causa de disolución
- Nombramiento de liquidadores

##### 1.12 Escritura de Liquidación de Sociedad
**Descripción:** Distribución del haber social entre los socios.
**Fundamento:** LGSM Arts. 242–249.
**Requisitos:**
- Liquidador(es)
- Inventario y balance final
- Haber social a distribuir
- Declaración de extinción

##### 1.13 Escritura de Aumento de Capital
**Descripción:** Incremento del capital social.
**Fundamento:** LGSM Arts. 182, 216.
**Requisitos:**
- Acuerdo de asamblea
- Monto del aumento y tipo de aportación
- Nuevas acciones/partes y suscriptores

##### 1.14 Escritura de Reducción de Capital
**Descripción:** Disminución del capital social.
**Fundamento:** LGSM Arts. 9, 182, 216.
**Requisitos:**
- Causa de la reducción (pérdidas, devolución)
- Acuerdo de asamblea
- Nuevo capital y acciones canceladas
- Publicación para protección de acreedores

##### 1.15 Testimonio Notarial
**Descripción:** Copia autorizada de un instrumento del protocolo.
**Fundamento:** Ley del Notariado CDMX/Edomex.
**Requisitos:**
- Número de instrumento original
- Notaría y fecha
- Persona a cuyo favor se expide
- Fojas y sellos

##### 1.16 Fe de Hechos
**Descripción:** Certificación notarial de un hecho percibido directamente.
**Fundamento:** Ley del Notariado CDMX/Edomex.
**Requisitos:**
- Hecho a certificar (lugar, fecha, hora)
- Personas presentes
- Documentos o elementos relacionados

##### 1.17 Fe de Erratas
**Descripción:** Corrección de errores materiales en instrumento anterior.
**Fundamento:** Ley del Notariado CDMX.
**Requisitos:**
- Instrumento que se corrige
- Texto erróneo y correcto
- Causa del error

##### 1.18 Protesto Notarial
**Descripción:** Constancia de falta de pago/aceptación de título de crédito.
**Fundamento:** LGTOC Arts. 140–149.
**Requisitos:**
- Tipo de título (letra, pagaré, cheque)
- Datos del título: librador/aceptante, beneficiario, monto, vencimiento
- Lugar de presentación y resultado
- Fecha y hora de la diligencia

##### 1.19 Acta de Protesto
**Descripción:** Documento notarial que formaliza el protesto.
**Fundamento:** LGTOC Arts. 140–149.
**Requisitos:** Mismos que protesto. Acta detallada de la diligencia.

##### 1.20 Certificación Notarial
**Descripción:** Certificación de autenticidad de copia, firma o traducción.
**Fundamento:** Ley del Notariado CDMX/Edomex.
**Requisitos:**
- Tipo de certificación
- Documento o hecho objeto
- Personas involucradas

##### 1.21 Inventario Notarial
**Descripción:** Relación detallada de bienes (sucesorios, conyugales, societarios).
**Fundamento:** CC DF Arts. 1702–1718.
**Requisitos:**
- Causa del inventario
- Descripción de cada bien
- Valor asignado
- Pasivos a deducir

##### 1.22 Aviso Notarial
**Descripción:** Comunicación formal del notario a terceros.
**Fundamento:** Ley del Notariado CDMX; LGSM.
**Requisitos:**
- Tipo de aviso (fusión, protocolización, etc.)
- Destinatario y objeto
- Acto al que se refiere

##### 1.23 Copia Certificada Electrónica (Notario)
**Descripción:** Versión digital con firma electrónica del notario.
**Fundamento:** Ley del Notariado Edomex; Ley de Firma Electrónica Avanzada.
**Requisitos:**
- Número de instrumento
- Datos del solicitante
- Propósito

---

#### 2. DOCUMENTOS DEL REGISTRO PÚBLICO DE LA PROPIEDAD (RPP)

---

##### 2.1 Solicitud de Inscripción en el RPP
**Descripción:** Solicitud de inscripción de un acto jurídico.
**Fundamento:** CC DF Arts. 3005–3056.
**Requisitos:**
- Instrumento o resolución a inscribir
- Solicitante y carácter
- Inmueble (folio real, clave catastral)
- Tipo de acto (compraventa, hipoteca, cancelación)

##### 2.2 Certificado de Libertad de Gravámenes
**Descripción:** Certifica que un inmueble no tiene gravámenes vigentes.
**Fundamento:** CC DF Art. 3017.
**Requisitos:**
- Folio real
- Propietario registral
- Período (normalmente 20 años)
- Propósito

##### 2.3 Certificado de Gravámenes
**Descripción:** Certifica los gravámenes que pesan sobre un inmueble.
**Fundamento:** CC DF Art. 3017.
**Requisitos:**
- Folio real
- Propietario

##### 2.4 Certificado de No Inscripción de Inmueble
**Descripción:** Certifica que un inmueble no está inscrito en el RPP.
**Requisitos:**
- Ubicación, superficie, colindancias
- Solicitante

##### 2.5 Aviso Preventivo al RPP (Estado de México)
**Descripción:** Reserva provisional del folio real durante la tramitación de la escritura.
**Fundamento:** Ley Registral Edomex.
**Requisitos:**
- Folio real
- Adquirente y enajenante
- Tipo de acto
- Notaría autorizante

##### 2.6 Instrumento de Inmatriculación
**Descripción:** Primera inscripción de un inmueble en el RPP.
**Fundamento:** CC Edomex.
**Requisitos:**
- Descripción técnica (plano, superficie, linderos)
- Documentos que acreditan propiedad
- Certificado de no inscripción
- Dictamen técnico (si se requiere)

##### 2.7 Resolución de Inmatriculación (Estado de México)
**Descripción:** Resolución que declara procedente la inmatriculación.
**Fundamento:** Ley Registral Edomex.
**Requisitos:**
- Datos del procedimiento
- Inmueble a inmatricular
- Resultado de verificación catastral

##### 2.8 Certificación de Asientos Registrales
**Descripción:** Certifica el contenido de asientos del folio real.
**Fundamento:** CC DF/Edomex; Ley Registral.
**Requisitos:**
- Folio real
- Asientos a certificar
- Solicitante y propósito

##### 2.9 Cancelación de Asiento Registral
**Descripción:** Extinción total o parcial de una inscripción.
**Fundamento:** CC DF Arts. 3042–3045.
**Requisitos:**
- Folio real y asiento a cancelar
- Causa (pago, resolución judicial, prescripción)
- Documento que acredita la causa

##### 2.10 Anotación de Promesa de Contrato en el RPP
**Descripción:** Inscripción provisional de un contrato de promesa.
**Fundamento:** CC DF Arts. 2243–2247.
**Requisitos:**
- Contrato de promesa (fecha, partes, inmueble, precio)
- Folio real
- Vigencia de la anotación

##### 2.11 Anotación de Providencia Precautoria en el RPP
**Descripción:** Publicidad registral de embargo o providencia precautoria.
**Fundamento:** CC DF Arts. 3042–3056; CNPCF.
**Requisitos:**
- Resolución judicial
- Juzgado, expediente y partes
- Folio real
- Monto del crédito cautelado

##### 2.12 Cédula Hipotecaria (Estado de México)
**Descripción:** Instrumento procesal para ejecución de hipotecas en Edomex.
**Fundamento:** CPC Edomex.
**Requisitos:**
- Escritura de hipoteca (número, notaría, fecha, inscripción)
- Monto del crédito vencido y accesorios
- Folio real
- Deudor y acreedor

---

#### 3. TESTAMENTOS

---

##### 3.1 Testamento Público Abierto
**Descripción:** Testamento ante notario con testigos y lectura pública.
**Fundamento:** CC DF Arts. 1511–1541.
**Requisitos:**
- Nombre, estado civil, CURP del testador
- Declaración de plena capacidad
- Inventario de bienes
- Herederos y relación con el testador
- Legados (si los hay)
- Albacea
- Sustitución de herederos
- Cláusulas especiales (dispensa de colación, desheredamiento)
- Testigos instrumentales

##### 3.2 Testamento Público Simplificado (Estado de México)
**Descripción:** Testamento ante notario sin testigos instrumentales.
**Fundamento:** CC Edomex.
**Requisitos:** Mismos que 3.1, sin testigos.

##### 3.3 Testamento Ológrafo
**Descripción:** Testamento escrito de puño y letra por el testador.
**Fundamento:** CC DF Arts. 1550–1556.
**Requisitos:**
- Nombre y datos del testador
- Fecha de redacción (año, mes, día en letra)
- Contenido íntegro escrito a mano y firmado
- Debe depositarse ante notario o juzgado antes del fallecimiento

##### 3.4 Testamento Cerrado
**Descripción:** Testamento en sobre cerrado, secreto para el notario.
**Fundamento:** CC DF Arts. 1542–1549.
**Requisitos:**
- Sobre cerrado con el documento firmado
- Declaración del testador
- Testigos instrumentales

##### 3.5 Testamento Militar
**Descripción:** Otorgado en campaña militar ante comandante u oficial.
**Fundamento:** CC DF Arts. 1557–1567.
**Requisitos:**
- Circunstancia de campaña
- Funcionario autorizante
- Disposiciones y testigos

##### 3.6 Testamento Marítimo
**Descripción:** Otorgado a bordo de buque ante capitán.
**Fundamento:** CC DF Arts. 1568–1575.
**Requisitos:**
- Viaje marítimo
- Capitán del buque
- Disposiciones y testigos

##### 3.7 Testamento de Ciego
**Descripción:** Testamento para persona con discapacidad visual, se requiere lectura en voz alta.
**Fundamento:** CC DF Arts. 1536, 1549.
**Requisitos:**
- Mismos que testamento público abierto
- Lectura en voz alta del texto
- Testigos instrumentales

##### 3.8 Testamento de Sordo
**Descripción:** Testamento para persona con discapacidad auditiva.
**Fundamento:** CC DF Arts. 1536, 1549.
**Requisitos:**
- Mismos que testamento público abierto
- Redacción por escrito de la voluntad
- Testigos instrumentales

##### 3.9 Testamento en Lugar Incomunicado
**Descripción:** Otorgado en lugar incomunicado por epidemia u otra causa.
**Fundamento:** CC DF Arts. 1576–1583.
**Requisitos:**
- Causa de incomunicación
- Autoridad que autoriza
- Disposiciones y testigos

##### 3.10 Codicilo
**Descripción:** Disposición de última voluntad accesoria al testamento, con formalidades reducidas.
**Fundamento:** CC DF Arts. 1557–1559.
**Requisitos:**
- Testador
- Disposiciones específicas (legados, mandas, reconocimiento de hijos)
- Fecha y firma
- Testigos

---

#### 4. PODERES Y MANDATOS

---

##### 4.1 Poder Notarial (General)
**Descripción:** Instrumento que confiere facultades a un apoderado.
**Fundamento:** CC DF Arts. 2553–2583.
**Requisitos:**
- Poderdante y apoderado (nombre, RFC, CURP, domicilio)
- Tipo de poder (dominio, administración, pleitos, especial)
- Facultades expresas
- Sustitución (si se permite)
- Límites y vigencia

##### 4.2 Poder General para Actos de Dominio
**Descripción:** Faculta para disponer de bienes (vender, hipotecar, donar).
**Fundamento:** CC DF Art. 2554.
**Requisitos:**
- Datos de poderdante y apoderado
- Cláusula de actos de dominio
- Limitaciones si aplican

##### 4.3 Poder General para Actos de Administración
**Descripción:** Faculta para gestión ordinaria de bienes.
**Fundamento:** CC DF Art. 2554.
**Requisitos:**
- Datos de poderdante y apoderado
- Cláusula de administración

##### 4.4 Poder General para Pleitos y Cobranzas
**Descripción:** Faculta para representar en juicios y cobrar créditos.
**Fundamento:** CC DF Art. 2554; CNPCF Art. 47.
**Requisitos:**
- Datos de poderdante y apoderado (cédula profesional de abogado)
- Cláusula de pleitos y cobranzas
- Facultades especiales (desistir, transigir, comprometer en árbitros, recusar)

##### 4.5 Poder Especial
**Descripción:** Poder para uno o varios actos determinados.
**Fundamento:** CC DF Arts. 2553, 2560.
**Requisitos:**
- Acto específico autorizado
- Descripción precisa
- Condiciones o límites

##### 4.6 Carta Poder ante Dos Testigos
**Descripción:** Poder simple sin formalidad notarial.
**Fundamento:** CC DF Art. 2555.
**Requisitos:**
- Poderdante y apoderado
- Acto autorizado
- Dos testigos (nombre, domicilio, firma)

##### 4.7 Mandato General
**Descripción:** Contrato de mandato con facultades generales.
**Fundamento:** CC DF Arts. 2546–2583.
**Requisitos:**
- Mandante y mandatario
- Facultades generales
- Plazo y condiciones

##### 4.8 Mandato Especial
**Descripción:** Mandato para actos específicos determinados.
**Fundamento:** CC DF Arts. 2546–2583.
**Requisitos:**
- Actos específicos
- Instrucciones del mandante

##### 4.9 Mandato Especial para Actos ante el Registro Civil
**Descripción:** Mandato para trámites específicos ante el Registro Civil.
**Requisitos:**
- Trámite específico (registro de nacimiento, matrimonio, etc.)
- Datos del mandante y mandatario
- Documentos de identidad

---

#### 5. ACTAS DEL REGISTRO CIVIL

---

##### 5.1 Acta de Nacimiento
**Descripción:** Documento que acredita nacimiento y filiación.
**Fundamento:** CC DF Arts. 55–77.
**Requisitos:**
- Nombre del registrado
- Fecha, hora y lugar de nacimiento
- Nombre, edad, CURP del padre y madre
- Declarantes (si son distintos)
- Testigos (si se requieren)
- Oficial del Registro Civil

##### 5.2 Acta de Nacimiento Primigenia
**Descripción:** Primer registro cuando nunca se inscribió al individuo.
**Fundamento:** CC DF Arts. 134–140.
**Requisitos:**
- Pruebas supletorias (constancia hospitalaria, testigos, resolución judicial)
- Datos del individuo
- Imposibilidad de registro oportuno

##### 5.3 Acta de Nacimiento de Expósito
**Descripción:** Registro de persona de padres desconocidos.
**Requisitos:**
- Datos del expósito
- Lugar y fecha de recogida
- Autoridad o institución que lo presenta

##### 5.4 Acta de Nacimiento de Hijo Fuera del Matrimonio
**Descripción:** Registro de hijo nacido fuera de matrimonio, con reconocimiento.
**Requisitos:**
- Datos del hijo
- Datos del padre/madre reconociente
- Acta de reconocimiento (si aplica)

##### 5.5 Acta de Reconocimiento
**Descripción:** Reconocimiento de hijo por el padre o ambos.
**Fundamento:** CC DF Arts. 360–369.
**Requisitos:**
- Reconociente y acreditación de identidad
- Hijo reconocido (acta de nacimiento)
- Consentimiento del otro progenitor o resolución judicial

##### 5.6 Acta de Adopción
**Descripción:** Formalización de la adopción plena.
**Fundamento:** CC DF Arts. 390–410.
**Requisitos:**
- Resolución judicial de adopción
- Adoptante(s) y adoptado
- Nueva filiación

##### 5.7 Acta de Matrimonio
**Descripción:** Fe de la celebración del matrimonio.
**Fundamento:** CC DF Arts. 97–161.
**Requisitos:**
- Contrayentes (nombre, edad, estado civil, CURP)
- Padres de cada contrayente
- Testigos (mínimo 2 por cada contrayente)
- Régimen patrimonial
- Constancia de curso prenupcial (CDMX)

##### 5.8 Acta de Divorcio Administrativo (CDMX)
**Descripción:** Divorcio ante Oficial del Registro Civil (sin hijos menores, bienes liquidados).
**Fundamento:** CC DF Art. 272.
**Requisitos:**
- Cónyuges (nombre, CURP)
- Acta de matrimonio
- Convenio de bienes
- Declaración de no tener hijos menores o incapaces

##### 5.9 Acta de Defunción
**Descripción:** Fe del fallecimiento de una persona.
**Fundamento:** CC DF Arts. 117–135.
**Requisitos:**
- Nombre, CURP, domicilio del fallecido
- Fecha, hora y lugar del deceso
- Causa de muerte (certificado médico)
- Declarante
- Médico certificante

##### 5.10 Constancia de Inexistencia de Registro
**Descripción:** Certifica que no existe acta en el Registro Civil.
**Requisitos:**
- Tipo de acta buscada
- Datos del interesado
- Período de búsqueda

##### 5.11 Constancia de Alumbramiento (Estado de México)
**Descripción:** Certifica nacimiento con base en constancia médica.
**Fundamento:** CC Edomex.
**Requisitos:**
- Constancia médica de alumbramiento
- Datos del recién nacido y padres

##### 5.12 Constancia de Origen (Estado de México)
**Descripción:** Certifica origen o procedencia de una persona.
**Requisitos:**
- Datos del individuo
- Municipio de origen
- Propósito

##### 5.13 Certificado de Defunción
**Descripción:** Documento médico-legal que certifica la muerte.
**Fundamento:** Ley General de Salud.
**Requisitos:**
- Nombre del fallecido
- Fecha, hora y lugar
- Causa directa e indirecta
- Médico certificante

##### 5.14 Certificado de Deudor Alimentario (REDAM)
**Descripción:** Certifica si una persona está inscrita en el REDAM.
**Fundamento:** Ley del Registro de Deudores Alimentarios Morosos del DF.
**Requisitos:**
- Nombre y CURP del solicitante
- Propósito (trámite notarial, matrimonial, laboral)

##### 5.15 Constancia de Curso Prenupcial (CDMX)
**Descripción:** Acredita asistencia al curso prenupcial.
**Fundamento:** CC DF Arts. 98–100.
**Requisitos:**
- Nombre y CURP de los contrayentes
- Fecha y asistencias

##### 5.16 Acta de Nacimiento por Identidad de Género (Estado de México)
**Descripción:** Acta de reconocimiento de identidad de género autopercibida.
**Fundamento:** CC Edomex.
**Requisitos:**
- Nombre anterior y nombre solicitado
- CURP y acta original
- Resolución o dictamen de identidad de género

---

### Lectura de documentos
- Extraer texto de PDF o Word
- Identificar: partes, bienes, datos registrales (folio real)
- Verificar antecedentes registrales
- Identificar régimen patrimonial y estado civil de comparecientes


## 6. Reglas adicionales

- En compraventa: verificar libertad de gravámenes, estado fiscal, ISR e ISAI.
- En poderes para pleitos: listar facultades especiales (desistir, transigir, comprometer en árbitros, recusar — CC DF Art. 2587).
- En testamentos: no incluir disposiciones que impliquen renuncia a alimentos (nulas de pleno derecho).
- En inmatriculaciones: obtener certificado de no inscripción antes de iniciar.
- Testamento ológrafo: debe estar íntegramente escrito, fechado y firmado de puño y letra del testador.


# Skill: Redactor de Documentos — Derecho Fiscal y Tributario
**Fase 4 | 64 tipos de documentos**
Fuentes: Código Fiscal de la Federación (CFF), Ley del ISR (LISR), Ley del IVA (LIVA), Ley del SAT (93_041218), Resolución Miscelánea Fiscal (RMF), Ley Federal de Procedimiento Contencioso Administrativo (LFPCA).

---

## 1. Nombre
**"Redactor de documentos fiscales y tributarios"**
(Formato forense — alineaciones, mayúsculas, tabuladores, justificación)

## 2. Objetivo
A partir de documentos adjuntos por el usuario (PDF/Word) y de instrucciones conversacionales, generar cualquier escrito, declaración, recurso o documento fiscal que cumpla con las normas de presentación:
- Encabezado alineado a la derecha (contribuyente, RFC, asunto, expediente)
- Autoridad destinataria (SAT, TFJA, etc.) + ciudad + PRESENTE, alineación derecha
- Cuerpo justificado, sangría 1.27 cm por párrafo
- Puntos petitorios enumerados (PRIMERO, SEGUNDO…) con sangría francesa
- Exportación a Word (.docx) con el formato exacto

## 3. Entradas del usuario
- **Documentos subidos** (opcional): resoluciones, créditos fiscales, declaraciones, CFDI, oficios del SAT
- **Indicación del tipo de documento**: declaración, recurso, solicitud, contrato, etc.
- **Datos específicos**: RFC y nombre del contribuyente, ejercicio/período fiscal, montos, impuestos involucrados, autoridad fiscal, hechos y fundamentos legales

### 4.3 Catálogo de documentos y requisitos

---

#### 1. DOCUMENTOS DEL CONTRIBUYENTE

---

##### 1.1 Declaración Anual
**Descripción:** Declaración del ISR del ejercicio (personas físicas en abril, morales en marzo).
**Fundamento:** CFF Arts. 31–32; LISR Arts. 9, 150.
**Requisitos:**
- RFC y nombre/denominación del contribuyente
- Ejercicio fiscal
- Ingresos acumulables por fuente
- Deducciones autorizadas
- PTU pagada (personas morales)
- Pagos provisionales acreditables
- Impuesto retenido
- ISR a cargo o a favor

##### 1.2 Declaración Provisional (Pagos Provisionales)
**Descripción:** Pago mensual/bimestral a cuenta del ISR anual.
**Fundamento:** CFF Art. 31; LISR Arts. 14, 106, 111.
**Requisitos:**
- RFC y período (mes/bimestre)
- Ingresos acumulados del período
- Coeficiente de utilidad (PM) o base (PF)
- Pagos provisionales anteriores acreditados
- ISR provisional a pagar

##### 1.3 Declaración Informativa
**Descripción:** Información al SAT sin generar pago (DIOT, retenciones, partes relacionadas, etc.).
**Fundamento:** CFF Art. 31-A; LISR Arts. 76, 86, 110.
**Requisitos:**
- Tipo de declaración informativa
- Período
- Datos de terceros (RFC, monto de operaciones)

##### 1.4 Declaración Informativa País por País
**Descripción:** Reporte de grupos multinacionales sobre ingresos y actividades por país.
**Fundamento:** LISR Art. 76-A; CFF Art. 32-H.
**Requisitos:**
- Grupo multinacional y entidad reportante
- Ingresos, utilidades, impuestos, empleados por país
- Entidades constitutivas por jurisdicción

##### 1.5 Declaración Informativa de Situación Fiscal (DISIF)
**Descripción:** Reporte de grandes contribuyentes sobre situación fiscal general.
**Fundamento:** CFF Art. 32-H.
**Requisitos:**
- Información financiera del ejercicio
- Datos del auditor externo (si aplica)
- Resumen de obligaciones fiscales

##### 1.6 Esquema Reportable (Declaración de Revelación)
**Descripción:** Revelación de esquemas de planeación fiscal agresiva.
**Fundamento:** CFF Arts. 197–202.
**Requisitos:**
- Descripción del esquema
- Beneficio fiscal esperado
- Contribuyentes involucrados
- Número de identificación del esquema (si está asignado)

##### 1.7 CFDI (Factura Electrónica / Recibo de Honorarios / Recibo de Nómina)
**Descripción:** Comprobante Fiscal Digital por Internet que acredita ingresos, egresos o traslados.
**Fundamento:** CFF Arts. 29–29-A.
**Requisitos:**
- RFC del emisor y receptor
- Clave de producto/servicio (SAT)
- Cantidad y precio unitario
- Descuentos (si aplican)
- Tasa de IVA e impuesto
- Forma y método de pago
- Uso del CFDI (receptor)

##### 1.8 Nota de Crédito (CFDI de Egreso)
**Descripción:** CFDI que reduce o cancela una factura emitida.
**Fundamento:** CFF Art. 29-A Fr. VII-b.
**Requisitos:**
- Folio fiscal del CFDI original
- Motivo (devolución, descuento, bonificación)
- Monto reducido e IVA correspondiente

##### 1.9 Comprobante Fiscal
**Descripción:** Documento que acredita ingresos, egresos o retenciones.
**Fundamento:** CFF Arts. 29, 29-A.
**Requisitos:** RFC, monto, impuestos trasladados, fecha, sello digital.

##### 1.10 Aviso de Inscripción al RFC
**Descripción:** Alta ante el RFC para personas físicas o morales.
**Fundamento:** CFF Arts. 27, 27-A.
**Requisitos:**
- Tipo de contribuyente (física o moral)
- CURP (PF) o acta constitutiva (PM)
- Actividades económicas
- Domicilio fiscal

##### 1.11 Aviso de Actualización de Datos / Cancelación al RFC
**Descripción:** Modificación o baja del RFC.
**Fundamento:** CFF Art. 27 Fr. III y V.
**Requisitos:**
- RFC a actualizar/cancelar
- Motivo
- Documentos de soporte

##### 1.12 Aviso de Compensación
**Descripción:** Aviso de compensación de saldos a favor contra adeudos.
**Fundamento:** CFF Art. 23.
**Requisitos:**
- RFC
- Impuesto con saldo a favor (monto y período)
- Adeudo contra el que se compensa

##### 1.13 Certificado de Sello Digital (CSD)
**Descripción:** Certificado para emitir CFDI con sello digital.
**Fundamento:** CFF Art. 29.
**Requisitos:**
- RFC del contribuyente
- Solicitud de renovación o trámite inicial
- e.firma vigente

##### 1.14 Certificado de Firma Electrónica Avanzada (e.firma)
**Descripción:** Certificado de firma electrónica para trámites fiscales.
**Fundamento:** CFF Art. 17-D.
**Requisitos:**
- RFC y CURP
- Identificación oficial
- Medios de contacto

##### 1.15 Cédula de Identificación Fiscal
**Descripción:** Documento del SAT con datos de identificación del contribuyente.
**Requisitos:**
- RFC
- Nombre/denominación
- Domicilio fiscal

##### 1.16 Estado de Cuenta / Balance General / Estado de Resultados / Balanza de Comprobación
**Descripción:** Estados financieros del contribuyente para fines fiscales.
**Requisitos:**
- Período
- Saldos y movimientos
- Cuentas contables
- Firma del contador

##### 1.17 Solicitud de Devolución
**Descripción:** Solicitud de devolución de saldos a favor.
**Fundamento:** CFF Art. 22.
**Requisitos:**
- RFC y nombre
- Impuesto, ejercicio/período
- Monto del saldo a favor y origen
- Cuenta bancaria

##### 1.18 Solicitud de Compensación
**Descripción:** Compensación de saldos a favor contra adeudos.
**Fundamento:** CFF Art. 23.
**Requisitos:**
- RFC
- Impuesto con saldo a favor y contra el que se compensa

##### 1.19 Solicitud de Acuerdo Conclusivo
**Descripción:** Solicitud ante PRODECON para acuerdo con autoridad durante facultades de comprobación.
**Fundamento:** CFF Arts. 69-C–69-H.
**Requisitos:**
- Datos del contribuyente
- Autoridad revisora
- Hechos u omisiones
- Propuesta de acuerdo

##### 1.20 Escrito de Aclaración Fiscal
**Descripción:** Aclaración de inconsistencias o errores en declaraciones o registros del SAT.
**Fundamento:** CFF Art. 33-A; RMF.
**Requisitos:**
- Inconsistencia a aclarar
- Declaraciones o CFDI involucrados
- Documentos de soporte

##### 1.21 Acuse de Recibo Electrónico (con Sello Digital)
**Descripción:** Acuse de recepción de declaraciones o trámites fiscales.
**Requisitos:**
- Folio del acuse
- Fecha y hora de presentación
- Sello digital
- Datos del contribuyente

##### 1.22 Opinión del Cumplimiento de Obligaciones Fiscales
**Descripción:** Certificación del SAT sobre cumplimiento de obligaciones.
**Fundamento:** CFF Art. 32-D; RMF.
**Requisitos:**
- RFC del contribuyente
- Propósito

##### 1.23 Certificado de Número de Identificación de Esquema Reportable
**Descripción:** Número asignado por el SAT a un esquema reportable.
**Fundamento:** CFF Arts. 197–202.
**Requisitos:**
- Descripción del esquema
- Beneficio fiscal
- Contribuyente que lo implementa

---

#### 2. ACTOS DE AUTORIDAD FISCAL (SAT / AUTORIDADES)

---

##### 2.1 Orden de Visita Domiciliaria
**Descripción:** Orden para revisar contabilidad en el domicilio fiscal.
**Fundamento:** CFF Arts. 42 Fr. III, 43–46.
**Requisitos:**
- RFC y nombre del contribuyente
- Autoridad emisora
- Ejercicios/períodos a revisar
- Impuestos objeto de la visita
- Visitador(es) designados

##### 2.2 Acta de Inicio de Visita
**Descripción:** Acta que inicia la visita domiciliaria.
**Fundamento:** CFF Arts. 44–46.
**Requisitos:**
- Fecha, hora y lugar
- Documentación sellada
- Hechos al inicio
- Firmas

##### 2.3 Acta Parcial
**Descripción:** Acta de resultados parciales durante la visita.
**Fundamento:** CFF Arts. 44–46.
**Requisitos:**
- Hechos observados parcialmente
- Documentación revisada
- Hallazgos preliminares

##### 2.4 Acta Final de Visita
**Descripción:** Acta que concluye la visita domiciliaria.
**Fundamento:** CFF Arts. 44–46.
**Requisitos:**
- Hechos y omisiones detectados
- Documentación revisada
- Plazo para desvirtuar

##### 2.5 Oficio de Observaciones
**Descripción:** Comunicación de irregularidades con plazo para desvirtuar.
**Fundamento:** CFF Art. 48 Fr. IV; Art. 46-A.
**Requisitos:**
- Número de oficio y expediente
- Irregularidades detectadas
- Crédito fiscal preliminar estimado
- Plazo (20 + 10 días prorrogables)

##### 2.6 Oficio de Discrepancias
**Descripción:** Comunicación de discrepancias fiscales detectadas.
**Fundamento:** CFF Art. 48.
**Requisitos:**
- Discrepancias
- Montos estimados
- Plazo para aclarar

##### 2.7 Resolución de Crédito Fiscal / Resolución de Determinación
**Descripción:** Determinación líquida del crédito fiscal a cargo del contribuyente.
**Fundamento:** CFF Arts. 16, 55–65.
**Requisitos:**
- RFC y nombre
- Impuestos, ejercicios, montos (impuesto, recargos, multas, actualización)
- Fundamento
- Plazo para pagar o impugnar (30 días)

##### 2.8 Resolución de Sanción
**Descripción:** Imposición de multa o sanción fiscal.
**Fundamento:** CFF Arts. 70–84.
**Requisitos:**
- Contribuyente sancionado
- Infracción cometida
- Fundamento y monto de la sanción

##### 2.9 Resolución Provisional (Acuerdo Conclusivo)
**Descripción:** Resolución de PRODECON en el procedimiento de acuerdo conclusivo.
**Fundamento:** CFF Arts. 69-C–69-H.
**Requisitos:**
- Hechos u omisiones
- Términos del acuerdo
- Reducción de multas

##### 2.10 Acuerdo Conclusivo
**Descripción:** Acuerdo entre contribuyente y autoridad con mediación de PRODECON.
**Fundamento:** CFF Arts. 69-C–69-H.
**Requisitos:**
- Hechos materia del acuerdo
- Monto a pagar
- Beneficios
- Firmas

##### 2.11 Resolución Miscelánea Fiscal / Reglas de Carácter General
**Descripción:** Disposiciones del SAT para facilitar el cumplimiento fiscal.
**Fundamento:** CFF Art. 33 Fr. I inciso g).
**Requisitos:**
- Número de regla y RMF aplicable
- Tema o facilidad
- RFC del contribuyente que la invoca

##### 2.12 Lineamientos / Circulares / Criterios Normativos
**Descripción:** Disposiciones interpretativas o administrativas del SAT.
**Requisitos:**
- Número y fecha
- Tema
- Fundamento

##### 2.13 Requerimiento de Información
**Descripción:** Solicitud de información o documentación al contribuyente.
**Fundamento:** CFF Arts. 40, 41.
**Requisitos:**
- Datos del contribuyente
- Información solicitada
- Plazo de cumplimiento

##### 2.14 Requerimiento de Pago
**Descripción:** Exigencia de pago de un crédito fiscal.
**Fundamento:** CFF Art. 65.
**Requisitos:**
- Crédito fiscal
- Monto actualizado
- Plazo

##### 2.15 Mandamiento de Ejecución
**Descripción:** Inicio del Procedimiento Administrativo de Ejecución (PAE).
**Fundamento:** CFF Arts. 145–196.
**Requisitos:**
- RFC y nombre del deudor
- Monto del crédito actualizado
- Notificación previa

##### 2.16 Auto de Mandamiento en Forma (Ejecución Fiscal)
**Descripción:** Auto formal del PAE con designación de depositario.
**Fundamento:** CFF Arts. 145–146.
**Requisitos:**
- Crédito fiscal
- Bienes a embargar
- Depositario

##### 2.17 Acta de Adjudicación (PAE)
**Descripción:** Acta de adjudicación de bienes rematados en el PAE.
**Fundamento:** CFF Arts. 173–185.
**Requisitos:**
- Bienes adjudicados
- Adjudicatario
- Precio y constancia de pago

##### 2.18 Convocatoria de Remate (PAE)
**Descripción:** Convocatoria a postores para remate de bienes.
**Fundamento:** CFF Arts. 173–185.
**Requisitos:**
- Bienes a rematar
- Valor base
- Fecha, hora y lugar
- Requisitos para postores

##### 2.19 Avalúo / Avalúo Pericial (PAE)
**Descripción:** Determinación del valor de bienes embargados en el PAE.
**Requisitos:**
- Identificación del bien
- Valor del avalúo
- Perito valuador

##### 2.20 Acta de Notificación Fiscal
**Descripción:** Acta que formaliza la notificación de actos fiscales.
**Requisitos:**
- Acto notificado
- Notificado
- Fecha, hora y lugar
- Forma de notificación

##### 2.21 Notificación por Estrados / Edictos
**Descripción:** Notificación mediante publicación oficial.
**Fundamento:** CFF Arts. 134–137.
**Requisitos:**
- Acto a notificar
- Contribuyente (si es conocido)
- Publicación oficial

##### 2.22 Billete de Depósito / Póliza de Fianza (Garantía Fiscal)
**Descripción:** Documentos de garantía del interés fiscal.
**Fundamento:** CFF Arts. 141–142.
**Requisitos:**
- Monto garantizado (+ recargos 12 meses)
- Tipo de garantía
- Institución emisora

##### 2.23 Certificado de Gravámenes
**Descripción:** Certificación de adeudos fiscales sobre un inmueble.
**Requisitos:**
- Inmueble (folio real)
- Solicitante

##### 2.24 Constancia de Situación Fiscal
**Descripción:** Documento del SAT que certifica la situación fiscal del contribuyente.
**Requisitos:**
- RFC
- Propósito

---

#### 3. RECURSOS EN MATERIA FISCAL

---

##### 3.1 Recurso de Revocación
**Descripción:** Medio de defensa ante la propia autoridad fiscal contra una resolución.
**Fundamento:** CFF Arts. 116–133.
**Requisitos:**
- RFC y nombre del recurrente
- Resolución impugnada (número, fecha, autoridad)
- Agravios (razones de ilegalidad)
- Fundamento legal
- Pruebas documentales
- Garantía del interés fiscal (si se solicita suspensión)

##### 3.2 Recurso de Revocación Exclusivo de Fondo
**Descripción:** Modalidad limitada a cuestiones de interpretación de ley (sin vicios formales).
**Fundamento:** CFF Arts. 133-A–133-B.
**Requisitos:**
- Mismos que recurso ordinario
- Manifestación expresa de elegir esta modalidad
- Argumentos estrictamente de fondo

##### 3.3 Juicio Contencioso Administrativo (TFJA)
**Descripción:** Juicio ante el Tribunal Federal de Justicia Administrativa.
**Fundamento:** LFPCA Arts. 1–72; CFF Art. 14 LOTFJA.
**Requisitos:**
- RFC y datos del demandante
- Resolución impugnada (copia)
- Agravios de legalidad (nulidad absoluta o relativa)
- Fundamento legal
- Pruebas documentales y periciales (si aplican)
- Solicitud de suspensión

---

### Lectura de documentos
- Extraer texto de PDF o Word
- Identificar: RFC, montos, impuestos, períodos, autoridades
- Identificar resoluciones impugnadas, créditos fiscales, garantías
- Verificar plazos legales aplicables


## 6. Reglas adicionales

- Recurso de revocación: plazo 30 días hábiles (CFF Art. 121).
- Juicio contencioso: 30 días hábiles (ordinario) o 15 días (sumario) desde notificación (LFPCA Art. 13).
- Suspensión del PAE: garantía debe cubrir crédito + recargos proyectados 12 meses (CFF Art. 144).
- Acuerdo conclusivo: primera solicitud = 100 % reducción de multas; subsecuentes descuentos menores (CFF Art. 69-G).
- CFDI: debe emitirse al momento de la operación; omisión genera multas (CFF Arts. 81–82).


# Skill: Redactor de Documentos — Derecho Mercantil y Sociedades
**Fase 5 | 61 tipos de documentos**
Fuentes: Código de Comercio (CCom), Ley General de Sociedades Mercantiles (LGSM), Ley General de Títulos y Operaciones de Crédito (LGTOC), Ley de la CNBV, CODEX/CCom.txt.

---

## 1. Nombre
**"Redactor de documentos mercantiles y societarios"**
(Formato forense/contractual — alineaciones, mayúsculas, tabuladores, justificación)

## 2. Objetivo
A partir de documentos adjuntos por el usuario y de instrucciones conversacionales, generar cualquier título de crédito, contrato mercantil, acta societaria o documento de ejecución mercantil que cumpla con las formalidades legales y de presentación.

## 3. Entradas del usuario
- **Documentos subidos** (opcional): contratos previos, escrituras, actas, títulos de crédito
- **Indicación del tipo de documento**: pagaré, contrato, acta, título, etc.
- **Datos específicos**: partes, montos, plazos, garantías, cláusulas

### 4.3 Catálogo de documentos y requisitos

---

#### 1. TÍTULOS DE CRÉDITO (LGTOC)

---

##### 1.1 Letra de Cambio
**Descripción:** Orden incondicional de pago del girador al girado a favor del beneficiario.
**Fundamento:** LGTOC Arts. 76–116.
**Requisitos:**
- Girador, girado y beneficiario
- Monto en número y letra
- Lugar y fecha de expedición
- Fecha de vencimiento (vista, cierto tiempo vista, cierto tiempo fecha, día fijo)
- Lugar de pago
- Cláusula de intereses (opcional)
- Aval (nombre del avalista)

##### 1.2 Pagaré
**Descripción:** Promesa incondicional de pago del suscriptor al beneficiario.
**Fundamento:** LGTOC Arts. 170–174.
**Requisitos:**
- Suscriptor y beneficiario
- Monto en número y letra
- Lugar y fecha de suscripción
- Fecha de vencimiento
- Tasa de interés ordinaria y moratoria
- Lugar de pago
- Aval

##### 1.3 Cheque
**Descripción:** Orden de pago a la vista del librador a la institución de crédito.
**Fundamento:** LGTOC Arts. 175–207.
**Requisitos:**
- Librador y número de cuenta
- Institución librada
- Beneficiario (o "al portador")
- Monto en número y letra
- Lugar y fecha de expedición
- Tipo (nominativo, a la orden, al portador, cruzado, para abono en cuenta, certificado, de caja)

##### 1.4 Certificado de Depósito
**Descripción:** Acredita la propiedad de mercancías depositadas en almacén general.
**Fundamento:** LGTOC Arts. 229–251.
**Requisitos:**
- Depositante y almacén emisor
- Mercancías (descripción y valor)
- Plazo del depósito

##### 1.5 Bono de Prenda
**Descripción:** Constituye prenda sobre las mercancías depositadas.
**Fundamento:** LGTOC Arts. 229–251.
**Requisitos:**
- Depositante y almacén
- Mercancías
- Endoso del bono si se da en garantía

##### 1.6 Conocimiento de Embarque
**Descripción:** Acredita recepción de mercancías para transporte marítimo.
**Fundamento:** LGTOC Arts. 252–262; CCom.
**Requisitos:**
- Cargador, consignatario y transportista
- Mercancías (peso, volumen, naturaleza)
- Puerto de carga y descarga
- Flete
- Originales emitidos

##### 1.7 Carta Porte
**Descripción:** Documento que ampara el transporte terrestre de mercancías.
**Fundamento:** CCom Arts. 580–588.
**Requisitos:**
- Remitente, porteador y destinatario
- Mercancías
- Origen y destino
- Flete y plazo

##### 1.8 Carta de Crédito / Crédito Documentario
**Descripción:** Banco emisor garantiza pago al beneficiario contra presentación de documentos.
**Fundamento:** LGTOC Arts. 311–314; UCP 600.
**Requisitos:**
- Ordenante, beneficiario, banco emisor y confirmador
- Monto y moneda
- Documentos requeridos
- Vigencia
- Tipo (irrevocable, confirmado, a la vista, diferido)

##### 1.9 Acción (Título Representativo de Capital)
**Descripción:** Título que representa parte alícuota del capital social.
**Fundamento:** LGSM Arts. 111–140; LGTOC Arts. 22–25.
**Requisitos:**
- Denominación social y RFC de la sociedad
- Número y serie
- Valor nominal
- Accionista (si nominativa)
- Derechos incorporados
- Firma del administrador

##### 1.10 Obligación / Obligación Subordinada / Bono Corporativo / Bono Bancario
**Descripción:** Título representativo de crédito colectivo a cargo de la emisora.
**Fundamento:** LGSM Arts. 210–217; LGTOC Arts. 208–228.
**Requisitos:**
- Sociedad emisora
- Monto de emisión y valor nominal
- Tasa de interés y forma de pago
- Plazo y vencimiento
- Garantías
- Representante común

##### 1.11 Certificado de Depósito Bancario de Dinero (A Plazo Fijo)
**Descripción:** Título emitido por institución de crédito que acredita un depósito a plazo.
**Fundamento:** LGTOC Arts. 185–188.
**Requisitos:**
- Banco emisor y depositante
- Monto y plazo
- Tasa de interés

##### 1.12 Certificado de Participación (Ordinario / Amortizable)
**Descripción:** Título que representa derechos sobre bienes fideicomitidos.
**Fundamento:** LGTOC Arts. 228-a–228-s.
**Requisitos:**
- Fiduciaria emisora
- Bienes subyacentes
- Derechos (rendimientos o principal)
- Valor nominal y plazo

##### 1.13 Endoso
**Descripción:** Transmisión de derechos incorporados en un título.
**Fundamento:** LGTOC Arts. 26–38.
**Requisitos:**
- Tipo (propiedad, procuración, garantía, sin recurso)
- Endosante y endosatario
- Título al que corresponde

##### 1.14 Aval
**Descripción:** Garantía cambiaria solidaria.
**Fundamento:** LGTOC Arts. 109–116.
**Requisitos:**
- Avalista y persona garantizada
- Monto (total o parcial)
- Título al que corresponde

##### 1.15 Protesto / Acta de Protesto
**Descripción:** Constancia de falta de pago/aceptación de un título.
**Fundamento:** LGTOC Arts. 140–149.
**Requisitos:**
- Título protestado (tipo, monto, vencimiento, partes)
- Fecha y lugar de presentación
- Resultado (negativa de pago, no localización)
- Fedatario público que levanta el acta

---

#### 2. DOCUMENTOS SOCIETARIOS (LGSM)

---

##### 2.1 Acta Constitutiva / Escritura Constitutiva
**Descripción:** Acuerdo fundacional de la sociedad, formalizado en escritura notarial.
**Fundamento:** LGSM Arts. 5–6.
**Requisitos:**
- Denominación o razón social y tipo societario
- Socios fundadores (datos, aportaciones)
- Capital social, acciones o partes sociales
- Objeto social
- Duración y domicilio
- Órganos de administración y vigilancia
- Cláusulas estatutarias especiales

##### 2.2 Acta de la Asamblea Constitutiva
**Descripción:** Acta de la primera asamblea de socios fundadores.
**Requisitos:** Mismos que acta constitutiva. Quórum inicial. Nombramiento de primer consejo.

##### 2.3 Estatutos Sociales
**Descripción:** Norma interna de organización y funcionamiento de la sociedad.
**Fundamento:** LGSM Arts. 6, 78, 182.
**Requisitos:**
- Denominación, objeto, domicilio, duración, capital
- Acciones, asambleas, administración, vigilancia
- Disolución y liquidación
- Restricciones a transmisión de acciones

##### 2.4 Acta de Asamblea de Accionistas / Socios
**Descripción:** Registro de acuerdos en asamblea ordinaria o extraordinaria.
**Fundamento:** LGSM Arts. 178–200.
**Requisitos:**
- Tipo de asamblea (ordinaria/extraordinaria)
- Fecha, hora, lugar
- Lista de asistentes y representados (% de capital)
- Quórum y votación
- Orden del día y resoluciones
- Presidente y secretario

##### 2.5 Convocatoria a Asamblea
**Descripción:** Anuncio de celebración de asamblea.
**Fundamento:** LGSM Arts. 186–187.
**Requisitos:**
- Denominación social
- Tipo de asamblea
- Orden del día
- Fecha, hora y lugar
- Plazo mínimo de anticipación

##### 2.6 Orden del Día
**Descripción:** Lista de asuntos a tratar en la asamblea.
**Requisitos:**
- Puntos numerados y redactados con precisión

##### 2.7 Minuta de Sesión
**Descripción:** Registro de acuerdos del consejo de administración.
**Fundamento:** LGSM Arts. 142–144.
**Requisitos:**
- Sesión y número
- Consejeros presentes y ausentes
- Quórum y votos
- Acuerdos adoptados

##### 2.8 Libro de Actas
**Descripción:** Libro oficial donde se registran las actas de asambleas y sesiones.
**Fundamento:** LGSM Arts. 34, 78.
**Requisitos:**
- Actas encuadernadas
- Numeración progresiva
- Fecha y firma

##### 2.9 Libro de Registro de Socios / Acciones
**Descripción:** Libro donde se anotan los socios y sus aportaciones o los accionistas y sus títulos.
**Fundamento:** LGSM Arts. 128–129.
**Requisitos:**
- Nombre del socio/accionista
- Número de acciones/partes sociales
- Transmisiones y cancelaciones

##### 2.10 Certificado de Acciones / Certificado Provisional
**Descripción:** Título que acredita titularidad de acciones (provisional: antes del pago total).
**Fundamento:** LGSM Arts. 124–128.
**Requisitos:**
- Denominación social
- Serie y número de acción
- Titular
- Valor nominal e importe exhibido
- Firma del administrador

---

#### 3. CONTRATOS MERCANTILES (CCom / LGTOC / LGSM)

---

##### 3.1 Contrato de Compraventa Mercantil
**Descripción:** Transmisión de bien mueble con propósito de lucro.
**Fundamento:** CCom Arts. 371–382.
**Requisitos:**
- Vendedor y comprador (nombre, RFC)
- Bien (cantidad, calidad, especie)
- Precio y moneda
- Entrega (lugar y plazo)
- Forma de pago
- Garantías

##### 3.2 Contrato de Arrendamiento Mercantil
**Descripción:** Cesión de uso de bien con propósito comercial.
**Fundamento:** CCom Art. 75 Fr. I.
**Requisitos:**
- Arrendador y arrendatario
- Bien
- Renta y plazo
- Ajuste y renovación
- Depósito

##### 3.3 Contrato de Arrendamiento Financiero (Leasing)
**Descripción:** Arrendadora adquiere bien y lo arrienda con opción de compra.
**Fundamento:** LGTOC Arts. 408–418.
**Requisitos:**
- Arrendadora y arrendataria
- Bien
- Rentas, plazo y periodicidad
- Opción al vencimiento (compra, prórroga, venta)
- Valor residual
- Seguro

##### 3.4 Contrato de Factoraje Financiero
**Descripción:** Empresa de factoraje adquiere derechos de crédito del cliente.
**Fundamento:** LGTOC Arts. 419–431.
**Requisitos:**
- Cedente y factoraje
- Créditos cedidos (facturas, montos, vencimientos)
- Precio/descuento
- Tipo (con o sin recurso)
- Notificación a deudores

##### 3.5 Contrato de Franquicia
**Descripción:** Uso de marca y sistema comercial a cambio de regalías.
**Fundamento:** LPI Arts. 142–142-ter.
**Requisitos:**
- Franquiciante y franquiciatario
- Marca y sistema
- Zona y exclusividad
- Regalías
- Plazo y terminación

##### 3.6 Contrato de Transporte Mercantil
**Descripción:** Traslado de mercancías a cambio de flete.
**Fundamento:** CCom Arts. 576–604.
**Requisitos:**
- Cargador, porteador y consignatario
- Mercancías
- Origen y destino
- Plazo y flete
- Responsabilidad

##### 3.7 Contrato de Hospedaje
**Descripción:** Alojamiento temporal a cambio de precio.
**Fundamento:** CCom Arts. 604–629.
**Requisitos:**
- Hotelero y huésped
- Tipo de alojamiento y tarifa
- Período
- Responsabilidad del hotelero

##### 3.8 Contrato de Sociedad (Mercantil)
**Descripción:** Constitución de sociedad (antes de escritura pública).
**Fundamento:** LGSM Arts. 1–7.
**Requisitos:**
- Tipo de sociedad
- Aportaciones de cada socio
- Participación en pérdidas y ganancias

##### 3.9 Contrato de Asociación en Participación
**Descripción:** Asociante y asociado participan en utilidades de un negocio sin crear persona jurídica.
**Fundamento:** LGSM Arts. 252–260.
**Requisitos:**
- Asociante y asociado
- Aportaciones
- Participación en utilidades y pérdidas

##### 3.10 Contrato de Mandato Mercantil
**Descripción:** Mandatario realiza actos de comercio por cuenta del mandante.
**Fundamento:** CCom Arts. 264–289.
**Requisitos:**
- Mandante y mandatario
- Actos encomendados
- Facultades y límites
- Remuneración

##### 3.11 Contrato de Obras a Precio Alzado
**Descripción:** Contrato para ejecución de obra por precio fijo.
**Requisitos:**
- Contratista y cliente
- Descripción de la obra
- Precio alzado y forma de pago
- Plazo de ejecución
- Penalizaciones

##### 3.12 Contrato de Fideicomiso / Fideicomiso de Garantía
**Descripción:** Transmisión de bienes a fiduciario para fin lícito.
**Fundamento:** LGTOC Arts. 381–407.
**Requisitos:**
- Fideicomitente, fiduciario, fideicomisarios
- Bienes fideicomitidos
- Fin y duración
- Instrucciones irrevocables

##### 3.13 Contrato de Hipoteca Mercantil
**Descripción:** Garantía hipotecaria sobre inmueble para obligación mercantil.
**Fundamento:** CCom Arts. 302–308.
**Requisitos:**
- Deudor y acreedor
- Inmueble
- Obligación garantizada
- Inscripción en RPP

##### 3.14 Contrato de Prenda Mercantil / Prenda sin Transmisión de Posesión
**Descripción:** Garantía prendaria (con o sin entrega del bien).
**Fundamento:** CCom Arts. 334–345; LGTOC Arts. 346–380.
**Requisitos:**
- Deudor prendario y acreedor
- Bien en garantía
- Obligación garantizada
- Para prenda sin transmisión: inscripción en RUG

##### 3.15 Contrato de Crédito Refaccionario
**Descripción:** Crédito para financiar equipos o mejoras.
**Fundamento:** LGTOC Arts. 323–333.
**Requisitos:**
- Institución crediticia y acreditado
- Monto y destino
- Garantía
- Tasa, plazo y pago

##### 3.16 Contrato de Reaseguro
**Descripción:** Aseguradora cede riesgo a reasegurador.
**Fundamento:** LCS Arts. 17, 108–109.
**Requisitos:**
- Cedente y reasegurador
- Riesgos cedidos
- Prima cedida y comisión
- Tipo (proporcional, no proporcional)

##### 3.17 Contrato de Reporto
**Descripción:** Adquisición de títulos con obligación de retorno a precio superior.
**Fundamento:** LGTOC Arts. 259–278.
**Requisitos:**
- Reportador y reportado
- Títulos objeto
- Precio de adquisición y retorno
- Plazo

##### 3.18 Contrato de Descuento de Créditos en Libros
**Descripción:** Institución anticipa importe de cuentas por cobrar.
**Fundamento:** LGTOC Arts. 288–290.
**Requisitos:**
- Banco y cliente
- Cartera a descontar
- Tasa de descuento
- Responsabilidad del cliente

##### 3.19 Contrato de Apertura de Crédito Simple / en Cuenta Corriente
**Descripción:** Banco pone fondos a disposición hasta monto límite.
**Fundamento:** LGTOC Arts. 291–310.
**Requisitos:**
- Banco y acreditado
- Límite de crédito
- Tipo (simple o cuenta corriente)
- Tasa, plazo y disposición
- Garantías

##### 3.20 Contrato de Arbitraje / Cláusula Compromisoria
**Descripción:** Acuerdo para someter controversias a arbitraje.
**Fundamento:** CCom Arts. 1415–1463.
**Requisitos:**
- Partes
- Controversias sometidas
- Institución o reglas (CAM, ICC, CANACO, ad hoc)
- Árbitros y designación
- Sede, idioma y ley aplicable

---

#### 4. DOCUMENTOS DE EJECUCIÓN MERCANTIL

---

##### 4.1 Póliza de Corredor Público
**Descripción:** Instrumento que da fe de actos mercantiles, con valor de escritura pública.
**Fundamento:** Ley Federal de Correduría Pública.
**Requisitos:**
- Número de póliza y correduría
- Acto certificado
- Partes comparecientes
- Términos del acto

##### 4.2 Título de Habilitación de Corredor Público
**Descripción:** Documento que acredita la autorización del corredor público.
**Fundamento:** Ley Federal de Correduría Pública.
**Requisitos:**
- Nombre del corredor
- Número de habilitación
- Fecha de expedición

##### 4.3 Acuerdo de Arbitraje
**Descripción:** Convenio independiente de sometimiento a arbitraje.
**Requisitos:**
- Partes
- Controversias
- Institución
- Sede y ley aplicable

---

### Lectura de documentos
- Extraer texto de PDF o Word
- Identificar: partes, montos, plazos, garantías, tasas de interés
- Identificar tipo de título o contrato mercantil
- Verificar requisitos de validez del título ejecutivo


## 6. Reglas adicionales

- Pagaré: tasa moratoria debe pactarse expresamente; si no, solo interés legal (9 % anual).
- Cheque: plazo de presentación 15 días (plaza), 1 mes (fuera), 3 meses (extranjero).
- Prenda sin transmisión: falta de inscripción en RUG la hace inoponible a terceros.
- Actas de asamblea extraordinaria: deben protocolizarse ante notario e inscribirse en RPPyC.
- Arrendamiento financiero y factoraje: solo por instituciones autorizadas por la CNBV.


# Skill: Redactor de Documentos — Derecho Procesal Penal
**Fase 6 | 50 tipos de documentos**
Fuentes: Código Nacional de Procedimientos Penales (CNPP), Código Penal Federal (CPF), Código Penal para el DF/CDMX, Código Penal del Estado de México (codvig006).

---

## 1. Nombre
**"Redactor de documentos de derecho procesal penal"**
(Formato forense — alineaciones, mayúsculas, tabuladores, justificación)

## 2. Objetivo
A partir de documentos adjuntos por el usuario (PDF/Word) y de instrucciones conversacionales, generar cualquier escrito, resolución, recurso o acto procesal penal que cumpla exactamente con las normas de presentación judicial.

## 3. Entradas del usuario
- **Documentos subidos** (opcional): carpeta de investigación, resoluciones, actas, dictámenes
- **Indicación del tipo de documento**: denuncia, querella, acusación, recurso, etc.
- **Datos específicos**: imputado, víctima, delito, hechos, pruebas, agravios

### 4.3 Catálogo de documentos y requisitos

---

#### 1. ESCRITOS Y ACTOS DE PARTE / MINISTERIO PÚBLICO

---

##### 1.1 Denuncia
**Descripción:** Noticia al MP de la probable comisión de un delito.
**Fundamento:** CNPP Arts. 221–224.
**Requisitos:**
- Nombre y datos del denunciante (o anónimo)
- Hechos cronológicos y detallados
- Fecha, hora y lugar
- Posibles responsables (nombre o descripción)
- Testigos
- Documentos, fotografías o evidencia

##### 1.2 Querella
**Descripción:** Manifestación de la víctima en delitos perseguibles a petición de parte.
**Fundamento:** CNPP Arts. 225–226.
**Requisitos:**
- Nombre y datos del querellante
- Querellado (nombre o descripción)
- Hechos constitutivos del delito
- Tipo penal
- Daños y perjuicios
- Voluntad expresa de ejercer acción penal

##### 1.3 Imputación
**Descripción:** Comunicación formal del MP al imputado de los hechos que se le atribuyen.
**Fundamento:** CNPP Arts. 307–309.
**Requisitos:**
- Datos del imputado
- Hechos imputados (lugar, tiempo, modo)
- Tipo penal
- Derechos del imputado

##### 1.4 Pliego de Consignación
**Descripción:** Escrito del MP que pone a disposición del juez al imputado detenido.
**Fundamento:** CNPP Arts. 138–140.
**Requisitos:**
- Datos del imputado
- Hechos y tipo penal
- Circunstancias de la detención
- Pruebas recabadas
- Solicitud de vinculación o libertad

##### 1.5 Acusación / Escrito de Acusación
**Descripción:** Formulación de cargos por el MP al concluir la etapa intermedia.
**Fundamento:** CNPP Arts. 335–345.
**Requisitos:**
- Datos del imputado
- Hechos (lugar, tiempo, modo)
- Tipo penal y calificativas
- Grado de participación
- Pruebas para juicio oral
- Reparación del daño

##### 1.6 Solicitud de Orden de Aprehensión
**Descripción:** Solicitud del MP al Juez de Control para ordenar la detención.
**Fundamento:** CNPP Art. 141; Const. Art. 16.
**Requisitos:**
- Datos del imputado
- Hechos y tipo penal
- Datos de prueba
- Probable responsabilidad

##### 1.7 Requerimiento del Ministerio Público
**Descripción:** Solicitud al Juez de Control sobre medidas cautelares, vinculación, cateos.
**Fundamento:** CNPP Arts. 307–319.
**Requisitos:**
- Tipo de requerimiento
- Fundamento fáctico y jurídico
- Datos del imputado y carpeta

##### 1.8 Alegato de Apertura
**Descripción:** Exposición oral al inicio del juicio sobre teoría del caso.
**Fundamento:** CNPP Art. 394.
**Requisitos:**
- Teoría del caso
- Pruebas y lo que acreditan
- Resultado esperado

##### 1.9 Alegato de Clausura / Alegatos Finales
**Descripción:** Argumentación al cierre del desahogo de pruebas.
**Fundamento:** CNPP Arts. 393–401.
**Requisitos:**
- Pruebas desahogadas y su valor
- Acreditación del delito o su ausencia
- Propuesta de fallo

##### 1.10 Escrito de Coadyuvancia (Víctima u Ofendido)
**Descripción:** Intervención de la víctima para coadyuvar con el MP.
**Fundamento:** CNPP Arts. 105–115.
**Requisitos:**
- Nombre de la víctima
- Argumentos que apoyan la acusación
- Monto de reparación del daño
- Pruebas propias

---

#### 2. RESOLUCIONES JUDICIALES PENALES

---

##### 2.1 Auto de Vinculación a Proceso
**Descripción:** Resolución que vincula al imputado al proceso.
**Fundamento:** CNPP Arts. 316–319; Const. Art. 19.
**Requisitos:**
- Datos del imputado
- Hechos y tipo penal
- Datos de prueba
- Plazo de investigación complementaria

##### 2.2 Auto de No Vinculación a Proceso
**Descripción:** Libertad del imputado por no cumplir requisitos del Art. 316 CNPP.
**Fundamento:** CNPP Art. 319.
**Requisitos:**
- Datos del imputado
- Razones de no acreditación

##### 2.3 Auto de Formal Prisión / Sujeción a Proceso
**Descripción:** Resolución del sistema tradicional anterior a 2008 (transitorio).
**Requisitos:**
- Datos del inculpado
- Delito y tipo penal
- Cuerpo del delito y probable responsabilidad

##### 2.4 Auto de Libertad
**Descripción:** Resolución que decreta la libertad del imputado.
**Fundamento:** CNPP Art. 319; Const. Art. 16.
**Requisitos:**
- Datos del imputado
- Causa (falta de elementos, vencimiento de plazo, etc.)

##### 2.5 Auto de Apertura a Juicio Oral
**Descripción:** Conclusión de etapa intermedia, envía la causa a juicio oral.
**Fundamento:** CNPP Arts. 347–349.
**Requisitos:**
- Hechos y tipos penales admitidos
- Pruebas admitidas y excluidas
- Acuerdos probatorios

##### 2.6 Auto de Radicación (Segunda Instancia)
**Descripción:** Auto que radica el recurso en el tribunal de alzada.
**Requisitos:**
- Expediente
- Partes
- Recurso interpuesto

##### 2.7 Auto de Turno
**Descripción:** Asignación del asunto a un juzgado o tribunal.
**Requisitos:**
- Carpeta o causa
- Juzgado/Tribunal asignado

##### 2.8 Sentencia Condenatoria / Absolutoria / Definitiva
**Descripción:** Resolución final del Tribunal de Enjuiciamiento.
**Fundamento:** CNPP Arts. 402–416.
**Requisitos:**
- Datos del acusado
- Hechos probados y valoración
- Tipo penal y participación
- Pena (prisión, multa, reparación)
- Causa de absolución si procede

---

#### 3. ÓRDENES JUDICIALES

---

##### 3.1 Orden de Aprehensión
**Descripción:** Autorización judicial de detención.
**Fundamento:** CNPP Art. 141; Const. Art. 16.
**Requisitos:**
- Solicitud del MP
- Hechos y datos de prueba
- Tipo penal y probable responsabilidad

##### 3.2 Orden de Comparecencia
**Descripción:** Citación judicial para que el imputado se presente voluntariamente.
**Fundamento:** CNPP Art. 141.
**Requisitos:**
- Imputado y domicilio
- Fecha, hora y lugar
- Tipo penal

##### 3.3 Orden de Cateo
**Descripción:** Autorización para registro de un lugar.
**Fundamento:** CNPP Arts. 282–290; Const. Art. 16.
**Requisitos:**
- Lugar (descripción precisa)
- Personas u objetos buscados
- Delito y datos de prueba

##### 3.4 Orden de Visita Domiciliaria (Penal)
**Descripción:** Autorización para ingreso a domicilio por investigación penal.
**Fundamento:** CNPP Arts. 282–290.
**Requisitos:**
- Domicilio a visitar
- Objeto de la visita
- Fundamento

##### 3.5 Orden de Suspensión
**Descripción:** Suspensión provisional de funciones o actividades.
**Fundamento:** CNPP Arts. 155–158.
**Requisitos:**
- Persona o actividad suspendida
- Causa
- Plazo

##### 3.6 Orden de Protección
**Descripción:** Medida urgente a favor de la víctima.
**Fundamento:** CNPP Arts. 137–138; LGAMVLV.
**Requisitos:**
- Víctima e imputado
- Hechos de violencia
- Tipo de medida

##### 3.7 Orden de Descuento para Alimentos
**Descripción:** Retención de sueldo del imputado para alimentos.
**Fundamento:** CNPP Art. 138 Fr. VII.
**Requisitos:**
- Obligado y beneficiario
- Porcentaje o monto
- Patrón o empleador

---

#### 4. RECURSOS PENALES

---

##### 4.1 Recurso de Apelación (Penal)
**Descripción:** Recurso contra resoluciones apelables del Juez de Control o Tribunal.
**Fundamento:** CNPP Arts. 467–484.
**Requisitos:**
- Resolución impugnada
- Agravios (violación de derechos, incorrecta valoración)
- Fundamento legal
- Pruebas admisibles en segunda instancia

##### 4.2 Recurso de Queja (Penal)
**Descripción:** Contra actos del MP que afecten derechos de las partes.
**Fundamento:** CNPP Arts. 258–261.
**Requisitos:**
- Acto u omisión del MP
- Agravio
- Solicitud de subsanación

##### 4.3 Recurso de Revocación (Penal)
**Descripción:** Contra autos y decretos no apelables, ante el mismo órgano.
**Fundamento:** CNPP Arts. 465–466.
**Requisitos:**
- Auto impugnado
- Agravios
- Petición concreta

---

#### 5. ACTAS E INSTRUMENTOS PENALES

---

##### 5.1 Acta de Detención
**Descripción:** Registro de las circunstancias de la detención.
**Fundamento:** CNPP Arts. 132, 308.
**Requisitos:**
- Detenido y datos de identificación
- Hora, lugar y circunstancias
- Causa legal (flagrancia, caso urgente, orden judicial)
- Funcionario que detiene
- Derechos informados

##### 5.2 Acta de Retención
**Descripción:** Registro de retención para investigación.
**Fundamento:** CNPP Arts. 134–135.
**Requisitos:**
- Retenido
- Motivo
- Plazo máximo (48 horas)

##### 5.3 Acta Circunstanciada (Penal)
**Descripción:** Registro detallado de diligencias de investigación.
**Requisitos:**
- Diligencia realizada
- Funcionario actuante
- Personas intervinientes
- Hechos observados

##### 5.4 Registro de Detención
**Descripción:** Documento administrativo que registra la detención.
**Requisitos:**
- Datos del detenido
- Hora de ingreso
- Autoridad que detiene
- Derechos leídos

##### 5.5 Declaración del Imputado / Testigo / Víctima
**Descripción:** Registro de declaraciones rendidas ante el MP o juez.
**Fundamento:** CNPP Arts. 113, 131, 337–338, 364–365.
**Requisitos:**
- Declarante (nombre, calidad procesal)
- Contenido narrativo
- Admonición de decir verdad (testigos)
- Derecho a no autoincriminarse (imputado)

##### 5.6 Carpeta de Investigación
**Descripción:** Expediente del MP con registros de la investigación.
**Fundamento:** CNPP Art. 217.
**Requisitos:**
- Número de carpeta
- Denunciante/querellante
- Hechos y tipo penal
- Registros integrados

##### 5.7 Registro de Cadena de Custodia
**Descripción:** Manejo ininterrumpido de indicios y evidencias.
**Fundamento:** CNPP Arts. 227–235.
**Requisitos:**
- Indicio (descripción física, número)
- Lugar, fecha y hora de recolección
- Funcionario recolector
- Cada transferencia de custodia
- Estado en cada transferencia

---

#### 6. MECANISMOS ALTERNATIVOS (MASC) Y SALIDAS ALTERNAS

---

##### 6.1 Acuerdo Reparatorio
**Descripción:** Acuerdo imputado-víctima que extingue la acción penal.
**Fundamento:** CNPP Arts. 186–196.
**Requisitos:**
- Imputado y víctima
- Tipo penal
- Forma, monto y plazo de reparación
- Conformidad de la víctima
- Ratificación judicial

##### 6.2 Suspensión Condicional del Proceso
**Descripción:** Plan de actividades del imputado; si lo cumple, se extingue el proceso.
**Fundamento:** CNPP Arts. 191–203.
**Requisitos:**
- Imputado y tipo penal
- Plan de actividades (actividades, plazos, condiciones)
- Anuencia de la víctima (si aplica)

##### 6.3 Criterio de Oportunidad
**Descripción:** Abstención del MP de ejercer acción penal por supuesto legal.
**Fundamento:** CNPP Arts. 256–258.
**Requisitos:**
- Imputado y tipo penal
- Supuesto legal
- Reparación del daño (si se impone)

##### 6.4 Procedimiento Abreviado (Solicitud)
**Descripción:** Terminación anticipada con reducción de pena.
**Fundamento:** CNPP Arts. 201–207.
**Requisitos:**
- Imputado y causa
- Aceptación libre e informada de hechos
- Pena solicitada con beneficios
- Anuencia de la víctima sobre reparación

##### 6.5 Escrito de Coadyuvancia
*(Ver 1.10)*

---

#### 7. ÓRDENES Y TÉCNICAS DE INVESTIGACIÓN

---

##### 7.1 Solicitud de Intervención de Comunicaciones Privadas
**Descripción:** Solicitud del MP al Juez Federal para intervenir comunicaciones.
**Fundamento:** CNPP Arts. 291–296; Const. Art. 16.
**Requisitos:**
- Persona cuyas comunicaciones se intervendrán
- Delito (grave o delincuencia organizada)
- Datos de prueba
- Plazo y tipo de comunicación

##### 7.2 Orden de Decomiso
**Descripción:** Privación definitiva de bienes producto o instrumento del delito.
**Fundamento:** CNPP Arts. 229–231; CPF Art. 40.
**Requisitos:**
- Bienes a decomisar
- Vínculo con el delito
- Sentencia o resolución que lo sustenta

##### 7.3 Solicitud de Asistencia Jurídica Internacional
**Descripción:** Solicitud a autoridad extranjera para colaboración en investigación.
**Fundamento:** CNPP Arts. 583–595.
**Requisitos:**
- Autoridad requirente y requerida
- Delito investigado
- Diligencias solicitadas
- Tratado aplicable

##### 7.4 Comunicación del Fallo / Fallo (Juicio Oral)
**Descripción:** Anuncio del sentido del fallo al concluir el juicio oral.
**Fundamento:** CNPP Art. 401.
**Requisitos:**
- Acusado
- Fallo (condenatorio o absolutorio)
- Pena o libertad
- Lectura de sentencia programada

---

### Lectura de documentos
- Extraer texto de PDF o Word
- Identificar: imputado, víctima, delito, carpeta de investigación, juzgado
- Identificar etapa procesal y medidas cautelares
- Identificar datos de prueba y testigos


## 6. Reglas adicionales

- El imputado tiene derecho a no declarar; nunca redactar autoinculpación sin constancia de voluntariedad (CNPP Art. 113 Fr. II).
- Detención en flagrancia: poner a disposición del MP en menos de 48 horas (Const. Art. 16).
- Acuerdo reparatorio: solo en delitos ≤ 5 años de prisión y culposos, excepto los que causaron muerte (CNPP Art. 187).
- Procedimiento abreviado: requiere aceptación expresa, libre e informada.
- Apelación: expresión de agravios indispensable; omisión = desechamiento (CNPP Art. 471).


# Skill: Redactor de Documentos — Derecho Agrario
**Fase 7 | 46 tipos de documentos**
Fuentes: Ley Agraria (LAgra), Ley Orgánica de los Tribunales Agrarios (159.txt), Reglamento de la Ley Agraria, CODEX/LAgra.txt.

---

## 1. Nombre
**"Redactor de documentos agrarios"**
(Formato forense — alineaciones, mayúsculas, tabuladores, justificación)

## 2. Objetivo
A partir de documentos adjuntos por el usuario y de instrucciones conversacionales, generar cualquier escrito, acta, contrato o documento agrario que cumpla con las normas de presentación judicial.

## 3. Entradas del usuario
- **Documentos subidos** (opcional): certificados, actas de asamblea, planos, títulos
- **Indicación del tipo de documento**: demanda agraria, acta de asamblea, contrato, certificado
- **Datos específicos**: ejido, parcela, ejidatarios, hechos, pretensiones

### 4.3 Catálogo de documentos y requisitos

---

#### 1. JUICIO AGRARIO (ANTE TRIBUNALES UNITARIOS AGRARIOS)

---

##### 1.1 Demanda Agraria (Escrita u Oral)
**Descripción:** Escrito o narración oral que inicia el juicio agrario.
**Fundamento:** LAgra Arts. 163–200; Ley 159 Arts. 18–25.
**Requisitos:**
- Actor (ejidatario, comunero, avecindado o sujeto agrario)
- Demandado
- Ejido o comunidad y municipio
- Predio o parcela (superficie, ubicación, certificado parcelario)
- Hechos cronológicos
- Pretensiones (restitución, reconocimiento, indemnización)
- Fundamento legal
- Pruebas (planos, certificados, actas, testimoniales, periciales)

##### 1.2 Contestación de Demanda Agraria
**Descripción:** Respuesta del demandado.
**Fundamento:** LAgra Art. 170.
**Requisitos:**
- Demandado (nombre, domicilio)
- Expediente y Tribunal
- Respuesta a cada hecho
- Excepciones (prescripción, cosa juzgada, falta de acción)
- Fundamento y pruebas

##### 1.3 Ofrecimiento de Pruebas (Agrario)
**Descripción:** Ofrecimiento de pruebas ante el Tribunal.
**Fundamento:** LAgra Arts. 170–187.
**Requisitos:**
- Expediente
- Pruebas (documentales, testimoniales, periciales, inspección)
- Hecho que cada prueba acredita

##### 1.4 Alegatos (Agrario — Audiencia Única)
**Descripción:** Exposición oral al concluir el desahogo de pruebas.
**Fundamento:** LAgra Art. 185.
**Requisitos:**
- Hechos probados
- Valor probatorio
- Conclusión sobre pretensiones

##### 1.5 Solicitud de Diligencias de Aseguramiento
**Descripción:** Medida cautelar sobre predios o derechos en disputa.
**Fundamento:** LAgra Art. 166.
**Requisitos:**
- Bien o derecho a asegurar
- Riesgo a evitar
- Fundamento

##### 1.6 Escrito de Jurisdicción Voluntaria (Agraria)
**Descripción:** Solicitud de intervención judicial sin controversia.
**Requisitos:**
- Objeto de la solicitud
- Hechos que la justifican
- Documentos de soporte

##### 1.7 Recurso de Revisión (Tribunal Superior Agrario)
**Descripción:** Recurso contra sentencias de Tribunales Unitarios.
**Fundamento:** LAgra Arts. 198–200; Ley 159 Arts. 9–11.
**Requisitos:**
- Sentencia impugnada (expediente, Tribunal, fecha)
- Agravios (errores de fondo o forma)
- Fundamento
- Pruebas admisibles

##### 1.8 Sentencia Agraria
**Descripción:** Resolución definitiva del Tribunal Unitario.
**Fundamento:** LAgra Arts. 186–196.
**Requisitos:**
- Hechos probados
- Pretensiones procedentes/improcedentes
- Condena o absolución

##### 1.9 Aclaración de Sentencia Agraria
**Descripción:** Solicitud para aclarar puntos oscuros de la sentencia.
**Requisitos:**
- Sentencia a aclarar
- Puntos oscuros o contradictorios
- Lo que se solicita aclarar

##### 1.10 Resolución en Recurso de Revisión (TSA)
**Descripción:** Resolución del Tribunal Superior Agrario.
**Requisitos:**
- Recurso resuelto
- Agravios analizados
- Confirmación, revocación o modificación

##### 1.11 Auto de Ejecución de Sentencia
**Descripción:** Auto que ordena el cumplimiento de la sentencia.
**Requisitos:**
- Sentencia ejecutoriada
- Plazo de cumplimiento
- Medidas de apremio

##### 1.12 Acta de Audiencia de Ley
**Descripción:** Acta que registra la audiencia única agraria.
**Elementos:**
- Fecha, hora y lugar
- Partes asistentes
- Conciliación, pruebas, alegatos y sentencia
- Firmas

---

#### 2. PROCEDIMIENTOS INTERNOS DEL EJIDO Y LA COMUNIDAD

---

##### 2.1 Convocatoria a Asamblea Ejidal
**Descripción:** Citación a ejidatarios a asamblea general.
**Fundamento:** LAgra Arts. 23–28.
**Requisitos:**
- Ejido y municipio
- Tipo (ordinaria/extraordinaria) y quórum
- Orden del día
- Fecha, hora y lugar (1ª y 2ª convocatoria)
- Forma y plazo de notificación
- Quién convoca

##### 2.2 Acta de Asamblea Ejidal
**Descripción:** Registro de acuerdos de la asamblea. Debe inscribirse en RAN.
**Fundamento:** LAgra Arts. 22–32.
**Requisitos:**
- Ejido, tipo y fecha
- Asistentes con firmas
- Quórum
- Resoluciones con votación
- Presidente y secretario
- Fedatario RAN o notario (si aplica)

##### 2.3 Acta de Asamblea de Formalidades Especiales
**Descripción:** Para dominio pleno, delimitación,terminación del régimen ejidal, desarrollo urbano.
**Fundamento:** LAgra Arts. 23–25, 29–34, 56, 81–84.
**Requisitos:**
- Mismos que 2.2
- Quórum reforzado (2/3 partes)
- Fedatario RAN o notario
- Plano técnico

##### 2.4 Reglamento Interno del Ejido
**Descripción:** Norma interna del ejido aprobada por la asamblea.
**Fundamento:** LAgra Arts. 10–11.
**Requisitos:**
- Ejido
- Órganos de gobierno
- Derechos y obligaciones
- Uso de tierras
- Sanciones

##### 2.5 Estatuto Comunal
**Descripción:** Norma interna de la comunidad agraria.
**Requisitos:**
- Comunidad
- Órganos de gobierno
- Derechos y obligaciones de comuneros

##### 2.6 Lista de Ejidatarios / Padrón Ejidal
**Descripción:** Lista oficial de ejidatarios del núcleo agrario.
**Requisitos:**
- Nombre de cada ejidatario
- Derechos reconocidos
- Fecha de actualización

##### 2.7 Solicitud de Adopción del Dominio Pleno
**Descripción:** Solicitud del ejidatario a la asamblea para dominio pleno.
**Fundamento:** LAgra Arts. 81–83.
**Requisitos:**
- Ejidatario solicitante
- Certificado parcelario
- Consecuencias informadas
- Resolución de asamblea

##### 2.8 Solicitud de Aportación de Tierras a Sociedad
**Descripción:** Aporte de tierras ejidales como capital a sociedad mercantil o civil.
**Fundamento:** LAgra Arts. 75–79.
**Requisitos:**
- Tierras a aportar
- Sociedad receptora
- Valor y participación
- Aprobación de asamblea

##### 2.9 Programa de Delimitación y Destino (PROCEDE)
**Descripción:** Programa de delimitación, destino y asignación de tierras ejidales.
**Fundamento:** LAgra Arts. 56–60.
**Requisitos:**
- Ejido y superficie total
- Parcelas individuales
- Tierras de uso común
- Solares urbanos
- Plano general

---

#### 3. DOCUMENTOS DEL REGISTRO AGRARIO NACIONAL (RAN)

---

##### 3.1 Certificado Parcelario
**Descripción:** Acredita derechos del ejidatario sobre su parcela.
**Fundamento:** LAgra Arts. 56–68.
**Requisitos:**
- Ejidatario titular
- Ejido y municipio
- Parcela (número, superficie, colindancias)
- Plano
- Folio RAN

##### 3.2 Certificado de Derechos sobre Tierras de Uso Común
**Descripción:** Acredita derechos proporcionales sobre tierras comunes.
**Fundamento:** LAgra Art. 56.
**Requisitos:**
- Ejidatario
- Ejido
- Proporción de derechos

##### 3.3 Certificado de Derechos Ejidales (Certificado Único)
**Descripción:** Documento unificado que acredita derechos parcelarios y de uso común.
**Requisitos:**
- Ejidatario
- Parcela y derechos de uso común
- Folio RAN

##### 3.4 Título de Solar Urbano
**Descripción:** Acredita derechos del avecindado sobre su solar.
**Fundamento:** LAgra Arts. 68–69.
**Requisitos:**
- Avecindado titular
- Solar (superficie, colindancias)
- Folio RAN

##### 3.5 Solicitud de Inscripción en el RAN
**Descripción:** Solicitud de inscripción de acto jurídico agrario.
**Fundamento:** LAgra Art. 149.
**Requisitos:**
- Acto a inscribir
- Partes
- Expediente o instrumento
- Ejido y municipio

##### 3.6 Cancelación de Inscripción en el RAN
**Descripción:** Solicitud de cancelación de asiento registral.
**Requisitos:**
- Inscripción a cancelar
- Causa
- Documentos de soporte

##### 3.7 Solicitud de Constancia / Certificación al RAN
**Descripción:** Petición de certificaciones o constancias del RAN.
**Fundamento:** LAgra Art. 149.
**Requisitos:**
- Tipo de constancia
- Datos del ejido o sujeto agrario
- Propósito

---

#### 4. CONTRATOS Y ACTOS JURÍDICOS AGRARIOS

---

##### 4.1 Contrato de Aparcería Agraria
**Descripción:** Cesión temporal de parcela a cambio de parte de frutos.
**Fundamento:** LAgra Arts. 45, 79.
**Requisitos:**
- Cedente (ejidatario) y aparcero
- Parcela
- Porcentaje de frutos por parte
- Plazo y terminación
- Obligaciones

##### 4.2 Contrato de Mediería
**Descripción:** Aportación de tierra y trabajo con división de productos por mitades.
**Requisitos:**
- Ejidatario y mediero
- Parcela
- Proporción de productos

##### 4.3 Contrato de Arrendamiento de Parcela Ejidal
**Descripción:** Cesión temporal de uso a cambio de renta.
**Fundamento:** LAgra Art. 45.
**Requisitos:**
- Arrendador (ejidatario) y arrendatario
- Parcela
- Renta y periodicidad
- Plazo (máx. 30 años)
- Uso permitido

##### 4.4 Contrato de Usufructo sobre Parcelas Ejidales
**Descripción:** Derecho de usar y aprovechar la parcela temporalmente.
**Fundamento:** LAgra Art. 45.
**Requisitos:**
- Nudo propietario (ejidatario) y usufructuario
- Parcela
- Plazo
- Obligaciones de conservación

##### 4.5 Contrato de Asociación en Participación (Tierras Ejidales)
**Descripción:** Asociación del ejidatario con un tercero para explotar la parcela.
**Requisitos:**
- Ejidatario y asociado
- Aportaciones
- Participación en utilidades

##### 4.6 Contrato de Aprovechamiento de Tierras Ejidales
**Descripción:** Ejidatario permite a un tercero el aprovechamiento de su parcela.
**Requisitos:**
- Ejidatario y tercero
- Tipo de aprovechamiento
- Plazo y contraprestación

##### 4.7 Contrato de Cesión de Derechos Parcelarios
**Descripción:** Transferencia de derechos entre ejidatarios del mismo ejido.
**Fundamento:** LAgra Arts. 80, 84.
**Requisitos:**
- Cedente y cesionario (mismo ejido)
- Derechos cedidos
- Precio
- Inscripción RAN

##### 4.8 Escritura Pública de Enajenación de Parcela (Dominio Pleno)
**Descripción:** Enajenación como propiedad privada tras dominio pleno.
**Fundamento:** LAgra Art. 83.
**Requisitos:**
- Enajenante y adquirente
- Folio real RPP
- Precio y forma de pago
- ISR

---

#### 5. PROCEDIMIENTOS ESPECIALES AGRARIOS

---

##### 5.1 Expropiación de Bienes Ejidales o Comunales
**Descripción:** Privación por causa de utilidad pública con indemnización.
**Fundamento:** LAgra Arts. 93–96; Const. Art. 27.
**Requisitos:**
- Ejido afectado
- Tierras (superficie)
- Causa de utilidad pública
- Indemnización
- Decreto expropiatorio

##### 5.2 Reversión de Tierras Expropiadas
**Descripción:** Recuperación de tierras no destinadas al fin público.
**Fundamento:** LAgra Art. 97.
**Requisitos:**
- Decreto expropiatorio
- Acreditación de desvío de fin
- Solicitud de restitución

##### 5.3 Diligencias de Deslinde / Acta de Deslinde
**Descripción:** Determinación de límites de predio ejidal.
**Fundamento:** LAgra Arts. 56–57.
**Requisitos:**
- Predio a deslindar
- Colindantes
- Plano topográfico
- Peritos
- Acta de acuerdos

##### 5.4 Restitución de Tierras, Bosques y Aguas
**Descripción:** Juicio para recuperar tierras privadas ilegalmente.
**Fundamento:** LAgra Arts. 18, 48–50.
**Requisitos:**
- Núcleo agrario solicitante
- Tierras reclamadas
- Privación ilegal
- Documentos históricos

##### 5.5 Constancia de Posesión
**Descripción:** Acredita posesión material de un terreno.
**Fundamento:** LAgra Arts. 48–50.
**Requisitos:**
- Poseedor
- Predio (superficie, colindancias)
- Tiempo de posesión
- Autoridad emisora

##### 5.6 Título de Propiedad Ejidal / Concesión Agraria
**Descripción:** Reconocimiento oficial de derechos agrarios del ejido.
**Fundamento:** Const. Art. 27; LAgra Transitorios.
**Requisitos:**
- Ejido o comunidad
- Tierras reconocidas
- Resolución presidencial o dotación

---

### Lectura de documentos
- Extraer texto de PDF o Word
- Identificar: ejido, parcela, ejidatario, derechos, superficie
- Identificar número de certificado parcelario o folio RAN


## 6. Reglas adicionales

- Derechos parcelarios: solo cedibles entre ejidatarios/avecindados del mismo ejido (LAgra Art. 80).
- Contratos de uso de tierras ejidales: duración máx. 30 años (LAgra Art. 45).
- Asambleas de formalidades especiales: quórum de 1/2 + 1 en primera y 3/4 en segunda convocatoria (LAgra Art. 24).
- Dominio pleno: requiere asamblea + inscripción RAN + inscripción RPP.
- Expropiación: solo por el Ejecutivo Federal; indemnización a valor comercial.


# Skill: Redactor de Documentos Administrativos Generales
**Fase 8 | 41 tipos de documentos**
Fuentes: Constitución Política de los Estados Unidos Mexicanos (CPEUM), Ley Federal de Procedimiento Administrativo (LFPA), Ley Orgánica de la Administración Pública Federal (LOAPF), CODEX/CPEUM.txt, CCom (para actos administrativos mercantiles).

---

## 1. Nombre
**"Redactor de documentos administrativos generales"**
(Formato forense administrativo — alineaciones, mayúsculas, tabuladores, justificación)

## 2. Objetivo
A partir de documentos adjuntos por el usuario y de instrucciones conversacionales, generar cualquier acto de autoridad administrativa, permiso, licencia, concesión, comunicación administrativa o dictamen que cumpla con las formalidades legales y de presentación.

## 3. Entradas del usuario
- **Documentos subidos** (opcional): oficios previos, reglamentos, formatos oficiales, dictámenes
- **Indicación del tipo de documento**: decreto, acuerdo, oficio, permiso, constancia, dictamen, etc.
- **Datos específicos**: autoridad emisora, fundamento legal, destinatario, hechos, determinación

### 4.3 Catálogo de documentos y requisitos

---

#### 1. ACTOS DE AUTORIDAD ADMINISTRATIVA

---

##### 1.1 Decreto
**Descripción:** Disposición de carácter general o particular emitida por el Ejecutivo Federal, estatal o municipal.
**Fundamento:** CPEUM Art. 89; LOAPF.
**Requisitos:**
- Autoridad emisora (Presidente, Gobernador, Presidente Municipal)
- Considerandos (fundamento legal y motivos)
- Artículos del decreto (dispositivos)
- Transitorios (vigencia, abrogaciones)
- Lugar, fecha y firma

##### 1.2 Acuerdo (Presidencial, Secretarial, de Junta de Gobierno)
**Descripción:** Decisión formal de una autoridad administrativa sobre un asunto concreto.
**Fundamento:** LOAPF; LFPA.
**Requisitos:**
- Autoridad que lo emite
- Número de acuerdo
- Antecedentes
- Considerandos
- Acuerdo (determinación concreta)
- Fundamento legal
- Firma

##### 1.3 Resolución Administrativa
**Descripción:** Acto definitivo de autoridad que decide un procedimiento administrativo.
**Fundamento:** LFPA Arts. 3–10.
**Requisitos:**
- Autoridad resolutora
- Número de expediente
- Resultandos (hechos del procedimiento)
- Considerandos (fundamentos legales y valoración)
- Resolutivos
- Notificación y recursos
- Firma

##### 1.4 Oficio
**Descripción:** Comunicación escrita entre autoridades o de autoridad a particular.
**Requisitos:**
- Dependencia y número de oficio
- Fecha
- Destinatario (cargo y nombre)
- Asunto
- Texto del mensaje
- Fundamento (si es requerimiento o notificación)
- Firma del emisor

##### 1.5 Circular
**Descripción:** Comunicación dirigida a múltiples destinatarios para dar instrucciones o informar.
**Requisitos:**
- Dependencia emisora
- Número de circular
- Destinatarios (generales)
- Instrucción o información
- Vigencia
- Firma

##### 1.6 Lineamientos
**Descripción:** Disposiciones de carácter general para la aplicación de leyes o políticas.
**Requisitos:**
- Autoridad emisora
- Fundamento legal
- Objeto y ámbito de aplicación
- Definiciones
- Lineamientos específicos numerados
- Transitorios
- Firma

##### 1.7 Reglas de Carácter General
**Descripción:** Normas administrativas generales emitidas por autoridades administrativas.
**Requisitos:**
- Autoridad emisora
- Fundamento
- Reglas numeradas
- Anexos (si aplica)
- Transitorios

##### 1.8 Convocatoria (Licitación, Concurso, Asamblea)
**Descripción:** Llamado público a participar en un procedimiento administrativo.
**Requisitos:**
- Autoridad convocante
- Objeto de la convocatoria
- Requisitos de participación
- Fechas, lugares y plazos
- Criterios de selección
- Publicación oficial

##### 1.9 Orden del Día
**Descripción:** Lista de asuntos a tratar en una sesión o reunión.
**Requisitos:**
- Órgano colegiado
- Fecha, hora y lugar
- Puntos numerados
- Lectura y aprobación del acta anterior (si aplica)
- Asuntos generales

##### 1.10 Minuta de Sesión
**Descripción:** Registro resumido de los acuerdos de una sesión.
**Requisitos:**
- Órgano colegiado
- Fecha, hora y lugar
- Asistentes
- Acuerdos adoptados
- Firma del secretario

##### 1.11 Acuerdo de Cabildo / Bando Municipal
**Descripción:** Disposición normativa municipal aprobada por el Cabildo.
**Fundamento:** CPEUM Art. 115.
**Requisitos:**
- Municipio y Cabildo
- Considerandos
- Artículos del bando/acuerdo
- Transitorios
- Fecha y firmas

##### 1.12 Reglamento
**Descripción:** Disposición normativa general de carácter administrativo.
**Fundamento:** CPEUM Art. 89 Fr. I; LOAPF.
**Requisitos:**
- Autoridad emisora
- Fundamento legal
- Títulos, capítulos y artículos
- Transitorios
- Publicación oficial

##### 1.13 Plan de Desarrollo
**Descripción:** Instrumento de planeación estratégica de la administración pública.
**Requisitos:**
- Autoridad que lo emite
- Diagnóstico
- Ejes, objetivos y estrategias
- Metas e indicadores
- Plazo de ejecución

##### 1.14 Programa de Gobierno
**Descripción:** Programa específico de acción gubernamental.
**Requisitos:**
- Dependencia responsable
- Objetivos
- Actividades y cronograma
- Presupuesto
- Evaluación

---

#### 2. PERMISOS, LICENCIAS Y CONCESIONES

---

##### 2.1 Permiso
**Descripción:** Autorización temporal para realizar un acto específico.
**Requisitos:**
- Autoridad que otorga
- Solicitante (nombre, RFC)
- Acto autorizado (descripción precisa)
- Plazo de vigencia
- Condiciones
- Fundamento legal
- Fecha y firma

##### 2.2 Licencia
**Descripción:** Autorización para ejercer una actividad regulada.
**Requisitos:**
- Autoridad emisora
- Titular (nombre, RFC, datos de identificación)
- Tipo de licencia
- Vigencia
- Requisitos cumplidos
- Fundamento

##### 2.3 Autorización
**Descripción:** Acto por el que la autoridad permite la realización de un acto previo cumplimiento de requisitos.
**Requisitos:**
- Autoridad
- Solicitante
- Acto autorizado
- Condiciones
- Plazo
- Fundamento

##### 2.4 Concesión
**Descripción:** Acto por el que el Estado otorga a un particular la explotación de un bien o servicio público.
**Fundamento:** CPEUM Arts. 25, 27, 28.
**Requisitos:**
- Concedente y concesionario
- Bien o servicio
- Plazo (máx. 30 años, prorrogable)
- Derechos y obligaciones
- Contraprestación
- Causas de revocación

##### 2.5 Título de Concesión
**Descripción:** Documento formal que acredita la concesión otorgada.
**Requisitos:**
- Datos de la concesión
- Concesionario
- Bien o servicio
- Plazo y condiciones
- Fecha y firma

##### 2.6 Registro
**Descripción:** Inscripción formal en un registro administrativo.
**Requisitos:**
- Autoridad registral
- Persona o bien registrado
- Número de registro
- Datos del registro
- Vigencia

##### 2.7 Inscripción
**Descripción:** Asiento formal en un padrón o registro público.
**Requisitos:**
- Registro o padrón
- Datos del inscrito
- Documentos presentados
- Fecha de inscripción

##### 2.8 Acreditación
**Descripción:** Reconocimiento oficial de que una persona o entidad cumple requisitos para una actividad.
**Requisitos:**
- Entidad acreditadora
- Acreditado
- Alcance de la acreditación
- Vigencia
- Fundamento

##### 2.9 Certificado de Idoneidad
**Descripción:** Documento que certifica la aptitud de una persona para una función.
**Requisitos:**
- Autoridad emisora
- Persona certificada
- Materia de idoneidad
- Fundamento
- Fecha

##### 2.10 Certificado de Acreditación de Uso del Suelo
**Descripción:** Certifica que un inmueble puede destinarse a un uso específico conforme al plan de desarrollo urbano.
**Requisitos:**
- Inmueble (ubicación, superficie)
- Uso solicitado
- Zonificación aplicable
- Autoridad emisora
- Vigencia

##### 2.11 Diploma
**Descripción:** Documento que acredita la conclusión de estudios o capacitación.
**Requisitos:**
- Institución educativa o capacitadora
- Persona que lo recibe
- Estudio o capacitación cursada
- Fecha

##### 2.12 Título Profesional
**Descripción:** Documento oficial que acredita una carrera profesional.
**Fundamento:** Ley Reglamentaria del Art. 5 CPEUM.
**Requisitos:**
- Institución educativa
- Profesionista (nombre, CURP)
- Carrera y especialidad
- Cédula profesional
- Fecha de expedición

---

#### 3. COMUNICACIONES ADMINISTRATIVAS

---

##### 3.1 Requerimiento
**Descripción:** Solicitud formal de autoridad a particular o autoridad para que haga o entregue algo.
**Requisitos:**
- Autoridad requirente
- Destinatario
- Documentación o acción requerida
- Plazo de cumplimiento
- Apercibimiento
- Fundamento
- Firma

##### 3.2 Notificación Administrativa
**Descripción:** Comunicación formal de un acto administrativo al interesado.
**Fundamento:** LFPA Arts. 25–36.
**Requisitos:**
- Acto que se notifica
- Notificado (nombre y domicilio)
- Fecha, hora y lugar
- Forma de notificación (personal, por oficio, por estrados, por edictos)
- Nombre del notificador

##### 3.3 Citatorio Administrativo
**Descripción:** Citación de la autoridad a un particular para que comparezca.
**Requisitos:**
- Autoridad que cita
- Citado (nombre, domicilio)
- Día, hora y lugar
- Objeto de la citación
- Apercibimiento

##### 3.4 Acta de Verificación
**Descripción:** Acta que registra los resultados de una verificación administrativa.
**Requisitos:**
- Autoridad verificadora
- Lugar, fecha y hora
- Objeto de la verificación
- Hechos observados
- Documentación revisada
- Nombre y firma del verificador
- Testigos (si los hay)

##### 3.5 Acta de Visita de Inspección
**Descripción:** Registro de los hechos constatados durante una visita de inspección.
**Requisitos:**
- Autoridad inspectora
- Lugar inspeccionado
- Fecha y hora (inicio y fin)
- Hechos observados
- Documentos y bienes revisados
- Nombre y firma del inspector y testigos

##### 3.6 Constancia
**Descripción:** Documento que acredita un hecho, acto o situación administrativa.
**Requisitos:**
- Autoridad emisora
- Hecho que se constata
- Datos del interesado
- Fundamento (si aplica)
- Fecha y firma

##### 3.7 Certificación
**Descripción:** Documento que da fe de la autenticidad de un acto, documento o hecho.
**Requisitos:**
- Autoridad certificante
- Documento o hecho certificado
- Persona solicitante
- Fecha y firma

##### 3.8 Informe
**Descripción:** Exposición escrita sobre un asunto o situación.
**Requisitos:**
- Autoridad o persona que informa
- Destinatario
- Objeto del informe
- Hechos, análisis y conclusiones
- Fecha y firma

##### 3.9 Dictamen
**Descripción:** Opinión técnica o jurídica sobre un asunto.
**Requisitos:**
- Dictaminador (nombre, cédula si perito)
- Objeto del dictamen
- Metodología
- Consideraciones técnicas o jurídicas
- Conclusiones
- Fecha y firma

##### 3.10 Dictamen Médico
**Descripción:** Opinión médica sobre el estado de salud de una persona.
**Requisitos:**
- Médico (nombre, cédula)
- Paciente
- Diagnóstico
- Pronóstico
- Fecha y firma

##### 3.11 Dictamen del Visitador
**Descripción:** Opinión del visitador sobre los hechos constatados en una visita.
**Requisitos:**
- Visitador
- Visita realizada
- Hechos observados
- Irregularidades detectadas
- Propuesta de acción

##### 3.12 Dictamen de Auditor Externo
**Descripción:** Opinión de un auditor independiente sobre estados financieros.
**Requisitos:**
- Auditor o firma auditora
- Entidad auditada
- Período auditado
- Opinión (limpia, con salvedades, adversa, abstención)
- Fecha y firma

##### 3.13 Informe Financiero y Actuarial
**Descripción:** Reporte financiero y actuarial de una entidad.
**Requisitos:**
- Entidad reportante
- Período
- Estados financieros
- Reservas técnicas
- Opinión actuarial

##### 3.14 Opinión Técnica
**Descripción:** Opinión especializada sobre un aspecto técnico específico.
**Requisitos:**
- Técnico o especialista
- Objeto de la opinión
- Análisis y fundamentos
- Conclusión
- Fecha y firma

##### 3.15 Fe de Erratas (DOF)
**Descripción:** Corrección de errores materiales en publicaciones del Diario Oficial de la Federación.
**Requisitos:**
- Publicación que se corrige (fecha, sección)
- Texto erróneo
- Texto correcto
- Fecha de publicación de la fe de erratas

---

### Lectura de documentos
- Extraer texto de PDF o Word
- Identificar: autoridad emisora, fundamento legal, destinatario, objeto
- Identificar tipo de acto administrativo


## 6. Reglas adicionales

- Decretos y reglamentos: requieren publicación en el DOF o periódico oficial estatal para su vigencia.
- Concesiones: plazo máx. 30 años, prorrogable; requieren título formal.
- Notificaciones administrativas: el acto debe notificarse personalmente o por el medio que señale la ley (LFPA Arts. 25–36).
- Dictámenes periciales: requieren cédula profesional y metodología explícita.
- Oficios: numeración correlativa por año y dependencia.


# Skill: Redactor de Documentos — Derecho de Seguros e Instituciones Financieras
**Fase 9 | 38 tipos de documentos**
Fuentes: Ley sobre el Contrato de Seguro (211.txt), Ley de Instituciones de Seguros y Fianzas (LISF), Ley de Instituciones de Crédito (LIC), Ley del Mercado de Valores (LCNBV), Ley de la Comisión Nacional Bancaria y de Valores, Ley de Ahorro y Crédito Popular, Ley de Uniones de Crédito, CCom.

---

## 1. Nombre
**"Redactor de documentos de seguros y financieros"**
(Formato forense/contractual — alineaciones, mayúsculas, tabuladores, justificación)

## 2. Objetivo
A partir de documentos adjuntos por el usuario y de instrucciones conversacionales, generar cualquier póliza de seguro, documento bancario, contrato financiero o fianza que cumpla con las formalidades legales y de presentación.

## 3. Entradas del usuario
- **Documentos subidos** (opcional): pólizas previas, contratos, estados de cuenta, solicitudes
- **Indicación del tipo de documento**: póliza, endoso, reclamación, contrato bancario, fianza, etc.
- **Datos específicos**: aseguradora/banco, tomador/contratante, bienes, montos, primas, plazos

### 4.3 Catálogo de documentos y requisitos

---

#### 1. DOCUMENTOS DEL CONTRATO DE SEGURO

---

##### 1.1 Póliza de Seguro
**Descripción:** Documento que formaliza el contrato de seguro y contiene las coberturas, primas y condiciones.
**Fundamento:** LCS Arts. 1–31.
**Requisitos:**
- Aseguradora (nombre, RFC)
- Contratante y asegurado (nombre, RFC, domicilio)
- Beneficiario(s)
- Riesgos cubiertos y exclusiones
- Suma asegurada
- Prima (monto, forma de pago, periodicidad)
- Vigencia (inicio y fin)
- Deducibles y coaseguro
- Condiciones generales y particulares
- Fecha de emisión y firma

##### 1.2 Póliza de Seguro de Caución
**Descripción:** Garantiza el cumplimiento de obligaciones del contratante ante el beneficiario.
**Fundamento:** LCS Arts. 278–294.
**Requisitos:**
- Afianzadora, contratante y beneficiario
- Obligación garantizada
- Monto de la caución
- Prima
- Vigencia
- Causas de ejecución

##### 1.3 Póliza Reducida (Conversión por Valor Garantizado)
**Descripción:** Póliza con reducción de cobertura por pago de primas con valor garantizado.
**Requisitos:**
- Póliza original
- Valor garantizado disponible
- Nueva suma asegurada reducida
- Condiciones aplicables

##### 1.4 Endoso de Seguro
**Descripción:** Modificación a las condiciones de una póliza vigente.
**Fundamento:** LCS Arts. 22–24.
**Requisitos:**
- Póliza que se modifica
- Cláusula o condición modificada
- Nuevo texto
- Fecha de entrada en vigor
- Firma de la aseguradora

##### 1.5 Solicitud de Seguro
**Descripción:** Cuestionario y declaración del solicitante para la celebración del contrato.
**Fundamento:** LCS Arts. 8–10.
**Requisitos:**
- Solicitante (nombre, RFC, domicilio)
- Riesgos a cubrir
- Suma asegurada solicitada
- Cuestionario de salud (seguros de personas) o descripción de bienes (daños)
- Declaración de veracidad

##### 1.6 Certificado de Seguro
**Descripción:** Documento emitido para acreditar la cobertura de un asegurado individual bajo una póliza colectiva.
**Requisitos:**
- Póliza colectiva
- Asegurado individual
- Coberturas y suma asegurada
- Vigencia

##### 1.7 Certificado de Seguro de Caución
**Descripción:** Documento que acredita la garantía de caución a favor del beneficiario.
**Requisitos:**
- Póliza de caución
- Beneficiario
- Obligación garantizada
- Monto

##### 1.8 Recibo de Prima
**Descripción:** Comprobante de pago de la prima del seguro.
**Requisitos:**
- Póliza
- Tomador
- Prima pagada y período
- Fecha de pago

##### 1.9 Declaración de Siniestro
**Descripción:** Comunicación del asegurado a la aseguradora sobre la ocurrencia del siniestro.
**Fundamento:** LCS Arts. 66–69.
**Requisitos:**
- Póliza
- Asegurado
- Fecha, hora y lugar del siniestro
- Descripción de los hechos
- Daños sufridos (estimación)
- Documentos de soporte

##### 1.10 Aviso de Siniestro
**Descripción:** Notificación formal e inmediata del siniestro a la aseguradora.
**Fundamento:** LCS Art. 66.
**Requisitos:**
- Póliza
- Siniestro (fecha, lugar, descripción)
- Asegurado
- Daños preliminares

##### 1.11 Reclamación de Seguro
**Descripción:** Solicitud formal de pago de la indemnización.
**Fundamento:** LCS Arts. 70–80.
**Requisitos:**
- Póliza y endosos
- Asegurado o beneficiario
- Siniestro (hechos, fecha)
- Daños cuantificados
- Documentación (dictámenes, facturas, actas)
- Cuenta para pago

##### 1.12 Préstamo sobre Póliza
**Descripción:** Préstamo automático con cargo al valor de rescate de la póliza.
**Requisitos:**
- Póliza con valor en efectivo
- Monto del préstamo
- Tasa de interés
- Plazo
- Consecuencias de impago

##### 1.13 Cesión de Derechos del Contrato de Seguro
**Descripción:** Transmisión de los derechos del asegurado o beneficiario a un tercero.
**Requisitos:**
- Póliza
- Cedente y cesionario
- Derechos cedidos
- Aceptación de la aseguradora

##### 1.14 Contrato de Reaseguro
**Descripción:** Contrato por el que la aseguradora cede parte del riesgo al reasegurador.
**Fundamento:** LCS Arts. 17, 108–109; LISF.
**Requisitos:**
- Cedente y reasegurador
- Riesgos cedidos
- Prima cedida y comisión
- Tipo (proporcional, no proporcional, facultativo, automático)

##### 1.15 Póliza de Fianza
**Descripción:** Garantía por la que la afianzadora se obliga a cumplir la obligación del fiado ante el beneficiario.
**Fundamento:** LISF; CC DF Arts. 2794–2847.
**Requisitos:**
- Afianzadora, fiado y beneficiario
- Obligación garantizada
- Monto
- Prima
- Vigencia
- Causas de ejecución

##### 1.16 Contrafianza
**Descripción:** Garantía que el fiado otorga a la afianzadora para asegurar el reembolso.
**Requisitos:**
- Afianzadora y contrafiador
- Fianza contragarantizada
- Bienes o garantías otorgadas

##### 1.17 Contrato de Coafianzamiento
**Descripción:** Varias afianzadoras garantizan solidariamente la misma obligación.
**Requisitos:**
- Afianzadoras partícipes
- Fiado y beneficiario
- Monto total y participación de cada una
- Condiciones de solidaridad

##### 1.18 Contrato de Reafianzamiento
**Descripción:** Una afianzadora cede parte del riesgo asumido a otra.
**Requisitos:**
- Afianzadora cedente y reafianzadora
- Riesgos cedidos
- Prima cedida

---

#### 2. DOCUMENTOS BANCARIOS Y FINANCIEROS

---

##### 2.1 Certificado de Depósito Bancario
**Descripción:** Título que acredita un depósito en una institución de crédito.
**Fundamento:** LIC Arts. 46, 92; LGTOC.
**Requisitos:**
- Banco emisor
- Depositante
- Monto
- Plazo
- Tasa de interés

##### 2.2 Certificado de Depósito Bancario de Dinero a Plazo Fijo
**Descripción:** Depósito a plazo fijo con tasa de interés garantizada.
**Requisitos:**
- Banco, depositante, monto, plazo, tasa, fecha de vencimiento

##### 2.3 Estado de Cuenta Bancario
**Descripción:** Reporte periódico de movimientos de una cuenta bancaria.
**Requisitos:**
- Banco y titular
- Número de cuenta
- Período
- Saldo inicial, movimientos (cargos y abonos), saldo final

##### 2.4 Fianza Judicial
**Descripción:** Fianza otorgada en un proceso judicial para garantizar obligaciones procesales.
**Requisitos:**
- Afianzadora, fiado, juzgado
- Juicio y expediente
- Obligación garantizada
- Monto
- Vigencia

##### 2.5 Fianza Administrativa
**Descripción:** Fianza para garantizar obligaciones ante autoridades administrativas.
**Requisitos:**
- Afianzadora, fiado, autoridad
- Obligación garantizada
- Monto y vigencia

##### 2.6 Carta de Crédito
**Descripción:** Institución de crédito garantiza el pago al beneficiario contra documentos.
**Fundamento:** LGTOC Arts. 311–314.
**Requisitos:**
- Banco emisor, ordenante y beneficiario
- Monto y moneda
- Documentos exigidos
- Plazo de vigencia
- Tipo (irrevocable, confirmado, a la vista)

##### 2.7 Crédito Documentario
**Descripción:** Especie de carta de crédito con documentos comerciales.
**Requisitos:** Mismos que carta de crédito, con especificación de documentos de embarque.

##### 2.8 Contrato de Apertura de Crédito
**Descripción:** Banco se obliga a poner fondos a disposición del acreditado.
**Fundamento:** LGTOC Arts. 291–310.
**Requisitos:**
- Banco y acreditado
- Monto de la línea
- Tipo (simple, en cuenta corriente, quirografario)
- Tasa de interés
- Plazo y disposiciones
- Garantías

##### 2.9 Contrato de Depósito Bancario de Dinero a la Vista
**Descripción:** Depósito disponible en cualquier momento.
**Requisitos:**
- Banco y depositante
- Monto inicial
- Condiciones de disposición
- Intereses (si aplican)

##### 2.10 Contrato de Depósito Bancario de Ahorro
**Descripción:** Depósito de ahorro con rendimiento.
**Requisitos:**
- Banco y ahorrador
- Monto mínimo
- Tasa de interés
- Condiciones de retiro

##### 2.11 Contrato de Cuenta Corriente
**Descripción:** Cuenta bancaria con cheques y líneas de crédito asociadas.
**Requisitos:**
- Banco y titular
- Límite de sobregiro
- Comisiones y tasas
- Estado de cuenta

##### 2.12 Contrato de Préstamo Quirografario / Crédito Simple
**Descripción:** Préstamo personal sin garantía específica.
**Requisitos:**
- Banco y acreditado
- Monto, tasa, plazo
- Forma de pago
- Pagaré como título ejecutivo

##### 2.13 Contrato de Arrendamiento Financiero
**Descripción:** Arrendadora adquiere bien y lo arrienda con opción de compra.
**Fundamento:** LGTOC Arts. 408–418.
**Requisitos:**
- Arrendadora y arrendataria
- Bien
- Rentas y plazo
- Opción de compra
- Valor residual

##### 2.14 Contrato de Factoraje Financiero
**Descripción:** Empresa de factoraje adquiere derechos de crédito.
**Fundamento:** LGTOC Arts. 419–431.
**Requisitos:**
- Cedente y factoraje
- Créditos cedidos
- Precio/descuento
- Tipo (con o sin recurso)

##### 2.15 Contrato de Reporto
**Descripción:** Adquisición de títulos con obligación de retorno.
**Fundamento:** LGTOC Arts. 259–278.
**Requisitos:**
- Reportador y reportado
- Títulos
- Precio de compra y retorno
- Plazo

##### 2.16 Contrato de Responsabilidades (Agrupación Financiera)
**Descripción:** Contrato que establece responsabilidades entre entidades de un grupo financiero.
**Fundamento:** LCNBV; LIC.
**Requisitos:**
- Entidades del grupo
- Responsabilidades asumidas
- Mecanismos de compensación

##### 2.17 Acuerdo de Intercambio de Información
**Descripción:** Acuerdo entre instituciones para compartir información crediticia o financiera.
**Fundamento:** LIC; LFPDPPP.
**Requisitos:**
- Partes
- Tipo de información intercambiada
- Propósito
- Confidencialidad
- Plazo

##### 2.18 Reporte de Crédito / Reporte de Crédito Especial
**Descripción:** Reporte emitido por SOC (Sociedad de Información Crediticia) sobre historial crediticio.
**Fundamento:** LIC Arts. 19–22; Ley para Regular las SOC.
**Requisitos:**
- Sujeto de crédito (nombre, RFC)
- Solicitante del reporte
- Propósito
- Historial de créditos, pagos y morosidad

---

### Lectura de documentos
- Extraer texto de PDF o Word
- Identificar: partes, montos, primas, plazos, coberturas, garantías
- Identificar tipo de seguro o instrumento financiero


## 6. Reglas adicionales

- Póliza de seguro: debe contener coberturas, exclusiones, sumas aseguradas, deducibles y primas.
- Declaración de siniestro: debe presentarse dentro del plazo estipulado en la póliza (generalmente 5 días).
- Préstamo sobre póliza: solo disponible si la póliza tiene valor de rescate.
- Fianza judicial: requiere aprobación del juez; la afianzadora debe estar autorizada por la CNSF.
- Arrendamiento financiero: solo por entidades autorizadas por la CNBV.
- Reportes de crédito: regulados por la Ley para Regular las SOC; requieren autorización del sujeto.


# Skill: Redactor de Documentos — Contratos Civiles
**Fase 10 | 33 tipos de documentos**
Fuentes: Código Civil Federal, Código Civil para el DF/CDMX (CODIGO_CIVIL_PARA_EL_DF_15.3.txt), Código Civil del Estado de México (codvig001.txt), CODEX/CCom.txt.

---

## 1. Nombre
**"Redactor de contratos civiles"**
(Formato contractual — alineaciones, mayúsculas, tabuladores, justificación)

## 2. Objetivo
A partir de documentos adjuntos por el usuario y de instrucciones conversacionales, generar cualquier contrato civil (traslaticio de dominio, uso, servicio, garantía, representación, asociativo o convenio) que cumpla con las formalidades legales.

## 3. Entradas del usuario
- **Documentos subidos** (opcional): contratos previos, títulos de propiedad, identificaciones
- **Indicación del tipo de contrato**: compraventa, arrendamiento, mandato, hipoteca, etc.
- **Datos específicos**: partes, objeto, precio, plazos, garantías, cláusulas especiales

### 4.3 Catálogo de documentos y requisitos

---

#### 1. CONTRATOS TRASLATICIOS DE DOMINIO

---

##### 1.1 Contrato de Compraventa (Bien Inmueble)
**Descripción:** Transmisión de propiedad de inmueble a cambio de precio.
**Fundamento:** CC DF Arts. 2248–2322.
**Requisitos:**
- Vendedor y comprador (nombre, RFC, CURP, estado civil, domicilio)
- Inmueble (ubicación, superficie, medidas, colindancias, clave catastral, folio real)
- Antecedentes de propiedad
- Precio y forma de pago
- Fecha de entrega
- Garantías de evicción y vicios ocultos
- Gastos de escrituración e impuestos
- Debe constar en escritura pública

##### 1.2 Contrato de Compraventa (Bien Mueble)
**Descripción:** Transmisión de propiedad de bien mueble.
**Fundamento:** CC DF Arts. 2248–2322.
**Requisitos:**
- Vendedor y comprador
- Bien (cantidad, calidad, especie)
- Precio y forma de pago
- Entrega (lugar y plazo)
- Garantías

##### 1.3 Compraventa bajo Condición Resolutoria
**Descripción:** Venta que se resuelve si no se cumple una condición.
**Requisitos:**
- Mismos que compraventa
- Condición resolutoria expresa
- Efectos de la resolución

##### 1.4 Contrato de Donación
**Descripción:** Transmisión gratuita de un bien.
**Fundamento:** CC DF Arts. 2332–2383.
**Requisitos:**
- Donante y donatario
- Bien donado (descripción, valor)
- Causa (liberal, remuneratoria, con carga)
- Escritura pública si supera el umbral legal
- Reserva de inoficiosidad (herederos forzosos)

##### 1.5 Contrato de Permuta
**Descripción:** Intercambio de un bien por otro.
**Fundamento:** CC DF Arts. 2323–2331.
**Requisitos:**
- Partes
- Bienes permutados (descripción y valor)
- Diferencia en dinero (si aplica)
- Entrega

##### 1.6 Contrato de Renta Vitalicia
**Descripción:** Obligación de pagar una pensión periódica vitalicia a cambio de un capital.
**Fundamento:** CC DF Arts. 2790–2793.
**Requisitos:**
- Deudor y acreedor de la renta
- Capital entregado
- Monto y periodicidad de la renta
- Duración (vida del acreedor o de un tercero)
- Escritura pública

---

#### 2. CONTRATOS DE USO Y DISFRUTE

---

##### 2.1 Contrato de Arrendamiento
**Descripción:** Cesión temporal de uso de bien a cambio de renta.
**Fundamento:** CC DF Arts. 2398–2496.
**Requisitos:**
- Arrendador y arrendatario
- Bien (descripción)
- Renta, forma y fecha de pago
- Plazo
- Depósito en garantía
- Destino del bien
- Reparaciones
- Subarrendamiento (prohibido o permitido)

##### 2.2 Contrato de Arrendamiento de Vivienda
**Descripción:** Arrendamiento de inmueble destinado a habitación.
**Requisitos:** Mismos que 2.1. Régimen de renta con tope legal (si aplica CDMX). Protección al arrendatario.

##### 2.3 Contrato de Arrendamiento Financiero (Leasing)
**Descripción:** Arrendadora adquiere bien y lo arrienda con opción de compra.
**Fundamento:** LGTOC Arts. 408–418.
**Requisitos:**
- Arrendadora y arrendataria
- Bien
- Rentas, plazo
- Opción de compra, valor residual
- Seguro

##### 2.4 Contrato de Comodato
**Descripción:** Préstamo gratuito de uso de un bien.
**Fundamento:** CC DF Arts. 2497–2523.
**Requisitos:**
- Comodante y comodatario
- Bien (descripción)
- Plazo o destino
- Prohibición de usar para distinto fin
- Responsabilidad del comodatario

##### 2.5 Contrato de Aparcería
**Descripción:** Aportación de tierra y trabajo con división de productos.
**Fundamento:** CC DF Arts. 2739–2753.
**Requisitos:**
- Propietario y aparcero
- Tierra y productos
- Proporción de cada parte
- Plazo

---

#### 3. CONTRATOS DE PRESTACIÓN DE SERVICIOS

---

##### 3.1 Contrato de Prestación de Servicios Profesionales
**Descripción:** Profesionista se obliga a prestar servicios a cambio de honorarios.
**Fundamento:** CC DF Arts. 2606–2615.
**Requisitos:**
- Prestador (nombre, cédula profesional)
- Cliente
- Servicios a prestar
- Honorarios y forma de pago
- Plazo
- Responsabilidad profesional

##### 3.2 Contrato de Obra a Precio Alzado
**Descripción:** Contratista ejecuta obra por precio fijo.
**Fundamento:** CC DF Arts. 2616–2643.
**Requisitos:**
- Contratista y cliente
- Descripción de la obra
- Precio alzado
- Plazo de ejecución
- Materiales (quién los aporta)
- Penalizaciones por demora
- Recepción de obra

##### 3.3 Contrato de Transporte (Civil)
**Descripción:** Traslado de personas o bienes por tierra, agua o aire.
**Fundamento:** CC DF Arts. 2644–2675.
**Requisitos:**
- Porteador y pasajero/remitente
- Origen y destino
- Precio (flete/pasaje)
- Plazo
- Responsabilidad por daños

##### 3.4 Contrato de Hospedaje
**Descripción:** Alojamiento temporal a cambio de precio.
**Fundamento:** CC DF Arts. 2666–2674.
**Requisitos:**
- Hotelero y huésped
- Tipo de alojamiento
- Tarifa
- Período
- Responsabilidad del hotelero

---

#### 4. CONTRATOS DE GARANTÍA

---

##### 4.1 Contrato de Hipoteca
**Descripción:** Garantía real sobre inmueble para asegurar una obligación.
**Fundamento:** CC DF Arts. 2893–2943.
**Requisitos:**
- Deudor hipotecante y acreedor
- Inmueble (folio real, descripción)
- Obligación garantizada (monto, tasa, plazo)
- Escritura pública e inscripción RPP
- Vencimiento anticipado

##### 4.2 Contrato de Hipoteca Inversa (Estado de México)
**Descripción:** Hipoteca que permite al propietario recibir pagos periódicos garantizados con el inmueble.
**Fundamento:** CC Edomex.
**Requisitos:**
- Propietario e institución
- Inmueble
- Pagos periódicos
- Plazo
- Liquidación al fallecimiento

##### 4.3 Contrato de Prenda
**Descripción:** Garantía real sobre bien mueble entregado al acreedor.
**Fundamento:** CC DF Arts. 2856–2892.
**Requisitos:**
- Deudor prendario y acreedor
- Bien (descripción)
- Obligación garantizada
- Entrega del bien
- Derecho de retención

##### 4.4 Contrato de Fianza
**Descripción:** Fiador garantiza el cumplimiento de una obligación.
**Fundamento:** CC DF Arts. 2794–2847.
**Requisitos:**
- Fiador, deudor y acreedor
- Obligación garantizada
- Monto
- Plazo
- Beneficio de excusión (renunciable)

##### 4.5 Contrato de Depósito
**Descripción:** Depositario recibe un bien para su guarda y custodia.
**Fundamento:** CC DF Arts. 2516–2545.
**Requisitos:**
- Depositante y depositario
- Bien (descripción)
- Plazo
- Retribución (gratuito u oneroso)
- Responsabilidad del depositario

---

#### 5. CONTRATOS DE REPRESENTACIÓN Y GESTIÓN

---

##### 5.1 Contrato de Mandato
**Descripción:** Mandatario actúa por cuenta del mandante.
**Fundamento:** CC DF Arts. 2546–2590.
**Requisitos:**
- Mandante y mandatario
- Actos encomendados
- Facultades y límites
- Sustitución (permitida o no)
- Remuneración
- Rendición de cuentas

##### 5.2 Contrato de Gestión de Negocios (Cuasicontrato)
**Descripción:** Persona gestiona negocios ajenos sin mandato.
**Fundamento:** CC DF Arts. 1896–1910.
**Requisitos:**
- Gestor y dueño del negocio
- Negocio gestionado
- Ausencia de mandato
- Obligación de rendir cuentas
- Derecho a reembolso

##### 5.3 Capitulaciones Matrimoniales
**Descripción:** Convenio que regula el régimen patrimonial del matrimonio.
**Fundamento:** CC DF Arts. 179–217.
**Requisitos:**
- Futuros cónyuges
- Régimen elegido (sociedad conyugal o separación de bienes)
- Bienes aportados y su valor
- Deudas
- Gastos del hogar
- Escritura pública ante notario

---

#### 6. CONTRATOS ASOCIATIVOS

---

##### 6.1 Contrato de Asociación
**Descripción:** Varias personas se unen para un fin común no lucrativo.
**Fundamento:** CC DF Arts. 2670–2687.
**Requisitos:**
- Asociados
- Denominación
- Objeto (no preponderantemente económico)
- Aportaciones
- Órganos de gobierno
- Escritura pública e inscripción RPP

##### 6.2 Contrato de Sociedad Civil
**Descripción:** Varias personas aportan bienes para un fin común lucrativo.
**Fundamento:** CC DF Arts. 2688–2736.
**Requisitos:**
- Socios (nombre, RFC, aportaciones)
- Razón social
- Objeto
- Capital social
- Participación en ganancias y pérdidas
- Administración
- Escritura pública

##### 6.3 Contrato de Apuesta y Juego
**Descripción:** Promesa de premio a quien acierte un resultado.
**Fundamento:** CC DF Arts. 2754–2762.
**Requisitos:**
- Partes
- Objeto de la apuesta
- Premio
- Condiciones
- No son exigibles judicialmente (salvo deportivos autorizados)

---

#### 7. CONVENIOS MODIFICATIVOS Y EXTINTIVOS

---

##### 7.1 Contrato de Transacción (Convenio Transaccional)
**Descripción:** Acuerdo para evitar o terminar un litigio mediante concesiones recíprocas.
**Fundamento:** CC DF Arts. 2944–2957.
**Requisitos:**
- Partes
- Litigio o controversia existente
- Concesiones recíprocas
- Obligaciones asumidas
- Efecto de cosa juzgada

##### 7.2 Cláusula Compromisoria
**Descripción:** Acuerdo para someter controversias a arbitraje, inserta en un contrato.
**Fundamento:** CC DF Arts. 2947–2950; CCom Arts. 1415–1463.
**Requisitos:**
- Controversias sometidas
- Institución arbitral
- Número de árbitros
- Sede e idioma

##### 7.3 Cláusula Penal
**Descripción:** Prestación pactada para el caso de incumplimiento.
**Fundamento:** CC DF Arts. 1840–1849.
**Requisitos:**
- Obligación principal
- Monto de la pena
- Incumplimiento que la genera
- No puede exceder del valor de la obligación principal

##### 7.4 Contrato de Promesa
**Descripción:** Obligación de celebrar un contrato futuro.
**Fundamento:** CC DF Arts. 2243–2247.
**Requisitos:**
- Promitentes
- Contrato a celebrar (tipo, elementos esenciales)
- Plazo para celebrarlo
- Requisitos debe estar determinado

##### 7.5 Convenio de Alimentos
**Descripción:** Acuerdo sobre el monto y forma de pago de alimentos.
**Fundamento:** CC DF Arts. 301–323; CC Edomex.
**Requisitos:**
- Acreedor y deudor alimentario
- Parentesco o relación
- Monto o porcentaje
- Periodicidad
- Forma de pago
- Actualización

##### 7.6 Convenio de Divorcio (ante Notario o Juez)
**Descripción:** Acuerdo de los cónyuges sobre los efectos del divorcio.
**Fundamento:** CC DF Arts. 266–272.
**Requisitos:**
- Cónyuges
- Hijos (guarda, custodia, visitas, alimentos)
- Bienes (liquidación de sociedad conyugal)
- Domicilio conyugal
- Debe ser ratificado ante juez o notario

##### 7.7 Convenio de Adjudicación de Bien Hipotecado
**Descripción:** Acuerdo para adjudicar el inmueble hipotecado al acreedor en pago del crédito.
**Requisitos:**
- Deudor y acreedor hipotecario
- Inmueble
- Crédito insoluto
- Valor de adjudicación
- Cancelación de hipoteca

---

### Lectura de documentos
- Extraer texto de PDF o Word
- Identificar: partes, bienes, montos, plazos, garantías
- Identificar tipo de contrato y elementos esenciales


## 6. Reglas adicionales

- Compraventa de inmueble: exige escritura pública ante notario (CC DF Art. 2317).
- Donación: requiere escritura pública si el valor excede el umbral legal.
- Hipoteca: debe inscribirse en el RPP para ser oponible a terceros.
- Prenda: requiere entrega del bien al acreedor (posesión).
- Mandato: las facultades especiales deben estar expresamente señaladas (desistir, transigir, etc.).
- Capitulaciones matrimoniales: deben otorgarse antes del matrimonio o durante este, mediante escritura pública.
- Transacción: tiene efectos de cosa juzgada entre las partes.
- Cláusula penal: no puede exceder el valor de la obligación principal (CC DF Art. 1842).

- Clausulado: `PRIMERA:`, `SEGUNDA:` con sangría francesa.


# Skill: Redactor de Documentos — Seguridad Social
**Fase 11 | 29 tipos de documentos**
Fuentes: Ley del Seguro Social (LSS), Ley del ISSSTE (LISSSTE), Ley del SAR.

---

## 1. Nombre
**"Redactor de documentos de seguridad social"**

## 2. Objetivo
Generar avisos, solicitudes, recursos, convenios y resoluciones en materia de seguridad social (IMSS, ISSSTE, AFORE).

## 3. Entradas del usuario
- **Documentos subidos** (opcional): resoluciones, avisos previos, estados de cuenta
- **Datos**: trabajador, patrón, NSS, RFC, régimen, cuotas, prestaciones

### Lectura de documentos
- Extraer texto de PDF o Word
- Identificar: NSS, RFC, trabajador, patrón, salario, régimen
- Identificar tipo de prestación o trámite


## 4. Catálogo de documentos y requisitos

### Aviso de Incorporación al IMSS
**Fundamento:** LSS Arts. 15–23.
**Requisitos:** Patrón, trabajador, NSS, salario, fecha de ingreso.

### Aviso de Modificación de Salario
**Fundamento:** LSS Art. 15.
**Requisitos:** Trabajador, NSS, salario anterior, nuevo salario.

### Aviso de Baja del IMSS
**Fundamento:** LSS Art. 15.
**Requisitos:** Trabajador, NSS, fecha de baja, causa.

### Solicitud de Incorporación al Régimen Obligatorio
**Requisitos:** Trabajador, patrón, NSS, identificación.

### Solicitud de Prestaciones en Especie (IMSS)
**Fundamento:** LSS Arts. 91–98.
**Requisitos:** Asegurado o beneficiario, NSS, tipo de prestación.

### Solicitud de Pensión (Cesantía, Vejez, Invalidez, Vida)
**Fundamento:** LSS Arts. 154–185.
**Requisitos:** Trabajador, NSS, acta de nacimiento, historial de cotización, dictamen médico (invalidez).

### Solicitud de Subsidio (Enfermedad, Maternidad)
**Fundamento:** LSS Arts. 96–107.
**Requisitos:** Asegurado, NSS, certificado médico, fechas.

### Recurso de Inconformidad ante el IMSS
**Fundamento:** LSS Arts. 294–304.
**Requisitos:** Resolución impugnada, agravios, pruebas, firma.

### Recurso de Revisión ante el ISSSTE
**Fundamento:** LISSSTE Arts. 160–170.
**Requisitos:** Resolución impugnada, agravios, pruebas.

### Convenio de Incorporación Voluntaria al IMSS
**Fundamento:** LSS Arts. 238–250.
**Requisitos:** Solicitante, actividad, trabajadores, salarios.

### Solicitud de Devolución de Cuotas
**Fundamento:** LSS Art. 291.
**Requisitos:** Patrón, período, cuotas pagadas, causa de devolución.

### Constancia de Semanas Cotizadas
**Requisitos:** Trabajador, NSS, período.
**Propósito:** Acreditar semanas de cotización.

### Estado de Cuenta Individual (AFORE)
**Fundamento:** LSS Arts. 159–178; LSAR.
**Requisitos:** Trabajador, NSS, AFORE, período.
**Propósito:** Mostrar saldo y movimientos.

### Dictamen de Invalidez
**Fundamento:** LSS Arts. 119–128.
**Requisitos:** Trabajador, NSS, expediente clínico, evaluación.

### Acuerdo de Pensión
**Fundamento:** LSS Arts. 170–185.
**Requisitos:** Trabajador, NSS, tipo de pensión, monto, forma de pago.




### Aviso de Incorporación al IMSS
**Fundamento:** LSS Arts. 15–23.
**Requisitos:** Datos del patrón, trabajador, NSS, salario, fecha de ingreso, tipo de jornada.

### Aviso de Modificación de Salario
**Fundamento:** LSS Art. 15.
**Requisitos:** Trabajador, NSS, salario anterior, nuevo salario, fecha del cambio.

### Aviso de Baja del IMSS
**Fundamento:** LSS Art. 15.
**Requisitos:** Trabajador, NSS, fecha de baja, causa (renuncia, despido, terminación).

### Aviso de Suspensión Temporal
**Fundamento:** LSS Art. 15.
**Requisitos:** Trabajador, NSS, causa (incapacidad, huelga, etc.), período.

### Solicitud de Incorporación Voluntaria
**Fundamento:** LSS Arts. 238–250.
**Requisitos:** Solicitante, régimen, trabajadores a incorporar, actividad.

### Solicitud de Prestaciones en Especie (IMSS)
**Fundamento:** LSS Arts. 91–98.
**Requisitos:** Asegurado o beneficiario, NSS, tipo de prestación, diagnóstico.

### Solicitud de Subsidio por Enfermedad
**Fundamento:** LSS Arts. 96–102.
**Requisitos:** Asegurado, NSS, certificado de incapacidad, fechas, salario.

### Solicitud de Subsidio por Maternidad
**Fundamento:** LSS Arts. 103–107.
**Requisitos:** Asegurada, NSS, certificado de embarazo, fecha probable de parto.

### Solicitud de Pensión por Cesantía en Edad Avanzada
**Fundamento:** LSS Arts. 154–161.
**Requisitos:** Trabajador, NSS, acta de nacimiento, historial de cotización (mín. 500 semanas).

### Solicitud de Pensión por Vejez
**Fundamento:** LSS Arts. 162–170.
**Requisitos:** Trabajador, NSS, acta de nacimiento, historial de cotización (mín. 800 semanas si aplica).

### Solicitud de Pensión por Invalidez
**Fundamento:** LSS Arts. 119–128.
**Requisitos:** Trabajador, NSS, dictamen médico, historial de cotización.

### Solicitud de Pensión por Viudez
**Fundamento:** LSS Arts. 130–137.
**Requisitos:** Beneficiario, acta de defunción, acta de matrimonio, NSS del causante.

### Solicitud de Pensión por Orfandad
**Fundamento:** LSS Arts. 138–143.
**Requisitos:** Menor o representante, actas de nacimiento y defunción, NSS del causante.

### Solicitud de Pensión por Ascendencia
**Fundamento:** LSS Arts. 144–148.
**Requisitos:** Ascendiente, actas de nacimiento y defunción, dependencia económica.

### Solicitud de Ayuda para Gastos de Funeral
**Fundamento:** LSS Art. 149.
**Requisitos:** Beneficiario, acta de defunción, factura de servicios funerarios.

### Recurso de Inconformidad ante el IMSS
**Fundamento:** LSS Arts. 294–304.
**Requisitos:** Resolución impugnada, agravios, pruebas documentales, firma.

### Recurso de Revisión ante el ISSSTE
**Fundamento:** LISSSTE Arts. 160–170.
**Requisitos:** Resolución impugnada, agravios, pruebas, fundamento.

### Convenio de Incorporación Voluntaria
**Fundamento:** LSS Arts. 238–250.
**Requisitos:** Solicitante, actividad, trabajadores, salarios, cuotas.

### Contrato de Prestación de Servicios (Subcontratación)
**Fundamento:** LSS Arts. 15-A–15-D.
**Requisitos:** Contratante, contratista, servicios, número de registro REPSE.

### Solicitud de Devolución de Cuotas
**Fundamento:** LSS Art. 291.
**Requisitos:** Patrón, período, cuotas pagadas en exceso, causa.

### Constancia de Semanas Cotizadas
**Requisitos:** Trabajador, NSS, período.
**Propósito:** Acreditar semanas de cotización ante IMSS.

### Estado de Cuenta Individual (AFORE)
**Fundamento:** LSS Arts. 159–178; LSAR.
**Requisitos:** Trabajador, NSS, AFORE, período.
**Propósito:** Mostrar saldo, aportaciones y rendimientos.

### Dictamen de Invalidez
**Fundamento:** LSS Arts. 119–128.
**Requisitos:** Trabajador, NSS, expediente clínico, evaluación médica.

### Resolución de Pensión (IMSS)
**Requisitos:** Solicitud, NSS, historial, cálculo.
**Contenido:** Monto, forma de pago, vigencia.

### Convenio de Pago de Cuotas en Parcialidades
**Fundamento:** LSS Art. 291.
**Requisitos:** Patrón, adeudo, número de parcialidades, garantía.

### Solicitud de Préstamo AFORE (Desempleo)
**Requisitos:** Trabajador, NSS, estado de cuenta, causa de desempleo.

### Dictamen de Riesgo de Trabajo
**Fundamento:** LSS Arts. 41–60.
**Requisitos:** Trabajador, NSS, acta de accidente, dictamen médico, incapacidad.

### Resolución de Determinación de Cuotas
**Fundamento:** LSS Arts. 285–290.
**Requisitos:** Patrón, período, cuotas determinadas, actualización, recargos.

### Constancia de Vigencia de Derechos
**Requisitos:** Trabajador, NSS.
**Propósito:** Acreditar que el trabajador está registrado y vigente ante el IMSS.


## 5. Reglas adicionales
- Incorporación al IMSS: dentro de los 5 días hábiles siguientes al inicio de la relación laboral.
- Pensión por cesantía: 60 años (hombres) o 55 años (mujeres) con 500 semanas de cotización.
- Recurso de inconformidad: 15 días hábiles desde la notificación.
- Cuotas obrero-patronales: base del SDI, no del salario nominal.
- Dictamen de invalidez: requiere certificado médico y evaluación del IMSS.
- Afore: el trabajador puede cambiar de AFORE cada 6 meses.

---


# Skill: Redactor de Documentos — Estado de México y CDMX (Legislación Local)
**Fase 12 | 29 tipos de documentos**
Fuentes: CC Edomex, CPC Edomex, CC CDMX, CP CDMX.

---

## 1. Nombre
**"Redactor de documentos locales — Estado de México y CDMX"**

## 2. Objetivo
Generar documentos propios de la legislación del Estado de México y la CDMX sin equivalente federal directo.

## 3. Entradas del usuario
- **Documentos subidos** (opcional): actas, escrituras, resoluciones
- **Datos**: según el tipo de documento local específico

### Lectura de documentos
- Extraer texto de PDF o Word
- Identificar: tipo de documento local, municipio/delegación
- Identificar legislación aplicable (Edomex o CDMX)


## 4. Catálogo de documentos y requisitos

### Testamento Público Simplificado (Edomex)
**Fundamento:** CC Edomex.
**Requisitos:** Testador, bienes, herederos, sin testigos instrumentales.

### Cédula Hipotecaria (Edomex)
**Fundamento:** CPC Edomex.
**Requisitos:** Escritura de hipoteca, monto, folio real, deudor y acreedor.

### Inmatriculación de Inmueble (Edomex)
**Fundamento:** Ley Registral Edomex.
**Requisitos:** Descripción técnica, certificado de no inscripción, plano.

### Aviso Preventivo al RPP (Edomex)
**Fundamento:** Ley Registral Edomex.
**Requisitos:** Folio real, adquirente, enajenante, tipo de acto, notaría.

### Divorcio Administrativo (CDMX)
**Fundamento:** CC CDMX Art. 272.
**Requisitos:** Acta de matrimonio, convenio de bienes, declaración de no hijos menores.

### Constancia de Curso Prenupcial (CDMX)
**Fundamento:** CC CDMX Arts. 98–100.
**Requisitos:** Contrayentes, fecha, asistencias.

### Acta de Nacimiento por Identidad de Género (Edomex)
**Fundamento:** CC Edomex.
**Requisitos:** Nombre anterior y solicitado, CURP, acta original.

### Reconocimiento de Hijo (Edomex/CDMX)
**Fundamento:** CC Edomex/CDMX.
**Requisitos:** Reconociente, hijo, consentimiento del otro progenitor.

### Acta de Nacimiento Primigenia
**Fundamento:** CC CDMX Arts. 134–140.
**Requisitos:** Pruebas supletorias, testigos, resolución judicial.

### Constancia de Inexistencia de Registro
**Requisitos:** Tipo de acta, datos del interesado, período de búsqueda.

### Constancia de Alumbramiento (Edomex)
**Requisitos:** Constancia médica, datos del recién nacido y padres.

### Capitulaciones Matrimoniales
**Fundamento:** CC CDMX Arts. 179–217.
**Requisitos:** Futuros cónyuges, régimen, bienes aportados, escritura pública.




### Testamento Público Simplificado (Edomex)
**Fundamento:** CC Edomex.
**Requisitos:** Testador, bienes, herederos, sin testigos instrumentales. Formalidad reducida.

### Cédula Hipotecaria (Edomex)
**Fundamento:** CPC Edomex.
**Requisitos:** Escritura de hipoteca inscrita, monto del crédito vencido, folio real, deudor y acreedor. Título ejecutivo.

### Inmatriculación de Inmueble (Edomex)
**Fundamento:** Ley Registral Edomex.
**Requisitos:** Descripción técnica, superficie, plano, certificado de no inscripción, testigos, colindancias.

### Aviso Preventivo al RPP (Edomex)
**Fundamento:** Ley Registral Edomex.
**Requisitos:** Folio real, adquirente, enajenante, tipo de acto, notaría, vigencia de la reserva.

### Solicitud de Divorcio Administrativo (CDMX)
**Fundamento:** CC CDMX Art. 272.
**Requisitos:** Acta de matrimonio, convenio de liquidación de bienes, declaración de no hijos menores o incapaces.

### Constancia de Curso Prenupcial (CDMX)
**Fundamento:** CC CDMX Arts. 98–100.
**Requisitos:** Nombres y CURP de contrayentes, fecha del curso, constancia de asistencia.

### Reconocimiento de Hijo (Edomex/CDMX)
**Fundamento:** CC Edomex/CDMX.
**Requisitos:** Reconociente, hijo (acta de nacimiento), consentimiento del otro progenitor o resolución judicial.

### Acta de Nacimiento por Identidad de Género (Edomex)
**Fundamento:** CC Edomex.
**Requisitos:** Nombre anterior, nuevo nombre, CURP, acta original, resolución o dictamen de identidad de género.

### Acta de Nacimiento Primigenia (CDMX)
**Fundamento:** CC CDMX Arts. 134–140.
**Requisitos:** Pruebas supletorias (constancia hospitalaria, testigos), resolución judicial, datos del individuo.

### Constancia de Inexistencia de Registro
**Requisitos:** Tipo de acta buscada, datos del interesado, período de búsqueda en el Registro Civil.

### Constancia de Alumbramiento (Edomex)
**Requisitos:** Constancia médica de alumbramiento, datos del recién nacido y padres.

### Capitulaciones Matrimoniales
**Fundamento:** CC CDMX Arts. 179–217.
**Requisitos:** Futuros cónyuges, régimen (sociedad conyugal o separación de bienes), bienes aportados y su valor, escritura pública.

### Solicitud de Cancelación de Acta (Edomex/CDMX)
**Requisitos:** Acta a cancelar, causa legal, resolución judicial o administrativa.

### Aclaración de Acta del Registro Civil
**Requisitos:** Acta a aclarar, datos erróneos y correctos, documentos de soporte.

### Solicitud de Matrimonio Civil (CDMX)
**Requisitos:** Contrayentes, testigos, constancia de curso prenupcial, identificación, actas de nacimiento.

### Solicitud de Registro de Nacimiento Extemporáneo
**Requisitos:** Persona a registrar, fecha y lugar de nacimiento, testigos, documentación que acredite identidad.

### Inscripción de Sentencia de Divorcio (Edomex/CDMX)
**Requisitos:** Sentencia ejecutoriada, acta de matrimonio, datos del juzgado, fecha de la sentencia.

### Fe de Erratas en Acta del Registro Civil
**Requisitos:** Acta, error material, texto correcto, fundamento.


## 5. Reglas adicionales
- Testamento simplificado Edomex: no requiere testigos instrumentales.
- Cédula hipotecaria Edomex: título ejecutivo para ejecución hipotecaria.
- Divorcio administrativo CDMX: solo sin hijos menores y bienes liquidados.
- Curso prenupcial CDMX: obligatorio para matrimonio civil.
- Inmatriculación: requiere certificado de no inscripción actualizado.

---


# Skill: Redactor de Documentos — Juicio de Amparo
**Fase 13 | 26 tipos de documentos**
Fuentes: Ley de Amparo (LAmp), Constitución Política de los Estados Unidos Mexicanos (CPEUM).

---

## 1. Nombre
**"Redactor de documentos de juicio de amparo"**

## 2. Objetivo
Generar demandas, recursos, informes y sentencias de amparo.

## 3. Entradas del usuario
- **Documentos subidos** (opcional): actos reclamados, sentencias, informes
- **Datos**: quejoso, autoridad responsable, acto reclamado, conceptos de violación
- **Tipo de amparo**: indirecto, directo, adhesivo

### Lectura de documentos
- Extraer texto de PDF o Word
- Identificar: quejoso, autoridad responsable, acto reclamado
- Identificar tipo de amparo (indirecto/directo/adhesivo)


## 4. Catálogo de documentos y requisitos

### Demanda de Amparo Indirecto
**Fundamento:** LAmp Arts. 107–114.
**Requisitos:** Quejoso, autoridad responsable, acto reclamado, conceptos de violación, derecho violado, firma.

### Demanda de Amparo Directo
**Fundamento:** LAmp Arts. 166–175.
**Requisitos:** Quejoso, sentencia impugnada, tribunal responsable, conceptos de violación.

### Amparo Adhesivo
**Fundamento:** LAmp Art. 182.
**Requisitos:** Parte que adhiere, sentencia impugnada, conceptos de violación.

### Solicitud de Suspensión del Acto Reclamado
**Fundamento:** LAmp Arts. 128–158.
**Requisitos:** Acto reclamado, apariencia del buen derecho, peligro en la demora, garantía (si aplica).

### Informe Previo / Justificado
**Fundamento:** LAmp Arts. 115–117.
**Requisitos:** Autoridad responsable, acto reclamado, fundamento, razones de no inconstitucionalidad.

### Recurso de Revisión (Amparo)
**Fundamento:** LAmp Arts. 81–96.
**Requisitos:** Resolución impugnada, agravios, concepto de violación.

### Recurso de Queja (Amparo)
**Fundamento:** LAmp Arts. 97–101.
**Requisitos:** Acto u omisión, agravio, solicitud de subsanación.

### Incidente de Exceso o Defecto en la Ejecución
**Fundamento:** LAmp Arts. 206–210.
**Requisitos:** Sentencia de amparo, acto de ejecución, exceso o defecto.

### Incidente de Inconformidad
**Fundamento:** LAmp Arts. 211–213.
**Requisitos:** Cumplimiento deficiente, sentencia de amparo, hechos.

### Incidente de Repetición del Acto Reclamado
**Fundamento:** LAmp Art. 214.
**Requisitos:** Acto reclamado, cumplimiento de sentencia, nuevo acto idéntico.

### Incidente de Nulidad de Notificaciones
**Fundamento:** LAmp Arts. 56–60.
**Requisitos:** Notificación, causa de nulidad, agravio.

### Sentencia de Amparo (Indirecto)
**Fundamento:** LAmp Arts. 73–80.
**Requisitos:** Quejoso, acto reclamado, conceptos de violación, consideraciones, efecto (concede o niega).

### Sentencia de Amparo (Directo)
**Fundamento:** LAmp Arts. 184–193.
**Requisitos:** Quejoso, sentencia impugnada, consideraciones, efecto (devuelve o niega).




### Demanda de Amparo Indirecto
**Fundamento:** LAmp Arts. 107–114.
**Requisitos:** Quejoso (nombre, domicilio), autoridad responsable, acto reclamado, conceptos de violación numerados, derecho fundamental violado, firma. Acompañar copia del acto reclamado.

### Demanda de Amparo Directo
**Fundamento:** LAmp Arts. 166–175.
**Requisitos:** Quejoso, sentencia definitiva impugnada, tribunal responsable, conceptos de violación, preceptos violados. Acompañar copia de la sentencia.

### Amparo Adhesivo
**Fundamento:** LAmp Art. 182.
**Requisitos:** Parte recurrida que se adhiere, sentencia impugnada, conceptos de violación, dentro del plazo de 15 días.

### Solicitud de Suspensión del Acto Reclamado
**Fundamento:** LAmp Arts. 128–158.
**Requisitos:** Acto reclamado, apariencia del buen derecho, peligro en la demora, garantía (si la suspensión requiere), tipo de suspensión.

### Incidente de Suspensión (Amparo Indirecto)
**Fundamento:** LAmp Arts. 131–147.
**Requisitos:** Acto reclamado, medidas solicitadas, garantía, efectos de la suspensión.

### Informe Previo (Autoridad Responsable)
**Fundamento:** LAmp Arts. 115–117.
**Requisitos:** Autoridad, acto reclamado, fundamento legal, razones por las que no es inconstitucional.

### Informe Justificado (Autoridad Responsable)
**Fundamento:** LAmp Arts. 117–119.
**Requisitos:** Autoridad, antecedentes del acto, fundamentos, defensas.

### Recurso de Revisión
**Fundamento:** LAmp Arts. 81–96.
**Requisitos:** Resolución impugnada, agravios (norma violada + razonamiento + perjuicio), concepto de violación, firma.

### Recurso de Queja
**Fundamento:** LAmp Arts. 97–101.
**Requisitos:** Acto u omisión de la autoridad, agravio, solicitud de subsanación, fundamento.

### Incidente de Exceso o Defecto en la Ejecución
**Fundamento:** LAmp Arts. 206–210.
**Requisitos:** Sentencia de amparo, acto de ejecución, exceso o defecto, solicitud de corrección.

### Incidente de Inconformidad
**Fundamento:** LAmp Arts. 211–213.
**Requisitos:** Cumplimiento deficiente o evasivo, sentencia de amparo, hechos, solicitud de apercibimiento.

### Incidente de Repetición del Acto Reclamado
**Fundamento:** LAmp Art. 214.
**Requisitos:** Acto reclamado original, cumplimiento de sentencia, nuevo acto idéntico, denuncia.

### Incidente de Nulidad de Notificaciones
**Fundamento:** LAmp Arts. 56–60.
**Requisitos:** Notificación impugnada, causa de nulidad, agravio.

### Incidente de Objeción de Documentos
**Requisitos:** Documento objetado, tipo de objeción, pruebas de falsedad.

### Incidente de Separación de Bienes (Amparo)
**Requisitos:** Quejoso, bienes embargados, solicitud de separación.

### Sentencia de Amparo (Indirecto)
**Fundamento:** LAmp Arts. 73–80.
**Requisitos:** Quejoso, acto reclamado, conceptos de violación, consideraciones, resolutivos (concede o niega).

### Sentencia de Amparo (Directo)
**Fundamento:** LAmp Arts. 184–193.
**Requisitos:** Quejoso, sentencia impugnada, consideraciones, resolutivos.

### Sentencia de Amparo Adhesivo
**Requisitos:** Recurrente, sentencia de amparo, consideraciones.

### Recurso de Reclamación
**Fundamento:** LAmp Arts. 102–106.
**Requisitos:** Acuerdo del presidente del tribunal, agravios, solicitud de revocación.

### Denuncia de Incumplimiento de Sentencia
**Fundamento:** LAmp Arts. 206–210.
**Requisitos:** Sentencia de amparo, incumplimiento, autoridad responsable, solicitud de medidas.

### Acuerdo de Admisión de Demanda
**Requisitos:** Demanda, juzgado, fecha, auto que admite, emplazamiento.

### Auto de Desechamiento
**Requisitos:** Causa de desechamiento (improcedencia, notoria improcedencia, extemporaneidad).

### Acuerdo de Sobreseimiento
**Requisitos:** Causa legal, hechos, determinación.

### Pedimento del MP (Amparo)
**Requisitos:** MP, opinión sobre el amparo, fundamento.


## 5. Reglas adicionales
- Amparo indirecto: 15 días hábiles desde el acto.
- Amparo directo: 15 días desde la sentencia firme.
- Suspensión: puede ser de oficio o a petición de parte.
- Revisión: 10 días hábiles desde la notificación.
- Queja: 5 días desde el acto.

---


# Skill: Redactor de Documentos — Extinción de Dominio
**Fase 14 | 14 tipos de documentos**
Fuentes: Ley Nacional de Extinción de Dominio (LNED).

---

## 1. Nombre
**"Redactor de documentos de extinción de dominio"**

## 2. Objetivo
Generar demandas, contestaciones, resoluciones y recursos en el juicio de extinción de dominio.

## 3. Entradas del usuario
- **Documentos subidos** (opcional): actas de aseguramiento, inventarios, resoluciones
- **Datos**: bienes, imputado, Ministerio Público, terceros interesados

### Lectura de documentos
- Extraer texto de PDF o Word
- Identificar: bienes, imputado, MP, terceros interesados
- Identificar tipo de aseguramiento


## 4. Catálogo de documentos y requisitos

### Demanda de Extinción de Dominio
**Fundamento:** LNED Arts. 1–25.
**Requisitos:** Bien, hecho ilícito, relación del bien, MP solicitante, pruebas.

### Contestación a la Demanda
**Fundamento:** LNED Arts. 26–35.
**Requisitos:** Afectado, bien, excepciones, pruebas, firma.

### Solicitud de Aseguramiento de Bienes
**Fundamento:** LNED Arts. 36–45.
**Requisitos:** Bien, riesgo de desaparición, hecho ilícito, MP solicitante.

### Acta de Aseguramiento
**Fundamento:** LNED Arts. 40–44.
**Requisitos:** Bien asegurado, fecha, hora, lugar, funcionario actuante, inventario.

### Oposición al Aseguramiento
**Fundamento:** LNED Arts. 46–50.
**Requisitos:** Tercero o afectado, derecho sobre el bien, pruebas.

### Sentencia de Extinción de Dominio
**Fundamento:** LNED Arts. 70–80.
**Requisitos:** Bien, hecho ilícito, acreditación, declaración de extinción, destino del bien.

### Recurso de Apelación
**Fundamento:** LNED Arts. 85–95.
**Requisitos:** Resolución impugnada, agravios, firma.

### Incidente de Oposición de Tercero
**Requisitos:** Tercero, bien, derecho real o posesorio, pruebas.

### Convenio de Terminación Anticipada
**Fundamento:** LNED Arts. 60–65.
**Requisitos:** MP y afectado, bien, condiciones, aprobación judicial.




### Demanda de Extinción de Dominio
**Fundamento:** LNED Arts. 1–25.
**Requisitos:** Bien objeto, hecho ilícito relacionado, MP solicitante, relación del bien con el delito, pruebas (documentales, testimoniales, periciales).

### Contestación a la Demanda
**Fundamento:** LNED Arts. 26–35.
**Requisitos:** Afectado o tercero, bien, excepciones y defensas, pruebas, firma.

### Solicitud de Aseguramiento Precautorio de Bienes
**Fundamento:** LNED Arts. 36–45.
**Requisitos:** Bien, riesgo de desaparición, ocultamiento o destrucción, hecho ilícito, fundamento de probabilidad.

### Acta de Aseguramiento
**Fundamento:** LNED Arts. 40–44.
**Requisitos:** Bien asegurado, fecha, hora, lugar, funcionario actuante, inventario detallado, testigos, depositario.

### Inventario de Bienes Asegurados
**Requisitos:** Descripción de cada bien, estado, valor estimado, ubicación.

### Oposición al Aseguramiento
**Fundamento:** LNED Arts. 46–50.
**Requisitos:** Tercero o afectado, derecho real o posesorio sobre el bien, pruebas de titularidad.

### Incidente de Levantamiento de Aseguramiento
**Requisitos:** Causa de levantamiento, acreditación del derecho, solicitud.

### Ofrecimiento de Pruebas (Extinción)
**Fundamento:** LNED.
**Requisitos:** Tipo de prueba, hecho a probar, datos del perito o testigo.

### Alegatos (Extinción de Dominio)
**Requisitos:** Hechos probados, valoración de pruebas, conclusiones sobre la procedencia.

### Sentencia de Extinción de Dominio
**Fundamento:** LNED Arts. 70–80.
**Requisitos:** Bien, hecho ilícito acreditado, declaración de extinción del derecho de propiedad, destino del bien (Estado).

### Sentencia Absolutoria (Extinción)
**Requisitos:** Bien, falta de acreditación, levantamiento de aseguramiento, devolución.

### Recurso de Apelación (Extinción)
**Fundamento:** LNED Arts. 85–95.
**Requisitos:** Resolución impugnada, agravios, pruebas admisibles en segunda instancia, firma.

### Incidente de Oposición de Tercero
**Requisitos:** Tercero ajeno al hecho ilícito, derecho real sobre el bien, pruebas de adquisición de buena fe.

### Convenio de Terminación Anticipada
**Fundamento:** LNED Arts. 60–65.
**Requisitos:** MP y afectado, bien, condiciones acordadas, aprobación judicial, efectos.

### Solicitud de Devolución de Bienes
**Requisitos:** Afectado o tercero, bien, causa de devolución, documentos.

### Resolución de Adjudicación al Estado
**Requisitos:** Bien extinguido, programa de administración de bienes, destino.


## 5. Reglas adicionales
- Procede sobre bienes relacionados con delincuencia organizada, secuestro, extorsión, corrupción, etc.
- El aseguramiento puede ser precautorio antes de la demanda.
- La sentencia declara la extinción del derecho de propiedad a favor del Estado.
- Plazo de contestación: 15 días hábiles.

---


# Skill: Redactor de Documentos — Ejecución Penal
**Fase 15 | 12 tipos de documentos**
Fuentes: Ley Nacional de Ejecución Penal (LNEP), CNPP.

---

## 1. Nombre
**"Redactor de documentos de ejecución penal"**

## 2. Objetivo
Generar incidentes, solicitudes, resoluciones y documentos penitenciarios ante el Juez de Ejecución.

## 3. Entradas del usuario
- **Documentos subidos** (opcional): sentencia, expediente, informes técnicos
- **Datos**: sentenciado, pena, centro penitenciario, beneficios solicitados

### Lectura de documentos
- Extraer texto de PDF o Word
- Identificar: sentenciado, pena, centro penitenciario
- Identificar beneficios solicitables


## 4. Catálogo de documentos y requisitos

### Incidente de Modificación de la Pena
**Fundamento:** LNEP Arts. 40–50.
**Requisitos:** Sentenciado, pena original, causa de modificación, fundamento.

### Incidente de Extinción de la Pena
**Fundamento:** LNEP Arts. 51–60.
**Requisitos:** Sentenciado, pena, causa de extinción (cumplimiento, indulto, etc.), documentos.

### Incidente de Sustitución de la Pena
**Fundamento:** LNEP Arts. 61–70.
**Requisitos:** Sentenciado, pena, medida sustitutiva propuesta, plan de actividades.

### Solicitud de Beneficio Penitenciario
**Fundamento:** LNEP Arts. 85–100.
**Requisitos:** Sentenciado, tipo de beneficio, requisitos cumplidos, informe técnico.

### Plan de Actividades para Beneficio
**Requisitos:** Sentenciado, beneficio, actividades propuestas, plazos.

### Resolución del Juez de Ejecución
**Requisitos:** Solicitud, antecedentes, consideraciones, determinación.

### Recurso de Apelación (Ejecución)
**Fundamento:** CNPP Arts. 467–484.
**Requisitos:** Resolución impugnada, agravios, firma.

### Informe Técnico Penitenciario
**Requisitos:** Sentenciado, centro, evaluación de conducta, estudio psicosocial.

### Constancia de Cumplimiento de Pena
**Requisitos:** Sentenciado, pena, fecha de cumplimiento, autoridad emisora.




### Incidente de Modificación de la Pena
**Fundamento:** LNEP Arts. 40–50.
**Requisitos:** Sentenciado, pena original, causa de modificación (cambio de ley, acumulación), fundamento legal.

### Incidente de Extinción de la Pena
**Fundamento:** LNEP Arts. 51–60.
**Requisitos:** Sentenciado, pena, causa de extinción (cumplimiento, indulto, amnistía, muerte), documentos probatorios.

### Incidente de Sustitución de la Pena
**Fundamento:** LNEP Arts. 61–70.
**Requisitos:** Sentenciado, pena privativa de libertad, medida sustitutiva propuesta (trabajo en favor de la comunidad, semilibertad, etc.), plan de actividades.

### Solicitud de Libertad Anticipada
**Fundamento:** LNEP Arts. 71–80.
**Requisitos:** Sentenciado, tiempo cumplido, requisitos (conducta, participación en actividades), informe técnico.

### Solicitud de Libertad Preparatoria
**Fundamento:** LNEP Arts. 81–90.
**Requisitos:** Sentenciado, parte de la pena cumplida, buena conducta, informe técnico, plan de libertad.

### Solicitud de Beneficio Penitenciario (Remisión Parcial)
**Fundamento:** LNEP Arts. 91–100.
**Requisitos:** Sentenciado, días de trabajo o estudio, solicitud de remisión de la pena.

### Plan de Actividades para Beneficio
**Requisitos:** Sentenciado, beneficio solicitado, actividades propuestas, horarios, plazos, compromisos.

### Resolución del Juez de Ejecución
**Requisitos:** Incidente o solicitud, antecedentes procesales, consideraciones, determinación fundada.

### Recurso de Apelación (Ejecución Penal)
**Fundamento:** CNPP Arts. 467–484.
**Requisitos:** Resolución del juez de ejecución impugnada, agravios, fundamento legal, firma.

### Informe Técnico Penitenciario
**Requisitos:** Sentenciado, centro penitenciario, evaluación de conducta, estudios psicosociales, recomendaciones.

### Constancia de Cumplimiento de Pena
**Requisitos:** Sentenciado, pena impuesta, fecha de cumplimiento, autoridad emisora, efectos legales.

### Solicitud de Reconocimiento de Prisión Preventiva
**Requisitos:** Sentenciado, tiempo en prisión preventiva, sentencia, cómputo.

### Incidencia de Cómputo de la Pena
**Requisitos:** Sentenciado, sentencia, tiempo de prisión preventiva, redenciones, cálculo de la pena.

### Escrito de Queja por Violación de Derechos Penitenciarios
**Fundamento:** LNEP Arts. 110–120.
**Requisitos:** Sentenciado, violación específica, autoridad penitenciaria, hechos, solicitud.


## 5. Reglas adicionales
- Juez de Ejecución: controla y supervisa las condiciones de cumplimiento de la pena.
- Beneficios penitenciarios: requieren informe técnico favorable.
- Sustitución de pena: procede para penas ≤ 5 años.

---


# Skill: Redactor de Documentos — Derecho Sucesorio
**Fase 16 | 12 tipos de documentos**
Fuentes: CC Federal, CC CDMX, CC Edomex.

---

## 1. Nombre
**"Redactor de documentos de derecho sucesorio"**

## 2. Objetivo
Generar testamentos, inventarios, particiones, adjudicaciones y declaratorias en materia sucesoria.

## 3. Entradas del usuario
- **Documentos subidos** (opcional): testamento, actas de defunción, escrituras, inventarios
- **Datos**: testador/herederos, bienes, albacea, legados

### Lectura de documentos
- Extraer texto de PDF o Word
- Identificar: testador/causante, herederos, bienes, albacea
- Identificar tipo de sucesión (testamentaria/intestamentaria)


## 4. Catálogo de documentos y requisitos

### Testamento Público Abierto
**Fundamento:** CC CDMX Arts. 1511–1541.
**Requisitos:** Testador, testigos, herederos, bienes, albacea, legados, cláusulas especiales.

### Testamento Ológrafo
**Fundamento:** CC CDMX Arts. 1550–1556.
**Requisitos:** Íntegro escrito, fechado y firmado por el testador. Debe depositarse.

### Declaratoria de Herederos (Intestado)
**Fundamento:** CC CDMX Arts. 1368–1455.
**Requisitos:** Acta de defunción, parentesco, declaración de no testamento, solicitud.

### Inventario de Bienes (Sucesorio)
**Requisitos:** Causante, bienes muebles e inmuebles, descripción, valor, pasivos.

### Avalúo de Bienes
**Requisitos:** Bienes, perito valuador, valor comercial.

### Plan de Partición / Proyecto Partitorio
**Requisitos:** Inventario, herederos, proporciones, colación, adjudicación por heredero.

### Adjudicación de Bienes Hereditarios
**Requisitos:** Heredero, bienes adjudicados, proporción, formalización notarial.

### Nombramiento de Albacea
**Requisitos:** Heredero o testador, albacea, aceptación, facultades.

### Rendición de Cuentas del Albacea
**Requisitos:** Albacea, período, ingresos, egresos, saldo.

### Denuncia de Juicio Sucesorio
**Requisitos:** Acta de defunción, parentesco o interés, bienes conocidos.

### Incidente de Liquidación de Legados
**Requisitos:** Legado, legatario, bienes disponibles, forma de entrega.

### Petición de Herencia
**Fundamento:** CC CDMX Arts. 1281–1290.
**Requisitos:** Heredero, bienes, poseedor demandado, título de heredero.




### Testamento Público Abierto
**Fundamento:** CC CDMX Arts. 1511–1541.
**Requisitos:** Testador en pleno uso de facultades, testigos instrumentales (3), herederos y legatarios, inventario de bienes, nombramiento de albacea, cláusulas especiales (sustitución, desheredamiento, dispensa de colación).

### Testamento Público Simplificado (Edomex)
**Fundamento:** CC Edomex.
**Requisitos:** Testador, bienes, herederos, sin necesidad de testigos instrumentales.

### Testamento Ológrafo
**Fundamento:** CC CDMX Arts. 1550–1556.
**Requisitos:** Escrito íntegramente de puño y letra del testador, fechado (año, mes, día en letra) y firmado. Debe depositarse ante notario o juzgado.

### Testamento Cerrado
**Fundamento:** CC CDMX Arts. 1542–1549.
**Requisitos:** Sobre cerrado con el documento firmado, declaración del testador ante notario, testigos.

### Testamento Militar / Marítimo
**Fundamento:** CC CDMX Arts. 1557–1575.
**Requisitos:** Circunstancia especial (campaña, viaje marítimo), autoridad autorizante, disposiciones, testigos.

### Codicilo
**Fundamento:** CC CDMX Arts. 1557–1559.
**Requisitos:** Testador, disposiciones específicas (legados, mandas, reconocimiento de hijos), fecha, firma, testigos.

### Declaratoria de Herederos (Intestado)
**Fundamento:** CC CDMX Arts. 1368–1455.
**Requisitos:** Acta de defunción del autor de la herencia, parentesco del solicitante, declaración de inexistencia de testamento, datos de los demás herederos.

### Inventario de Bienes (Sucesorio)
**Requisitos:** Causante, bienes muebles e inmuebles, descripción detallada, valor estimado, pasivos y deudas.

### Avalúo de Bienes Hereditarios
**Requisitos:** Bienes, perito valuador, metodología, valor comercial por unidad.

### Proyecto de Partición / Plan Partitorio
**Requisitos:** Inventario de bienes, herederos y sus proporciones, colación de donaciones, adjudicación específica por heredero, saldos y compensaciones.

### Nombramiento de Albacea
**Requisitos:** Testador o herederos, persona propuesta, aceptación expresa, facultades (administración, disposición), garantía (si aplica).

### Rendición de Cuentas del Albacea
**Requisitos:** Albacea, período de gestión, ingresos recibidos, egresos realizados, saldo o remanente.

### Solicitud de Intervención del Albacea
**Requisitos:** Heredero, albacea, causa de intervención, solicitud.

### Remoción de Albacea
**Requisitos:** Heredero, albacea, causa legal (negligencia, mala administración, conflicto de intereses), pruebas.

### Adjudicación de Bienes
**Requisitos:** Heredero o legatario, bienes adjudicados, proporción, formalización notarial o judicial.

### Denuncia de Juicio Sucesorio
**Requisitos:** Persona que denuncia, acta de defunción, interés legítimo, bienes conocidos del causante.

### Incidente de Liquidación de Legados
**Requisitos:** Legado específico, legatario, bienes disponibles en la masa hereditaria, forma de entrega.

### Petición de Herencia
**Fundamento:** CC CDMX Arts. 1281–1290.
**Requisitos:** Heredero (título), bienes hereditarios, poseedor demandado, acción reivindicatoria.

### Incidente de Aprobación de Cuentas
**Requisitos:** Albacea, cuentas rendidas, herederos, aprobación judicial.

### Solicitud de Posesión Definitiva de Bienes
**Requisitos:** Heredero declarado, bienes, sentencia de declaratoria, formalización.


## 5. Reglas adicionales
- Testamento público abierto: requiere 3 testigos.
- Herederos forzosos: descendientes, ascendientes y cónyuge.
- Albacea: debe rendir cuentas anualmente o al concluir su gestión.
- Partición: debe respetar las proporciones legales o testamentarias.
- Plazo para aceptar o repudiar herencia: 10 años.

---


# Skill: Redactor de Documentos — Derecho de Género y Familia
**Fase 17 | 11 tipos de documentos**
Fuentes: Ley General de Acceso de las Mujeres a una Vida Libre de Violencia (LGAMVLV.txt), Ley General de Derechos de Niñas, Niños y Adolescentes (LGDNNA.txt), Código Civil del Estado de México (codvig001.txt).

---

## 1. Nombre
**"Redactor de documentos de género y familia"**
(Formato forense — alineaciones, mayúsculas, tabuladores, justificación)

## 2. Objetivo
Generar órdenes de protección, denuncias, querellas y solicitudes en materia de violencia de género, identidad de género, interdicción, alimentos y descuento.

## 3. Entradas del usuario
- **Documentos subidos** (opcional): actas, denuncias previas, dictámenes médicos
- **Datos**: víctima, agresor, menores, hechos de violencia, parentesco

### Lectura de documentos
- Extraer texto de PDF o Word
- Identificar: víctima, imputado, tipo de violencia, medidas de protección
- Identificar relación familiar y menores involucrados


## 5. Catálogo de documentos y requisitos

---

##### 1. Medida de Protección (Orden de Protección)
**Descripción:** Medida urgente para proteger a la víctima de violencia.
**Fundamento:** LGAMVLV Arts. 27–31.
**Requisitos:** Víctima, agresor, hechos de violencia, tipo de medida solicitada.

##### 2. Orden de Protección de Emergencia
**Descripción:** Medida inmediata dictada por el MP o autoridad administrativa.
**Fundamento:** LGAMVLV Art. 27.
**Requisitos:** Riesgo inminente, hechos, medida urgente.

##### 3. Orden de Protección Preventiva
**Descripción:** Medida para prevenir la repetición de la violencia.
**Requisitos:** Hechos de violencia, riesgo de repetición, medida específica.

##### 4. Orden de Protección de Naturaleza Civil
**Descripción:** Medida civil como pensión provisional, guarda o uso del domicilio.
**Fundamento:** LGAMVLV Art. 28.
**Requisitos:** Víctima, agresor, necesidad, tipo de medida civil.

##### 5. Denuncia por Violencia Familiar
**Descripción:** Denuncia ante MP o autoridad administrativa por violencia familiar.
**Fundamento:** LGAMVLV Arts. 16–20.
**Requisitos:** Víctima, agresor, parentesco, hechos cronológicos, pruebas.

##### 6. Querella por Violencia de Género
**Descripción:** Querella por delitos de género perseguibles a petición de parte.
**Requisitos:** Querellante, querellado, hechos, tipo penal, daños.

##### 7. Acta de Nacimiento para Reconocimiento de Identidad de Género
**Descripción:** Rectificación de acta de nacimiento para reconocer identidad de género autopercibida.
**Fundamento:** CC Edomex; CDMX.
**Requisitos:** Nombre anterior y nuevo, CURP, acta original, resolución judicial o administrativa.

##### 8. Solicitud de Rectificación de Acta de Nacimiento (Identidad de Género)
**Descripción:** Solicitud para cambiar nombre y sexo en el acta de nacimiento.
**Requisitos:** Solicitante, acta original, nombre solicitado, documentos de identidad.

##### 9. Escrito de Petición de Declaración de Estado de Interdicción
**Descripción:** Solicitud para declarar incapaz a una persona mayor de edad.
**Fundamento:** CC DF Arts. 450–466.
**Requisitos:** Presunto incapaz, causa, dictamen médico, propuesta de tutor.

##### 10. Convenio de Alimentos
**Descripción:** Acuerdo sobre monto y forma de pago de alimentos.
**Fundamento:** CC DF Arts. 301–323.
**Requisitos:** Acreedor, deudor, parentesco, monto, periodicidad, duración.

##### 11. Orden de Descuento para Alimentos
**Descripción:** Orden al patrón para retener salario por alimentos.
**Requisitos:** Obligado, beneficiario, patrón, porcentaje, monto.

---

## 8. Reglas adicionales
- Órdenes de protección: se dictan de oficio o a petición (LGAMVLV Art. 27).
- Denuncia: 24 horas para inicio de investigación.
- Interdicción: requiere dictamen médico y audiencia del presunto incapaz.

# Skill: Redactor de Documentos — Arbitraje Nacional e Internacional
**Fase 18 | 10 tipos de documentos**
Fuentes: Código de Comercio (CCom.txt), Ley General de Títulos y Operaciones de Crédito (LGTOC.txt), Convención de Nueva York.

---

## 1. Nombre
**"Redactor de documentos de arbitraje"**
(Formato forense/contractual — alineaciones, mayúsculas, tabuladores, justificación)

## 2. Objetivo
Generar acuerdos de arbitraje, solicitudes, laudos, recursos y exhortos internacionales.

## 3. Entradas del usuario
- **Documentos subidos** (opcional): contratos, laudos previos, cláusulas compromisorias
- **Datos**: partes, materia arbitrable, árbitros, sede, ley aplicable

### Lectura de documentos
- Extraer texto de PDF o Word
- Identificar: partes, sede arbitral, institución, ley aplicable
- Identificar cláusula compromisoria o acuerdo de arbitraje


## 5. Catálogo de documentos y requisitos

---

##### 1. Acuerdo de Arbitraje
**Descripción:** Convenio para someter controversias a arbitraje.
**Fundamento:** CCom Arts. 1415–1463.
**Requisitos:** Partes, controversias, institución (CAM, ICC, CANACO, ad hoc), árbitros, sede, idioma, ley aplicable.

##### 2. Solicitud de Arbitraje
**Descripción:** Escrito que inicia el procedimiento arbitral.
**Requisitos:** Partes, acuerdo de arbitraje, controversia, pretensiones, designación de árbitro.

##### 3. Laudo Arbitral
**Descripción:** Resolución final del tribunal arbitral.
**Fundamento:** CCom Arts. 1440–1460.
**Requisitos:** Partes, cuestión decidida, consideraciones, puntos resolutivos, costas, lugar y fecha, firmas.

##### 4. Laudo Parcial
**Descripción:** Laudo que resuelve parte de la controversia antes del laudo final.
**Requisitos:** Mismos que laudo, limitado a la cuestión parcial.

##### 5. Laudo de Procedimiento
**Descripción:** Decisión del tribunal arbitral sobre cuestiones procesales.
**Requisitos:** Cuestión procesal decidida, fundamento, determinación.

##### 6. Recurso de Nulidad de Laudo
**Descripción:** Recurso contra el laudo arbitral por causas taxativas.
**Fundamento:** CCom Arts. 1457–1462.
**Requisitos:** Laudo impugnado, causa de nulidad (incapacidad, acuerdo inválido, falta de notificación, ultra petita, composición irregular, orden público), agravios.

##### 7. Reconocimiento y Ejecución de Laudo Extranjero
**Descripción:** Solicitud para reconocer y ejecutar un laudo extranjero en México.
**Fundamento:** CCom Arts. 1461–1463; Convención de Nueva York.
**Requisitos:** Laudo extranjero (copia certificada), acuerdo de arbitraje, tratado aplicable, solicitud de reconocimiento.

##### 8. Exhorto / Carta Rogatoria Internacional
**Descripción:** Solicitud a autoridad extranjera para práctica de diligencias.
**Requisitos:** Autoridad exhortante y exhortada, diligencias, traducción, apostilla.

##### 9. Solicitud de Restitución Internacional de NNA
**Descripción:** Solicitud de restitución de niña, niño o adolescente sustraído ilícitamente.
**Fundamento:** Convenio de La Haya; CCom.
**Requisitos:** NNA, país de origen, padre/madre solicitante, hechos de sustracción.

##### 10. Solicitud de Videoconferencia (Procesos Internacionales)
**Descripción:** Solicitud para desahogar pruebas por videoconferencia en proceso internacional.
**Requisitos:** Partes, país, testigo/perito, hora y fecha, plataforma.

---

## 8. Reglas adicionales
- Acuerdo de arbitraje: debe constar por escrito (CCom Art. 1423).
- Nulidad: causas taxativas (CCom Art. 1457).
- Laudo extranjero: reconocimiento vía Convención de Nueva York.
- Restitución NNA: 6 semanas para resolver (Convenio de La Haya).

# Skill: Redactor de Documentos — Derechos Humanos
**Fase 18 | 10 tipos de documentos**
Fuentes: Ley de la Comisión Nacional de los Derechos Humanos (LCNDH.txt), CODEX/LCNDH.txt.

---

## 1. Nombre
**"Redactor de documentos en derechos humanos"**
(Formato forense/administrativo — alineaciones, mayúsculas, tabuladores, justificación)

## 2. Objetivo
Generar quejas, recomendaciones, informes y acuerdos ante la CNDH u organismos locales de derechos humanos.

## 3. Entradas del usuario
- **Documentos subidos** (opcional): actos de autoridad reclamados, documentos de soporte
- **Datos**: quejoso, autoridad señalada, violación de derechos humanos, hechos

### Lectura de documentos
- Extraer texto de PDF o Word
- Identificar: quejoso, autoridad señalada, derechos violados
- Identificar tipo de violación y organismo competente


## 5. Catálogo de documentos y requisitos

---

##### 1. Queja ante la CNDH
**Descripción:** Escrito de queja por violación de derechos humanos.
**Fundamento:** LCNDH Arts. 15–30.
**Requisitos:**
- Quejoso (nombre, domicilio)
- Autoridad señalada
- Hechos violatorios
- Derechos humanos violados
- Pruebas (documentales, testimoniales)
- Firma

##### 2. Recomendación de la CNDH
**Descripción:** Recomendación dirigida a la autoridad para reparar la violación.
**Fundamento:** LCNDH Arts. 40–46.
**Requisitos:**
- Autoridad destinataria
- Hechos acreditados
- Derechos violados
- Recomendaciones específicas
- Plazo de cumplimiento

##### 3. Recomendación General
**Descripción:** Recomendación sin caso concreto, sobre prácticas violatorias recurrentes.
**Fundamento:** LCNDH Art. 140.
**Requisitos:**
- Práctica violatoria generalizada
- Autoridades involucradas
- Recomendaciones
- Publicación

##### 4. Informe Especial
**Descripción:** Informe sobre una situación particular de violaciones graves.
**Fundamento:** LCNDH Art. 35.
**Requisitos:**
- Hechos
- Análisis
- Conclusiones
- Propuestas

##### 5. Pronunciamiento
**Descripción:** Posición pública de la CNDH sobre un tema de derechos humanos.
**Requisitos:**
- Tema
- Posición
- Fundamento

##### 6. Exhortación
**Descripción:** Llamado de la CNDH a una autoridad para que cumpla con sus obligaciones.
**Requisitos:**
- Autoridad
- Obligación
- Plazo

##### 7. Acuerdo de Admisión de Queja
**Descripción:** Acuerdo que admite a trámite la queja.
**Requisitos:**
- Queja admitida
- Hechos
- Autoridad señalada
- Medidas cautelares (si proceden)

##### 8. Acuerdo de No Admisión
**Descripción:** Acuerdo que desecha la queja por improcedente.
**Requisitos:**
- Causa de no admisión
- Fundamento
- Orientación al quejoso

##### 9. Acuerdo de Acumulación
**Descripción:** Acumulación de quejas relacionadas.
**Requisitos:**
- Quejas acumuladas
- Hechos conexos
- Expediente principal

##### 10. Informe de Actividades (Anual)
**Descripción:** Informe anual de actividades de la CNDH.
**Requisitos:**
- Período
- Quejas recibidas y resueltas
- Recomendaciones emitidas
- Estadísticas

---

## 8. Reglas adicionales
- Queja: 15 días hábiles desde el acto (prorrogable por causa justificada).
- Recomendaciones: no son vinculantes pero la autoridad debe responder si las acepta (LCNDH Art. 44).

# Skill: Redactor de Documentos — Derecho Migratorio
**Fase 18 | 10 tipos de documentos**
Fuentes: Ley de Migración (LCM.txt), Reglamento de la Ley de Migración, CODEX/LCM.txt.

---

## 1. Nombre
**"Redactor de documentos migratorios"**
(Formato administrativo — alineaciones, mayúsculas, tabuladores, justificación)

## 2. Objetivo
Generar solicitudes, tarjetas, permisos y constancias en materia migratoria.

## 3. Entradas del usuario
- **Documentos subidos** (opcional): pasaporte, actas, comprobantes
- **Datos**: persona, nacionalidad, estatus migratorio, propósito de estancia

### Lectura de documentos
- Extraer texto de PDF o Word
- Identificar: persona, nacionalidad, estatus migratorio
- Identificar propósito de estancia


## 5. Catálogo de documentos y requisitos

---

##### 1. Visa
**Descripción:** Autorización para ingresar a México.
**Fundamento:** LCM Arts. 37–44.
**Requisitos:**
- Persona (nombre, nacionalidad, pasaporte)
- Tipo de visa (turista, trabajo, estudiante, residente)
- Propósito
- Documentos de soporte
- Vigencia

##### 2. Documento de Identidad y Viaje
**Descripción:** Documento para acreditar identidad y estancia regular.
**Requisitos:**
- Persona
- Nacionalidad
- Vigencia
- Fotografía

##### 3. Tarjeta de Residente Temporal
**Descripción:** Permiso de estancia por hasta 4 años.
**Fundamento:** LCM Arts. 51–54.
**Requisitos:**
- Persona
- Oferta de empleo, vínculo familiar u otro causa
- Vigencia
- Permiso de trabajo

##### 4. Tarjeta de Residente Permanente
**Descripción:** Permiso de estancia indefinida.
**Fundamento:** LCM Arts. 55–58.
**Requisitos:**
- Persona
- Causa (4 años como temporal, vínculo familiar, etc.)
- Derechos

##### 5. Tarjeta de Visitante (Sin Permiso de Actividades Remuneradas)
**Descripción:** Estancia temporal sin trabajar.
**Requisitos:**
- Persona
- Propósito
- Vigencia

##### 6. Tarjeta de Visitante (Con Permiso de Actividades Remuneradas)
**Descripción:** Estancia temporal con permiso de trabajo.
**Requisitos:**
- Persona
- Oferta de trabajo
- Vigencia

##### 7. Permiso de Internación
**Descripción:** Permiso para internación por causa humanitaria o asilo.
**Fundamento:** LCM Arts. 60–63.
**Requisitos:**
- Persona
- Causa humanitaria
- Plazo

##### 8. Forma Migratoria
**Descripción:** Formulario de ingreso o salida del país.
**Requisitos:**
- Persona
- Nacionalidad
- Fecha de ingreso/salida
- Tipo de estancia

##### 9. Certificado de Salud (de Origen)
**Descripción:** Certificado médico requerido para trámites migratorios.
**Requisitos:**
- Persona
- Exámenes realizados
- Resultados

##### 10. Constancia de Situación Migratoria
**Descripción:** Documento del INM que certifica el estatus migratorio.
**Requisitos:**
- Persona
- Estancia actual
- Historial migratorio

---

## 8. Reglas adicionales
- Residente temporal: hasta 4 años (LCM Art. 52).
- Residente permanente: indefinido, con permiso de trabajo.
- Visa: se solicita en consulados mexicanos en el extranjero.

# Skill: Redactor de Documentos — Derecho Aduanero
**Fase 21 | 9 tipos de documentos**
Fuentes: Ley Aduanera (LAdua.txt), Reglamento de la Ley Aduanera, CODEX/LAdua.txt.

---

## 1. Nombre
**"Redactor de documentos aduaneros"**
(Formato administrativo — alineaciones, mayúsculas, tabuladores, justificación)

## 2. Objetivo
Generar pedimentos, actas, certificados y órdenes en materia aduanera.

## 3. Entradas del usuario
- **Documentos subidos** (opcional): facturas, conocimientos de embarque, certificados
- **Datos**: importador/exportador, mercancías, valor, origen, destino

### Lectura de documentos
- Extraer texto de PDF o Word
- Identificar: importador/exportador, mercancías, fracción arancelaria
- Identificar valor, origen, destino


## 5. Catálogo de documentos y requisitos

---

##### 1. Pedimento de Importación
**Descripción:** Declaración aduanera para la importación de mercancías.
**Fundamento:** LAdua Arts. 35–46.
**Requisitos:**
- Importador (RFC, nombre)
- Mercancías (fracción arancelaria, descripción, cantidad, valor)
- País de origen
- Incoterm
- Impuestos (IGI, IVA, cuotas compensatorias)
- Factura comercial y documento de embarque

##### 2. Pedimento de Exportación
**Descripción:** Declaración aduanera para la exportación de mercancías.
**Requisitos:**
- Exportador
- Mercancías (fracción, cantidad, valor)
- Destino
- Impuestos (si aplican)

##### 3. Acta de Inicio de Reconocimiento Aduanero
**Descripción:** Acta que inicia el reconocimiento de mercancías en la aduana.
**Fundamento:** LAdua Arts. 43–46.
**Requisitos:**
- Aduana
- Mercancías
- Funcionario designado
- Fecha y hora

##### 4. Acta de Irregularidades
**Descripción:** Acta que registra irregularidades detectadas en el reconocimiento.
**Requisitos:**
- Irregularidades (discrepancias de cantidad, valor, clasificación)
- Mercancías
- Sanciones aplicables

##### 5. Carta Porte (Con Complemento CFDI)
**Descripción:** Documento de transporte de mercancías con complemento fiscal.
**Requisitos:**
- Remitente, porteador, destinatario
- Mercancías
- Origen y destino
- Complemento CFDI de carta porte

##### 6. Conocimiento de Embarque
**Descripción:** Documento del transporte marítimo que acredita recepción de mercancías.
**Requisitos:**
- Cargador, consignatario, transportista
- Mercancías (peso, volumen)
- Puerto de carga y descarga
- Flete

##### 7. Orden de Verificación Vehicular
**Descripción:** Orden para verificar físicamente un vehículo en la aduana.
**Requisitos:**
- Vehículo (VIN, marca, modelo)
- Importador
- Fundamento

##### 8. Certificado de Verificación Vehicular
**Descripción:** Certificado que acredita el resultado de la verificación.
**Requisitos:**
- Vehículo
- Resultado (conforme/no conforme)
- Verificador

##### 9. Acuerdo Migratorio / Despacho Aduanal
**Descripción:** Acuerdo entre autoridades migratorias y aduaneras para el despacho de personas y mercancías.
**Requisitos:**
- Autoridades participantes
- Objeto
- Procedimiento

---

## 8. Reglas adicionales
- Pedimento: debe presentarse electrónicamente ante la aduana (LAdua Art. 36).
- Reconocimiento aduanero: primera y segunda vista (LAdua Arts. 43–44).
- Irregularidades: pueden generar multas del 30% al 130% del valor de la mercancía.
- Carta porte CFDI: obligatoria para transporte de mercancías (SAT).

# Skill: Redactor de Documentos — Procesos Concursales y Quiebra
**Fase 22 | 8 tipos de documentos**
Fuentes: Código de Comercio (CCom.txt), Ley de Concursos Mercantiles, CODEX/CCom.txt.

---

## 1. Nombre
**"Redactor de documentos concursales y de quiebra"**
(Formato forense — alineaciones, mayúsculas, tabuladores, justificación)

## 2. Objetivo
Generar solicitudes, resoluciones, convenios y sentencias en procesos de concurso mercantil y quiebra.

## 3. Entradas del usuario
- **Documentos subidos** (opcional): estados financieros, listas de acreedores, contratos
- **Datos**: comerciante, acreedores, pasivos, activos, incumplimiento

### Lectura de documentos
- Extraer texto de PDF o Word
- Identificar: comerciante, acreedores, pasivos, activos
- Identificar tipo de incumplimiento


## 5. Catálogo de documentos y requisitos

---

##### 1. Solicitud de Concurso Mercantil
**Descripción:** Solicitud del comerciante o del acreedor para declarar el concurso mercantil.
**Fundamento:** CCom Arts. 960–1016; LCM.
**Requisitos:**
- Solicitante (comerciante o acreedor)
- Datos del comerciante
- Incumplimiento generalizado de obligaciones
- Estados financieros
- Relación de acreedores y montos
- Causa del incumplimiento

##### 2. Auto de Inicio del Proceso Concursal
**Descripción:** Auto del juez que admite la solicitud e inicia el concurso.
**Requisitos:**
- Comerciante declarado en concurso
- Designación de visitador o conciliador
- Plazo para la conciliación
- Medidas cautelares

##### 3. Resolución de Concurso Mercantil
**Descripción:** Declaración formal de concurso mercantil.
**Requisitos:**
- Comerciante
- Fecha de declaración
- Efectos legales

##### 4. Acuerdo de Acreedor Reconocido
**Descripción:** Reconocimiento de créditos de cada acreedor.
**Requisitos:**
- Acreedor
- Crédito (monto, grado, preferencia)
- Documentos de soporte

##### 5. Convenio Concursal
**Descripción:** Acuerdo entre el comerciante y sus acreedores para pago de adeudos.
**Fundamento:** CCom Arts. 1017–1040.
**Requisitos:**
- Comerciante
- Acreedores que lo suscriben
- Porcentaje de pago
- Plazos
- Garantías
- Mayoría requerida

##### 6. Plan de Reestructura
**Descripción:** Plan para la reestructura financiera y operativa del comerciante.
**Requisitos:**
- Medidas de reestructura
- Plazo
- Proyecciones financieras

##### 7. Sentencia de Quiebra
**Descripción:** Declaración de quiebra cuando fracasa la conciliación.
**Fundamento:** CCom Arts. 1041–1100.
**Requisitos:**
- Comerciante declarado en quiebra
- Causa (falta de convenio, incumplimiento)
- Designación de síndico
- Efectos (administración, liquidación)

##### 8. Inventario de la Masa Concursal
**Descripción:** Relación detallada de activos del comerciante en concurso.
**Requisitos:**
- Activos (bienes muebles e inmuebles, créditos)
- Pasivos
- Avalúo

---

## 8. Reglas adicionales
- Concurso mercantil: procede cuando el comerciante incumple generalizadamente sus obligaciones (CCom Art. 960).
- Convenio concursal: requiere aprobación de la mayoría de acreedores.
- Quiebra: conlleva la liquidación de activos para pago de acreedores.

# Skill: Redactor de Documentos — Protección de Datos Personales
**Fase 23 | 7 tipos de documentos**
Fuentes: Ley Federal de Protección de Datos Personales en Posesión de los Particulares (LFPDPPP.txt), Reglamento de la LFPDPPP, CODEX/LFPDPPP.txt.

---

## 1. Nombre
**"Redactor de documentos de protección de datos personales"**
(Formato administrativo — alineaciones, mayúsculas, tabuladores, justificación)

## 2. Objetivo
Generar avisos de privacidad, solicitudes ARCO, revocaciones y resoluciones del INAI.

## 3. Entradas del usuario
- **Documentos subidos** (opcional): avisos previos, identificaciones, formatos INAI
- **Datos**: titular, responsable, datos personales, derechos ARCO

### Lectura de documentos
- Extraer texto de PDF o Word
- Identificar: titular, responsable, datos personales
- Identificar derechos ARCO y tipo de solicitud


## 5. Catálogo de documentos y requisitos

---

##### 1. Aviso de Privacidad
**Descripción:** Documento que informa al titular sobre el tratamiento de sus datos personales.
**Fundamento:** LFPDPPP Arts. 8–16.
**Requisitos:**
- Responsable (nombre, domicilio)
- Datos recabados
- Finalidades del tratamiento
- Transferencias (si aplican)
- Derechos ARCO
- Procedimiento para ejercicio de derechos
- Cambios al aviso de privacidad

##### 2. Solicitud de Acceso a Datos Personales (ARCO)
**Descripción:** Solicitud para conocer qué datos personales tiene el responsable.
**Fundamento:** LFPDPPP Arts. 28–36.
**Requisitos:**
- Titular (nombre, identificación)
- Responsable
- Datos a los que se solicita acceso
- Modalidad de entrega
- Firma

##### 3. Solicitud de Rectificación de Datos Personales
**Descripción:** Solicitud para corregir datos personales inexactos o incompletos.
**Requisitos:**
- Titular
- Dato a rectificar
- Dato correcto
- Prueba de inexactitud

##### 4. Solicitud de Cancelación de Datos Personales
**Descripción:** Solicitud para cancelar datos personales del tratamiento.
**Requisitos:**
- Titular
- Datos a cancelar
- Causa de cancelación

##### 5. Solicitud de Oposición al Tratamiento
**Descripción:** Solicitud para oponerse al tratamiento de datos personales.
**Requisitos:**
- Titular
- Datos
- Causa legítima
- Daño o afectación

##### 6. Escrito de Revocación de Consentimiento
**Descripción:** Revocación del consentimiento otorgado para el tratamiento de datos.
**Fundamento:** LFPDPPP Art. 8.
**Requisitos:**
- Titular
- Responsable
- Datos
- Fecha de revocación

##### 7. Resolución del INAI
**Descripción:** Resolución del INAI que determina procedencia de una solicitud ARCO o revocación.
**Fundamento:** LFPDPPP Arts. 37–44.
**Requisitos:**
- Solicitud ARCO
- Determinación (procedente/improcedente)
- Plazo de cumplimiento
- Fundamento

---

## 8. Reglas adicionales
- Aviso de privacidad: debe ponerse a disposición del titular (LFPDPPP Art. 8).
- Derechos ARCO: acceso, rectificación, cancelación y oposición.
- Plazo: 20 días hábiles para respuesta del responsable (LFPDPPP Art. 32).
- INAI: Instituto Nacional de Transparencia, Acceso a la Información y Protección de Datos Personales.
---

#### EJEMPLO DE INICIO DE DEMANDAS Y ESCRITOS CON ABOGADOS, PASANTES, ESTDUIANTES  Y CEDULAS REALES, CON LA DIRECCION DE CORREO ELETRÓNICO REAL

```
[NOMBRE COMPLETO QUEJOSO], por mi propio derecho, señalando como domicilio para oír y recibir notificaciones [DOMICILIO SI EXISTE], y señalando el correo electrónico 11589824@pjdomex.gob para recibir notificaciones electrónicas, así como autorizando para oír y recibir todo tipo de notificaciones, aun las de carácter personal y documentos, menos valores, a los Licenciados en Derecho VÍCTOR ANTONIO TREJO CHÁVEZ (cédula profesional 11589824), LUIS ALBERTO TORRES MARTÍNEZ (cédula profesional 13480425), ARTURO PÉREZ TORRES (cédula profesional 7366833) y MARTHA MERCADO ARAIZA, y a los pasantes y estudiantes de derecho EDMUNDO MIGUEL QUINTERO TREJO, ERIKA ADRIANA ROCHA REYES, RODRIGO QUINTANAR CASILLAS y ÁNGEL LÓPEZ AVIÑA, con fundamento en los artículos [AQUI DERECHO CORRESPONDIENTE]; así mismo, solicito tener acceso al expediente por medio del TRIBUNAL ELECTRÓNICO, manifestando que la presente promoción se suscribe con la Firma Electrónica Avanzada correspondiente, ante Usted, con el debido respeto, comparezco y expongo:
```  
- ESTOS SON LOS ABOGADOS Y PERSONAL AUTORIZADO QUE SIEMPRE SE DEBE PONER, JUNTO CON CEDULA Y CORREO.






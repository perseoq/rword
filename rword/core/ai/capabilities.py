"""Capacidades de IA: escritura inteligente y corrección avanzada."""

from __future__ import annotations

from rword.core.ai.session import build_messages


def _chat(client, prompt: str, context: str = "", temperature: float = 0.7,
          max_tokens: int = 2048) -> str:
    messages = build_messages(prompt, context)
    return client.chat(messages, temperature=temperature, max_tokens=max_tokens)


# --- Escritura inteligente -------------------------------------------------

def redact(client, instruction: str, context: str = "") -> str:
    return _chat(client, f"Redacta un texto a partir de esta instrucción: {instruction}", context)


def continue_writing(client, text: str) -> str:
    return _chat(
        client,
        "Continúa el siguiente texto de forma natural y coherente:",
        text,
    )


def complete_sentence(client, text: str) -> str:
    return _chat(client, "Completa la frase de forma natural:", text)


def rewrite(client, text: str, instruction: str) -> str:
    return _chat(
        client,
        f"Reescribe el siguiente texto. {instruction} Devuelve solo el texto resultante.",
        text,
    )


def change_tone(client, text: str, tone: str) -> str:
    return rewrite(client, text, f"Cambia el tono a: {tone}.")


def summarize(client, text: str) -> str:
    return _chat(client, "Resume el siguiente texto en un párrafo claro y conciso:", text)


def expand(client, text: str) -> str:
    return _chat(client, "Expande el siguiente texto añadiendo detalles y ejemplos:", text)


def reduce_text(client, text: str) -> str:
    return _chat(client, "Reduce el siguiente texto conservando las ideas clave:", text)


def simplify(client, text: str) -> str:
    return _chat(client, "Simplifica el lenguaje del siguiente texto:", text)


def make_professional(client, text: str) -> str:
    return rewrite(client, text, "Haz el texto más profesional.")


def make_persuasive(client, text: str) -> str:
    return rewrite(client, text, "Haz el texto más persuasivo.")


def make_friendly(client, text: str) -> str:
    return rewrite(client, text, "Haz el texto más amigable.")


def make_neutral(client, text: str) -> str:
    return rewrite(client, text, "Haz el texto más neutral y objetivo.")


def adapt_audience(client, text: str, audience: str) -> str:
    return rewrite(client, text, f"Adapta el texto para {audience}.")


# --- Corrección avanzada ---------------------------------------------------

def correct(client, text: str) -> str:
    return _chat(
        client,
        "Corrige ortografía, gramática y puntuación. Devuelve únicamente el texto corregido.",
        text,
        temperature=0.2,
    )


def detect_redundancies(client, text: str) -> str:
    return _chat(
        client,
        "Detecta redundancias, muletillas y repeticiones. Devuelve una lista breve.",
        text,
        temperature=0.2,
    )


def suggest_better_words(client, text: str) -> str:
    return _chat(
        client,
        "Sugiere mejores palabras para el siguiente texto y explica brevemente.",
        text,
    )


def improve_fluidity(client, text: str) -> str:
    return rewrite(client, text, "Mejora la fluidez y cohesión del texto.")


def improve_clarity(client, text: str) -> str:
    return rewrite(client, text, "Mejora la claridad del texto.")


def detect_ambiguities(client, text: str) -> str:
    return _chat(
        client,
        "Detecta ambigüedades y frases demasiado largas. Devuelve una lista breve.",
        text,
    )


# --- Traducción ------------------------------------------------------------

def translate(client, text: str, target_language: str) -> str:
    return _chat(
        client,
        f"Traduce el siguiente texto a {target_language} manteniendo el significado. "
        "Devuelve únicamente la traducción:",
        text,
        temperature=0.2,
    )


def detect_language(client, text: str) -> str:
    return _chat(
        client,
        "Detecta el idioma del siguiente texto y responde con el nombre del idioma.",
        text,
        temperature=0.1,
        max_tokens=64,
    )


# --- Análisis del documento ------------------------------------------------

def main_ideas(client, text: str) -> str:
    return _chat(client, "Extrae las ideas principales del siguiente texto:", text)


def extract_conclusions(client, text: str) -> str:
    return _chat(client, "Extrae las conclusiones del siguiente texto:", text)


def detect_inconsistencies(client, text: str) -> str:
    return _chat(
        client,
        "Detecta inconsistencias, contradicciones e información faltante. "
        "Devuelve una lista breve.",
        text,
        temperature=0.2,
    )


def reading_difficulty(client, text: str) -> str:
    return _chat(
        client,
        "Calcula la dificultad de lectura del texto y explica brevemente.",
        text,
        temperature=0.2,
    )


def target_audience(client, text: str) -> str:
    return _chat(
        client,
        "Identifica el público objetivo del siguiente texto.",
        text,
        temperature=0.2,
    )


def classify_document(client, text: str) -> str:
    return _chat(
        client,
        "Clasifica el tipo de documento (informe, contrato, carta, artículo...) "
        "y justifica brevemente.",
        text,
        temperature=0.2,
    )


def executive_summary(client, text: str) -> str:
    return _chat(
        client,
        "Genera un resumen ejecutivo del siguiente texto.",
        text,
    )


# --- Operaciones sobre la selección ----------------------------------------

def explain(client, text: str) -> str:
    return _chat(client, "Explica el siguiente texto de forma clara:", text)


def generate_questions(client, text: str) -> str:
    return _chat(
        client,
        "Genera preguntas de comprensión sobre el siguiente texto:",
        text,
    )


def answer_question(client, document: str, question: str) -> str:
    return _chat(
        client,
        f"Responde a la pregunta usando únicamente el contenido del documento. "
        f"Pregunta: {question}",
        document,
        temperature=0.3,
    )


# --- Dominios especializados: Legal ----------------------------------------

def draft_contract(client, instruction: str, context: str = "") -> str:
    return _chat(
        client,
        f"Redacta un contrato profesional a partir de la instrucción: {instruction}",
        context,
    )


def review_clauses(client, contract_text: str) -> str:
    return _chat(
        client,
        "Revisa el contrato y detecta cláusulas abusivas o riesgos legales. "
        "Devuelve una lista con recomendaciones.",
        contract_text,
        temperature=0.2,
    )


def legal_risks(client, contract_text: str) -> str:
    return _chat(
        client,
        "Identifica los riesgos legales del siguiente contrato:",
        contract_text,
        temperature=0.2,
    )


def explain_law(client, article: str) -> str:
    return _chat(client, "Explica en términos sencillos el siguiente artículo o norma:", article)


def compare_contracts(client, text_a: str, text_b: str) -> str:
    return _chat(
        client,
        "Compara los dos contratos, resume las diferencias importantes "
        "y sugiere un documento unificado.",
        f"Contrato A:\n{text_a}\n\nContrato B:\n{text_b}",
        temperature=0.2,
    )


def summarize_contract(client, contract_text: str) -> str:
    return _chat(
        client,
        "Resume el contrato destacando las obligaciones de cada parte:",
        contract_text,
    )


# --- Programación ----------------------------------------------------------

def format_code(client, code: str) -> str:
    return _chat(
        client,
        "Formatea el siguiente código con un estilo limpio:",
        code,
        temperature=0.2,
    )


def explain_code(client, code: str) -> str:
    return _chat(client, "Explica qué hace el siguiente código:", code)


def generate_code(client, instruction: str) -> str:
    return _chat(client, f"Genera el código necesario para: {instruction}", temperature=0.3)


def convert_language(client, code: str, target: str) -> str:
    return _chat(client, f"Convierte el siguiente código a {target}:", code, temperature=0.2)


def document_function(client, code: str) -> str:
    return _chat(client, "Documenta la siguiente función con comentarios y docstring:", code)


def detect_code_errors(client, code: str) -> str:
    return _chat(client, "Detecta errores y sugiere correcciones en el siguiente código:", code)


def optimize_code(client, code: str) -> str:
    return _chat(client, "Optimiza el siguiente código para mejorar su rendimiento:", code)


def sql_query(client, instruction: str) -> str:
    return _chat(client, f"Escribe una consulta SQL para: {instruction}", temperature=0.2)


# --- Educación --------------------------------------------------------------

def explain_concept(client, concept: str) -> str:
    return _chat(client, "Explica el siguiente concepto de forma clara y con ejemplos:", concept)


def generate_exercises(client, topic: str, count: int = 5) -> str:
    return _chat(
        client, f"Genera {count} ejercicios sobre: {topic}", temperature=0.4
    )


def solve_problem(client, problem: str) -> str:
    return _chat(client, "Resuelve el siguiente problema paso a paso:", problem)


def create_quiz(client, topic: str, count: int = 5) -> str:
    return _chat(
        client, f"Crea un cuestionario de {count} preguntas sobre: {topic}",
        temperature=0.4,
    )


def create_flashcards(client, topic: str, count: int = 10) -> str:
    return _chat(
        client,
        f"Crea {count} tarjetas de repaso (pregunta/respuesta) sobre: {topic}",
        temperature=0.4,
    )


# --- Negocios ---------------------------------------------------------------

def write_proposal(client, instruction: str) -> str:
    return _chat(client, f"Redacta una propuesta comercial profesional para: {instruction}")


def write_email(client, instruction: str) -> str:
    return _chat(client, f"Redacta un correo electrónico profesional para: {instruction}")


def meeting_minutes(client, text: str) -> str:
    return _chat(client, "Genera una minuta de reunión a partir de las notas:", text)


def executive_report(client, text: str) -> str:
    return _chat(client, "Genera un reporte ejecutivo a partir de los datos:", text)


# --- Investigación ----------------------------------------------------------

def research(client, query: str) -> str:
    return _chat(client, f"Investiga sobre el tema y sintetiza la información: {query}")


def generate_bibliography(client, text: str) -> str:
    return _chat(
        client,
        "Genera una bibliografía en formato académico a partir del texto:",
        text,
    )

import httpx
import json
from schemas import MeetingResponse
import logging
import os
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:latest"

logger = logging.getLogger(__name__)

def save_to_markdown(minuta: MeetingResponse, filepath: str):
    """
    Guarda la minuta estructurada en un archivo Markdown con formato profesional.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    m = minuta.reunion
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# {m.titulo}\n\n")
        f.write(f"**Fecha:** {m.fecha}\n\n")
        
        f.write("## Resumen Ejecutivo\n")
        f.write(f"{m.resumen_ejecutivo}\n\n")
        
        if m.objetivo:
            f.write("## Objetivo Principal\n")
            f.write(f"{m.objetivo}\n\n")
        
        f.write("## Participantes\n")
        for p in m.participantes:
            f.write(f"- **{p.nombre}** ({p.rol})\n")
        f.write("\n")
        
        f.write("## Temas Discutidos\n")
        for t in m.temas:
            f.write(f"### {t.titulo}\n")
            if t.puntos_clave:
                f.write("**Puntos Clave:**\n")
                for pk in t.puntos_clave:
                    f.write(f"- {pk}\n")
            if t.decisiones:
                f.write("**Decisiones:**\n")
                for d in t.decisiones:
                    f.write(f"- {d}\n")
            f.write("\n")
            
        if m.requerimientos:
            f.write("## Requerimientos Detectados\n")
            for req in m.requerimientos:
                f.write(f"- {req}\n")
            f.write("\n")
            
        f.write("## Tareas Asignadas\n")
        for tarea in m.tareas:
            fecha_lim = f" (Límite: {tarea.fecha_limite})" if tarea.fecha_limite else ""
            f.write(f"- [ ] **{tarea.descripcion}** - Responsable: {tarea.responsable} - Prioridad: {tarea.prioridad}{fecha_lim}\n")
        f.write("\n")
        
        if m.riesgos:
            f.write("## Riesgos Identificados\n")
            for riesgo in m.riesgos:
                f.write(f"- {riesgo}\n")
            f.write("\n")
            
        if m.pendientes:
            f.write("## Temas Pendientes / Bloqueos\n")
            for pen in m.pendientes:
                f.write(f"- {pen}\n")
            f.write("\n")
        
        f.write("## Próximos Pasos\n")
        for paso in m.proximos_pasos:
            f.write(f"- {paso}\n")

async def extract_structured_minutes(transcript: str) -> str:
    """
    Extrae la minuta en formato Markdown puro, forzando la detección de nombres y roles.
    """
    prompt = f"""
    Eres un analista experto en ingeniería aeroespacial y gestión de proyectos técnicos. 
    Tu tarea es generar una minuta de reunión extremadamente precisa basada en la transcripción adjunta.

    INSTRUCCIONES DE FORMATO:
    1. Identifica a TODOS los participantes que hablan o son mencionados.
    2. Usa tablas de Markdown para las 'Tareas Asignadas'.
    3. No dejes el campo 'Responsable' vacío; usa el nombre de la persona detectada.
    4. Responde DIRECTAMENTE con el contenido en Markdown, empezando con el título (#).
    5. No incluyas introducciones, saludos ni comentarios adicionales.

    SECCIONES REQUERIDAS:
    # [Título de la Reunión]
    **Fecha:** [Extraer fecha]
    **Participantes:** [Listar nombres y roles, ej: Laura (Líder Proyecto)]

    ## 1. Resumen Ejecutivo
    ## 2. Temas Discutidos (con viñetas técnicas detalladas)
    
    ## 3. Tareas Asignadas
    | Tarea | Responsable | Prioridad | Estado |
    | :--- | :--- | :--- | :--- |
    | [Descripción de la tarea] | [Nombre del responsable] | [Alta/Media/Baja] | [ ] |

    ## 4. Próximos Pasos

    TRANSCRIPCIÓN:
    {transcript}
    """

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": 3000,
            "temperature": 0.1,  # Estricto para no perder nombres
            "top_p": 0.9
        }
    }

    try:
        async with httpx.AsyncClient(timeout=1200.0) as client:
            response = await client.post(OLLAMA_URL, json=payload)
            response.raise_for_status()
            content = response.json().get("response", "").strip()
            
            # Limpiador: Asegura que el Markdown empiece en el primer título relevante
            indicadores = ["# ", "**Participantes", "**Fecha"]
            for ind in indicadores:
                pos = content.find(ind)
                if pos != -1:
                    content = content[pos:]
                    break
                    
            return content
            
    except Exception as e:
        logger.error(f"Error procesando con Ollama: {e}")
        raise e

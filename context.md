# Contexto del Proyecto: Minutas-IA V1

## Objetivo
Desarrollar un asistente de reuniones de escritorio (Desktop App) enfocado en la privacidad (Local-First) y en la generación de inteligencia de negocio estructurada a partir de documentos y audio.

## Lecciones Aprendidas (Transferred from Previous Prototype)

1.  **Gestión de Memoria (Hardware de 8GB RAM):**
    *   Los modelos de 2B-3B parámetros (Qwen 2.5:3B, Llama 3.2:3B) son el "sweet spot" entre razonamiento y consumo para máquinas locales.
    *   Evitar base de datos de grafos pesadas (como Neo4j) inicialmente; priorizar SQLite y VectorDB ligero.

2.  **Procesamiento de Documentos Largos (Chunking):**
    *   La fragmentación del texto es obligatoria para evitar el olvido semántico por límites de contexto del LLM.
    *   Un solapamiento (overlap) del 10-15% ayuda a mantener la continuidad entre ideas divididas.

3.  **Estabilidad de la Interfaz:**
    *   Confiar en el "Zero-shot" para JSON es arriesgado. Se requiere validación estricta de salida (Pydantic / Instructor) para alimentar el frontend sin errores.

4.  **Arquitectura de Red (Docker):**
    *   La comunicación entre contenedores (n8n, FastAPI, Ollama) requiere una configuración de red explícita y variables de entorno robustas para evitar errores de conexión (SSRF).

5.  **Captura de Audio:**
    *   El paso de web app a aplicación nativa (Desktop) es necesario para capturar audio del sistema/drivers sin complicaciones técnicas para el usuario final.

## Estructura Inicial
- `backend/`: API central en FastAPI.
  - `agent/`: Lógica de agentes heredada del prototipo.
  - `.venv/`: Entorno virtual Python (en proceso).
- `frontend/`: Aplicación en Next.js (propuesta para Tauri).
- `shared/`: Modelos de datos y esquemas comunes.

## Próximos Pasos
1. Finalizar la creación del entorno virtual en `backend/`.
2. Definir el esquema JSON maestro para las minutas.
3. Crear el primer endpoint de FastAPI para procesamiento de documentos.

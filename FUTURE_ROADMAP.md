# 🚀 Roadmap & Trabajo Futuro (Performance API)

Este documento enumera las oportunidades de mejora arquitectónica para la versión **V1 (FastAPI + React)**. El objetivo es que los próximos desarrolladores puedan llevar la velocidad y la experiencia de usuario (UX) al siguiente nivel, especialmente al lidiar con documentos de Word inmensos.

## 1. Streaming de Respuesta (Server-Sent Events)
Actualmente, el backend de FastAPI espera a que Ollama termine de procesar el JSON completo (lo que puede demorar decenas de minutos en textos masivos) antes de enviar la respuesta HTTP al Frontend de React.
- **Propuesta:** Implementar Server-Sent Events (SSE) o WebSockets en FastAPI.
- **Impacto UX:** El usuario final no verá un spinner de "Cargando..." durante 30 minutos. En su lugar, verá cómo la minuta se va escribiendo en la pantalla de React palabra por palabra (efecto máquina de escribir, igual que en ChatGPT). Esto elimina por completo la ansiedad del usuario y la sensación de "el sistema se colgó".

## 2. Decodificación Restringida (Instructor Library)
Actualmente, utilizamos Pydantic para validar que el JSON que escupe Ollama sea correcto. Si el modelo se equivoca en una coma, Pydantic rechaza el JSON y obliga a Ollama a re-procesar todo el texto de nuevo, duplicando el tiempo de procesamiento.
- **Propuesta:** Integrar la librería [Instructor para Python](https://python.useinstructor.com/) o habilitar el modo `format: "json"` estructurado (Constrained Decoding) directo en la API de Ollama.
- **Impacto:** Ollama es forzado matemáticamente a escupir tokens que coincidan *únicamente* con el esquema JSON predefinido. Esto reduce los errores de validación a **0%**, eliminando los costosos reintentos de procesamiento y bajando los tiempos a la mitad.

## 3. Barras de Progreso en Tiempo Real (Chunking Feedback)
Cuando el backend realiza *Smart Chunking* para dividir un documento de 50 páginas en 10 partes más pequeñas, el frontend no se entera de esto.
- **Propuesta:** Que el enrutador de FastAPI emita eventos asíncronos cada vez que un *Chunk* finaliza.
- **Impacto UX:** La interfaz de React puede mostrar una barra de progreso real: `"Analizando página 15 de 50 (30% completado)..."`. Esto otorga transparencia total sobre la performance real del motor.

## 4. Vectorización Diferida (RAG Local)
Para evitar saturar los 32GB de RAM leyendo documentos completos en cada petición.
- **Propuesta:** Incorporar una base de datos vectorial local (ej. ChromaDB o FAISS en memoria) dentro de FastAPI.
- **Impacto:** Si un usuario sube un pliego de condiciones de 100 páginas, el backend primero lo vectoriza. Luego, usa LLM en modo RAG para preguntarle a la base de datos: *"Extrae únicamente los compromisos de fecha"*. El LLM procesará solo los 3 párrafos relevantes en lugar de leer el documento entero, reduciendo el procesamiento de 40 minutos a apenas unos **segundos**.

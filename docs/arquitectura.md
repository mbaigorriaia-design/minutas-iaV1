# Documentación de Minutas-IA V1

Este documento explica la arquitectura y el funcionamiento interno del proyecto **Minutas-IA V1**.

## Arquitectura General

El proyecto está diseñado como una aplicación de escritorio **Local-First**, lo que significa que el procesamiento de datos ocurre en tu propia máquina para garantizar la privacidad total.

### Componentes Principales:
1.  **Frontend (Próximamente):** Una interfaz moderna desarrollada en Next.js (que se empaquetará con Tauri) para permitir la interacción del usuario y la captura de documentos de Word.
2.  **Backend (FastAPI):** El cerebro del sistema. Escrito en Python, gestiona las solicitudes de procesamiento y la lógica de negocio.
3.  **Motor de IA (Ollama):** Un servidor local que corre modelos de lenguaje (LLMs) como Llama 3.2 o SmolLM2. Funciona dentro de un contenedor Docker para aislar sus dependencias.

## Flujo de Trabajo

Cuando se procesa una minuta, el sistema sigue estos pasos:

1.  **Ingesta de Datos:** El usuario envía una transcripción de texto a través del endpoint `/process`.
2.  **Preparación del Prompt:** El Backend toma el texto y lo envuelve en un "Prompt Maestro" que define exactamente qué información extraer (Participantes, Decisiones, Tareas).
3.  **Procesamiento de IA:** Se envía la solicitud a Ollama. El modelo procesa el lenguaje natural y genera una respuesta obligatoriamente formateada como JSON.
4.  **Validación:** El Backend valida que el JSON recibido cumpla con el esquema definido en `schemas.py` (usando Pydantic).
5.  **Entrega:** Se devuelve una respuesta estructurada lista para ser mostrada en la interfaz o guardada en la base de datos.

## Configuración para Hardware de 32GB RAM

Para asegurar que el sistema funcione en equipos con recursos limitados, hemos implementado las siguientes estrategias:

-   **Modelos Pequeños:** Uso de modelos de entre 1B y 3B parámetros (ej. Llama 3.2 o SmolLM2).
-   **Timeouts Extendidos:** Se han configurado tiempos de espera de hasta 5 minutos para permitir que la CPU procese sin cortar la conexión.
-   **Keep-Alive:** Ollama mantiene el modelo cargado en memoria durante 60 minutos para evitar esperas repetitivas de carga.

## Desarrollo Actual
- **Estado:** Backend funcional con endpoints `/process` y `/process-dummy`.
- **Puerto:** `8000`
- **Modelos Recomendados:**
  - `llama3.2:latest` (Alta calidad - más lento)
  - `smollm2:1.7b` (Alta velocidad - recomendado para 32GB)

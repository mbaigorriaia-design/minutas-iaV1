# 🚀 Minutas-IA V1 (Desktop Edition)

<div align="center">
  <p><strong>Guía de Arquitectura y Mantenimiento para Desarrolladores</strong></p>
</div>

---

Bienvenido al repositorio de **Minutas-IA V1**. Este documento es la guía técnica de traspaso para que cualquier desarrollador pueda tomar el proyecto, entender sus decisiones de diseño y continuar su mantenimiento fácilmente.

Esta versión **abandona los orquestadores web (como n8n) en favor de una arquitectura App moderna** (FastAPI + React), pensada para ser compilada como una aplicación de escritorio nativa que funcione 100% de manera local y autónoma.

## 🏗️ La Arquitectura V1 (¿Por qué cambió?)

La versión anterior (Legacy) funcionaba bien en servidores grandes, pero en V1 el objetivo es operar en **hardware restringido (8GB RAM)**. Por ende, la arquitectura migró a:

1. **Backend Ligero (`FastAPI` / Python)**
   - Gestiona toda la lógica pesada, enrutamiento y Chunking de documentos.
   - En lugar de confiar ciegamente en el LLM para generar JSON, utiliza **Pydantic** para estructurar un *contrato de datos estricto*. Si el LLM alucina un formato, el backend lo intercepta y reintenta.
2. **Frontend Reactivo (`Next.js` / React)**
   - UI limpia y rápida, diseñada con vistas a ser empaquetada mediante frameworks de escritorio (ej. Tauri/Electron).
3. **Motor de IA (`Ollama`)**
   - Utilizamos modelos de rango 2B-3B (ej. `Llama 3.2:3B` o `Qwen 2.5:3B`). Son el balance perfecto entre razonamiento inteligente y consumo de RAM para que la PC del usuario final no colapse.

## 📂 Dónde Encontrar las Cosas (Estructura)

- `backend/`: Aquí vive FastAPI. Cualquier cambio en la extracción semántica, el algoritmo de Chunking o el esquema JSON va aquí.
  - `backend/agent/`: Lógica de comunicación con el LLM.
- `frontend/`: Aplicación Single Page Application en Next.js.
- `shared/`: Modelos de datos (tipos) compartidos entre Front y Back para mantener coherencia de contratos.
- `INICIAR_MINUTAS.bat`: Script maestro para levantar todo el entorno de un solo clic.

## 🚀 Cómo Levantar el Entorno Local

```bash
# 1. Clona el proyecto
git clone https://github.com/mbaigorriaia-design/minutas-iaV1.git
cd minutas-iaV1

# 2. Ejecuta el script de inicio
./INICIAR_MINUTAS.bat
```
*(Nota: Asegúrate de tener instalado Ollama en tu máquina y el modelo base descargado usando `ollama run qwen2.5:3b`)*

## ⚠️ Guía de Resolución de Problemas (Troubleshooting)

1. **Memoria Insuficiente (OOM) al procesar un audio:**
   - Si la aplicación crashea, significa que el tamaño del *Chunk* enviado al LLM excede la ventana de contexto o la RAM física de la laptop. Debes ajustar el porcentaje de *overlap* (10-15%) o el tamaño del paquete en el script de Chunking del `backend`.
2. **El Frontend no recibe el JSON esperado:**
   - La validación de *Pydantic* probablemente está rechazando una alucinación del LLM. Revisa los logs de FastAPI (`backend`). Para arreglarlo, ajusta el *System Prompt* en la lógica del Agente para ser más explícito con el formato requerido.
3. **El modelo genera basura léxica:**
   - Asegúrate de que el modelo configurado en Ollama sea el correcto (idealmente Qwen 2.5 para español o Llama 3.2). Los modelos de 1B de parámetros suelen "romperse" semánticamente en español; **usa siempre versiones de 3B**.

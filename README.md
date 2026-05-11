<div align="center">
  <h1>🚀 Minutas-IA V1 (Desktop Edition)</h1>
  <p><strong>El asistente definitivo de reuniones local-first. Captura, transcribe y estructura inteligencia de negocios sin depender de la nube.</strong></p>
</div>

---

## 🎯 ¿Qué es Minutas-IA V1?
Minutas-IA V1 es la evolución hacia una arquitectura nativa de escritorio enfocada 100% en la privacidad (Local-First). Diseñada para operar de manera autónoma incluso en hardware restringido (8GB RAM), transforma transcripciones de audio y documentos en JSON estrictamente estructurado mediante modelos LLM optimizados ejecutándose en tu propia máquina.

## ✨ Características Principales
- 🔒 **Zero-Cloud & Privacy First**: Todo el procesamiento (audio, texto, LLM) ocurre localmente. Absoluta confidencialidad.
- 🪶 **Optimizado para Hardware Restringido**: Diseñado para correr de manera eficiente con modelos de la familia 2B-3B (como `Llama 3.2:3B` o `Qwen 2.5:3B`) balanceando perfectamente razonamiento semántico y consumo de memoria.
- 🛡️ **Contrato de Datos Estricto**: Adiós a las alucinaciones de formato. Integración nativa de `Pydantic` en el backend para forzar a la IA a retornar la minuta en un esquema JSON validado antes de llegar al usuario.
- 📚 **Smart Chunking**: Procesamiento de documentos súper extensos mediante algoritmos de fragmentación con overlap (10-15%) para mantener el contexto general sin exceder el límite de tokens del LLM.

## 🛠️ Arquitectura y Stack Tecnológico
La versión V1 abandona los orquestadores web de prototipo en favor de una arquitectura App moderna:

- **Backend (Motor Core)**: `FastAPI` (Python) - Servidor ultrarrápido que gestiona las reglas de negocio, chunking y validación de esquemas (Pydantic).
- **Frontend (Interfaz de Usuario)**: `Next.js` / React - UI reactiva, limpia y construida pensando en empaquetado Desktop (Tauri).
- **Capa de Inferencia IA**: `Ollama` - Ejecución eficiente de modelos cuantizados de forma nativa.
- **Base de Datos Ligera**: `SQLite` (Persistencia de minutas) + *VectorDB* ligera (Búsqueda semántica futura).

## 📂 Estructura del Proyecto
```text
📦 minutas-iaV1
 ┣ 📂 backend/      # API FastAPI, Pydantic schemas, Chunking logic
 ┣ 📂 frontend/     # Next.js SPA
 ┣ 📂 shared/       # Interfaces y contratos de datos comunes
 ┣ 📂 docs/         # Documentación de arquitectura
 ┗ 📜 context.md    # Lecciones aprendidas y roadmap
```

## 🚀 Despliegue Rápido (Entorno de Desarrollo)

Puedes iniciar todo el ecosistema de IA local con el script principal:

```bash
# Clonar el proyecto
git clone https://github.com/mbaigorriaia-design/minutas-iaV1.git
cd minutas-iaV1

# Levantar Backend y Frontend 
./INICIAR_MINUTAS.bat
```
*(Asegúrate de tener Ollama corriendo en tu sistema con el modelo base descargado: `ollama run qwen2.5:3b`)*

---
*Construyendo el futuro de la automatización empresarial local, un commit a la vez.*

---
name: context-logger
description: Habilidad estricta para registrar automáticamente el avance de tareas en un archivo de bitácora (context-log.md) al finalizar cualquier implementación o despliegue.
trigger: Al finalizar una tarea final, antes de concluir la intervención o notificar al usuario.
---

# Funcionalidad del Skill: Registro de Contexto (Context Logger)

Esta habilidad asegura que el estado del proyecto, su arquitectura y el historial de todas las acciones realizadas por la IA estén siempre documentados para consumo humano en un archivo llamado `context-log.md` en la raíz del repositorio.

## Reglas de Ejecución Obligatorias

CADA VEZ que finalices una tarea asignada, y estrictamente **ANTES** de dar por concluida tu intervención o avisarle al usuario, tu **última acción en segundo plano** debe ser actualizar el archivo `context-log.md`.

### 1. Inicialización de `context-log.md`
Si descubres que el archivo `context-log.md` **no existe** en la raíz del proyecto, debes crearlo inmediatamente con la siguiente estructura base e inferir su contenido leyendo el entorno:

```markdown
# Contexto del Proyecto

## Descripción general del proyecto
[Agrega aquí una breve síntesis de contexto de qué trata el proyecto actual]

## Arquitectura y componente
[Agrega aquí las tecnologías clave utilizadas, componentes, módulos de Python o nodos principales de n8n si aplica]

## Log de avances y Seguimiento de Tareas
[Comienza la lista aquí abajo]
```

### 2. Instrucciones de Finalización e Inserción
Al momento de registrar tu trabajo en el archivo:
1. Redacta un resumen muy breve (1 o 2 líneas máximo) de la tarea abstracta y técnica que acabas de resolver.
2. Formatea la entrada de texto de la siguiente manera exacta (usando la fecha actual real de tu metadata):
   `* **[DD-MM-YYYY]**: <Descripción concisa de la acción realizada y su resultado o impacto>.`
3. Usa la herramienta `multi_replace_file_content`, `replace_file_content` (o simplemente adiciona al final del archivo si ya puedes identificar el bloque) para **agregar** este nuevo *bullet point* al final de la sección "Log de avances y Seguimiento de Tareas".

### Ejemplo de Log a añadir:
* **[26-03-2026]**: Se actualizó el nodo webhook de n8n para aceptar peticiones GET y se validó la comunicación entre el workflow y RAG Postgres.
* **[27-03-2026]**: Se refactorizó la clase principal del Gemelo Digital en Python cumpliendo estrictamente con PEP 8.

### Criterio de Bloqueo 🛑
No consideres una tarea como "completamente terminada" sin haber verificado fehacientemente que tu nuevo punto fue insertado de forma correcta en el `context-log.md`.

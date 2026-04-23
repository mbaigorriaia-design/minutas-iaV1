---
name: lidr-standards
description: Habilidades y estándares rigurosos de desarrollo en backend, frontend, documentación y arquitectura, importados del hub AI-Specs (LIDR).
---

# Funcionalidad del Skill

Este directorio contiene las especificaciones maestras de diseño del proyecto (`.mdc` y `.yml`). 
Como sub-agente, CUANDO implementes o planifiques código para este proyecto (ya sea en `/sdd-apply`, `/sdd-explore` o `/sdd-propose`), **debes** leer e integrar las reglas definidas en los archivos de este directorio:

- `base-standards.mdc`: Reglas de ORO del proyecto. No negociables.
- `backend-standards.mdc`: Guías de rendimiento, seguridad de APIs REST/n8n.
- `frontend-standards.mdc`: Reglas de interfaces limpias, estado, naming.
- `documentation-standards.mdc`: Convención de documentación técnica y readme.
- `data-model.md` / `api-spec.yml`: Modelos preexistentes (léelos si el requerimiento influye en base de datos).

Revisa siempre el `base-standards.mdc` de este directorio antes de emitir tu resultado (artifacts, spec, code).

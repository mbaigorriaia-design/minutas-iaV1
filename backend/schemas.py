from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class Participante(BaseModel):
    nombre: str
    rol: Optional[str] = None

class Tema(BaseModel):
    titulo: str
    puntos_clave: List[str]
    decisiones: List[str] = []

class Tarea(BaseModel):
    descripcion: str
    responsable: str
    prioridad: str = "Media"
    fecha_limite: Optional[str] = None

from typing import Any
class Minuta(BaseModel):
    titulo: str
    fecha: date
    objetivo: Optional[str] = None
    participantes: List[Participante]
    resumen_ejecutivo: str
    requerimientos: List[Any] = []
    temas: List[Tema]
    tareas: List[Tarea]
    riesgos: List[Any] = []
    pendientes: List[Any] = []
    proximos_pasos: List[Any] = []

class MeetingResponse(BaseModel):
    reunion: Minuta

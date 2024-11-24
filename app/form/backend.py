from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime


Respuesta = Literal["Sí", "No", "No sabe"]
Resultado = Literal["No", "Sospecha", "Probablemente"]
Incertidumbre = "No sabe"


class Form(BaseModel):
    ehr: str
    fecha: datetime
    fiebre: Respuesta
    pustulas: Respuesta
    distribucion_pustulas: Optional[Respuesta] = Incertidumbre
    sobre_areas_enrojecidas: Optional[Respuesta] = Incertidumbre
    otros_sintomas: Respuesta
    dolor_articulaciones: Respuesta
    lesiones_escamosas: Respuesta
    psoriasis: Respuesta
    familiares_psoriasis: Respuesta
    brotes_similares: Respuesta
    lesion_mas_de_3_meses: Respuesta
    sintomas_post_infeccion: Respuesta
    cambio_medicamento: Respuesta
    estres_infecciones: Respuesta
    vacunacion_reciente: Respuesta
    resultado: Optional[Resultado] = None


def check_respuesta(res: Respuesta) -> bool:
    return res == "Sí"


def classify_form(c: Form):
    priority = calculate_priority(c)

    if priority <= 7:
        return "No"
    elif priority <= 14:
        return "Sospecha"
    else:
        return "Probablemente"


def calculate_priority(c: Form) -> float:
    priority = 0

    if check_respuesta(c.fiebre):
        priority += 2

    if check_respuesta(c.pustulas):
        priority += 3

        if check_respuesta(c.distribucion_pustulas):
            priority += 2

        if check_respuesta(c.sobre_areas_enrojecidas):
            priority += 2

    if check_respuesta(c.otros_sintomas):
        priority += 1

    if check_respuesta(c.dolor_articulaciones):
        priority += 1

    if check_respuesta(c.lesiones_escamosas):
        priority += 1

    if check_respuesta(c.psoriasis):
        priority += 2

    if check_respuesta(c.familiares_psoriasis):
        priority += 1

    if check_respuesta(c.brotes_similares):
        priority += 3

    if check_respuesta(c.lesion_mas_de_3_meses):
        priority += 2

    if check_respuesta(c.sintomas_post_infeccion):
        priority += 1

    if check_respuesta(c.cambio_medicamento):
        priority += 1

    if check_respuesta(c.estres_infecciones):
        priority += 1

    if check_respuesta(c.vacunacion_reciente):
        priority += 0.5

    return priority

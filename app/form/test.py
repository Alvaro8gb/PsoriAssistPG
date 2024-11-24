import pytest
from pydantic import ValidationError
from backend import (
    Form,
    calculate_priority,
)  # Asume que la clase está en cuestionario.py
from datetime import datetime


def test_creacion_valida():
    respuestas_validas = {
        "ehr": "Test",
        "fiebre": "Sí",
        "pustulas": "No",
        "otros_sintomas": "Sí",
        "dolor_articulaciones": "No",
        "lesiones_escamosas": "Sí",
        "psoriasis": "No",
        "familiares_psoriasis": "Sí",
        "brotes_similares": "No",
        "lesion_mas_de_3_meses": "Sí",
        "sintomas_post_infeccion": "No",
        "cambio_medicamento": "Sí",
        "estres_infecciones": "No",
        "vacunacion_reciente": "Sí",
        "fecha": datetime.now(),
    }

    cuestionario = Form(**respuestas_validas)

    assert cuestionario.fiebre == "Sí"
    assert cuestionario.pustulas == "No"
    assert cuestionario.otros_sintomas == "Sí"
    assert cuestionario.dolor_articulaciones == "No"
    assert cuestionario.lesiones_escamosas == "Sí"
    assert cuestionario.psoriasis == "No"
    assert cuestionario.familiares_psoriasis == "Sí"
    assert cuestionario.brotes_similares == "No"
    assert cuestionario.lesion_mas_de_3_meses == "Sí"
    assert cuestionario.sintomas_post_infeccion == "No"
    assert cuestionario.cambio_medicamento == "Sí"
    assert cuestionario.estres_infecciones == "No"
    assert cuestionario.vacunacion_reciente == "Sí"


def test_respuesta_invalida():

    respuestas_invalidas = {
        "ehr": "Test",
        "fiebre": "Sí",
        "pustulas": "Tal vez",  # Valor inválido
        "otros_sintomas": "Sí",
        "dolor_articulaciones": "No",
        "lesiones_escamosas": "Sí",
        "psoriasis": "No",
        "familiares_psoriasis": "Sí",
        "brotes_similares": "No",
        "lesion_mas_de_3_meses": "Sí",
        "sintomas_post_infeccion": "No",
        "cambio_medicamento": "Sí",
        "estres_infecciones": "No",
        "vacunacion_reciente": "Sí",
        "fecha": datetime.now(),
    }

    with pytest.raises(ValidationError):
        Form(**respuestas_invalidas)


def test_respuestas_opcionales():
    respuestas_opcionales = {
        "ehr": "Test",
        "fiebre": "Sí",
        "pustulas": "No",
        "otros_sintomas": "Sí",
        "dolor_articulaciones": "No",
        "lesiones_escamosas": "Sí",
        "psoriasis": "No",
        "familiares_psoriasis": "Sí",
        "brotes_similares": "No",
        "lesion_mas_de_3_meses": "Sí",
        "sintomas_post_infeccion": "No",
        "cambio_medicamento": "Sí",
        "estres_infecciones": "No",
        "vacunacion_reciente": "Sí",
        "fecha": datetime.now(),
    }

    cuestionario = Form(**respuestas_opcionales)

    assert cuestionario.distribucion_pustulas == "No sabe"
    assert cuestionario.sobre_areas_enrojecidas == "No sabe"


def test_priority_no_symptoms():
    base_data = {
        "ehr": "Test",
        "fiebre": "No",
        "pustulas": "No",
        "distribucion_pustulas": "No",
        "sobre_areas_enrojecidas": "No",
        "otros_sintomas": "No",
        "dolor_articulaciones": "No",
        "lesiones_escamosas": "No",
        "psoriasis": "No",
        "familiares_psoriasis": "No",
        "brotes_similares": "No",
        "lesion_mas_de_3_meses": "No",
        "sintomas_post_infeccion": "No",
        "cambio_medicamento": "No",
        "estres_infecciones": "No",
        "vacunacion_reciente": "No",
        "fecha": datetime.now(),
    }

    cuestionario = Form(**base_data)

    assert calculate_priority(cuestionario) == 0


def test_priority_all_symptoms():
    base_data = {
        "ehr": "Test",
        "fiebre": "Sí",
        "pustulas": "Sí",
        "distribucion_pustulas": "Sí",
        "sobre_areas_enrojecidas": "Sí",
        "otros_sintomas": "Sí",
        "dolor_articulaciones": "Sí",
        "lesiones_escamosas": "Sí",
        "psoriasis": "Sí",
        "familiares_psoriasis": "Sí",
        "brotes_similares": "Sí",
        "lesion_mas_de_3_meses": "Sí",
        "sintomas_post_infeccion": "Sí",
        "cambio_medicamento": "Sí",
        "estres_infecciones": "Sí",
        "vacunacion_reciente": "Sí",
        "fecha": datetime.now(),
    }

    cuestionario = Form(**base_data)

    assert calculate_priority(cuestionario) == 23.5

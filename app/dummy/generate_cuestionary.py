import random
import csv
import sys

from pathlib import Path
from datetime import datetime, timedelta


root_path = Path(__file__).parent.parent
sys.path.append(str(root_path))

from form.backend import Form, Respuesta, Incertidumbre, classify_form


def generate_random_datetime(start, end):
    """
    Generate a random datetime between two datetime objects.

    :param start: The start datetime
    :param end: The end datetime
    :return: A random datetime between start and end
    """
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=random_seconds)


def main():

    fieldnames = [
        "ehr",
        "fiebre",
        "pustulas",
        "distribucion_pustulas",
        "sobre_areas_enrojecidas",
        "otros_sintomas",
        "dolor_articulaciones",
        "lesiones_escamosas",
        "psoriasis",
        "familiares_psoriasis",
        "brotes_similares",
        "lesion_mas_de_3_meses",
        "sintomas_post_infeccion",
        "cambio_medicamento",
        "estres_infecciones",
        "vacunacion_reciente",
        "fecha",
        "resultado",
    ]

    respuestas = list(Respuesta.__args__)
    print(respuestas)
    respuestas.remove("No sabe")

    n_samples = 50
    # Generate 50 sample rows
    form_list = []
    for i in range(n_samples):
        form_fields = {
            "ehr": str(i),
            "fiebre": random.choice(respuestas),
            "pustulas": random.choice(respuestas),
            "distribucion_pustulas": (
                random.choice(respuestas)
                if random.choice([True, False])
                else Incertidumbre
            ),
            "sobre_areas_enrojecidas": (
                random.choice(respuestas)
                if random.choice([True, False])
                else Incertidumbre
            ),
            "otros_sintomas": random.choice(respuestas),
            "dolor_articulaciones": random.choice(respuestas),
            "lesiones_escamosas": random.choice(respuestas),
            "psoriasis": random.choice(respuestas),
            "familiares_psoriasis": random.choice(respuestas),
            "brotes_similares": random.choice(respuestas),
            "lesion_mas_de_3_meses": random.choice(respuestas),
            "sintomas_post_infeccion": random.choice(respuestas),
            "cambio_medicamento": random.choice(respuestas),
            "estres_infecciones": random.choice(respuestas),
            "vacunacion_reciente": random.choice(respuestas),
            "fecha": generate_random_datetime(
                datetime(2020, 1, 1), datetime(2024, 11, 24)
            ),
            "resultado": None,
        }

        form = Form(**form_fields)

        form.resultado = classify_form(form)

        form_list.append(form)

    csv_file = f"{root_path}/db/cuestionario_samples_{n_samples}.csv"

    forms_dics = [f.model_dump() for f in form_list]
    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(forms_dics)

    print(f"Generated 50 sample form and saved to {csv_file}")


main()

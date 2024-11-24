import csv

from backend import Cuestionario


def dump_cuestionario(c: Cuestionario, path: str):

    data_dict = c.model_dump()

    with open(path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data_dict.keys())
        writer.writeheader()  # Write column headers
        writer.writerow(data_dict)  # Write the data

    print(f"Data successfully written to {c}")


if __name__ == "__main__":

    cuestionario = Cuestionario(
        fiebre="Sí",
        pustulas="No",
        otros_sintomas="Sí",
        dolor_articulaciones="No",
        lesiones_escamosas="Sí",
        psoriasis="No",
        familiares_psoriasis="Sí",
        brotes_similares="No",
        lesion_mas_de_3_meses="No",
        sintomas_post_infeccion="Sí",
        cambio_medicamento="No",
        estres_infecciones="Sí",
        vacunacion_reciente="No",
    )

    dump_cuestionario(cuestionario, "app/db/cuestionario_sample.csv")

import streamlit as st
from form.backend import Form, Resultado
from pydantic import ValidationError
from datetime import datetime


def form(img: list) -> Form:

    submitted = None
    with st.form("Form"):

        ehr = st.text_input("Electronic Health Record")

        # Sección 1: Síntomas Actuales
        st.subheader("Sección 1: Síntomas Actuales")

        # Pregunta 1
        fiebre = st.radio(
            "1. ¿El paciente ha presentado pirexia (temperatura ≥38°C) de causa no determinada en los últimos días?",
            ("Sí", "No"),
        )

        # Pregunta 2
        pustulas = st.radio(
            """2. ¿Se observan pústulas estériles sobre la superficie cutánea? 
                            (Se recomienda disponer de imágenes clínicas de referencia para correlación)""",
            ("Sí", "No"),
        )

        st.image(img, caption="Imagen psoriasis pustulosa generalizada")

        st.markdown(
            "[Para consultas más imagenes - DermNet](https://dermnetnz.org/images/generalised-pustular-psoriasis-images)"
        )

        # Si respondió "Sí" a la pregunta 2, añadir sub-preguntas

        distribucion_pustulas = "No"
        sobre_areas_enrojecidas = "No"
        if pustulas == "Sí":
            distribucion_pustulas = st.radio(
                """2.1 ¿Están distribuidas de manera generalizada (afectando áreas como tronco, 
                                             extremidades, abdomen, pero no limitadas a regiones acrales)?""",
                ("Sí", "No"),
            )

            sobre_areas_enrojecidas = st.radio(
                "2.2 ¿Se encuentran sobre placas eritematosas o piel con inflamación difusa?",
                ("Sí", "No"),
            )

        otros_sintomas = st.radio(
            "3. ¿Presenta el paciente síntomas sistémicos asociados como astenia, adinamia o malestar general?",
            ("Sí", "No"),
        )

        dolor_articulaciones = st.radio(
            "4. ¿Refiere dolor, inflamación articular o signos de artritis periférica o axial? (Importante para descartar artritis psoriásica asociada)",
            ("Sí", "No"),
        )

        lesiones_escamosas = st.radio(
            "5. ¿Existen áreas de descamación intensa, xerosis o placas inflamatorias fuera del área pustular?",
            ("Sí", "No"),
        )

        st.subheader("Sección 2: Antecedentes Clínicos")

        psoriasis = st.radio(
            "6. ¿Presenta antecedentes de psoriasis vulgar, inversa o guttata?",
            ("Sí", "No", "No sabe"),
        )

        familiares_psoriasis = st.radio(
            """7. ¿Hay antecedentes familiares de psoriasis u otras enfermedades autoinmunes
                                         (lupus eritematoso, artritis reumatoide, etc.)?""",
            ("Sí", "No"),
        )

        brotes_similares = st.radio(
            "8. ¿Ha experimentado episodios previos con características clínicas similares (brotes recurrentes)?",
            ("Sí", "No"),
        )

        lesion_mas_de_3_meses = st.radio(
            "9. ¿Los signos y síntomas actuales persisten por un periodo mayor a tres meses? (Indicar si hay sospecha de PPG persistente o crónica)",
            ("Sí", "No"),
        )

        sintomas_post_infeccion = st.radio(
            "10. ¿Ha experimentado síntomas similares después de infecciones recientes (como faringitis) o de suspender medicamentos como corticoides?",
            ("Sí", "No"),
        )

        # Sección 3: Factores Desencadenantes
        st.subheader("Sección 3: Factores Desencadenantes")

        cambio_medicamento = st.radio(
            """11. ¿Han aparecido los síntomas tras infecciones recientes (faringitis estreptocócica, infecciones virales) 
            o después de la suspensión abrupta de corticosteroides sistémicos?""",
            ("Sí", "No"),
        )

        estres_infecciones = st.radio(
            """12. ¿Ha estado expuesto a factores desencadenantes como estrés psicológico intenso, embarazo, 
            ciclos menstruales recientes o infecciones bacterianas/virales?""",
            ("Sí", "No"),
        )

        vacunacion_reciente = st.radio(
            "13. ¿Ha recibido alguna vacuna recientemente (incluyendo vacunas contra SARS-CoV-2, H1N1 (Gripe))?",
            ("Sí", "No"),
        )

        submitted = st.form_submit_button("Enviar Respuesta")

        if submitted:

            respuestas = {
                "ehr": ehr,
                "fiebre": fiebre,
                "pustulas": pustulas,
                "distribucion_pustulas": distribucion_pustulas,
                "sobre_areas_enrojecidas": sobre_areas_enrojecidas,
                "otros_sintomas": otros_sintomas,
                "dolor_articulaciones": dolor_articulaciones,
                "lesiones_escamosas": lesiones_escamosas,
                "psoriasis": psoriasis,
                "familiares_psoriasis": familiares_psoriasis,
                "brotes_similares": brotes_similares,
                "lesion_mas_de_3_meses": lesion_mas_de_3_meses,
                "sintomas_post_infeccion": sintomas_post_infeccion,
                "cambio_medicamento": cambio_medicamento,
                "estres_infecciones": estres_infecciones,
                "vacunacion_reciente": vacunacion_reciente,
                "fecha": datetime.now(),
            }

            try:
                cuestionario = Form(**respuestas)
                st.write(
                    "Gracias por completar el cuestionario. Los datos han sido recibidos."
                )
                return cuestionario

            except ValidationError as e:
                st.error(f"Error en los datos: {e}")


def visualize_resultado(resultado: Resultado):

    if resultado == "No":
        st.warning("Descarte de PPG", icon="❌")
    elif resultado == "Sospecha":
        st.info("Sospecha Moderada de PPG", icon="⚠️")
    elif resultado == "Probablemente":
        st.success("Posible Confirmación de PPG", icon="✅")

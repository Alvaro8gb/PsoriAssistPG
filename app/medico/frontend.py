import pandas as pd
import streamlit as st
import plotly.express as px


sintomas = [
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
]


def medical_dashboard(df_forms, ehr, image_ms, image_scale, image_score):

    st.subheader(f"Respuestas del paciente {ehr}")
    patient_data = df_forms[df_forms["ehr"] == ehr].iloc[0]

    if "fecha" in patient_data:
        st.markdown(
            f"""
            <div style="background-color: #e3f2fd; padding: 12px; border-radius: 8px; margin-bottom: 15px; border: 1px solid #90caf9; font-size: 16px;">
                <strong style="color: #0d47a1;">Fecha:</strong>
                <span style="color: #0d47a1;">{patient_data['fecha'] if patient_data['fecha'] else 'Sin respuesta'}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    for question, answer in patient_data.items():
        if question == "ehr" or question == "fecha":
            continue
        elif question == "resultado":
            if answer == "No":
                advice = """
                    **Evaluación del Diagnóstico**

                    Con base en la información proporcionada, el diagnóstico de **psoriasis pustulosa generalizada (PPG)** es poco probable. Recomendamos los siguientes pasos:

                    1. **Reevaluar los síntomas y el historial del paciente**:
                    Revise si las características clínicas han cambiado o si hay nuevos factores relevantes, como infecciones, medicamentos recientes o condiciones subyacentes.

                    2. **Explorar diagnósticos diferenciales**:
                    Considere otras posibles condiciones, como la **pustulosis exantemática aguda generalizada (AGEP)**, infecciones cutáneas o reacciones medicamentosas.

                    3. **Realizar pruebas adicionales si los síntomas persisten**:
                    Podría ser útil repetir pruebas de laboratorio, realizar una biopsia cutánea o derivar al paciente a un especialista en dermatología.

                    ⚠ **Nota:** Aunque el diagnóstico de PPG es poco probable, este resultado no excluye completamente la enfermedad. Considere un seguimiento clínico según sea necesario.
                    
                    **Referencias**:
                    
                    - Choon SE, van de Kerkhof P, Gudjonsson JE, et al. International Consensus Definition and Diagnostic Criteria for Generalized Pustular Psoriasis From the International Psoriasis Council. JAMA Dermatol. 2024;160(7):758-768. doi:10.1001/jamadermatol.2024.0915
                    - Armstrong AW, Elston CA, Elewski BE, et al. Generalized pustular psoriasis: A consensus statement from the National Psoriasis Foundation. J Am Acad Dermatol. 2024;90(4):727-730. doi:10.1016/j.jaad.2023.09.080
                    - Navarini AA, Burden AD, Capon F, et al. European consensus statement on phenotypes of pustular psoriasis. J Eur Acad Dermatol Venereol. 2017;31(11):1792–1799. doi: 10.1111/jdv.14386
                    - Puig L, Choon SE, Gottlieb AB, et al. Generalized pustular psoriasis: A global Delphi consensus on clinical course, diagnosis, treatment goals and disease management. J Eur Acad Dermatol Venereol. 2023;37(4):737-752. doi:10.1111/jdv.18851
                    - Rivera-Díaz R, Carrascosa Carrillo JM, Alfonso Zamora S, et al. Mejoras en la atención al paciente con psoriasis pustulosa generalizada en España: recomendaciones de un grupo de expertos. Actas Dermosifiliogr. 2024,115(8):801-813
                    """

                bg_color = "#D4EDDA"
                text_color = "#155724"
            elif answer == "Sospecha":
                advice = """
                    **Evaluación del Diagnóstico**

                    Con base en la información proporcionada, existe sospecha de que el paciente presente **psoriasis pustulosa generalizada (PPG)**. Recomendamos los siguientes pasos:

                    1. **Confirmar el diagnóstico**:

                    Considere solicitar análisis de laboratorio (PCR, neutrofilia) y, si es posible, realizar una biopsia cutánea para identificar características compatibles con la PPG.

                    2. **Descartar diagnósticos diferenciales**:

                    Verifique si hay hallazgos que sugieran condiciones como la **AGEP**, considerando factores como la presencia de eosinófilos en las pústulas o antecedentes de exposición a medicamentos.

                    3. **Evaluación de la gravedad mediante herramientas de validación**:

                    Se han desarrollado y validado instrumentos específicos para la GPP, como el **Índice de Área y Gravedad de la Psoriasis Pustulosa Generalizada (GPPASI)** y la **Evaluación Global Médica de la Psoriasis Pustulosa Generalizada (GPPGA)**.
                    
                    La validación del **GPPGA** demostró que evalúa eficazmente la gravedad de la enfermedad, convirtiéndolo en un valioso recurso para médicos e investigadores en el seguimiento y tratamiento de esta afección.
                    
                    Ambos, **GPPGA** y **GPPASI**, han sido validados psicométricamente, lo que demuestra que son herramientas válidas, fiables y sensibles para evaluar la gravedad de la enfermedad.

                    **GPPGA**: La puntuación se basa en la media de tres parámetros evaluados. Las puntuaciones son las siguientes:

                        - Claro: Puntuación 0
                        - Casi claro: Puntuación entre 1 y 1.5
                        - Leve: Puntuación entre 1.5 y 2.5
                        - Moderado: Puntuación entre 2.5 y 3.5
                        - Grave: Puntuación superior a 3.5

                    **GPPASI**: Se basa en una puntuación numérica del estado general de la enfermedad del paciente, con un rango de 0 a 72, para determinar la extensión y gravedad de la enfermedad.

                    Ambas herramientas fueron adaptadas de evaluaciones más generales utilizadas en la psoriasis en placas (PGA y PASI), con modificaciones para incluir características específicas de la GPP, como la postulación.

                    Burden AD, Bissonnette R, Lebwohl MG, et al. Psychometric validation of the GPPGA and GPPASI. J Eur Acad Dermatol Venereol. 2023;37(6):1125-1133. [https://doi.org/10.1111/jdv.18999](https://doi.org/10.1111/jdv.18999)
                    

                    4. **Establecer un plan de tratamiento**:
                    Basándose en el diagnóstico confirmado, elabore un plan de tratamiento adecuado, que podría incluir terapia sistémica y monitoreo para complicaciones potenciales (hipocalcemia, hipoalbuminemia, disfunción renal o hepática).

                    ⚠ **Nota**:
                    Este resultado es indicativo, pero no definitivo. Confirme el diagnóstico con base en hallazgos clínicos y pruebas adicionales según sea necesario.
                    
                    **Referencias**:

                    - Choon SE, van de Kerkhof P, Gudjonsson JE, et al. International Consensus Definition and Diagnostic Criteria for Generalized Pustular Psoriasis From the International Psoriasis Council. JAMA Dermatol. 2024;160(7):758-768. doi:10.1001/jamadermatol.2024.0915
                    - Armstrong AW, Elston CA, Elewski BE, et al. Generalized pustular psoriasis: A consensus statement from the National Psoriasis Foundation. J Am Acad Dermatol. 2024;90(4):727-730. doi:10.1016/j.jaad.2023.09.080
                    - Navarini AA, Burden AD, Capon F, et al. European consensus statement on phenotypes of pustular psoriasis. J Eur Acad Dermatol Venereol. 2017;31(11):1792–1799. doi: 10.1111/jdv.14386
                    - Puig L, Choon SE, Gottlieb AB, et al. Generalized pustular psoriasis: A global Delphi consensus on clinical course, diagnosis, treatment goals and disease management. J Eur Acad Dermatol Venereol. 2023;37(4):737-752. doi:10.1111/jdv.18851
                    - Rivera-Díaz R, Carrascosa Carrillo JM, Alfonso Zamora S, et al. Mejoras en la atención al paciente con psoriasis pustulosa generalizada en España: recomendaciones de un grupo de expertos. Actas Dermosifiliogr. 2024,115(8):801-813
                    """
                bg_color = "#FFF3CD"
                text_color = "#856404"
            elif answer == "Probablemente":
                advice = """
                    **Evaluación del Diagnóstico**

                    Con base en la información proporcionada, existe una alta probabilidad de que el paciente presente **psoriasis pustulosa generalizada (PPG)**. Recomendamos los siguientes pasos:

                    1. **Confirmar el diagnóstico**:

                    Considere solicitar análisis de laboratorio (PCR, neutrofilia) y, si es posible, realizar una biopsia cutánea para identificar características compatibles con la PPG.

                    2. **Descartar diagnósticos diferenciales**:

                    Verifique si hay hallazgos que sugieran condiciones como la **AGEP**, considerando factores como la presencia de eosinófilos en las pústulas o antecedentes de exposición a medicamentos.

                    3. **Evaluación de la gravedad mediante herramientas de validación**:

                    Se han desarrollado y validado instrumentos específicos para la GPP, como el **Índice de Área y Gravedad de la Psoriasis Pustulosa Generalizada (GPPASI)** y la **Evaluación Global Médica de la Psoriasis Pustulosa Generalizada (GPPGA)**.
                    
                    La validación del **GPPGA** demostró que evalúa eficazmente la gravedad de la enfermedad, convirtiéndolo en un valioso recurso para médicos e investigadores en el seguimiento y tratamiento de esta afección.
                    
                    Ambos, **GPPGA** y **GPPASI**, han sido validados psicométricamente, lo que demuestra que son herramientas válidas, fiables y sensibles para evaluar la gravedad de la enfermedad.

                    **GPPGA**: La puntuación se basa en la media de tres parámetros evaluados. Las puntuaciones son las siguientes:

                        - Claro: Puntuación 0
                        - Casi claro: Puntuación entre 1 y 1.5
                        - Leve: Puntuación entre 1.5 y 2.5
                        - Moderado: Puntuación entre 2.5 y 3.5
                        - Grave: Puntuación superior a 3.5

                    **GPPASI**: Se basa en una puntuación numérica del estado general de la enfermedad del paciente, con un rango de 0 a 72, para determinar la extensión y gravedad de la enfermedad.

                    Ambas herramientas fueron adaptadas de evaluaciones más generales utilizadas en la psoriasis en placas (PGA y PASI), con modificaciones para incluir características específicas de la GPP, como la postulación.

                    Burden AD, Bissonnette R, Lebwohl MG, et al. Psychometric validation of the GPPGA and GPPASI. J Eur Acad Dermatol Venereol. 2023;37(6):1125-1133. [https://doi.org/10.1111/jdv.18999](https://doi.org/10.1111/jdv.18999) 
                    

                    4. **Establecer un plan de tratamiento**:
                    Basándose en el diagnóstico confirmado, elabore un plan de tratamiento adecuado, que podría incluir terapia sistémica y monitoreo para complicaciones potenciales (hipocalcemia, hipoalbuminemia, disfunción renal o hepática).

                    ⚠ **Nota**:
                    Este resultado es indicativo, pero no definitivo. Confirme el diagnóstico con base en hallazgos clínicos y pruebas adicionales según sea necesario.
                    
                    **Referencias**:
                    - Choon SE, van de Kerkhof P, Gudjonsson JE, et al. International Consensus Definition and Diagnostic Criteria for Generalized Pustular Psoriasis From the International Psoriasis Council. JAMA Dermatol. 2024;160(7):758-768. doi:10.1001/jamadermatol.2024.0915
                    - Armstrong AW, Elston CA, Elewski BE, et al. Generalized pustular psoriasis: A consensus statement from the National Psoriasis Foundation. J Am Acad Dermatol. 2024;90(4):727-730. doi:10.1016/j.jaad.2023.09.080
                    - Navarini AA, Burden AD, Capon F, et al. European consensus statement on phenotypes of pustular psoriasis. J Eur Acad Dermatol Venereol. 2017;31(11):1792–1799. doi: 10.1111/jdv.14386
                    - Puig L, Choon SE, Gottlieb AB, et al. Generalized pustular psoriasis: A global Delphi consensus on clinical course, diagnosis, treatment goals and disease management. J Eur Acad Dermatol Venereol. 2023;37(4):737-752. doi:10.1111/jdv.18851
                    - Rivera-Díaz R, Carrascosa Carrillo JM, Alfonso Zamora S, et al. Mejoras en la atención al paciente con psoriasis pustulosa generalizada en España: recomendaciones de un grupo de expertos. Actas Dermosifiliogr. 2024,115(8):801-813
                    """

                bg_color = "#ffccd5"
                text_color = "#721C24"

        else:
            if answer == "Sí":
                icon = "✅"
                bg_color = "#D4EDDA"
                text_color = "#155724"
            elif answer == "No":
                icon = "❌"
                bg_color = "#F8D7DA"
                text_color = "#721C24"
            else:
                icon = "❓"
                bg_color = "#FFF3CD"
                text_color = "#856404"

            st.markdown(
                f"""
                <div style="background-color: {bg_color}; padding: 12px; border-radius: 8px; margin-bottom: 15px; border: 1px solid #ddd; font-size: 16px; display: flex; align-items: center;">
                    <span style="font-size: 20px; margin-right: 12px; color: {text_color};">{icon}</span>
                    <strong style="color: {text_color};">{question.replace('_', ' ').capitalize()}:</strong> 
                    <span style="color: {text_color}; margin-left: 8px;">{answer if answer else 'Sin respuesta'}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    patient_symptoms = patient_data[sintomas]

    response_counts = (
        patient_symptoms.to_frame().T.apply(pd.Series.value_counts).fillna(0)
    )

    total_responses = response_counts.sum(axis=1).reset_index()
    total_responses.columns = ["Respuesta", "Frecuencia"]

    fig = px.bar(
        total_responses,
        x="Respuesta",
        y="Frecuencia",
        color="Respuesta",
        title=f"Respuestas de síntomas del paciente {ehr}",
        labels={"Respuesta": "Respuesta", "Frecuencia": "Número de respuestas"},
        color_discrete_map={"Sí": "#D4EDDA", "No": "#F8D7DA", "No sabe": "#FFF3CD"},
        category_orders={"Respuesta": ["Sí", "No", "No sabe"]},
    )

    st.plotly_chart(fig)

    st.markdown(
        f"""
        <div style="background-color: {bg_color}; padding: 12px; border-radius: 8px; margin-bottom: 15px; border: 1px solid #ddd; font-size: 16px;">
            <strong style="color: {text_color};">Resultado:</strong>
            <span style="color: {text_color};">{answer}</span><br>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(advice, unsafe_allow_html=True)

    st.write("Imágenes de interés:")
    st.image(
        image_scale,
        caption="Link: https://academic.oup.com/view-large/figure/420393492/ljad071f1.tif",
    )
    st.image(
        image_ms,
        caption="Link: https://link.springer.com/article/10.1007/s40257-021-00653-0/figures/1",
    )
    st.image(
        image_score,
        caption="Link: https://link.springer.com/article/10.1007/s40257-021-00653-0/figures/2",
    )

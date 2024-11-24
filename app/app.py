import streamlit as st

from globals import TEXTS_MODULES, DESC
from resourceManager import load_svg, get_path, load_image

from form.fronted import form, visualize_resultado
from form.backend import classify_form

from medico.frontend import medical_dashboard
from medico.backend import load_forms

from ai.frontend import visualize_similars

from references.frontend import references_dashboard  # Nuevo import

if __name__ == "__main__":
    path_logo = get_path("static", "logo.svg")
    path_db = get_path("db", "cuestionario_samples_50.csv")
    image_path_example = get_path("static", "generalised-pustular-psoriasis-0004.jpg")
    image_path_ms = get_path("static", "measures.png")
    image_path_scale = get_path("static", "scale.jpeg")
    image_path_score = get_path("static", "score.png")

    image_example = load_image(image_path_example)
    image_ms = load_image(image_path_ms)
    image_scale = load_image(image_path_scale)
    image_score = load_image(image_path_score)

    logo = load_svg(path_logo)
    df_forms = load_forms(path_db)
    cuestionario = None

    st.sidebar.write(
        "<h1> PsoriAssistPG </h1>  <h2><i>Asistente para el diagnóstico de Psoriasis Pustulosa Generalizada (PPG)</i> </h2> ",
        unsafe_allow_html=True,
    )
    st.sidebar.write(logo, unsafe_allow_html=True)

    st.sidebar.markdown("### Navegación")
    selected_section = st.sidebar.radio(
        "Elige una sección:",
        [TEXTS_MODULES["form"], TEXTS_MODULES["med"], TEXTS_MODULES["ref"]],
    )

    if selected_section == TEXTS_MODULES["form"]:
        st.title("Formulario de detección 🩺")

        if "form_submitted" not in st.session_state:
            st.session_state.form_submitted = False
            st.markdown(DESC)

        if not st.session_state.form_submitted:
            cuestionario = form(image_example)
        else:
            st.write("Gracias, el formulario ya ha sido enviado.")

        if cuestionario:
            cuestionario.resultado = classify_form(cuestionario)
            st.session_state.form_submitted = True
            visualize_resultado(cuestionario.resultado)

    elif selected_section == TEXTS_MODULES["med"]:

        if not df_forms.empty:
            st.title("Visualización de Cuestionarios de Pacientes ⚕️")
            patient_ids = df_forms["ehr"].tolist()
            ehr = st.selectbox("Seleccione un paciente para visualizar:", patient_ids)

            medical_dashboard(df_forms, ehr, image_ms, image_scale, image_score)
            visualize_similars(df_forms, ehr)

        else:
            st.error("No hay formularios. Revisar log.")

    elif selected_section == TEXTS_MODULES["ref"]:
        references_dashboard()  # Llamada a la función de referencias

    else:
        pass

    footer = """
    <div style="text-align: center; padding: 20px; margin-top: 50px;">
        <hr>
        <p>© 2024 PsoriAssistGG</p>
        <p>Desarrollado por <br>Álvaro García Barragán, Alberto González Calatayud, Eduardo Martín Ruiz, Laura Masa Martínez y Enrique Solera Navarro.</p>
    </div>
    """
    st.sidebar.markdown(footer, unsafe_allow_html=True)

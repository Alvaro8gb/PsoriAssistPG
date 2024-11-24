import streamlit as st
from datetime import datetime

from references.backend import fetch_arxiv_references, fetch_pubmed_references


def references_dashboard():
    st.title("Referencias Actualizadas 📖")

    # Campo de entrada para el término de búsqueda principal
    search_query = st.text_input(
        "Ingrese el término de búsqueda principal", "General Pustular Psoriasis"
    )

    # Campo de entrada para palabras clave adicionales
    additional_keywords = st.multiselect(
        "Seleccione palabras clave adicionales",
        ["consensus", "guideline", "clinical trial"],
        default=[],
    )

    # Selector para el número de resultados
    max_results = st.slider("Número de resultados", min_value=1, max_value=50, value=10)

    # Selector para el año de inicio y fin
    start_year, end_year = st.select_slider(
        "Seleccione el rango de años",
        options=list(range(2000, datetime.now().year + 1)),
        value=(2015, datetime.now().year),
    )

    # Selector para elegir la fuente de datos
    data_source = st.selectbox("Seleccione la fuente de datos", ["arXiv", "PubMed"])

    if st.button("Buscar"):
        if data_source == "arXiv":

            # Mostrar las referencias
            st.header("Referencias de arXiv")
            fetch_arxiv_references(
                search_query, additional_keywords, max_results, start_year, end_year
            )
        elif data_source == "PubMed":

            st.header("Referencias de PubMed")
            fetch_pubmed_references(
                search_query, additional_keywords, max_results, start_year, end_year
            )

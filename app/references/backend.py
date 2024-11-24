import streamlit as st
import requests
import feedparser

from xml.etree import ElementTree as ET


def fetch_arxiv_references(
    search_query, additional_keywords, max_results, start_year, end_year
):
    # Construir la URL de la API de arXiv con filtros de fecha y palabras clave adicionales
    base_url = "http://export.arxiv.org/api/query?"
    date_filter = f"&start=0&max_results={max_results}"

    # Construir la consulta de búsqueda
    query_terms = [search_query]
    if additional_keywords:
        query_terms.extend(additional_keywords)
    query = " AND ".join(f"all:{term}" for term in query_terms)
    date_range = f" AND submittedDate:[{start_year}01010000 TO {end_year}12312359]"
    full_query = f"search_query={query}{date_range}"

    # Hacer la solicitud a la API de arXiv
    response = requests.get(base_url + full_query + date_filter)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Parsear el feed de arXiv
        feed = feedparser.parse(response.content)

        if feed.entries:
            for entry in feed.entries:
                # Filtrar por año
                published_year = int(entry.published[:4])
                if start_year <= published_year <= end_year:
                    title = entry.title
                    authors = ", ".join(author.name for author in entry.authors)
                    published = entry.published[:10]
                    link = entry.link

                    with st.expander(title):
                        st.write(f"**Autores:** {authors}")
                        st.write(f"**Fecha de publicación:** {published}")
                        st.markdown(f"[Leer más]({link})")
        else:
            st.write("No se encontraron referencias.")
    else:
        st.write("Error al conectar con la API de arXiv.")


def fetch_pubmed_references(
    search_query, additional_keywords, max_results, start_year, end_year
):
    # Construir la URL de la API de PubMed con filtros de fecha y palabras clave adicionales
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    search_url = base_url + "esearch.fcgi"
    fetch_url = base_url + "efetch.fcgi"

    # Construir la consulta de búsqueda
    query_terms = [search_query]

    if additional_keywords:
        query_terms.extend(additional_keywords)

    query = " AND ".join(query_terms)

    # Parámetros para la búsqueda
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "mindate": start_year,
        "maxdate": end_year,
        "datetype": "pdat",
        "retmode": "json",
    }

    # Hacer la solicitud a la API de PubMed
    response = requests.get(search_url, params=params)

    if response.status_code == 200:
        search_results = response.json()
        id_list = search_results.get("esearchresult", {}).get("idlist", [])

        if id_list:
            # Obtener los detalles de cada artículo
            fetch_params = {"db": "pubmed", "id": ",".join(id_list), "retmode": "xml"}
            fetch_response = requests.get(fetch_url, params=fetch_params)

            if fetch_response.status_code == 200:
                root = ET.fromstring(fetch_response.content)

                articles = root.findall(".//PubmedArticle")
                for article in articles:
                    article_title = article.findtext(".//ArticleTitle")
                    abstract = article.findtext(".//AbstractText")
                    pub_date = article.find(".//PubDate")
                    year = pub_date.findtext("Year")
                    if not year:
                        year = pub_date.findtext("MedlineDate")
                    authors_list = article.findall(".//Author")
                    authors = []
                    for author in authors_list:
                        last_name = author.findtext("LastName")
                        fore_name = author.findtext("ForeName")
                        if last_name and fore_name:
                            authors.append(f"{fore_name} {last_name}")
                    authors_str = ", ".join(authors)
                    pmid = article.findtext(".//PMID")
                    link = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"

                    with st.expander(article_title):
                        st.write(f"**Autores:** {authors_str}")
                        st.write(f"**Fecha de publicación:** {year}")
                        st.markdown(f"[Leer más]({link})")
                        if abstract:
                            st.write(f"**Resumen:** {abstract}")
            else:
                st.write("Error al obtener los detalles de los artículos de PubMed.")
        else:
            st.write("No se encontraron referencias.")
    else:
        st.write("Error al conectar con la API de PubMed.")

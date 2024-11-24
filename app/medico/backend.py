import pandas as pd
import streamlit as st


@st.cache_data
def load_forms(file_path: str) -> pd.DataFrame:
    try:
        df_forms = pd.read_csv(file_path)
        print("Load DF forms")
        return df_forms
    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()

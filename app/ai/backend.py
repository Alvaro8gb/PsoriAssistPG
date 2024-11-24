import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

pd.set_option("future.no_silent_downcasting", True)


def preprocesing(df):
    df_preprocess = df.copy()

    df_preprocess = pd.get_dummies(
        df_preprocess, columns=["resultado"], prefix=["resultado"], dtype=int
    )

    df_preprocess = df_preprocess.replace({"Sí": 1, "No": 0, "No sabe": 0})

    return df_preprocess


def fit(df):
    df_clasify = df.copy()

    min_neighbors = 5
    n_clusters = len(df_clasify) // min_neighbors
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df_clasify["cluster"] = kmeans.fit_predict(
        df_clasify.select_dtypes(include=["number"])
    )

    return df_clasify


def get_clusters(df):
    df_preprocess = preprocesing(df)
    df_clasify = fit(df_preprocess)

    pca = PCA(n_components=2)
    pca_components = pca.fit_transform(
        df_clasify.drop(columns=["ehr", "cluster", "fecha"])
    )

    df_clasify["PCA1"] = pca_components[:, 0]
    df_clasify["PCA2"] = pca_components[:, 1]

    return df_clasify


def get_patients_from_same_cluster(ehr_id: int, df: pd.DataFrame) -> pd.DataFrame:
    patient_cluster = df[df["ehr"] == ehr_id]["cluster"].iloc[0]

    same_cluster_patients = df[df["cluster"] == patient_cluster]

    return same_cluster_patients

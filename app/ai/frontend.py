import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt


from ai.backend import get_clusters, get_patients_from_same_cluster


def visualize_similars(df_forms, ehr):

    df_clusters = get_clusters(df_forms)

    st.write(f"Paciente con EHR {ehr} se parece a:")

    same_cluster_patients = get_patients_from_same_cluster(ehr, df_clusters)

    st.dataframe(same_cluster_patients.set_index("ehr"))

    st.write("En el siguiente grafico se puede apreciar la distancia entre pacientes:")

    fig, ax = plt.subplots(figsize=(8, 6))

    sns.scatterplot(
        data=same_cluster_patients,
        x="PCA1",
        y="PCA2",
        color="blue",
        label="Similar Patients",
        ax=ax,
    )

    # Mark the selected patient with a red 'X'
    selected_patient = df_clusters[df_clusters["ehr"] == ehr]
    ax.scatter(
        selected_patient["PCA1"],
        selected_patient["PCA2"],
        color="red",
        s=100,
        label=f"Patient {ehr}",
        marker="X",
    )

    for _, row in same_cluster_patients.iterrows():
        ax.text(
            row["PCA1"],
            row["PCA2"],
            f"{row['ehr']}",
            color="blue",
            fontsize=12,
            ha="right",
        )

    # Labeling
    ax.set_title("Pacientes Similares (Visualizado por ID de Paciente)")
    ax.set_xlabel("PCA Component 1")
    ax.set_ylabel("PCA Component 2")
    ax.legend()

    # Show the plot in Streamlit
    st.pyplot(fig)

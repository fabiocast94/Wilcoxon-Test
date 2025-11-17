import streamlit as st
import pandas as pd
from scipy.stats import wilcoxon

st.set_page_config(page_title="Test di Wilcoxon", page_icon="📊")

st.title("📊 Applicazione per Test di Wilcoxon")
st.write("Carica un file Excel con **due colonne di dati appaiati** per eseguire il test statistico.")

uploaded = st.file_uploader("Carica un file Excel (.xlsx)", type=["xlsx"])

if uploaded:
    try:
        df = pd.read_excel(uploaded)
        st.write("### Anteprima del file:")
        st.dataframe(df)

        columns = df.columns.tolist()

        if len(columns) < 2:
            st.error("⚠️ Il file deve contenere almeno due colonne.")
        else:
            col1 = st.selectbox("Seleziona la prima colonna", columns)
            col2 = st.selectbox("Seleziona la seconda colonna", columns)

            if st.button("Esegui Test di Wilcoxon"):
                serie1 = df[col1].dropna()
                serie2 = df[col2].dropna()

                if len(serie1) != len(serie2):
                    st.warning("Le due colonne devono avere la **stessa lunghezza** dopo la rimozione dei NaN.")
                else:
                    stat, p_value = wilcoxon(serie1, serie2)

                    st.subheader("📌 Risultati del Test di Wilcoxon")
                    st.write(f"**Statistic W:** {stat}")
                    st.write(f"**p-value:** {p_value}")

                    if p_value < 0.05:
                        st.error("❗ Differenza significativa (p < 0.05)")
                    else:
                        st.success("✔ Nessuna differenza significativa (p ≥ 0.05)")

    except Exception as e:
        st.error(f"Errore nella lettura del file: {e}")

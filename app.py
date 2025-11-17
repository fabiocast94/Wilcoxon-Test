import streamlit as st
import pandas as pd
from scipy.stats import wilcoxon

st.set_page_config(page_title="Test di Wilcoxon", page_icon="📊")

st.title("📊 Applicazione per Test di Wilcoxon")

st.write("""
Puoi eseguire il **Test di Wilcoxon** caricando un file Excel **oppure inserendo manualmente i valori**.
""")

# Selezione modalità
mode = st.radio(
    "Scegli il metodo per inserire i dati:",
    ["Carica file Excel", "Inserimento manuale dei dati"]
)

# ====================================================================================
# 1) MODALITÀ FILE EXCEL
# ====================================================================================
if mode == "Carica file Excel":
    uploaded = st.file_uploader("Carica un file Excel (.xlsx)", type=["xlsx"])

    if uploaded:
        try:
            df = pd.read_excel(uploaded)
            st.write("### Anteprima del file caricato:")
            st.dataframe(df)

            columns = df.columns.tolist()
            if len(columns) < 2:
                st.error("⚠️ Il file deve contenere almeno due colonne numeriche.")
            else:
                col1 = st.selectbox("Seleziona la prima colonna", columns)
                col2 = st.selectbox("Seleziona la seconda colonna", columns)

                if st.button("Esegui Test di Wilcoxon (File Excel)"):
                    serie1 = df[col1].dropna()
                    serie2 = df[col2].dropna()

                    if len(serie1) != len(serie2):
                        st.warning("⚠️ Le colonne selezionate devono avere la stessa lunghezza dopo il drop dei valori NaN.")
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

# ====================================================================================
# 2) MODALITÀ INSERIMENTO MANUALE
# ====================================================================================
elif mode == "Inserimento manuale dei dati":
    st.write("Inserisci i valori come liste di numeri separati da virgola.")

    input_x = st.text_area("Valori della prima serie (es: 10, 12, 9.5, 11)", "")
    input_y = st.text_area("Valori della seconda serie (es: 11, 13, 10, 12)", "")

    if st.button("Esegui Test di Wilcoxon (Dati manuali)"):
        try:
            x = [float(x.strip()) for x in input_x.split(",") if x.strip() != ""]
            y = [float(y.strip()) for y in input_y.split(",") if y.strip() != ""]

            if len(x) != len(y):
                st.error("⚠️ Le due liste devono avere la **stessa lunghezza**.")
            else:
                stat, p_value = wilcoxon(x, y)

                st.subheader("📌 Risultati del Test di Wilcoxon")
                st.write(f"**Statistic W:** {stat}")
                st.write(f"**p-value:** {p_value}")

                if p_value < 0.05:
                    st.error("❗ Differenza significativa (p < 0.05)")
                else:
                    st.success("✔ Nessuna differenza significativa (p ≥ 0.05)")

        except Exception as e:
            st.error(f"Errore nell'interpretazione dei dati: {e}")

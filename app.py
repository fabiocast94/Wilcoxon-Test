import streamlit as st
import pandas as pd
from scipy.stats import wilcoxon

st.set_page_config(page_title="Test di Wilcoxon", page_icon="📊")

st.title("📊 Applicazione per Test di Wilcoxon – Parametri Personalizzabili")

st.write("""
Questa applicazione permette di eseguire il **Test di Wilcoxon per dati appaiati**, 
con la possibilità di **modificare manualmente i parametri del test**.
""")

st.write("## 🔧 Parametri del Test")
st.write("""
Qui puoi modificare i parametri del test di Wilcoxon.  
Passa il mouse sopra ogni parametro per vedere la spiegazione.
""")

# -------------------------------
# PARAMETRI DEL TEST
# -------------------------------
colA, colB = st.columns(2)

with colA:
    alternative = st.selectbox(
        "alternative",
        options=["two-sided", "greater", "less"],
        help="""
Tipo di ipotesi statistica:
- **two-sided**: testa se c’è qualsiasi differenza
- **greater**: testa se x > y
- **less**: testa se x < y
Modificare questo parametro cambia il p-value.
        """
    )

    correction = st.checkbox(
        "correction (correzione di continuità)",
        value=False,
        help="""
Applica la correzione di continuità per piccole dimensioni del campione.
Rende il test più conservativo (p-value più alto).
        """
    )

with colB:
    zero_method = st.selectbox(
        "zero_method",
        options=["wilcox", "pratt", "zsplit"],
        help="""
Come trattare le differenze pari a 0 (x_i − y_i = 0):

- **wilcox (default)**: scarta le differenze zero  
- **pratt**: considera gli zero nella statistica → W e p possono cambiare  
- **zsplit**: divide gli zero tra positivi e negativi  
        """
    )

    mode = st.selectbox(
        "mode",
        options=["auto", "exact", "approx"],
        help="""
Metodo di calcolo del p-value:
- **auto**: scelta automatica (default)
- **exact**: calcolo esatto → più preciso per piccoli campioni
- **approx**: usa approssimazione normale → utile per grandi campioni
        """
    )

st.write("---")

# -------------------------------
# SCELTA: DATI EXCEL
# -------------------------------
st.write("## 📂 Caricamento dei dati")

uploaded = st.file_uploader("Carica un file Excel (.xlsx)", type=["xlsx"])

if uploaded:
    try:
        df = pd.read_excel(uploaded)
        st.write("### Anteprima del file:")
        st.dataframe(df)

        columns = df.columns.tolist()
        if len(columns) < 2:
            st.error("⚠️ Il file deve contenere almeno due colonne numeriche.")
        else:
            col1 = st.selectbox("Seleziona la prima colonna", columns)
            col2 = st.selectbox("Seleziona la seconda colonna", columns)

            if st.button("Esegui Test di Wilcoxon"):
                serie1 = df[col1].dropna()
                serie2 = df[col2].dropna()

                if len(serie1) != len(serie2):
                    st.warning("⚠️ Le colonne devono avere la stessa lunghezza dopo il drop dei NaN.")
                else:
                    stat, p_value = wilcoxon(
                        serie1,
                        serie2,
                        zero_method=zero_method,
                        correction=correction,
                        alternative=alternative,
                        mode=mode
                    )

                    st.subheader("📌 Risultati del Test di Wilcoxon")
                    st.write(f"**Statistic W:** {stat}")
                    st.write(f"**p-value:** {p_value}")

                    if p_value < 0.05:
                        st.error("❗ Differenza significativa (p < 0.05)")
                    else:
                        st.success("✔ Nessuna differenza significativa (p ≥ 0.05)")

    except Exception as e:
        st.error(f"Errore nella lettura del file: {e}")

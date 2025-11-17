import streamlit as st
from PIL import Image
import base64

# Caricamento immagine e conversione in base64
logo_path = "Policlinico.jpg"
with open(logo_path, "rb") as f:
    logo_bytes = f.read()
logo_base64 = base64.b64encode(logo_bytes).decode()

# Header con logo leggermente a sinistra e titolo centrato
st.markdown(
    f"""
    <div style="text-align: center;">
        <!-- Logo spostato leggermente a sinistra con margin-right -->
        <img src="data:image/jpg;base64,{logo_base64}" width="200" style="margin-right: 30px;">
        <h1>Test di Wilcoxon</h1>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("---")
st.write("""
Questa applicazione permette di eseguire il **Test di Wilcoxon per dati appaiati**, 
con la possibilità di **modificare manualmente i parametri del test**.
""")

# ----------------------------
# PARAMETRI DEL TEST
# ----------------------------
st.write("## 🔧 Parametri del Test")
st.write("""
Puoi modificare i parametri del test. Passa il mouse sopra ogni parametro per leggere la spiegazione.
""")

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
Applica la correzione di continuità per piccoli campioni. Rende il test più conservativo.
        """
    )

with colB:
    zero_method = st.selectbox(
        "zero_method",
        options=["wilcox", "pratt", "zsplit"],
        help="""
Come trattare le differenze pari a 0 (x_i − y_i = 0):
- **wilcox**: scarta gli zero
- **pratt**: considera gli zero nella statistica
- **zsplit**: divide gli zero tra positivi e negativi
        """
    )

    mode = st.selectbox(
        "mode",
        options=["auto", "exact", "approx"],
        help="""
Metodo di calcolo del p-value:
- **auto**: scelta automatica
- **exact**: calcolo esatto (piccoli campioni)
- **approx**: approssimazione normale (grandi campioni)
        """
    )

st.write("---")

# ----------------------------
# CARICAMENTO FILE EXCEL
# ----------------------------
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

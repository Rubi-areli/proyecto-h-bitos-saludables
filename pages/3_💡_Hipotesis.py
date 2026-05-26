import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Hipótesis", page_icon="💡", layout="wide")

st.markdown("""
<style>
    .hip-card {
        background: linear-gradient(135deg, #2a1a3e, #3d2060);
        border-left: 4px solid #a855f7;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1.5rem;
    }
    .hip-card h3 { color: #c084fc; margin: 0 0 0.4rem 0; }
    .hip-card p  { color: #a78bca; margin: 0; font-style: italic; }

    .result-box {
        background: #1e1030;
        border: 1px solid #7c3aed;
        border-radius: 10px;
        padding: 1rem 1.5rem;
        margin-top: 1rem;
    }
    .result-box p { color: #c4b5fd; margin: 0; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("data/Test_Data.csv")

df = load_data()

# ── BANNER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background: linear-gradient(135deg, #2a1a3e 0%, #3d2060 100%);
     padding: 2.5rem 2rem; border-radius: 16px; text-align: center; margin-bottom: 2rem;">
    <h1 style="color:#c084fc; margin:0;">💡 Validación de Hipótesis</h1>
    <p style="color:#a78bca; margin-top:0.5rem;">Análisis estadístico para validar supuestos sobre hábitos de salud</p>
</div>
""", unsafe_allow_html=True)

# ── HIPÓTESIS 1 ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hip-card">
    <h3>Hipótesis 1 — Zona de residencia vs enfermedades</h3>
    <p>Las personas que viven en zonas urbanas presentan mayor frecuencia de enfermedades
    debido a factores como estrés, contaminación y estilo de vida.</p>
</div>""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    agrupado = df.groupby('Living in?')['Illness count last year'].mean().reset_index()
    st.dataframe(agrupado, use_container_width=True)

with col2:
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    fig1.patch.set_facecolor('#1e1030')
    ax1.set_facecolor('#1e1030')
    sns.barplot(data=df, x='Living in?', y='Illness count last year',
                estimator='mean', errorbar=None, ax=ax1,
                palette=["#e832f8", "#13ec30"])
    ax1.set_title('Promedio de enfermedades según zona', color='white')
    ax1.tick_params(colors='white')
    for spine in ax1.spines.values():
        spine.set_edgecolor("#9061e0")
    st.pyplot(fig1)
    plt.close()

st.markdown("""
<div class="result-box">
    <p>📊 <b>Interpretación:</b> El gráfico muestra el promedio de enfermedades entre zonas urbanas
    y rurales. Las diferencias observadas permiten explorar si el entorno residencial
    influye en la salud de las personas.</p>
</div>
<br>""", unsafe_allow_html=True)

# ── HIPÓTESIS 2 ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hip-card">
    <h3>Hipótesis 2 — Tabaquismo vs BMI</h3>
    <p>El hábito de fumar influye en el índice de masa corporal (BMI) de las personas.</p>
</div>""", unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.dataframe(df.groupby('Smoker?')['BMI'].describe(), use_container_width=True)

with col4:
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    fig2.patch.set_facecolor('#1e1030')
    ax2.set_facecolor('#1e1030')
    sns.boxplot(data=df, x='Smoker?', y='BMI', ax=ax2,
                palette=["#55f7c6", "#f1621f"])
    ax2.set_title('BMI según hábito de fumar', color='white')
    ax2.tick_params(colors='white')
    for spine in ax2.spines.values():
        spine.set_edgecolor('#7c3aed')
    st.pyplot(fig2)
    plt.close()

st.markdown("""
<div class="result-box">
    <p>📊 <b>Interpretación:</b> El boxplot permite visualizar la dispersión del BMI entre
    fumadores y no fumadores, identificando diferencias en la distribución y posibles
    valores atípicos.</p>
</div>""", unsafe_allow_html=True)
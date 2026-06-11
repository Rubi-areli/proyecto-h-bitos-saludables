import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Hipótesis", page_icon="💡", layout="wide")

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }

.hero-container {
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
    border-bottom: 1px solid #c9a84c44;
    border-radius: 20px;
    padding: 3rem;
    text-align: center;
    margin-bottom: 2rem;
}

.hero-title {
    font-size: 2.8rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0;
}

.hero-title span {
    color: #c9a84c;
}

.hero-sub {
    color: #8899aa;
    font-size: 0.9rem;
    margin-top: 0.8rem;
}

.section-label {
    color: #8899aa;
    font-size: 0.72rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #2a2a3e;
}

.hip-card {
    background: #0f0f1a;
    border-left: 3px solid #c9a84c;
    border-radius: 0 12px 12px 0;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}

.hip-card h3 {
    color: #ffffff;
    margin-bottom: 0.5rem;
}

.hip-card p {
    color: #8899aa;
    margin: 0;
    line-height: 1.7;
}

.result-box {
    background: #0f0f1a;
    border-top: 2px solid #c9a84c;
    border-radius: 0 0 10px 10px;
    padding: 1.2rem;
    margin-top: 1rem;
}

.result-box p {
    color: #8899aa;
    margin: 0;
    line-height: 1.7;
}

.metric-card {
    background: #0f0f1a;
    border-top: 2px solid #c9a84c;
    border-radius: 0 0 8px 8px;
    padding: 1.2rem;
    text-align: center;
}

.metric-num {
    color: #ffffff;
    font-size: 2rem;
    font-weight: 700;
}

.metric-lbl {
    color: #8899aa;
    font-size: 0.75rem;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.divider-gold {
    height: 1px;
    background: linear-gradient(
        90deg,
        transparent,
        #c9a84c33,
        transparent
    );
    margin: 2rem 0;
}

</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("data/Test_Data.csv")

df = load_data()

# ─────────────────────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────────────────────

st.markdown("""
<div class="hero-container">
    <h1 
            <h1 style="color:#ffffff; margin:0;">💡 Validación de Hipótesis</h1>
    </h1>
    <p class="hero-sub">
        Análisis estadístico y visual para comprobar relaciones entre hábitos y salud
    </p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# MÉTRICAS
# ─────────────────────────────────────────────────────────────

st.markdown(
    '<p class="section-label">Indicadores Generales</p>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)

c1.markdown(f"""
<div class="metric-card">
<div class="metric-num">{len(df):,}</div>
<div class="metric-lbl">Registros</div>
</div>
""", unsafe_allow_html=True)

c2.markdown(f"""
<div class="metric-card">
<div class="metric-num">{df.shape[1]}</div>
<div class="metric-lbl">Variables</div>
</div>
""", unsafe_allow_html=True)

c3.markdown(f"""
<div class="metric-card">
<div class="metric-num">{df['Age'].mean():.1f}</div>
<div class="metric-lbl">Edad Promedio</div>
</div>
""", unsafe_allow_html=True)

c4.markdown(f"""
<div class="metric-card">
<div class="metric-num">{df['BMI'].mean():.1f}</div>
<div class="metric-lbl">BMI Promedio</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider-gold"></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# HIPÓTESIS 1
# ─────────────────────────────────────────────────────────────

st.markdown("""
<div class="hip-card">
<h3>Hipótesis 1 — Zona de residencia vs enfermedades</h3>

<p>
Las personas que viven en zonas urbanas podrían presentar una mayor frecuencia
de enfermedades debido a factores ambientales, contaminación,
estrés y estilos de vida más acelerados.
</p>

</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    agrupado = (
        df.groupby('Living in?')['Illness count last year']
        .mean()
        .reset_index()
    )

    st.dataframe(
        agrupado,
        width="stretch"
    )

with col2:

    fig1, ax1 = plt.subplots(figsize=(7,4))

    fig1.patch.set_facecolor('#0f0f1a')
    ax1.set_facecolor('#0f0f1a')

    sns.barplot(
        data=df,
        x='Living in?',
        y='Illness count last year',
        estimator='mean',
        errorbar=None,
        palette=["#c9a84c", "#01060e"],
        ax=ax1
    )

    ax1.set_title(
        "Promedio de enfermedades según zona",
        color="white"
    )

    ax1.tick_params(colors="white")

    for spine in ax1.spines.values():
        spine.set_edgecolor("#c9a84c")

    st.pyplot(fig1)
    plt.close()

st.markdown("""
<div class="result-box">
<p>

📊 <b>Interpretación:</b>

La comparación permite identificar si existe una diferencia apreciable
en el promedio de enfermedades reportadas entre personas que viven
en áreas urbanas y rurales.

</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider-gold"></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# HIPÓTESIS 2
# ─────────────────────────────────────────────────────────────

st.markdown("""
<div class="hip-card">
<h3>Hipótesis 2 — Tabaquismo vs BMI</h3>

<p>
El hábito de fumar puede influir en el Índice de Masa Corporal (BMI),
generando diferencias en la distribución de peso corporal entre fumadores
y no fumadores.
</p>

</div>
""", unsafe_allow_html=True)

col3, col4 = st.columns([1, 2])

with col3:

    st.dataframe(
        df.groupby('Smoker?')['BMI']
        .describe()
        .round(2),
        width="stretch"
    )

with col4:

    fig2, ax2 = plt.subplots(figsize=(7,4))

    fig2.patch.set_facecolor('#0f0f1a')
    ax2.set_facecolor('#0f0f1a')

    sns.boxplot(
        data=df,
        x='Smoker?',
        y='BMI',
        palette=["#c9a84c", "#4caf50"],
        ax=ax2
    )

    ax2.set_title(
        "BMI según hábito de fumar",
        color="white"
    )

    ax2.tick_params(colors="white")

    for spine in ax2.spines.values():
        spine.set_edgecolor("#c9a84c")

    st.pyplot(fig2)
    plt.close()

st.markdown("""
<div class="result-box">
<p>

📊 <b>Interpretación:</b>

El boxplot permite analizar diferencias en la distribución del BMI,
identificando variaciones, dispersión de datos y posibles valores
atípicos entre fumadores y no fumadores.

</p>
</div>
""", unsafe_allow_html=True)
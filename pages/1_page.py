import streamlit as st
import pandas as pd

st.set_page_config(page_title="Inicio", page_icon="🌿", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }

.hero-container {
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
    border-bottom: 1px solid #c9a84c44;
    border-radius: 20px;
    padding: 4rem 3rem;
    text-align: center;
    margin-bottom: 3rem;
    position: relative;
    overflow: hidden;
}
.hero-container::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #c9a84c, transparent);
}
.hero-title {
    font-size: 3.2rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0;
    letter-spacing: -1px;
}
.hero-title span { color: #c9a84c; }
.hero-sub {
    color: #8899aa;
    font-size: 0.8rem;
    margin-top: 0.8rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    font-weight: 300;
}
.hero-badge {
    display: inline-block;
    background: rgba(201,168,76,0.08);
    color: #c9a84c;
    border: 1px solid rgba(201,168,76,0.2);
    border-radius: 3px;
    padding: 3px 12px;
    font-size: 0.72rem;
    margin: 3px;
    letter-spacing: 1.5px;
}

.profile-card {
    background: #0f0f1a;
    border-left: 2px solid #c9a84c;
    border-radius: 0 12px 12px 0;
    padding: 2rem;
}
.profile-name {
    color: #ffffff;
    font-size: 1.6rem;
    font-weight: 600;
    margin: 0 0 0.2rem 0;
}
.profile-title {
    color: #c9a84c;
    font-size: 0.78rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
}
.profile-bio {
    color: #8899aa;
    font-size: 0.9rem;
    line-height: 1.8;
}
.tag {
    display: inline-block;
    color: #8899aa;
    border: 1px solid #2a2a3e;
    border-radius: 3px;
    padding: 2px 10px;
    font-size: 0.72rem;
    margin: 3px 2px;
    letter-spacing: 0.5px;
}

.metric-card {
    background: #0f0f1a;
    border-top: 2px solid #c9a84c;
    border-radius: 0 0 8px 8px;
    padding: 1.5rem;
    text-align: center;
}
.metric-num {
    font-size: 2.4rem;
    font-weight: 700;
    color: #ffffff;
}
.metric-lbl {
    font-size: 0.72rem;
    color: #8899aa;
    margin-top: 4px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}

.nav-card {
    background: #0f0f1a;
    border-bottom: 1px solid #2a2a3e;
    border-radius: 8px;
    padding: 1.4rem 1.8rem;
    margin-bottom: 0.8rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 1rem;
}
.nav-card:hover { border-bottom-color: #c9a84c; }
.nav-card-num {
    color: #c9a84c;
    font-size: 1.2rem;
    font-weight: 700;
    min-width: 30px;
    font-family: monospace;
}
.nav-card h4 {
    color: #ffffff;
    margin: 0 0 0.2rem 0;
    font-size: 0.95rem;
    font-weight: 600;
}
.nav-card p {
    color: #8899aa;
    margin: 0;
    font-size: 0.82rem;
    line-height: 1.4;
}

.section-label {
    color: #8899aa;
    font-size: 0.72rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #2a2a3e;
}
.divider-gold {
    height: 1px;
    background: linear-gradient(90deg, transparent, #c9a84c33, transparent);
    margin: 2.5rem 0;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("data/Test_Data.csv")

df = load_data()

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-container">
    <p class="hero-sub">Portafolio Profesional · Ciencia de Datos · UGB · 2026</p>
    <h1 class="hero-title">Análisis de <span>Hábitos Saludables</span></h1>
    <p style="color:#8899aa; margin-top:1rem; font-size:0.95rem;
       max-width:580px; margin-left:auto; margin-right:auto; line-height:1.7;">
        Exploración estadística, machine learning y análisis de sentimientos
        aplicados a datos de vida y salud de 6,480 personas.
    </p>
    <div style="margin-top:1.8rem;">
        <span class="hero-badge">PYTHON</span>
        <span class="hero-badge">STREAMLIT</span>
        <span class="hero-badge">SCIKIT-LEARN</span>
        <span class="hero-badge">NLP</span>
        <span class="hero-badge">DATA SCIENCE</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── PERFIL ────────────────────────────────────────────────────────────────────
col_foto, col_info = st.columns([1, 2], gap="large")

with col_foto:
    try:
        st.image("utils/foto.jpg", width=220)
    except:
        try:
            st.image("utils/foto.jpeg", width=220)
        except:
            st.info("Agrega tu foto en utils/foto.jpg")

with col_info:
    st.markdown("""
    <div class="profile-card">
        <p class="profile-name">Rubia Areli Alvarenga de Mendoza</p>
        <p class="profile-title">Ingeniería en Sistemas y Redes Informáticas &nbsp;·&nbsp; Universidad Gerardo Barrios</p>
        <p class="profile-bio">
        Estudiante apasionada por la tecnología y el análisis de datos, con interés
        en el desarrollo de soluciones inteligentes mediante Python y herramientas de
        Ciencia de Datos. En este portafolio se presenta un análisis completo de hábitos
        de vida saludables, aplicando técnicas de exploración de datos, validación de
        hipótesis, aprendizaje automático y análisis de sentimientos. 
        </p>
        <div style="margin-top:1.5rem;">
            <span class="tag">Python</span>
            <span class="tag">Streamlit</span>
            <span class="tag">Machine Learning</span>
            <span class="tag">Pandas</span>
            <span class="tag">Seaborn</span>
            <span class="tag">Scikit-learn</span>
            <span class="tag">NLP</span>
            <span class="tag">TextBlob</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="divider-gold"></div>', unsafe_allow_html=True)

# ── MÉTRICAS ──────────────────────────────────────────────────────────────────
st.markdown('<p class="section-label">Dataset — Hábitos Saludables</p>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
for col, (num, lbl) in zip([c1,c2,c3,c4], [
    (f"{len(df):,}", "Registros"),
    (str(df.shape[1]), "Variables"),
    (f"{df['Age'].mean():.1f} años", "Edad Promedio"),
    (f"{df['BMI'].mean():.1f}", "BMI Promedio"),
]):
    col.markdown(f"""
    <div class="metric-card">
        <div class="metric-num">{num}</div>
        <div class="metric-lbl">{lbl}</div>
    </div>""", unsafe_allow_html=True)

st.markdown('<div class="divider-gold"></div>', unsafe_allow_html=True)

# ── VIDEO ─────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-label">Data Storytelling</p>', unsafe_allow_html=True)
st.video("https://youtu.be/n_7QkX-q_HY")

st.markdown('<div class="divider-gold"></div>', unsafe_allow_html=True)
# ── NAVEGACIÓN ────────────────────────────────────────────────────────────────
st.markdown('<p class="section-label">Contenido del Portafolio</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

nav_items = [
    ("01", "Análisis Exploratorio", "Descripción del dataset, campos, navegador, graficador e hipótesis validadas.", "EDA"),
    ("02", "Machine Learning", "K-Means, Regresión Logística y Lineal con selección interactiva de variables.", "Machine Learning"),
    ("03", "Sistema de Recomendación", "Recomendador de recetas saludables según objetivos y preferencias.", "Recomendacion"),
    ("04", "Carga de Archivos", "Análisis automático de cualquier archivo CSV o Excel con gráficos.", "Carga de Archivos"),
    ("05", "Análisis de Sentimientos", "Scraping web, NLP con TextBlob, WordCloud y análisis de polaridad.", "Sentimientos"),
    ("06", "Hipótesis", "Validación estadística y visual de hipótesis sobre hábitos de salud.", "EDA"),
]

for i, (num, titulo, desc, pagina) in enumerate(nav_items):
    col = col1 if i % 2 == 0 else col2
    with col:
        st.markdown(f"""
        <div class="nav-card">
            <div class="nav-card-num">{num}</div>
            <div>
                <h4>{titulo}</h4>
                <p>{desc}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

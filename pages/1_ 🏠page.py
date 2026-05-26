import streamlit as st
import pandas as pd

# ── Banner ────────────────────────────────────────────────────────────────────
st.image("utils/banner.png", use_container_width=True)
st.set_page_config(
    page_title="Hábitos Saludables",
    page_icon="🌿",
    layout="wide"
)

# ── CSS general ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .hero {
        background: linear-gradient(135deg, #1a472a 0%, #2d6a4f 50%, #1b4332 100%);
        padding: 3rem 2rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .hero h1 { color: #d8f3dc; font-size: 2.8rem; margin: 0; }
    .hero p  { color: #b7e4c7; font-size: 1.2rem; margin-top: 0.5rem; }

    .card {
        background: #1a1f2e;
        border: 1px solid #2d6a4f;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .card h3 { color: #74c69d; margin-top: 0; }
    .card p  { color: #adb5bd; }

    .metric-box {
        background: linear-gradient(135deg, #1b4332, #2d6a4f);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        border: 1px solid #40916c;
    }
    .metric-box .num { font-size: 2rem; font-weight: 800; color: #d8f3dc; }
    .metric-box .lbl { font-size: 0.85rem; color: #95d5b2; margin-top: 4px; }

    .tag {
        display: inline-block;
        background: #2d6a4f;
        color: #d8f3dc;
        border-radius: 20px;
        padding: 4px 14px;
        font-size: 0.82rem;
        margin: 3px;
    }
</style>
""", unsafe_allow_html=True)

# ── Cargar datos ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv("data/Test_Data.csv")

df = load_data()

# ── HERO ──────────────────────────────────────────────────────────────────────


# ── MÉTRICAS ──────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-box">
        <div class="num">{len(df):,}</div>
        <div class="lbl">📋 Registros</div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-box">
        <div class="num">{df.shape[1]}</div>
        <div class="lbl">📊 Variables</div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-box">
        <div class="num">{df['Age'].mean():.1f}</div>
        <div class="lbl">📅 Edad promedio</div>
    </div>""", unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-box">
        <div class="num">{df['BMI'].mean():.1f}</div>
        <div class="lbl">⚖️ BMI promedio</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── CARDS ─────────────────────────────────────────────────────────────────────
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("""
    <div class="card">
        <h3>📌 Sobre el proyecto</h3>
        <p>Análisis de hábitos de vida y su relación con la salud,
        usando técnicas de EDA, visualización estadística y Machine Learning.</p>
        <span class="tag">Python</span>
        <span class="tag">Streamlit</span>
        <span class="tag">Scikit-learn</span>
        <span class="tag">Seaborn</span>
        <span class="tag">Pandas</span>
    </div>

    <div class="card">
        <h3>🎯 Objetivo</h3>
        <p>Predecir el número de enfermedades en el último año
        a partir de los hábitos de vida de cada persona.</p>
    </div>
    """, unsafe_allow_html=True)

with col_b:
    st.markdown("""
    <div class="card">
        <h3>📂 Variables del dataset</h3>
        <p>
        🥗 Alimentación · preferencia y seguimiento de dieta<br>
        🏃 Actividad física · horas de sueño<br>
        🧠 Salud mental · interacción social<br>
        🚬 Factores de riesgo · tabaco, alcohol, hereditarios<br>
        🏙️ Contexto · residencia, BMI, edad
        </p>
    </div>

    <div class="card">
        <h3>🗺️ Navegación</h3>
        <p>
        📊 <b>EDA</b> — Exploración y estadísticas<br>
        💡 <b>Hipótesis</b> — Validación con gráficos<br>
        🤖 <b>Machine Learning</b> — Clustering y predicción
        </p>
    </div>
    """, unsafe_allow_html=True)


# ── PREVIEW ───────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("🔍 Vista previa del dataset")
st.dataframe(df.head(8), use_container_width=True)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="EDA", page_icon="📊", layout="wide")

st.markdown("""
<style>
    .section-header {
        background: linear-gradient(135deg, #1a1f2e, #2c3e6b);
        border-left: 4px solid #4a9eff;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin-bottom: 1.5rem;
    }
    .section-header h2 { color: #7eb8ff; margin: 0; font-size: 1.5rem; }
    .section-header p  { color: #8899bb; margin: 0.3rem 0 0 0; font-size: 0.9rem; }

    .metric-box {
        background: linear-gradient(135deg, #1a2744, #2c3e6b);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        border: 1px solid #3a5a9a;
    }
    .metric-box .num { font-size: 2rem; font-weight: 800; color: #7eb8ff; }
    .metric-box .lbl { font-size: 0.85rem; color: #8899bb; margin-top: 4px; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("data/Test_Data.csv")

df = load_data()

# ── BANNER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background: linear-gradient(135deg, #1a2744 0%, #2c3e6b 100%);
     padding: 2.5rem 2rem; border-radius: 16px; text-align: center; margin-bottom: 2rem;">
    <h1 style="color:#7eb8ff; margin:0;">📊 Análisis Exploratorio de Datos</h1>
    <p style="color:#8899bb; margin-top:0.5rem;">Exploración estadística del dataset de hábitos saludables</p>
</div>
""", unsafe_allow_html=True)

# ── MÉTRICAS ──────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
metrics = [
    (f"{df.shape[0]:,}", "📋 Registros"),
    (str(df.shape[1]), "📊 Variables"),
    (str(df.isnull().sum().sum()), "❌ Valores nulos"),
    (f"{len(df.dropna()):,}", "✅ Registros completos"),
]
for col, (num, lbl) in zip([c1,c2,c3,c4], metrics):
    col.markdown(f"""
    <div class="metric-box">
        <div class="num">{num}</div>
        <div class="lbl">{lbl}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── ESTADÍSTICAS ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <h2>📋 Estadísticas Generales</h2>
    <p>Resumen estadístico de todas las variables numéricas</p>
</div>""", unsafe_allow_html=True)
st.dataframe(df.describe(), use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── GRÁFICOS FILA 1 ───────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <h2>📈 Distribuciones</h2>
    <p>Visualización de variables clave del dataset</p>
</div>""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(7, 4))
    fig.patch.set_facecolor('#1a2744')
    ax.set_facecolor('#1a2744')


    sns.histplot(df['BMI'], kde=True, ax=ax, color="#8db8e9")
    ax.set_title('Distribución del BMI', color='white')
    ax.tick_params(colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    for spine in ax.spines.values():
        spine.set_edgecolor('#3a5a9a')
    st.pyplot(fig)
    plt.close()

with col2:
    fig2, ax2 = plt.subplots(figsize=(7, 4))
    fig2.patch.set_facecolor("#748fc9")
    ax2.set_facecolor('#1a2744')
    col_edad = [c for c in df.columns if 'age' in c.lower() or 'edad' in c.lower()]
    if col_edad:
        sns.histplot(df[col_edad[0]].dropna(), kde=True, ax=ax2, color="#f3344d")
        ax2.set_title(f'Distribución de {col_edad[0]}', color='white')
    else:
        sns.histplot(df['Physical activity'].dropna(), kde=True, ax=ax2, color='#7eb8ff')
        ax2.set_title('Distribución de Actividad Física', color='white')
    ax2.tick_params(colors='white')
    for spine in ax2.spines.values():
        spine.set_edgecolor("#f7e92d")
    st.pyplot(fig2)
    plt.close()
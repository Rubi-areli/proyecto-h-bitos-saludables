import streamlit as st
import pandas as pd
import requests
import json

st.set_page_config(page_title="Interfaz IA", page_icon="🤖", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }

.hero-container {
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
    border-radius: 20px;
    padding: 3rem 2rem;
    text-align: center;
    margin-bottom: 2rem;
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
    font-size: 2.5rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0;
}
.hero-title span { color: #c9a84c; }

.chat-user {
    background: #0f0f1a;
    border-left: 2px solid #c9a84c;
    border-radius: 0 8px 8px 0;
    padding: 1rem 1.5rem;
    margin-bottom: 1rem;
    color: #ffffff;
    font-size: 0.95rem;
}
.chat-ai {
    background: #0f0f1a;
    border-left: 2px solid #4a9eff;
    border-radius: 0 8px 8px 0;
    padding: 1rem 1.5rem;
    margin-bottom: 1.5rem;
    color: #d0d8e8;
    font-size: 0.9rem;
    line-height: 1.7;
}
.chat-label-user {
    color: #c9a84c;
    font-size: 0.72rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}
.chat-label-ai {
    color: #4a9eff;
    font-size: 0.72rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
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
</style>
""", unsafe_allow_html=True)

# ── CARGAR DATOS ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv("data/Test_Data.csv")

df = load_data()

# ── BANNER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-container">
    <p style="color:#8899aa; font-size:0.75rem; letter-spacing:3px;
       text-transform:uppercase; margin-bottom:0.8rem;">
       Inteligencia Artificial · Consultas en Lenguaje Natural</p>
    <h1 class="hero-title">Asistente <span>IA</span></h1>
    <p style="color:#8899aa; margin-top:0.8rem; font-size:0.9rem;">
        Haz preguntas sobre el dataset de hábitos saludables en español o inglés
    </p>
</div>
""", unsafe_allow_html=True)

# ── HISTORIAL ─────────────────────────────────────────────────────────────────
if 'historial' not in st.session_state:
    st.session_state.historial = []

# ── EJEMPLOS ──────────────────────────────────────────────────────────────────
st.markdown('<p class="section-label">Preguntas sugeridas</p>', unsafe_allow_html=True)

ejemplos = [
    "¿Cuántas filas y columnas tiene el dataset?",
    "¿Cuál es la edad promedio?",
    "¿Cuántas personas fuman?",
    "¿Cuál es el BMI máximo y mínimo?",
    "¿Cuántas personas viven en zona urbana vs rural?",
    "¿Cuál es el promedio de enfermedades al año?",
]

cols = st.columns(3)
for i, ejemplo in enumerate(ejemplos):
    with cols[i % 3]:
        if st.button(ejemplo, key=f"ej_{i}", use_container_width=True):
            st.session_state['pregunta_actual'] = ejemplo

st.divider()

# ── INPUT ─────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-label">Tu pregunta</p>', unsafe_allow_html=True)

pregunta = st.text_input(
    "Escribe tu pregunta:",
    value=st.session_state.get('pregunta_actual', ''),
    placeholder="Ej: ¿Cuál es la correlación entre BMI y enfermedades?",
    label_visibility="collapsed"
)

col_btn, col_clear = st.columns([1, 5])
enviar = col_btn.button("Consultar", type="primary")
if col_clear.button("Limpiar historial"):
    st.session_state.historial = []
    st.session_state['pregunta_actual'] = ''
    st.rerun()

# ── PROCESAR PREGUNTA ─────────────────────────────────────────────────────────
if enviar and pregunta.strip():
    resumen = f"""
Dataset: Hábitos Saludables
- Filas: {df.shape[0]}
- Columnas: {df.shape[1]}
- Columnas disponibles: {', '.join(df.columns.tolist())}

Estadísticas principales:
{df.describe().to_string()}

Valores categóricos:
- Smoker?: {df['Smoker?'].value_counts().to_dict()}
- Living in?: {df['Living in?'].value_counts().to_dict()}
- Food preference: {df['Food preference'].value_counts().to_dict()}
- Any heriditary condition?: {df['Any heriditary condition?'].value_counts().to_dict()}

Nulos por columna:
{df.isnull().sum().to_dict()}
"""

    prompt = f"""Eres un asistente experto en análisis de datos. 
Tienes acceso al siguiente resumen de un dataset de hábitos saludables:

{resumen}

El usuario pregunta: {pregunta}

Responde de forma clara, precisa y en el mismo idioma de la pregunta.
Si la pregunta es sobre estadísticas, da los números exactos del dataset.
Sé conciso pero completo. Máximo 5 líneas."""

    with st.spinner("Analizando..."):
        try:
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers={"Content-Type": "application/json"},
                json={
                    "model": "claude-sonnet-4-20250514",
                    "max_tokens": 500,
                    "messages": [{"role": "user", "content": prompt}]
                },
                timeout=30
            )
            data = response.json()
            respuesta = data['content'][0]['text']
        except Exception as e:
            respuesta = f"Error al conectar con la IA: {e}"

    st.session_state.historial.append({
        'pregunta': pregunta,
        'respuesta': respuesta
    })
    st.session_state['pregunta_actual'] = ''
    st.rerun()

# ── HISTORIAL ─────────────────────────────────────────────────────────────────
if st.session_state.historial:
    st.markdown('<p class="section-label">Conversación</p>', unsafe_allow_html=True)

    for item in reversed(st.session_state.historial):
        st.markdown(f"""
        <div>
            <p class="chat-label-user">Tú</p>
            <div class="chat-user">{item['pregunta']}</div>
        </div>
        <div>
            <p class="chat-label-ai">Asistente IA</p>
            <div class="chat-ai">{item['respuesta']}</div>
        </div>
        """, unsafe_allow_html=True) 
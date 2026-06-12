import streamlit as st
import pandas as pd
import requests
import json
import google.generativeai as genai  # <-- Importamos la librería de Google

st.set_page_config(page_title="Interfaz IA", page_icon="🤖", layout="wide")

# Conectar la API Key de Google AI Studio desde los Secrets de Streamlit
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("🔑 Falta la clave 'GEMINI_API_KEY' en los Secrets de Streamlit Cloud o en tu archivo secrets.toml local.")

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
        # Corregido de use_container_width=True a width="stretch" por las alertas de la versión 1.57+
        if st.button(ejemplo, key=f"ej_{i}", width="stretch"):
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

# ── PROCESAR PREGUNTA CON GEMINI ──────────────────────────────────────────────
if enviar and pregunta.strip():
    # Creamos un contexto estadístico estructurado para inyectarle a la IA
 # Resumen optimizado y ligero en tokens
    resumen = f"""
Dataset: Hábitos Saludables
- Dimensiones: {df.shape[0]} filas y {df.shape[1]} columnas.
- Columnas: {', '.join(df.columns.tolist())}
- Edad promedio: {df['Age'].mean():.1f} años.
- BMI promedio: {df['BMI'].mean():.2f}.
- Total Fumadores (YES): {df['Smoker?'].value_counts().get('YES', 0)}
- Distribución Zona: Urbana ({df['Living in?'].value_counts().get('URBAN', 0)}), Rural ({df['Living in?'].value_counts().get('RURAL', 0)})
- Promedio Enfermedades/año: {df['Illness count last year'].mean():.2f}
"""

    prompt_completo = f"""Eres un asistente analista de datos clínico y experto en hábitos saludables.
Tienes acceso directo al siguiente resumen estructurado del dataset que contiene las respuestas de los usuarios:

{resumen}

El usuario te hace la siguiente pregunta: {pregunta}

Instrucciones obligatorias:
1. Responde de forma clara, precisa y exclusivamente en el mismo idioma en que te hablaron.
2. Si la pregunta requiere cálculos estadísticos (promedios, máximos, mínimos, conteos), básate estrictamente en los datos numéricos provistos en el resumen de arriba.
3. Sé profesional pero accesible. Máximo 5 líneas de respuesta. No inventes datos que no estén descritos arriba.
"""

    with st.spinner("Analizando con Gemini..."):
        try:
            # Obtenemos la API Key desde los secrets de Streamlit
            api_key = st.secrets["GEMINI_API_KEY"]
            
            # Construimos la URL directa a la API oficial de Google usando el modelo correcto
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            
            # Estructuramos la petición exactamente como la pide Google en su documentación
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": f"{prompt_completo}"}
                        ]
                    }
                ]
            }
            headers = {'Content-Type': 'application/json'}
            
            # Hacemos la consulta directa a internet
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response_json = response.json()
            
            # Extraemos la respuesta de texto de la IA de forma segura
            if response.status_code == 200:
                respuesta = response_json['candidates'][0]['content']['parts'][0]['text']
            else:
                respuesta = f"❌ Error de la API de Google (Código {response.status_code}): {response_json.get('error', {}).get('message', 'Error desconocido')}"
                
        except Exception as e:
            respuesta = f"❌ Error inesperado al procesar la pregunta: {e}"
            
    # Guardar en el historial interactivo
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
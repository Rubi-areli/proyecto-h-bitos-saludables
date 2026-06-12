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
            p = pregunta.lower()

            if any(x in p for x in ['fila', 'row', 'registro', 'cuantos datos']):
                respuesta = f"El dataset tiene **{df.shape[0]:,} filas** y **{df.shape[1]} columnas**."

            elif any(x in p for x in ['columna', 'variable', 'campo']):
                respuesta = f"El dataset tiene **{df.shape[1]} columnas**: {', '.join(df.columns.tolist())}."

            elif any(x in p for x in ['edad', 'age', 'promedio edad']):
                respuesta = f"La **edad promedio** es {df['Age'].mean():.1f} años. Mínima: {df['Age'].min()}, Máxima: {df['Age'].max()}."

            elif any(x in p for x in ['bmi', 'masa corporal', 'peso']):
                respuesta = f"El **BMI promedio** es {df['BMI'].mean():.2f}. Mínimo: {df['BMI'].min():.1f}, Máximo: {df['BMI'].max():.1f}."

            elif any(x in p for x in ['fum', 'smok', 'cigarro', 'tabaco']):
                fum = df['Smoker?'].value_counts()
                respuesta = f"**Fumadores:** {fum.get('YES', 0):,} personas. **No fumadores:** {fum.get('NO', 0):,} personas."

            elif any(x in p for x in ['urban', 'rural', 'zona', 'viv', 'living']):
                zona = df['Living in?'].value_counts()
                respuesta = f"**Zona urbana:** {zona.get('URBAN', 0):,} personas. **Zona rural:** {zona.get('RURAL', 0):,} personas."

            elif any(x in p for x in ['enfermedad', 'illness', 'sick', 'enfermos']):
                respuesta = f"El **promedio de enfermedades** al año es {df['Illness count last year'].mean():.2f}. Máximo: {df['Illness count last year'].max():.0f}."

            elif any(x in p for x in ['actividad', 'activity', 'ejercicio', 'físic']):
                respuesta = f"El **nivel promedio de actividad física** es {df['Physical activity'].mean():.2f} (escala 0-5)."

            elif any(x in p for x in ['sueño', 'sleep', 'dormir', 'horas']):
                respuesta = f"El **promedio de horas de sueño** es {df['Regular sleeping hours'].mean():.2f} (escala 0-5)."

            elif any(x in p for x in ['alcohol', 'bebida', 'drink']):
                respuesta = f"El **promedio de consumo de alcohol** es {df['Alcohol consumption'].mean():.2f} (escala 0-5)."

            elif any(x in p for x in ['dieta', 'diet', 'alimenta', 'comida', 'food']):
                food = df['Food preference'].value_counts()
                respuesta = f"**Preferencias alimentarias:** {food.to_dict()}"

            elif any(x in p for x in ['suplemento', 'supplement', 'vitamina']):
                respuesta = f"El **promedio de toma de suplementos** es {df['Taking supplements'].mean():.2f} (escala 0-5)."

            elif any(x in p for x in ['mental', 'salud mental', 'estrés', 'stress']):
                respuesta = f"El **promedio de gestión de salud mental** es {df['Mental health management'].mean():.2f} (escala 0-5)."

            elif any(x in p for x in ['nulo', 'null', 'faltante', 'missing', 'vacio']):
                nulos = df.isnull().sum()
                cols_nulos = nulos[nulos > 0]
                respuesta = f"**Valores nulos por columna:**\n{cols_nulos.to_string()}" if len(cols_nulos) > 0 else "No hay valores nulos significativos."

            elif any(x in p for x in ['hereditari', 'hereditar', 'genetica', 'genetic']):
                her = df['Any heriditary condition?'].value_counts()
                respuesta = f"**Condiciones hereditarias:** {her.to_dict()}"

            elif any(x in p for x in ['correlac', 'relacion', 'relación']):
                corr = df.corr(numeric_only=True)['Illness count last year'].sort_values(ascending=False)
                respuesta = f"**Correlaciones con enfermedades:**\n{corr.round(3).to_string()}"

            elif any(x in p for x in ['maxi', 'maxim', 'mayor', 'highest', 'mas alto']):
                respuesta = f"Valores máximos — Edad: {df['Age'].max()}, BMI: {df['BMI'].max():.1f}, Enfermedades: {df['Illness count last year'].max():.0f}."

            elif any(x in p for x in ['mini', 'minim', 'menor', 'lowest', 'mas bajo']):
                respuesta = f"Valores mínimos — Edad: {df['Age'].min()}, BMI: {df['BMI'].min():.1f}, Enfermedades: {df['Illness count last year'].min():.0f}."

            else:
                respuesta = (
                    f"Puedo responder preguntas sobre: edad, BMI, fumadores, zona de residencia, "
                    f"actividad física, horas de sueño, alcohol, dieta, enfermedades, suplementos, "
                    f"salud mental, condiciones hereditarias y correlaciones. "
                    f"El dataset tiene {df.shape[0]:,} registros y {df.shape[1]} variables."
                )

        except Exception as e:
            respuesta = f"Error al procesar la pregunta: {e}"

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
import streamlit as st
import pandas as pd

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
.hero-title { font-size: 2.5rem; font-weight: 700; color: #ffffff; margin: 0; }
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

@st.cache_data
def load_data():
    return pd.read_csv("data/Test_Data.csv")

df = load_data()

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

if 'historial' not in st.session_state:
    st.session_state.historial = []

st.markdown('<p class="section-label">Preguntas sugeridas</p>', unsafe_allow_html=True)

ejemplos = [
    "¿Cuántas filas y columnas tiene el dataset?",
    "¿Cuál es la edad promedio?",
    "¿Cuántas personas fuman?",
    "¿Cuál es el BMI máximo y mínimo?",
    "¿Cuántas personas viven en zona urbana vs rural?",
    "¿Cuál es el promedio de enfermedades al año?",
    "¿Cuál es la correlación entre BMI y enfermedades?",
    "¿Cuántos valores nulos tiene el dataset?",
    "¿Cuál es el nivel promedio de actividad física?",
]

cols = st.columns(3)
for i, ejemplo in enumerate(ejemplos):
    with cols[i % 3]:
        if st.button(ejemplo, key=f"ej_{i}", use_container_width=True):
            st.session_state['pregunta_actual'] = ejemplo

st.divider()

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

def analizar(pregunta, df):
    p = pregunta.lower().strip()

    if any(x in p for x in ['fila','row','registro','cuantos dato','dimension','tamaño']):
        return f"El dataset contiene **{df.shape[0]:,} filas** y **{df.shape[1]} columnas**, para un total de {df.shape[0] * df.shape[1]:,} celdas de datos."

    elif any(x in p for x in ['columna','variable','campo','atributo']):
        return f"El dataset tiene **{df.shape[1]} variables**: {', '.join(df.columns.tolist())}."

    elif any(x in p for x in ['edad','age']):
        return (f"La **edad promedio** es {df['Age'].mean():.1f} años. "
                f"La persona más joven tiene {df['Age'].min()} años y la mayor {df['Age'].max()} años. "
                f"La desviación estándar es {df['Age'].std():.1f} años.")

    elif any(x in p for x in ['bmi','masa corporal','índice de masa','peso']):
        return (f"El **BMI promedio** es {df['BMI'].mean():.2f}. "
                f"Mínimo: {df['BMI'].min():.1f}, Máximo: {df['BMI'].max():.1f}. "
                f"Un BMI entre 18.5 y 24.9 es considerado normal; el promedio del dataset está en rango de sobrepeso leve.")

    elif any(x in p for x in ['fum','smok','cigarro','tabaco']):
        fum = df['Smoker?'].value_counts()
        total = len(df)
        yes = fum.get('YES', 0)
        no = fum.get('NO', 0)
        return (f"De {total:,} personas, **{yes:,} fuman** ({yes/total*100:.1f}%) "
                f"y **{no:,} no fuman** ({no/total*100:.1f}%). "
                f"La mayoría de la población analizada no tiene hábito de fumar.")

    elif any(x in p for x in ['urban','rural','zona','viv','living','residen']):
        zona = df['Living in?'].value_counts()
        total = len(df)
        urb = zona.get('URBAN', 0)
        rur = zona.get('RURAL', 0)
        return (f"**{urb:,} personas viven en zona urbana** ({urb/total*100:.1f}%) "
                f"y **{rur:,} en zona rural** ({rur/total*100:.1f}%). "
                f"La distribución es relativamente equilibrada entre ambas zonas.")

    elif any(x in p for x in ['enfermedad','illness','sick','enfermos','padecimiento']):
        col = 'Illness count last year'
        return (f"El **promedio de enfermedades al año** es {df[col].mean():.2f}. "
                f"Mínimo: {df[col].min():.0f}, Máximo: {df[col].max():.0f}. "
                f"La mitad de la población tuvo {df[col].median():.0f} enfermedad(es) o menos en el último año.")

    elif any(x in p for x in ['actividad','activity','ejercicio','físic','deport']):
        return (f"El **nivel promedio de actividad física** es {df['Physical activity'].mean():.2f} "
                f"en una escala del 0 al 5. "
                f"Esto indica un nivel moderado-bajo de actividad en la población estudiada.")

    elif any(x in p for x in ['sueño','sleep','dormir','horas']):
        return (f"El **promedio de horas de sueño** es {df['Regular sleeping hours'].mean():.2f} "
                f"en escala 0-5. "
                f"Un sueño regular es clave para la salud; este valor sugiere hábitos de sueño moderados.")

    elif any(x in p for x in ['alcohol','bebida','drink']):
        return (f"El **promedio de consumo de alcohol** es {df['Alcohol consumption'].mean():.2f} "
                f"en escala 0-5. "
                f"Un valor bajo indica que la mayoría de personas tiene un consumo moderado o nulo.")

    elif any(x in p for x in ['dieta','diet','alimenta','comida','food','nutri']):
        food = df['Food preference'].value_counts()
        top = food.index[0]
        return (f"La preferencia alimentaria más común es **{top}** con {food.iloc[0]:,} personas. "
                f"Distribución completa: {food.to_dict()}.")

    elif any(x in p for x in ['suplemento','supplement','vitamina','mineral']):
        return (f"El **promedio de consumo de suplementos** es {df['Taking supplements'].mean():.2f} "
                f"en escala 0-5. Máximo: {df['Taking supplements'].max():.0f}.")

    elif any(x in p for x in ['mental','estrés','stress','ansiedad','psicolog']):
        return (f"El **promedio de gestión de salud mental** es {df['Mental health management'].mean():.2f} "
                f"en escala 0-5. "
                f"Esto sugiere que la población tiene una gestión moderada de su salud mental.")

    elif any(x in p for x in ['nulo','null','faltante','missing','vacio','incompleto']):
        nulos = df.isnull().sum()
        cols_nulos = nulos[nulos > 0]
        if len(cols_nulos) > 0:
            return f"**Columnas con valores nulos:**\n{cols_nulos.to_string()}\n\nTotal de nulos: {nulos.sum()}."
        return "El dataset no tiene valores nulos significativos."

    elif any(x in p for x in ['hereditari','hereditar','genetica','genetic','familiar']):
        her = df['Any heriditary condition?'].value_counts()
        total = len(df)
        return f"**Condiciones hereditarias:** {her.to_dict()}. El {her.iloc[0]/total*100:.1f}% de la población pertenece al grupo '{her.index[0]}'."

    elif any(x in p for x in ['correlac','relacion','relación','asocia']):
        corr = df.corr(numeric_only=True)['Illness count last year'].sort_values(ascending=False)
        top3 = corr[1:4]
        return (f"**Correlaciones más altas con enfermedades:**\n{top3.round(3).to_string()}\n\n"
                f"Valores cercanos a 1 o -1 indican relación fuerte.")

    elif any(x in p for x in ['maxi','maxim','mayor','highest','mas alto','más alto']):
        return (f"Valores máximos del dataset — "
                f"Edad: {df['Age'].max()} años, "
                f"BMI: {df['BMI'].max():.1f}, "
                f"Enfermedades/año: {df['Illness count last year'].max():.0f}, "
                f"Actividad física: {df['Physical activity'].max():.0f}.")

    elif any(x in p for x in ['mini','minim','menor','lowest','mas bajo','más bajo']):
        return (f"Valores mínimos del dataset — "
                f"Edad: {df['Age'].min()} años, "
                f"BMI: {df['BMI'].min():.1f}, "
                f"Enfermedades/año: {df['Illness count last year'].min():.0f}.")

    elif any(x in p for x in ['social','interaccion','interacción','amigo']):
        return (f"El **promedio de interacción social** es {df['Social interaction'].mean():.2f} "
                f"en escala 0-5. Mínimo: {df['Social interaction'].min():.0f}, "
                f"Máximo: {df['Social interaction'].max():.0f}.")

    elif any(x in p for x in ['recomendacion','recomendación','consejo','sugerencia','deberia','debería']):
        return (f"Basado en los datos: edad promedio {df['Age'].mean():.1f} años, "
                f"BMI promedio {df['BMI'].mean():.2f} y nivel de actividad física {df['Physical activity'].mean():.2f}/5. "
                f"Se recomienda incrementar la actividad física, mantener una dieta balanceada "
                f"y gestionar mejor la salud mental para reducir el promedio de "
                f"{df['Illness count last year'].mean():.2f} enfermedades anuales.")

    elif any(x in p for x in ['promedio','media','mean','average','típico']):
        return (f"Promedios generales del dataset: "
                f"Edad {df['Age'].mean():.1f} años · "
                f"BMI {df['BMI'].mean():.2f} · "
                f"Actividad física {df['Physical activity'].mean():.2f}/5 · "
                f"Sueño {df['Regular sleeping hours'].mean():.2f}/5 · "
                f"Alcohol {df['Alcohol consumption'].mean():.2f}/5 · "
                f"Enfermedades/año {df['Illness count last year'].mean():.2f}.")

    else:
        return (f"Puedo responder preguntas sobre: **edad, BMI, fumadores, zona de residencia, "
                f"actividad física, horas de sueño, alcohol, dieta, enfermedades, suplementos, "
                f"salud mental, condiciones hereditarias, correlaciones y promedios generales**. "
                f"El dataset tiene {df.shape[0]:,} registros y {df.shape[1]} variables. "
                f"Intenta ser más específico en tu pregunta.")

if enviar and pregunta.strip():
    with st.spinner("Analizando datos..."):
        respuesta = analizar(pregunta, df)

    st.session_state.historial.append({
        'pregunta': pregunta,
        'respuesta': respuesta
    })
    st.session_state['pregunta_actual'] = ''
    st.rerun()

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
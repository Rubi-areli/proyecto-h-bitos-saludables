

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="EDA", page_icon="📊", layout="wide")

st.markdown("""
<style>

.section-header{
    background:#0f0f1a;
    border-left:3px solid #c9a84c;
    border-radius:10px;
    padding:1rem 1.5rem;
    margin-bottom:1.5rem;
}

.section-header h2{
    color:#ffffff;
    margin:0;
    font-size:1.4rem;
    font-weight:600;
}

.section-header p{
    color:#8899aa;
    margin-top:6px;
    font-size:0.85rem;
}

.metric-box{
    background:#0f0f1a;
    border-top:2px solid #c9a84c;
    border-radius:0 0 10px 10px;
    padding:1.2rem;
    text-align:center;
}

.metric-box .num{
    color:#ffffff;
    font-size:2rem;
    font-weight:700;
}

.metric-box .lbl{
    color:#8899aa;
    font-size:0.8rem;
    text-transform:uppercase;
    letter-spacing:1px;
}

.info-card{
    background:#0f0f1a;
    border-left:3px solid #c9a84c;
    border-radius:10px;
    padding:1rem 1.5rem;
}

.gold-divider{
    height:1px;
    background:linear-gradient(
        90deg,
        transparent,
        #c9a84c55,
        transparent
    );
    margin:2rem 0;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
background:linear-gradient(135deg,#0a0a0a 0%,#1a1a2e 50%,#16213e 100%);
padding:3rem;
border-radius:18px;
text-align:center;
margin-bottom:2rem;
border-bottom:1px solid #c9a84c44;
">

<p style="
color:#8899aa;
font-size:0.8rem;
letter-spacing:3px;
text-transform:uppercase;
margin-bottom:10px;
">

</p>

<h1 style="
color:white;
margin:0;
font-size:2.8rem;
">
 Análisis Exploratorio de Datos
</h1>

<p style="
color:#8899aa;
margin-top:12px;
font-size:0.95rem;
">
Exploración estadística y visual del dataset de hábitos saludables
</p>

</div>
""", unsafe_allow_html=True)
@st.cache_data
def load_data():
    return pd.read_csv("data/Test_Data.csv")

df = load_data()


tabs = st.tabs([
    "📋 Descripción",
    "🔍 Campos",
    "🗂️ Navegador",
    "🔎 Buscador",
    "📈 Graficador",
    "💡 Hipótesis"
])

# ── TAB 1: DESCRIPCIÓN ────────────────────────────────────────────────────────
with tabs[0]:
    c1, c2, c3, c4 = st.columns(4)
    for col, (num, lbl) in zip([c1,c2,c3,c4], [
        (f"{df.shape[0]:,}", "📋 Registros"),
        (str(df.shape[1]), "📊 Variables"),
        (str(df.isnull().sum().sum()), "❌ Nulos"),
        (f"{len(df.dropna()):,}", "✅ Completos"),
    ]):
        col.markdown(f"""
        <div class="metric-box">
            <div class="num">{num}</div>
            <div class="lbl">{lbl}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="section-header">
        <h2>📂 Sobre el Dataset</h2>
        <p>Información de hábitos de vida y condiciones de salud</p>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    Este dataset contiene información sobre hábitos de vida y salud de **6,480 personas**.
    Incluye variables como actividad física, alimentación, tabaquismo, consumo de alcohol,
    salud mental y número de enfermedades en el último año.
    """)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="section-header">
        <h2>📋 Estadísticas Generales</h2>
    </div>""", unsafe_allow_html=True)
    st.dataframe(df.describe(), use_container_width=True)

# ── TAB 2: CAMPOS ─────────────────────────────────────────────────────────────
with tabs[1]:
    st.markdown("""
    <div class="section-header">
        <h2>🔍 Descripción de Campos</h2>
        <p>Selecciona un campo para ver su descripción detallada</p>
    </div>""", unsafe_allow_html=True)

    campo = st.selectbox("Selecciona un campo:", df.columns.tolist())

    descripciones = {
        "ID1": "Identificador único del registro.",
        "ID2": "Identificador secundario del registro.",
        "Age": "Edad de la persona en años.",
        "BMI": "Índice de Masa Corporal (peso/altura²).",
        "Smoker?": "Indica si la persona fuma (YES/NO).",
        "Living in?": "Zona de residencia (URBAN/RURAL).",
        "Food preference": "Tipo de alimentación preferida.",
        "Any heriditary condition?": "Si tiene condiciones hereditarias de salud.",
        "Follow Diet": "Nivel de seguimiento de dieta (0-5).",
        "Physical activity": "Nivel de actividad física (0-5).",
        "Regular sleeping hours": "Horas regulares de sueño (0-5).",
        "Alcohol consumption": "Nivel de consumo de alcohol (0-5).",
        "Social interaction": "Nivel de interacción social (0-5).",
        "Taking supplements": "Si toma suplementos alimenticios (0-5).",
        "Mental health management": "Gestión de salud mental (0-5).",
        "Illness count last year": "Número de enfermedades en el último año.",
        "Specific ailments": "Código de padecimientos específicos.",
    }

    st.markdown(f"""
    <div style="background:#1a2744; border-left:4px solid #4a9eff;
         border-radius:8px; padding:1rem 1.5rem; margin-bottom:1rem;">
        <p style="color:#7eb8ff; font-size:1.1rem; margin:0;">
            <b>{campo}</b></p>
        <p style="color:#8899bb; margin:0.5rem 0 0 0;">
            {descripciones.get(campo, "Campo del dataset.")}</p>
    </div>
    """, unsafe_allow_html=True)

    if df[campo].dtype in ['int64', 'float64']:
        st.markdown("**📊 Medidas estadísticas (campo cuantitativo):**")
        st.dataframe(df[campo].describe().to_frame(), use_container_width=True)
    else:
        st.markdown("**📋 Valores posibles (campo categórico):**")
        vals = df[campo].value_counts().reset_index()
        vals.columns = [campo, 'Frecuencia']
        st.dataframe(vals, use_container_width=True)

# ── TAB 3: NAVEGADOR ──────────────────────────────────────────────────────────
with tabs[2]:
    st.markdown("""
    <div class="section-header">
        <h2>🗂️ Navegador del Dataset</h2>
        <p>Explora todos los registros del dataset</p>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    filas = col1.slider("Registros a mostrar:", 10, 100, 20)
    col_filtro = col2.multiselect("Columnas a mostrar:", df.columns.tolist(),
                                   default=df.columns.tolist())
    st.dataframe(df[col_filtro].head(filas), use_container_width=True)

# ── TAB 4: BUSCADOR (BONUS) ───────────────────────────────────────────────────
with tabs[3]:
    st.markdown("""
    <div class="section-header">
        <h2>🔎 Buscador de Registros</h2>
        <p>Busca un registro por su código ID</p>
    </div>""", unsafe_allow_html=True)

    codigo = st.number_input("Ingresa el ID a buscar:", min_value=1, step=1)
    if st.button("🔍 Buscar"):
        resultado = df[df['ID1'] == codigo]
        if len(resultado) > 0:
            st.success(f"✅ Registro encontrado:")
            st.dataframe(resultado, use_container_width=True)
        else:
            st.error(f"❌ No se encontró ningún registro con ID: {codigo}")

# ── TAB 5: GRAFICADOR ─────────────────────────────────────────────────────────
with tabs[4]:
    st.markdown("""
    <div class="section-header">
        <h2>📈 Graficador Exploratorio</h2>
        <p>Selecciona un campo y se mostrará el gráfico más adecuado</p>
    </div>""", unsafe_allow_html=True)

    campo_grafico = st.selectbox("Selecciona un campo para graficar:", df.columns.tolist(), key="graficador")

    fig, ax = plt.subplots(figsize=(9, 4))
    fig.patch.set_facecolor('#1a2744')
    ax.set_facecolor('#1a2744')
    ax.tick_params(colors='white')
    ax.title.set_color('white')
    for spine in ax.spines.values():
        spine.set_edgecolor("#b2bfd8")

    if df[campo_grafico].dtype in ['int64', 'float64']:
        sns.histplot(df[campo_grafico].dropna(), kde=True, ax=ax, color="#ffc64a")
        ax.set_title(f'Distribución de {campo_grafico}')
        st.markdown("*Campo cuantitativo → Histograma con curva de densidad*")
    else:
        orden = df[campo_grafico].value_counts().index
        sns.countplot(data=df, x=campo_grafico, ax=ax,
                      palette='Blues_r', order=orden)
        ax.set_title(f'Frecuencia de {campo_grafico}')
        st.markdown("*Campo categórico → Gráfico de barras de frecuencia*")

    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    st.pyplot(fig)
    plt.close()

# ── TAB 6: HIPÓTESIS ──────────────────────────────────────────────────────────
with tabs[5]:
    st.markdown("""
    <div class="section-header">
        <h2>💡 Validación de Hipótesis</h2>
        <p>Selecciona una hipótesis para ver su análisis</p>
    </div>""", unsafe_allow_html=True)

    hipotesis = st.selectbox("Selecciona una hipótesis:", [
        "H1: Zona de residencia vs enfermedades",
        "H2: Tabaquismo vs BMI",
    ])

    if hipotesis == "H1: Zona de residencia vs enfermedades":
        st.markdown("**Hipótesis:** Las personas urbanas presentan más enfermedades que las rurales.")
        st.markdown("<br>", unsafe_allow_html=True)

        agrupado = df.groupby('Living in?')['Illness count last year'].mean().reset_index()
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(agrupado, use_container_width=True)
        with col2:
            fig, ax = plt.subplots(figsize=(6, 4))
            fig.patch.set_facecolor('#1a2744')
            ax.set_facecolor('#1a2744')
            sns.barplot(data=df, x='Living in?', y='Illness count last year',
                        estimator='mean', errorbar=None, ax=ax, palette=['#4a9eff','#7eb8ff'])
            ax.set_title('Promedio enfermedades por zona', color='white')
            ax.tick_params(colors='white')
            for spine in ax.spines.values():
                spine.set_edgecolor('#3a5a9a')
            st.pyplot(fig)
            plt.close()

        st.markdown("""
        <div style="background:#1a2744; border-left:4px solid #4a9eff;
             border-radius:8px; padding:1rem 1.5rem; margin-top:1rem;">
            <p style="color:#7eb8ff; margin:0;"><b>✅ Conclusión:</b></p>
            <p style="color:#8899bb; margin:0.5rem 0 0 0;">
            Los datos muestran que la diferencia en el promedio de enfermedades entre zonas
            urbanas y rurales es mínima (~1.75 en ambos casos). La hipótesis no se confirma
            con fuerza — el entorno residencial por sí solo no parece ser un factor determinante
            en la frecuencia de enfermedades en este dataset.</p>
        </div>""", unsafe_allow_html=True)

    else:
        st.markdown("**Hipótesis:** El tabaquismo influye significativamente en el BMI.")
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(df.groupby('Smoker?')['BMI'].describe(), use_container_width=True)
        with col2:
            fig, ax = plt.subplots(figsize=(6, 4))
            fig.patch.set_facecolor('#1a2744')
            ax.set_facecolor('#1a2744')
            sns.boxplot(data=df, x='Smoker?', y='BMI', ax=ax,
                        palette=["#4aff80","#ff7ee3"])
            ax.set_title('BMI según tabaquismo', color='white')
            ax.tick_params(colors='white')
            for spine in ax.spines.values():
                spine.set_edgecolor('#3a5a9a')
            st.pyplot(fig)
            plt.close()

        st.markdown("""
        <div style="background:#1a2744; border-left:4px solid #4a9eff;
             border-radius:8px; padding:1rem 1.5rem; margin-top:1rem;">
            <p style="color:#7eb8ff; margin:0;"><b>✅ Conclusión:</b></p>
            <p style="color:#8899bb; margin:0.5rem 0 0 0;">
            El boxplot muestra distribuciones de BMI similares entre fumadores y no fumadores,
            con medianas cercanas (~23). La hipótesis no se confirma plenamente — el tabaquismo
            no parece tener un efecto significativo sobre el BMI en este dataset, aunque
            los fumadores presentan una distribución ligeramente más dispersa.</p>
        </div>""", unsafe_allow_html=True)



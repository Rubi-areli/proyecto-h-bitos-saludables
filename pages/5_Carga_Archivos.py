import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

st.set_page_config(page_title="Carga de Archivos", page_icon="📁", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }
</style>
<div style="background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
     border-radius: 20px; padding: 3rem 2rem; text-align: center;
     margin-bottom: 2rem; position: relative; overflow: hidden;">
    <div style="position:absolute; top:0; left:0; right:0; height:2px;
         background: linear-gradient(90deg, transparent, #c9a84c, transparent);"></div>
    <p style="color:#8899aa; font-size:0.75rem; letter-spacing:3px;
       text-transform:uppercase; margin-bottom:0.8rem;">
       Análisis Dinámico · Carga de Archivos</p>
    <h1 style="color:#ffffff; margin:0; font-size:2.5rem; font-weight:700;
       letter-spacing:-1px;">Explorador de <span style="color:#c9a84c;">Datos</span></h1>
    <p style="color:#8899aa; margin-top:0.8rem; font-size:0.9rem;">
        Carga cualquier archivo CSV o Excel y analiza sus datos al instante</p>
    <div style="margin-top:1.5rem;">
        <span style="background:rgba(201,168,76,0.08); color:#c9a84c;
              border:1px solid rgba(201,168,76,0.2); border-radius:3px;
              padding:3px 12px; font-size:0.72rem; margin:3px; letter-spacing:1.5px;">
              CSV</span>
        <span style="background:rgba(201,168,76,0.08); color:#c9a84c;
              border:1px solid rgba(201,168,76,0.2); border-radius:3px;
              padding:3px 12px; font-size:0.72rem; margin:3px; letter-spacing:1.5px;">
              EXCEL</span>
        <span style="background:rgba(201,168,76,0.08); color:#c9a84c;
              border:1px solid rgba(201,168,76,0.2); border-radius:3px;
              padding:3px 12px; font-size:0.72rem; margin:3px; letter-spacing:1.5px;">
              VISUALIZACIÓN AUTOMÁTICA</span>
    </div>
</div>
""", unsafe_allow_html=True)
# ── CARGA ─────────────────────────────────────────────────────────────────────
archivo = st.file_uploader("📂 Selecciona un archivo:", type=['csv', 'xlsx', 'xls'])

if archivo is None:
    st.info(" Sube un archivo CSV o Excel para comenzar el análisis.")
    st.stop()

# ── LEER ARCHIVO ──────────────────────────────────────────────────────────────
try:
    if archivo.name.endswith('.csv'):
        try:
            df = pd.read_csv(archivo, encoding='utf-8')
        except UnicodeDecodeError:
            try:
                archivo.seek(0)
                df = pd.read_csv(archivo, encoding='latin1')
            except:
                archivo.seek(0)
                df = pd.read_csv(archivo, encoding='cp1252')
    else:
        df = pd.read_excel(archivo)
    st.success(f"✅ Archivo **{archivo.name}** cargado correctamente.")
except Exception as e:
    st.error(f"❌ Error al leer el archivo: {e}")
    st.stop()

st.divider()

# ── MÉTRICAS ──────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("📋 Filas", f"{df.shape[0]:,}")
c2.metric("📊 Columnas", df.shape[1])
c3.metric("❌ Valores nulos", df.isnull().sum().sum())
c4.metric("✅ Registros completos", f"{len(df.dropna()):,}")

st.divider()

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🗂️ Vista del Dataset", "📊 Estadísticas", "📈 Gráfico"])

with tab1:
    filas = st.slider("Registros a mostrar:", 5, 50, 10)
    st.dataframe(df.head(filas), use_container_width=True)

with tab2:
    st.markdown("**Tipos de datos:**")
    tipos = pd.DataFrame({
        'Columna': df.columns,
        'Tipo': df.dtypes.values,
        'Nulos': df.isnull().sum().values,
        'Únicos': df.nunique().values
    })
    st.dataframe(tipos, use_container_width=True)

    st.markdown("**Estadísticas generales:**")
    st.dataframe(df.describe(), use_container_width=True)

with tab3:
    st.markdown("**Selecciona una columna para graficar:**")
    columna = st.selectbox("Columna:", df.columns.tolist())

    fig, ax = plt.subplots(figsize=(9, 4))
    
    fig.patch.set_facecolor('#0f0f1a')
    ax.set_facecolor('#0f0f1a')
    
    ax.tick_params(colors='white')
    for spine in ax.spines.values():

        spine.set_edgecolor('#2a2a3e')

    if df[columna].dtype in ['int64', 'float64']:
        sns.histplot(df[columna].dropna(), kde=True, ax=ax, color='#4a9eff')
        ax.set_title(f'Distribución de {columna}', color='white')
        st.markdown("*Campo numérico → Histograma*")
    else:
        orden = df[columna].value_counts().index[:15]
        sns.countplot(data=df, x=columna, ax=ax, palette='Blues_r', order=orden)
        ax.set_title(f'Frecuencia de {columna}', color='white')
        plt.xticks(rotation=45)
        st.markdown("*Campo categórico → Barras de frecuencia*")

    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    st.pyplot(fig)
    plt.close()
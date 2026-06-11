import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Recomendación", page_icon="🍳", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }
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
def load_recetas():
    data = {
        'Nombre': [
            'Ensalada César', 'Pollo a la plancha', 'Sopa de verduras',
            'Avena con frutas', 'Batido verde', 'Arroz integral con atún',
            'Tortilla de espinacas', 'Pasta integral', 'Smoothie de proteína',
            'Bowl de quinoa', 'Salmón al horno', 'Wrap de pollo',
            'Yogur con granola', 'Lentejas guisadas', 'Tacos de pescado'
        ],
        'Categoria': [
            'Almuerzo','Almuerzo','Cena','Desayuno','Desayuno',
            'Almuerzo','Desayuno','Cena','Desayuno','Almuerzo',
            'Cena','Almuerzo','Desayuno','Cena','Almuerzo'
        ],
        'Calorias': [320,450,180,290,150,380,210,420,200,350,480,390,180,310,360],
        'Proteina': [15,40,8,12,5,35,18,20,25,22,42,38,10,20,28],
        'Tiempo_min': [15,20,30,10,5,15,20,25,5,20,30,15,5,40,25],
        'Dificultad': [
            'Fácil','Fácil','Media','Fácil','Fácil',
            'Fácil','Media','Fácil','Fácil','Media',
            'Media','Fácil','Fácil','Media','Media'
        ],
        'Objetivo': [
            'Bajar peso','Ganar músculo','Bajar peso','Energía',
            'Bajar peso','Ganar músculo','Energía','Ganar músculo',
            'Ganar músculo','Energía','Ganar músculo','Bajar peso',
            'Energía','Bajar peso','Energía'
        ],
        'Ingredientes': [
            'Lechuga, pollo, queso parmesano, aderezo césar',
            'Pechuga de pollo, limón, ajo, especias',
            'Zanahoria, papa, apio, cebolla, tomate',
            'Avena, leche, plátano, fresas, miel',
            'Espinaca, manzana, pepino, jengibre, agua',
            'Arroz integral, atún en lata, maíz, limón',
            'Huevos, espinaca, cebolla, queso',
            'Pasta integral, tomate, albahaca, aceite de oliva',
            'Leche, proteína en polvo, plátano, mantequilla de maní',
            'Quinoa, aguacate, tomate, pepino, limón',
            'Salmón, limón, ajo, eneldo, aceite de oliva',
            'Tortilla, pollo, lechuga, tomate, yogur',
            'Yogur griego, granola, frutos rojos, miel',
            'Lentejas, tomate, cebolla, zanahoria, especias',
            'Tortillas, pescado blanco, col, limón, salsa'
        ],
        'Puntuacion': [88,95,82,90,78,92,85,87,91,89,96,93,83,86,88]
    }
    return pd.DataFrame(data)

df_r = load_recetas()

# ── BANNER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg,#0a0a0a 0%,#1a1a2e 50%,#16213e 100%);
     border-radius:20px; padding:3rem 2rem; text-align:center;
     margin-bottom:2.5rem; position:relative; overflow:hidden;">
    <div style="position:absolute;top:0;left:0;right:0;height:2px;
         background:linear-gradient(90deg,transparent,#c9a84c,transparent);"></div>
    <p style="color:#8899aa;font-size:0.75rem;letter-spacing:3px;
       text-transform:uppercase;margin-bottom:0.8rem;">
       Sistema de Recomendación · Nutrición Inteligente</p>
    <h1 style="color:#ffffff;margin:0;font-size:2.5rem;font-weight:700;
       letter-spacing:-1px;">Recetas <span style="color:#c9a84c;">Saludables</span></h1>
    <p style="color:#8899aa;margin-top:0.8rem;font-size:0.9rem;">
        Sistema de recomendación personalizado basado en tus objetivos y preferencias</p>
</div>
""", unsafe_allow_html=True)

# ── FILTROS ───────────────────────────────────────────────────────────────────
st.markdown('<p class="section-label">Personaliza tu búsqueda</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**Objetivo**")
    objetivo = st.radio("", ['Todos','Bajar peso','Ganar músculo','Energía'],
                        label_visibility="collapsed")
with col2:
    st.markdown("**Momento del día**")
    categoria = st.radio("", ['Todas','Desayuno','Almuerzo','Cena'],
                         label_visibility="collapsed")
with col3:
    st.markdown("**Configuración**")
    dificultad = st.select_slider("Dificultad:", options=['Fácil','Todas'], value='Todas')
    max_tiempo = st.slider("Tiempo máximo:", 5, 40, 40, format="%d min")
    max_calorias = st.slider("Calorías máximas:", 100, 500, 500, format="%d kcal")

# ── FILTRADO ──────────────────────────────────────────────────────────────────
df_f = df_r.copy()
if objetivo != 'Todos':
    df_f = df_f[df_f['Objetivo'] == objetivo]
if categoria != 'Todas':
    df_f = df_f[df_f['Categoria'] == categoria]
if dificultad != 'Todas':
    df_f = df_f[df_f['Dificultad'] == dificultad]
df_f = df_f[df_f['Tiempo_min'] <= max_tiempo]
df_f = df_f[df_f['Calorias'] <= max_calorias]
df_f = df_f.sort_values('Puntuacion', ascending=False).reset_index(drop=True)

st.divider()

# ── KPIs ──────────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("Recetas encontradas", len(df_f))
k2.metric("Calorías promedio", f"{df_f['Calorias'].mean():.0f} kcal" if len(df_f) > 0 else "—")
k3.metric("Proteína promedio", f"{df_f['Proteina'].mean():.0f}g" if len(df_f) > 0 else "—")
k4.metric("Tiempo promedio", f"{df_f['Tiempo_min'].mean():.0f} min" if len(df_f) > 0 else "—")

st.divider()

if len(df_f) == 0:
    st.warning("No se encontraron recetas con esos filtros.")
    st.stop()

# ── RECETA DESTACADA ──────────────────────────────────────────────────────────
st.markdown('<p class="section-label">Mejor recomendación</p>', unsafe_allow_html=True)
top = df_f.iloc[0]

col_top, col_radar = st.columns(2, gap="large")

with col_top:
    st.markdown(f"""
    <div style="background:#0f0f1a; border:1px solid #c9a84c44; border-radius:12px;
         padding:1.8rem; position:relative; overflow:hidden;">
        <div style="position:absolute;top:0;left:0;right:0;height:2px;
             background:linear-gradient(90deg,transparent,#c9a84c,transparent);"></div>
        <div style="position:absolute;top:1rem;right:1rem;background:rgba(201,168,76,0.15);
             color:#c9a84c;border:1px solid rgba(201,168,76,0.3);border-radius:20px;
             padding:2px 10px;font-size:0.7rem;letter-spacing:1px;">★ TOP PICK</div>
        <p style="color:#ffffff;font-size:1.3rem;font-weight:600;margin:0 0 0.3rem 0;">
            {top['Nombre']}</p>
        <p style="color:#8899aa;font-size:0.8rem;margin:0 0 1.2rem 0;">
            {top['Categoria']} &nbsp;·&nbsp; {top['Objetivo']} &nbsp;·&nbsp; {top['Dificultad']}</p>
        <p style="color:#8899aa;font-size:0.75rem;margin:0 0 0.3rem 0;">Puntuación</p>
        <p style="color:#c9a84c;font-size:0.75rem;margin:0 0 1rem 0;">{top['Puntuacion']}%</p>
        <p style="color:#c9a84c;font-size:0.72rem;letter-spacing:1px;
           border-top:1px solid #2a2a3e;padding-top:0.8rem;margin:0 0 0.3rem 0;">INGREDIENTES</p>
        <p style="color:#8899aa;font-size:0.85rem;margin:0;line-height:1.6;">
            {top['Ingredientes']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"**Calorías:** {top['Calorias']} kcal")
    st.progress(int(top['Calorias']) / 500)
    st.markdown(f"**Proteína:** {top['Proteina']}g")
    st.progress(int(top['Proteina']) / 50)
    st.markdown(f"**Tiempo:** {top['Tiempo_min']} min")
    st.progress(int(top['Tiempo_min']) / 40)

with col_radar:
    categorias = ['Calorías', 'Proteína', 'Rapidez', 'Puntuación']
    valores = [
        top['Calorias'] / 500,
        top['Proteina'] / 50,
        1 - (top['Tiempo_min'] / 40),
        top['Puntuacion'] / 100
    ]
    valores += valores[:1]
    N = len(categorias)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor('#0f0f1a')
    ax.set_facecolor('#0f0f1a')
    ax.plot(angles, valores, 'o-', linewidth=2, color='#c9a84c')
    ax.fill(angles, valores, alpha=0.15, color='#c9a84c')
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categorias, color='white', size=9)
    ax.set_ylim(0, 1)
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(['', '', '', ''], color='white')
    ax.grid(color='#2a2a3e', linewidth=0.8)
    ax.spines['polar'].set_color('#2a2a3e')
    ax.set_title(f'Perfil — {top["Nombre"]}', color='white', pad=15, fontsize=10)
    st.pyplot(fig)
    plt.close()

st.divider()

# ── TODAS LAS RECETAS ─────────────────────────────────────────────────────────
st.markdown(f'<p class="section-label">Todas las recomendaciones — {len(df_f)} resultados</p>',
            unsafe_allow_html=True)

cols = st.columns(3)
for i, (_, row) in enumerate(df_f.iterrows()):
    with cols[i % 3]:
        st.markdown(f"""
        <div style="background:#0f0f1a; border:1px solid #2a2a3e; border-radius:10px;
             padding:1.2rem; margin-bottom:1rem; position:relative;">
            <div style="position:absolute;top:0.8rem;right:0.8rem;
                 background:rgba(201,168,76,0.12);color:#c9a84c;
                 border:1px solid rgba(201,168,76,0.25);border-radius:20px;
                 padding:1px 8px;font-size:0.68rem;">{row['Puntuacion']}%</div>
            <p style="color:#ffffff;font-size:0.95rem;font-weight:600;
               margin:0 0 0.2rem 0;">{row['Nombre']}</p>
            <p style="color:#8899aa;font-size:0.75rem;margin:0 0 0.8rem 0;">
                {row['Categoria']} &nbsp;·&nbsp; {row['Dificultad']} &nbsp;·&nbsp; {row['Tiempo_min']} min</p>
            <p style="color:#c9a84c;font-size:0.78rem;margin:0 0 0.5rem 0;">
                {row['Calorias']} kcal &nbsp;·&nbsp; {row['Proteina']}g proteína</p>
            <p style="color:#8899aa;font-size:0.78rem;margin:0;
               border-top:1px solid #2a2a3e;padding-top:0.6rem;line-height:1.5;">
                {row['Ingredientes']}</p>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ── COMPARADOR ────────────────────────────────────────────────────────────────
st.markdown('<p class="section-label">Comparador nutricional</p>', unsafe_allow_html=True)

seleccion = st.multiselect("Selecciona recetas para comparar:",
                            df_r['Nombre'].tolist(),
                            default=df_r['Nombre'].tolist()[:4])

if seleccion:
    df_comp = df_r[df_r['Nombre'].isin(seleccion)].set_index('Nombre')

    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    fig.patch.set_facecolor('#0f0f1a')

    titulos = ['Calorías (kcal)', 'Proteína (g)', 'Tiempo (min)']
    campos  = ['Calorias', 'Proteina', 'Tiempo_min']
    colores = ['#c9a84c', '#ffffff', '#8899aa']

    for ax, titulo, campo, color in zip(axes, titulos, campos, colores):
        ax.set_facecolor('#0f0f1a')
        bars = ax.barh(df_comp.index, df_comp[campo], color=color, alpha=0.85)
        ax.set_title(titulo, color='white', fontsize=10, pad=8)
        ax.tick_params(colors='white', labelsize=8)
        for spine in ax.spines.values():
            spine.set_edgecolor('#2a2a3e')
        for bar, val in zip(bars, df_comp[campo]):
            ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                   str(val), va='center', color='white', fontsize=8)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
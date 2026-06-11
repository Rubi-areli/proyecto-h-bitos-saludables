import streamlit as st
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from wordcloud import WordCloud
import re

st.set_page_config(page_title="Sentimientos", page_icon="😊", layout="wide")

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
       NLP · Web Scraping · TextBlob</p>
    <h1 style="color:#ffffff; margin:0; font-size:2.5rem; font-weight:700;
       letter-spacing:-1px;">Análisis de <span style="color:#c9a84c;">Sentimientos</span></h1>
    <p style="color:#8899aa; margin-top:0.8rem; font-size:0.9rem;">
        Scraping de opiniones web y análisis de polaridad y subjetividad</p>
    <div style="margin-top:1.5rem;">
        <span style="background:rgba(201,168,76,0.08); color:#c9a84c;
              border:1px solid rgba(201,168,76,0.2); border-radius:3px;
              padding:3px 12px; font-size:0.72rem; margin:3px; letter-spacing:1.5px;">
              TEXTBLOB</span>
        <span style="background:rgba(201,168,76,0.08); color:#c9a84c;
              border:1px solid rgba(201,168,76,0.2); border-radius:3px;
              padding:3px 12px; font-size:0.72rem; margin:3px; letter-spacing:1.5px;">
              WORDCLOUD</span>
        <span style="background:rgba(201,168,76,0.08); color:#c9a84c;
              border:1px solid rgba(201,168,76,0.2); border-radius:3px;
              padding:3px 12px; font-size:0.72rem; margin:3px; letter-spacing:1.5px;">
              WEB SCRAPING</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── FUENTE ────────────────────────────────────────────────────────────────────
st.markdown("### 🌐 Fuente de opiniones")

fuente = st.selectbox("Selecciona una fuente:", [
    "Quotes to Scrape (frases célebres)",
    "Ingresar texto manualmente"
])

opiniones = []

if fuente == "Quotes to Scrape (frases célebres)":
    paginas = st.slider("Páginas a leer:", 1, 5, 2)

    if st.button("🔍 Obtener y analizar opiniones"):
        with st.spinner("Leyendo opiniones del sitio web..."):
            for p in range(1, paginas + 1):
                try:
                    url = f"http://quotes.toscrape.com/page/{p}/"
                    r = requests.get(url, timeout=10)
                    soup = BeautifulSoup(r.text, 'html.parser')
                    for q in soup.find_all('span', class_='text'):
                        texto = q.get_text().replace('\u201c','').replace('\u201d','').strip()
                        if texto:
                            opiniones.append(texto)
                except:
                    st.warning(f"No se pudo leer la página {p}")

        if opiniones:
            st.session_state['opiniones'] = opiniones
            st.success(f"✅ {len(opiniones)} opiniones obtenidas.")
        else:
            st.error("No se pudieron obtener opiniones.")

    opiniones = st.session_state.get('opiniones', [])

else:
    texto_manual = st.text_area("Escribe o pega opiniones (una por línea):",
        placeholder="This product is amazing!\nI did not like it at all.\nIt was okay, nothing special.",
        height=150)
    if st.button("🔍 Analizar"):
        opiniones = [l.strip() for l in texto_manual.split('\n') if l.strip()]
        st.session_state['opiniones'] = opiniones

    opiniones = st.session_state.get('opiniones', [])

# ── ANÁLISIS ──────────────────────────────────────────────────────────────────
if opiniones:
    st.divider()

    resultados = []
    for op in opiniones:
        blob = TextBlob(op)
        pol = blob.sentiment.polarity
        sub = blob.sentiment.subjectivity
        if pol > 0.1:
            sentimiento = "Positivo"
        elif pol < -0.1:
            sentimiento = "Negativo"
        else:
            sentimiento = "Neutral"

        resultados.append({
            'Opinión': op[:90] + ('...' if len(op) > 90 else ''),
            'Polaridad': round(pol, 3),
            'Subjetividad': round(sub, 3),
            'Sentimiento': sentimiento
        })

    df_res = pd.DataFrame(resultados)

    positivos = len(df_res[df_res['Sentimiento'] == 'Positivo'])
    negativos = len(df_res[df_res['Sentimiento'] == 'Negativo'])
    neutrales = len(df_res[df_res['Sentimiento'] == 'Neutral'])
    pol_promedio = df_res['Polaridad'].mean()
    sub_promedio = df_res['Subjetividad'].mean()

    # ── MÉTRICAS ──────────────────────────────────────────────────────────────
    st.markdown("### 📊 Resumen del análisis")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("📝 Total", len(df_res))
    c2.metric("😊 Positivas", positivos)
    c3.metric("😐 Neutrales", neutrales)
    c4.metric("😠 Negativas", negativos)
    c5.metric("📈 Polaridad media", f"{pol_promedio:.2f}")

    st.divider()

    # ── FILA 1: PIE + BARRAS ──────────────────────────────────────────────────
    st.markdown("### 📈 Visualizaciones")
    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots(figsize=(5, 5))

        fig.patch.set_facecolor('#0f0f1a')
        ax.set_facecolor('#0f0f1a')
        sizes = [positivos, neutrales, negativos]
        labels = ['Positivo', 'Neutral', 'Negativo']
        colors = ['#22c55e', '#f59e0b', '#ef4444']
        validos = [(s, l, c) for s, l, c in zip(sizes, labels, colors) if s > 0]
        if validos:
            s, l, c = zip(*validos)
            wedges, texts, autotexts = ax.pie(
                s, labels=l, colors=c, autopct='%1.1f%%',
                textprops={'color': 'white', 'fontsize': 12},
                wedgeprops={'edgecolor': '#1a2744', 'linewidth': 2}
            )
        ax.set_title('Distribución de Sentimientos', color='white', fontsize=13)
        st.pyplot(fig)
        plt.close()

    with col2:
        fig2, ax2 = plt.subplots(figsize=(6, 5))
        fig2.patch.set_facecolor('#1a2744')
        ax2.set_facecolor('#1a2744')
        colores_bar = ['#22c55e' if p > 0.1 else '#ef4444'
                       if p < -0.1 else '#f59e0b'
                       for p in df_res['Polaridad']]
        ax2.bar(range(len(df_res)), df_res['Polaridad'], color=colores_bar, alpha=0.85)
        ax2.axhline(y=0, color='white', linestyle='--', alpha=0.5, linewidth=1)
        ax2.axhline(y=pol_promedio, color='#7eb8ff', linestyle='-',
                    alpha=0.7, linewidth=1.5, label=f'Promedio: {pol_promedio:.2f}')
        ax2.set_title('Polaridad por Opinión', color='white', fontsize=13)
        ax2.set_xlabel('Opinión #', color='white')
        ax2.set_ylabel('Polaridad', color='white')
        ax2.tick_params(colors='white')
        ax2.legend(facecolor='#1a2744', labelcolor='white')
        for spine in ax2.spines.values():
            spine.set_edgecolor('#2a2a3e')
        st.pyplot(fig2)
        plt.close()

    st.divider()

    # ── FILA 2: WORDCLOUD + SUBJETIVIDAD ──────────────────────────────────────
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("**☁️ Nube de palabras:**")
        texto_todo = ' '.join(opiniones)
        texto_limpio = re.sub(r'[^\w\s]', '', texto_todo.lower())
        stopwords_extra = {'the','a','an','and','or','but','in','on','at',
                           'to','for','of','with','is','it','this','that',
                           'was','be','as','by','from','are','have','has'}
        try:
            wc = WordCloud(
                width=600, height=350,
                background_color='#1a2744',
                colormap='Blues',
                stopwords=stopwords_extra,
                max_words=60
            ).generate(texto_limpio)

            fig3, ax3 = plt.subplots(figsize=(7, 4))
            fig3.patch.set_facecolor('#1a2744')
            ax3.imshow(wc, interpolation='bilinear')
            ax3.axis('off')
            st.pyplot(fig3)
            plt.close()
        except Exception as e:
            st.warning(f"No se pudo generar la nube: {e}")

    with col4:
        st.markdown("**🎭 Polaridad vs Subjetividad:**")
        fig4, ax4 = plt.subplots(figsize=(6, 4))
        fig4.patch.set_facecolor('#1a2744')
        ax4.set_facecolor('#1a2744')
        colores_scatter = ['#22c55e' if s == 'Positivo' else
                           '#ef4444' if s == 'Negativo' else '#f59e0b'
                           for s in df_res['Sentimiento']]
        ax4.scatter(df_res['Subjetividad'], df_res['Polaridad'],
                   c=colores_scatter, alpha=0.7, s=60, edgecolors='white', linewidth=0.3)
        ax4.axhline(y=0, color='white', linestyle='--', alpha=0.4)
        ax4.axvline(x=0.5, color='white', linestyle='--', alpha=0.4)
        ax4.set_xlabel('Subjetividad', color='white')
        ax4.set_ylabel('Polaridad', color='white')
        ax4.set_title('Polaridad vs Subjetividad', color='white')
        ax4.tick_params(colors='white')
        for spine in ax4.spines.values():
            spine.set_edgecolor('#3a5a9a')
        leyenda = [
            mpatches.Patch(color='#22c55e', label='Positivo'),
            mpatches.Patch(color='#f59e0b', label='Neutral'),
            mpatches.Patch(color='#ef4444', label='Negativo')
        ]
        ax4.legend(handles=leyenda, facecolor='#1a2744', labelcolor='white')
        st.pyplot(fig4)
        plt.close()

    st.divider()

    # ── TABLA DETALLE ─────────────────────────────────────────────────────────
    st.markdown("### 📋 Detalle de opiniones")

    filtro = st.selectbox("Filtrar por sentimiento:",
                          ['Todos', 'Positivo', 'Neutral', 'Negativo'])

    df_mostrar = df_res if filtro == 'Todos' else df_res[df_res['Sentimiento'] == filtro]

    def color_sentimiento(val):
        if 'Positivo' in str(val):
            return 'color: #22c55e'
        elif 'Negativo' in str(val):
            return 'color: #ef4444'
        return 'color: #f59e0b'

    st.dataframe(
        df_mostrar.style.map(color_sentimiento, subset=['Sentimiento']),
        use_container_width=True
    )
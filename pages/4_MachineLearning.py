import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (accuracy_score, confusion_matrix,
                              classification_report, mean_squared_error, r2_score)
import numpy as np

st.set_page_config(page_title="Machine Learning", page_icon="🤖", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("data/Test_Data.csv")

df = load_data()

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
<div style="background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
     border-radius: 20px; padding: 3rem 2rem; text-align: center;
     margin-bottom: 2rem; position: relative; overflow: hidden;">
    <div style="position:absolute; top:0; left:0; right:0; height:2px;
         background: linear-gradient(90deg, transparent, #c9a84c, transparent);"></div>
    <p style="color:#8899aa; font-size:0.75rem; letter-spacing:3px;
       text-transform:uppercase; margin-bottom:0.8rem;">
       Machine Learning · Modelos Predictivos</p>
    <h1 style="color:#ffffff; margin:0; font-size:2.5rem; font-weight:700;
       letter-spacing:-1px;">Aprendizaje <span style="color:#c9a84c;">Automático</span></h1>
    <p style="color:#8899aa; margin-top:0.8rem; font-size:0.9rem;">
        Modelos interactivos para analizar patrones de salud</p>
    <div style="margin-top:1.5rem;">
        <span style="background:rgba(201,168,76,0.08); color:#c9a84c;
              border:1px solid rgba(201,168,76,0.2); border-radius:3px;
              padding:3px 12px; font-size:0.72rem; margin:3px; letter-spacing:1.5px;">
              K-MEANS</span>
        <span style="background:rgba(201,168,76,0.08); color:#c9a84c;
              border:1px solid rgba(201,168,76,0.2); border-radius:3px;
              padding:3px 12px; font-size:0.72rem; margin:3px; letter-spacing:1.5px;">
              REGRESIÓN LOGÍSTICA</span>
        <span style="background:rgba(201,168,76,0.08); color:#c9a84c;
              border:1px solid rgba(201,168,76,0.2); border-radius:3px;
              padding:3px 12px; font-size:0.72rem; margin:3px; letter-spacing:1.5px;">
              REGRESIÓN LINEAL</span>
    </div>
</div>
""", unsafe_allow_html=True)
# ── CONTROLES PRINCIPALES ─────────────────────────────────────────────────────
st.markdown("###  Configuración del Modelo")

col1, col2, col3 = st.columns(3)

algoritmo = col1.selectbox("Algoritmo:", [
    "K-Means Clustering",
    "Regresión Logística",
    "Regresión Lineal"
])

variables_numericas = ['Age', 'BMI', 'Physical activity', 'Regular sleeping hours',
                        'Alcohol consumption', 'Follow Diet', 'Taking supplements',
                        'Mental health management', 'Illness count last year']

variable_analizar = col2.selectbox(" Variable a analizar:", variables_numericas)
variable_independiente = col3.selectbox(" Variable independiente:",
    [v for v in variables_numericas if v != variable_analizar])

st.divider()

# ── K-MEANS ───────────────────────────────────────────────────────────────────
if algoritmo == "K-Means Clustering":
    st.subheader(" K-Means Clustering")

    k = st.slider("Número de clusters:", 2, 6, 3)

    df_km = df[[variable_analizar, variable_independiente]].dropna().copy()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_km)

    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    df_km['Cluster'] = kmeans.fit_predict(X_scaled)

    col_a, col_b = st.columns(2)

    with col_a:
        fig, ax = plt.subplots(figsize=(7, 4))
        fig.patch.set_facecolor('#1a2744')
        ax.set_facecolor('#1a2744')
        colores = ['#4a9eff','#a855f7','#22c55e','#f59e0b','#ef4444','#06b6d4']
        for i in range(k):
            subset = df_km[df_km['Cluster'] == i]
            ax.scatter(subset[variable_independiente], subset[variable_analizar],
                      label=f'Cluster {i}', alpha=0.6, color=colores[i], s=20)
        ax.set_xlabel(variable_independiente, color='white')
        ax.set_ylabel(variable_analizar, color='white')
        ax.set_title(f'Clusters: {variable_analizar} vs {variable_independiente}', color='white')
        ax.tick_params(colors='white')
        ax.legend(facecolor='#1a2744', labelcolor='white')
        for spine in ax.spines.values():
            spine.set_edgecolor('#3a5a9a')
        st.pyplot(fig)
        plt.close()

    with col_b:
        st.markdown("**Promedios por cluster:**")
        st.dataframe(df_km.groupby('Cluster').mean().round(2), use_container_width=True)
        st.markdown("**Tamaño de clusters:**")
        st.dataframe(df_km['Cluster'].value_counts().reset_index(), use_container_width=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Clusters", k)
    c2.metric("Registros analizados", len(df_km))
    c3.metric("Inercia del modelo", f"{kmeans.inertia_:.1f}")

    st.markdown("""
    <div style="background:#1a2744; border-left:4px solid #4a9eff;
         border-radius:8px; padding:1rem 1.5rem; margin-top:1rem;">
        <p style="color:#8899bb; margin:0;">🔍 <b style="color:#7eb8ff;">Interpretación:</b>
        K-Means agrupa personas con hábitos similares. Cada cluster representa un perfil
        de salud distinto. La inercia mide qué tan compactos son los grupos — menor inercia
        indica mejor agrupación.</p>
    </div>""", unsafe_allow_html=True)

# ── REGRESIÓN LOGÍSTICA ───────────────────────────────────────────────────────
elif algoritmo == "Regresión Logística":
    st.subheader("🎯 Regresión Logística")

    test_size = st.slider("Porcentaje de datos de prueba:", 10, 40, 20)

    df_clf = df[[variable_analizar, variable_independiente,
                 'Illness count last year']].dropna().copy()
    df_clf['target'] = (df_clf['Illness count last year'] > 1).astype(int)

    X = df_clf[[variable_analizar, variable_independiente]]
    y = df_clf['target']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size/100, random_state=42)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_train_pred = model.predict(X_train)

    acc = accuracy_score(y_test, y_pred)
    acc_train = accuracy_score(y_train, y_train_pred)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🎯 Accuracy prueba", f"{acc*100:.1f}%")
    c2.metric("📚 Accuracy entrenamiento", f"{acc_train*100:.1f}%")
    c3.metric("📊 Datos entrenamiento", len(X_train))
    c4.metric("🧪 Datos prueba", len(X_test))

    col_a, col_b = st.columns(2)

    with col_a:
        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_facecolor('#1a2744')
        ax.set_facecolor('#1a2744')
        cm = confusion_matrix(y_test, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax)
        ax.set_title('Matriz de Confusión', color='white')
        ax.set_xlabel('Predicho', color='white')
        ax.set_ylabel('Real', color='white')
        ax.tick_params(colors='white')
        st.pyplot(fig)
        plt.close()

    with col_b:
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        fig2.patch.set_facecolor('#1a2744')
        ax2.set_facecolor('#1a2744')
        idx = range(min(50, len(y_test)))
        ax2.scatter(idx, y_test.values[:50], label='Real', color='#4a9eff', alpha=0.7, s=30)
        ax2.scatter(idx, y_pred[:50], label='Predicho', color='#a855f7', alpha=0.7,
                   marker='x', s=50)
        ax2.set_title('Real vs Predicho (primeros 50)', color='white')
        ax2.tick_params(colors='white')
        ax2.legend(facecolor='#1a2744', labelcolor='white')
        for spine in ax2.spines.values():
            spine.set_edgecolor("#7b96cc")
        st.pyplot(fig2)
        plt.close()

    st.markdown("**Reporte de clasificación:**")
    report = classification_report(y_test, y_pred, output_dict=True)
    st.dataframe(pd.DataFrame(report).transpose().round(2), use_container_width=True)

    st.markdown("""
    <div style="background:#1e1030; border-left:4px solid #a855f7;
         border-radius:8px; padding:1rem 1.5rem; margin-top:1rem;">
        <p style="color:#a78bca; margin:0;">🎯 <b style="color:#c084fc;">Interpretación:</b>
        La regresión logística predice si una persona tendrá más de 1 enfermedad al año.
        El accuracy indica el porcentaje de predicciones correctas. La matriz de confusión
        muestra los aciertos y errores del modelo.</p>
    </div>""", unsafe_allow_html=True)

# ── REGRESIÓN LINEAL ──────────────────────────────────────────────────────────
else:
    st.subheader("📈 Regresión Lineal")

    test_size = st.slider("Porcentaje de datos de prueba:", 10, 40, 20)

    df_lr = df[[variable_analizar, variable_independiente]].dropna().copy()

    X = df_lr[[variable_independiente]]
    y = df_lr[variable_analizar]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size/100, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_train_pred = model.predict(X_train)

    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📐 R² Score", f"{r2:.3f}")
    c2.metric("📉 RMSE", f"{rmse:.3f}")
    c3.metric("📊 Datos entrenamiento", len(X_train))
    c4.metric("🧪 Datos prueba", len(X_test))
    
    st.markdown(f"**Coeficiente:** `{model.coef_[0]:.4f}` &nbsp;&nbsp; **Intercepto:** `{model.intercept_:.4f}`")

    fig, ax = plt.subplots(figsize=(10, 4))
    fig.patch.set_facecolor('#1a2744')
    ax.set_facecolor('#1a2744')

    ax.scatter(X_train, y_train, color='#4a9eff', alpha=0.4, s=15, label='Entrenamiento')
    ax.scatter(X_test, y_test, color='#22c55e', alpha=0.6, s=20, label='Prueba (real)')
    ax.scatter(X_test, y_pred, color='#a855f7', alpha=0.8, s=20,
               marker='x', label='Prueba (predicho)')

    x_line = np.linspace(X[variable_independiente].min(),
                         X[variable_independiente].max(), 100)
    y_line = model.coef_[0] * x_line + model.intercept_
    ax.plot(x_line, y_line, color='#f59e0b', linewidth=2, label='Línea de regresión')

    ax.set_xlabel(variable_independiente, color='white')
    ax.set_ylabel(variable_analizar, color='white')
    ax.set_title(f'Regresión Lineal: {variable_independiente} → {variable_analizar}',
                color='white')
    ax.tick_params(colors='white')
    ax.legend(facecolor='#1a2744', labelcolor='white')
    for spine in ax.spines.values():
        spine.set_edgecolor('#3a5a9a')
    st.pyplot(fig)
    plt.close()

    st.markdown("""
    <div style="background:#1a2744; border-left:4px solid #4a9eff;
         border-radius:8px; padding:1rem 1.5rem; margin-top:1rem;">
        <p style="color:#8899bb; margin:0;">📈 <b style="color:#7eb8ff;">Interpretación:</b>
        La regresión lineal muestra la relación entre dos variables numéricas.
        R² indica qué tan bien el modelo explica la variación — más cercano a 1 es mejor.
        El RMSE mide el error promedio de las predicciones.</p>
    </div>""", unsafe_allow_html=True)
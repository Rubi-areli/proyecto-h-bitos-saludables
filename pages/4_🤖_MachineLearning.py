import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

st.set_page_config(page_title="Machine Learning", page_icon="🤖", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("data/Test_Data.csv")

df = load_data()

st.title("🤖 Machine Learning")

st.divider()
col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.image("utils/image.jpg", width=250)
tab1, tab2 = st.tabs(["📦 Clustering K-Means", "🎯 Clasificación"])

# ── TAB 1: K-MEANS ────────────────────────────────────────────────────────────
with tab1:
    st.subheader("Segmentación de perfiles de salud con K-Means")
    st.markdown("Agrupa personas según sus hábitos usando variables numéricas.")

    features = ['Age', 'BMI', 'Physical activity', 'Regular sleeping hours',
                'Alcohol consumption', 'Illness count last year']

    df_km = df[features].dropna()

    k = st.slider("Número de clusters", 2, 6, 3)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_km)

    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    df_km = df_km.copy()
    df_km['Cluster'] = kmeans.fit_predict(X_scaled)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Distribución por cluster**")
        st.dataframe(df_km['Cluster'].value_counts().reset_index(), use_container_width=True)

    with col2:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.scatterplot(data=df_km, x='BMI', y='Physical activity',
                        hue='Cluster', palette='Set1', ax=ax)
        ax.set_title('Clusters: BMI vs Actividad Física')
        st.pyplot(fig)
        plt.close()

    st.markdown("**Promedios por cluster**")
    st.dataframe(df_km.groupby('Cluster').mean().round(2), use_container_width=True)

# ── TAB 2: CLASIFICACIÓN ──────────────────────────────────────────────────────
with tab2:
    st.subheader("Predicción: ¿Más de 1 enfermedad al año?")
    st.markdown("Modelo de Regresión Logística para predecir riesgo de enfermedades.")

    features_clf = ['Age', 'BMI', 'Physical activity', 'Regular sleeping hours',
                    'Alcohol consumption', 'Follow Diet', 'Taking supplements']

    df_clf = df[features_clf + ['Illness count last year']].dropna()
    df_clf = df_clf.copy()
    df_clf['target'] = (df_clf['Illness count last year'] > 1).astype(int)

    X = df_clf[features_clf]
    y = df_clf['target']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("**Reporte de clasificación**")
        report = classification_report(y_test, y_pred, output_dict=True)
        st.dataframe(pd.DataFrame(report).transpose().round(2), use_container_width=True)

    with col4:
        fig2, ax2 = plt.subplots(figsize=(5, 4))
        sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d',
                    cmap='Blues', ax=ax2)
        ax2.set_title('Matriz de Confusión')
        ax2.set_xlabel('Predicho')
        ax2.set_ylabel('Real')
        st.pyplot(fig2)
        plt.close()

    st.divider()
    st.subheader("🔮 Hacer una predicción")
    st.markdown("Ingresa los datos de una persona para predecir su riesgo:")

    c1, c2, c3 = st.columns(3)
    age = c1.number_input("Edad", 10, 90, 30)
    bmi = c2.number_input("BMI", 10.0, 50.0, 22.0)
    activity = c3.number_input("Actividad física (0-5)", 0.0, 5.0, 3.0)

    c4, c5, c6 = st.columns(3)
    sleep = c4.number_input("Horas de sueño (0-5)", 0.0, 5.0, 3.0)
    alcohol = c5.number_input("Alcohol (0-5)", 0.0, 5.0, 1.0)
    diet = c6.number_input("Sigue dieta (0-5)", 0.0, 5.0, 2.0)
    supp = st.number_input("Suplementos (0-5)", 0.0, 5.0, 1.0)

    if st.button("Predecir"):
        entrada = pd.DataFrame([[age, bmi, activity, sleep, alcohol, diet, supp]],
                               columns=features_clf)
        resultado = model.predict(entrada)[0]
        proba = model.predict_proba(entrada)[0][1]

        if resultado == 1:
            st.error(f"⚠️ Alto riesgo de más de 1 enfermedad al año ({proba*100:.1f}% probabilidad)")
        else:
            st.success(f"✅ Bajo riesgo de enfermedades ({proba*100:.1f}% probabilidad)")
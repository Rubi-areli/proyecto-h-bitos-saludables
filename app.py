import streamlit as st

pg = st.navigation(
    {
        "Portafolio": [
            st.Page("pages/1_ 🏠page.py", title="Inicio"),
        ],
        "Tarea 1": [
            st.Page("pages/2_📊_EDA.py", title="EDA"),
            st.Page("pages/4_🤖_MachineLearning.py", title="Machine Learning"),
            st.Page("pages/7_🍳_Recomendacion.py", title="Recomendación"),
        ],
        "Tarea 2": [
            st.Page("pages/5_📂_Carga_Archivos.py", title="Carga de Archivos"),
            st.Page("pages/6_😊_Sentimientos.py", title="Sentimientos"),
        ],
        "Opcional": [
            st.Page("pages/8_🤖_IA.py", title="Asistente IA"),
        ],
    }
)

pg.run()
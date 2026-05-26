import streamlit as st

pg = st.navigation(
    {
        "🌿 Proyecto": [
            st.Page("pages/1_ 🏠page.py", title="Inicio", icon="🏠"),
        

            st.Page("pages/2_📊_EDA.py", title="EDA", icon="📊"),
            st.Page("pages/3_💡_Hipotesis.py", title="Hipótesis", icon="💡"),
            st.Page("pages/4_🤖_MachineLearning.py", title="Machine Learning", icon="🤖"),
        ],
    }
)

pg.run()

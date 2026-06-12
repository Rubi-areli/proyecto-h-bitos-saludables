import streamlit as st

pg = st.navigation(
    {
        "🌿 Proyecto": [
            st.Page("pages/1_page.py", title="Inicio"),

            st.Page("pages/2_EDA.py", title="EDA"),

           

            st.Page("pages/4_MachineLearning.py", title="Machine Learning"),

            st.Page("pages/5_Carga_Archivos.py",
                    title="Carga de Archivos"),

            st.Page("pages/6_Sentimientos.py",
                    title="Sentimientos"),

                  st.Page("pages/7_Recomendacion.py",
                          title="Recomendacion"), 
                st.Page("pages/8_IA.py",
                         title="IA"),
            
        ],
    }
)

pg.run()
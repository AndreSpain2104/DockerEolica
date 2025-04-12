import streamlit as st
import pandas as pd

# Configuración general
st.set_page_config(
    page_title="Energía Eólica en Colombia", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5em;
        color: #2c3e50;
        text-align: center;
    }
    .sub-header {
        font-size: 1.8em;
        color: #3498db;
    }
    .card {
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        background-color: #f8f9fa;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Carga de datos (puedes moverlo a un archivo separado si deseas)
@st.cache_data
def load_data():
    try:
        return pd.read_csv("energia_eolica.csv")
    except:
        return pd.DataFrame()

df = load_data()

st.markdown('<h1 class="main-header"> Energía Eólica en Colombia</h1>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])
with col1:
    st.image("https://img.freepik.com/vector-gratis/ilustracion-concepto-turbina-eolica_114360-2800.jpg", use_column_width=True)
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("""
    ### Bienvenido
    
    Esta aplicación interactiva presenta un análisis exploratorio de datos sobre proyectos 
    y potencial de energía eólica en Colombia.

    Navega por las secciones en la barra lateral:
    - Mapa Interactivo
    - Dashboard (análisis)
    """)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.dataframe(df.head())
    
import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster, HeatMap
from streamlit_folium import st_folium

st.markdown('<h1 class="main-header"> Mapa Interactivo de Energía Eólica</h1>', unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("energia_eolica.csv")

df = load_data()

# Filtrado por categoría
if not df.empty and "Categoría" in df.columns:
    categorias = sorted(df["Categoría"].unique())
    categoria_seleccionada = st.selectbox("Selecciona la categoría", categorias)
    df = df[df["Categoría"] == categoria_seleccionada]

    map_type = st.radio("Tipo de visualización", ["Marcadores", "Mapa de calor", "Clusters"], horizontal=True)

    m = folium.Map(location=[4.6, -74.1], zoom_start=5, tiles="CartoDB positron")

    if map_type == "Marcadores":
        for _, row in df.iterrows():
            folium.CircleMarker(
                location=[row["Latitud"], row["Longitud"]],
                radius=min(max(row["Valor"]/5, 5), 15),
                popup=row["Departamento"],
                color="#3498db", fill=True
            ).add_to(m)
    elif map_type == "Mapa de calor":
        HeatMap([[row["Latitud"], row["Longitud"], row["Valor"]] for _, row in df.iterrows()], radius=15).add_to(m)
    else:
        cluster = MarkerCluster().add_to(m)
        for _, row in df.iterrows():
            folium.Marker(
                location=[row["Latitud"], row["Longitud"]],
                popup=row["Departamento"]
            ).add_to(cluster)

    st_folium(m, width=1000, height=600)

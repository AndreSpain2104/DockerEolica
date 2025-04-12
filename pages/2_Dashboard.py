import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    return pd.read_csv("energia_eolica.csv")

df = load_data()

st.markdown('<h1 class="main-header"> Análisis de Datos de Energía Eólica</h1>', unsafe_allow_html=True)

# Filtrar datos
categorias = sorted(df["Categoría"].unique())
departamentos = sorted(df["Departamento"].unique())

cat_selected = st.multiselect("Categorías", categorias, default=categorias[:2])
dept_selected = st.multiselect("Departamentos", departamentos, default=departamentos[:3])

filtered = df[df["Categoría"].isin(cat_selected) & df["Departamento"].isin(dept_selected)]

st.markdown("### Distribución por Categoría")
fig = px.box(filtered, x="Categoría", y="Valor", color="Categoría", template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

st.markdown("### Promedio por Departamento")
avg = filtered.groupby("Departamento")["Valor"].mean().reset_index()
fig2 = px.bar(avg, x="Departamento", y="Valor", color="Valor", color_continuous_scale="viridis")
st.plotly_chart(fig2, use_container_width=True)

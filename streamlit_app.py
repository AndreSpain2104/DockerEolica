import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
from folium.plugins import MarkerCluster, HeatMap

# --- Configuración de la página ---
st.set_page_config(
    page_title="Energía Eólica en Colombia", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Aplicar estilos CSS personalizados ---
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5em;
        color: #2c3e50;
        text-align: center;
        text-decoration: none !important;
        cursor: default;
    }
    .sub-header {
        font-size: 1.8em;
        color: #3498db;
        text-decoration: none !important;
        cursor: default;
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


# --- Función para cargar datos ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("energia_eolica.csv")
        return df
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        # Datos de ejemplo en caso de error
        return pd.DataFrame({
            "Departamento": ["La Guajira", "Atlántico", "Bolívar"],
            "Categoría": ["Velocidad del viento", "Potencial eólico", "Proyectos instalados"],
            "Valor": [7.5, 150, 5],
            "Latitud": [11.5, 10.9, 10.4],
            "Longitud": [-72.9, -74.8, -75.5]
        })

# --- Cargar datos ---
df = load_data()

# --- Sidebar con navegación y filtros ---
st.sidebar.markdown("## **Energía Eólica Colombia**")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navegación", 
    ["Inicio", "Análisis Descriptivo", "Mapa Interactivo", "Acerca de"]
)

# Si tenemos categorías y departamentos en los datos, crear filtros globales
if not df.empty:
    st.sidebar.markdown("---")
    st.sidebar.markdown("## Filtros Globales")
    
    # Filtros que solo aparecen en ciertas páginas
    if menu in ["Análisis Descriptivo", "Mapa Interactivo"]:
        all_categories = sorted(df["Categoría"].unique())
        selected_categories = st.sidebar.multiselect(
            "Categorías",
            options=all_categories,
            default=all_categories[:3] if len(all_categories) > 3 else all_categories
        )
        
        all_departments = sorted(df["Departamento"].unique())
        selected_departments = st.sidebar.multiselect(
            "Departamentos",
            options=all_departments,
            default=all_departments[:5] if len(all_departments) > 5 else all_departments
        )
        
        # Aplicar filtros
        if selected_categories and selected_departments:
            filtered_df = df[
                (df["Categoría"].isin(selected_categories)) & 
                (df["Departamento"].isin(selected_departments))
            ]
        elif selected_categories:
            filtered_df = df[df["Categoría"].isin(selected_categories)]
        elif selected_departments:
            filtered_df = df[df["Departamento"].isin(selected_departments)]
        else:
            filtered_df = df.copy()
    else:
        filtered_df = df.copy()

# --- Función para crear tarjetas con estadísticas clave ---
def create_metric_cards(dataframe):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric(
            label="Total de Registros", 
            value=f"{len(dataframe):,}"
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric(
            label="Departamentos", 
            value=f"{dataframe['Departamento'].nunique()}"
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric(
            label="Categorías", 
            value=f"{dataframe['Categoría'].nunique()}"
        )
        st.markdown("</div>", unsafe_allow_html=True)

# --- INICIO ---
if menu == "Inicio":
    st.markdown('<h1 class="main-header"> Energía Eólica en Colombia</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.image("https://img.freepik.com/vector-gratis/ilustracion-concepto-turbina-eolica_114360-2800.jpg", use_column_width=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st. markdown("""
        ### Bienvenido
        
        Esta aplicación interactiva presenta un análisis exploratorio de datos sobre proyectos 
        y potencial de energía eólica en Colombia.
        
        La energía eólica representa una alternativa sostenible y limpia para diversificar 
        la matriz energética del país.
        
        ### Navega por las secciones:
        - **Análisis Descriptivo**: Estadísticas y gráficos
        - **Mapa Interactivo**: Visualización geográfica
        """)
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Mostrar tarjetas con métricas clave
    create_metric_cards(df)
    
    # Gráfico de resumen en la página de inicio
    st.markdown('<h2 class="sub-header">Panorama General</h2>', unsafe_allow_html=True)
    
    if not df.empty and "Categoría" in df.columns and "Valor" in df.columns:
        summary_data = df.groupby("Categoría")["Valor"].mean().reset_index()
        fig = px.bar(
            summary_data,
            x="Categoría",
            y="Valor",
            color="Categoría",
            title="Valor Promedio por Categoría",
            template="plotly_white"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

# --- ANÁLISIS DESCRIPTIVO ---
elif menu == "Análisis Descriptivo":
    st.markdown('<h1 class="main-header"> Análisis de Datos de Energía Eólica</h1>', unsafe_allow_html=True)
    
    # Mostrar tarjetas con métricas clave
    create_metric_cards(filtered_df)
    
    # Tabla de datos con opciones de filtro
    with st.expander("🔍 Ver datos filtrados", expanded=False):
        st.dataframe(filtered_df, use_container_width=True)
    
    # Dividir la pantalla para mostrar gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h3 class="sub-header">Distribución por Categoría</h3>', unsafe_allow_html=True)
        if not filtered_df.empty and "Categoría" in filtered_df.columns and "Valor" in filtered_df.columns:
            fig1 = px.box(
                filtered_df, 
                x="Categoría", 
                y="Valor", 
                color="Categoría",
                points="all",
                notched=True,
                template="plotly_white"
            )
            fig1.update_layout(height=400)
            st.plotly_chart(fig1, use_container_width=True)
            
    with col2:
        st.markdown('<h3 class="sub-header">Promedio por Departamento</h3>', unsafe_allow_html=True)
        if not filtered_df.empty and "Departamento" in filtered_df.columns and "Valor" in filtered_df.columns:
            avg_depto = filtered_df.groupby("Departamento")["Valor"].mean().sort_values(ascending=False).reset_index()
            fig2 = px.bar(
                avg_depto, 
                x="Departamento", 
                y="Valor", 
                color="Valor",
                color_continuous_scale="viridis",
                template="plotly_white"
            )
            fig2.update_layout(height=400)
            st.plotly_chart(fig2, use_container_width=True)
    
    # Estadísticas detalladas
    st.markdown('<h3 class="sub-header">Estadísticas Detalladas</h3>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Estadísticas por Categoría", "Comparativa", "Correlaciones"])
    
    with tab1:
        if not filtered_df.empty and "Categoría" in filtered_df.columns and "Valor" in filtered_df.columns:
            stats_cat = filtered_df.groupby("Categoría")["Valor"].describe().round(2)
            st.dataframe(stats_cat, use_container_width=True)
    
    with tab2:
        if not filtered_df.empty and "Categoría" in filtered_df.columns and "Departamento" in filtered_df.columns and "Valor" in filtered_df.columns:
            pivot_data = filtered_df.pivot_table(
                index="Departamento", 
                columns="Categoría", 
                values="Valor", 
                aggfunc="mean"
            ).fillna(0)
            
            st.markdown("#### Matriz comparativa de valores promedio por departamento y categoría")
            st.dataframe(pivot_data, use_container_width=True)
            
            # Heatmap de la matriz
            fig3 = px.imshow(
                pivot_data,
                color_continuous_scale="viridis",
                title="Heatmap: Valores por Departamento y Categoría",
                template="plotly_white"
            )
            st.plotly_chart(fig3, use_container_width=True)
    
    with tab3:
        st.markdown("#### Comparativa entre categorías")
        if not filtered_df.empty and "Categoría" in filtered_df.columns:
            categories = filtered_df["Categoría"].unique()
            if len(categories) >= 2:
                cat1 = st.selectbox("Categoría 1", options=categories, index=0)
                cat2 = st.selectbox("Categoría 2", options=categories, index=min(1, len(categories)-1))
                
                df_cat1 = filtered_df[filtered_df["Categoría"] == cat1]
                df_cat2 = filtered_df[filtered_df["Categoría"] == cat2]
                
                # Crear un dataframe combinado para la correlación
                df_merged = pd.merge(
                    df_cat1[["Departamento", "Valor"]].rename(columns={"Valor": cat1}),
                    df_cat2[["Departamento", "Valor"]].rename(columns={"Valor": cat2}),
                    on="Departamento"
                )
                
                if not df_merged.empty:
                    fig4 = px.scatter(
                        df_merged,
                        x=cat1,
                        y=cat2,
                        hover_name="Departamento",
                        trendline="ols",
                        title=f"Correlación entre {cat1} y {cat2}",
                        template="plotly_white"
                    )
                    st.plotly_chart(fig4, use_container_width=True)
                    
                    # Calcular correlación
                    corr = df_merged[cat1].corr(df_merged[cat2])
                    st.info(f"Coeficiente de correlación: {corr:.4f}")
            else:
                st.info("Se necesitan al menos dos categorías diferentes para mostrar correlaciones.")

# --- MAPA INTERACTIVO ---
elif menu == "Mapa Interactivo":
    st.markdown('<h1 class="main-header"> Mapa Interactivo de Energía Eólica</h1>', unsafe_allow_html=True)
    
    # Opciones de visualización del mapa
    map_options = st.radio(
        "Tipo de visualización", 
        ["Marcadores", "Mapa de calor", "Clusters"], 
        horizontal=True
    )
    
    # Selector de categoría específico para el mapa
    if "Categoría" in df.columns:
        map_category = st.selectbox(
            "Selecciona una categoría para visualizar en el mapa", 
            options=sorted(filtered_df["Categoría"].unique())
        )
        map_df = filtered_df[filtered_df["Categoría"] == map_category]
    else:
        map_df = filtered_df.copy()
    
    # Crear mapa base
    m = folium.Map(
        location=[4.6, -74.1], 
        zoom_start=5, 
        tiles="CartoDB positron"
    )
    
    # Añadir la capa de visualización según la opción seleccionada
    if map_options == "Marcadores":
        for _, row in map_df.iterrows():
            folium.CircleMarker(
                location=[row["Latitud"], row["Longitud"]],
                radius=min(max(row["Valor"]/5, 5), 15),  # Escalar el tamaño según el valor
                color="#3498db",
                fill=True,
                fill_color="#3498db",
                fill_opacity=0.7,
                popup=f"""
                <b>{row['Departamento']}</b><br>
                Categoría: {row.get('Categoría', 'N/A')}<br>
                Valor: {row['Valor']:.2f}
                """
            ).add_to(m)
    
    elif map_options == "Mapa de calor":
        heat_data = [[row["Latitud"], row["Longitud"], row["Valor"]] for _, row in map_df.iterrows()]
        HeatMap(heat_data, radius=15).add_to(m)
    
    else:  # Clusters
        marker_cluster = MarkerCluster().add_to(m)
        for _, row in map_df.iterrows():
            folium.Marker(
                location=[row["Latitud"], row["Longitud"]],
                popup=f"""
                <b>{row['Departamento']}</b><br>
                Categoría: {row.get('Categoría', 'N/A')}<br>
                Valor: {row['Valor']:.2f}
                """
            ).add_to(marker_cluster)
    
    # Mostrar el mapa
    st_folium(m, width=1000, height=600)
    
    # Tabla de datos del mapa
    with st.expander(" Ver datos del mapa", expanded=False):
        st.dataframe(map_df, use_container_width=True)

# --- ACERCA DE ---
elif menu == "Acerca de":
    st.markdown('<h1 class="main-header">ℹ Acerca de esta Aplicación</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    ### Información del Proyecto
    
    Esta aplicación fue desarrollada como herramienta de visualización para analizar datos sobre el potencial y desarrollo
    de la energía eólica en Colombia. 
    
    ### Fuente de Datos
    
    Los datos utilizados en esta aplicación provienen del repositorio:
    [GitHub - Datos_DATAVIZ](https://github.com/Kalbam/Datos_DATAVIZ)
    
    ### Tecnologías Utilizadas
    
    - **Streamlit**: Framework para desarrollo de aplicaciones web de datos
    - **Pandas**: Manipulación y análisis de datos
    - **Folium**: Visualización de mapas interactivos
    - **Plotly**: Gráficos interactivos""")
    
    
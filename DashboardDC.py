import streamlit as st
import pandas as pd
import plotly.express as px
 
st.set_page_config(layout="wide") # Opcional: para usar todo el ancho de la página
 
st.title('Dashboard de Personajes de Cómics DC')
 
# --- Cargar Datos ---
# Asegúrate de que el archivo 'dc-wikia-data.csv' esté en la misma carpeta que tu app.py
# O especifica la ruta completa: pd.read_csv('/ruta/completa/dc-wikia-data.csv')
try:
    comics_df = pd.read_csv('datos/dc-wikia-data.csv')
except FileNotFoundError:
    st.error("Error: El archivo 'dc-wikia-data.csv' no se encontró. Asegúrate de que la ruta sea correcta.")
    st.stop()
 
# --- 1. Distribución de la Alineación de Personajes (ALIGN) ---
st.header('1. Distribución de la Alineación de Personajes')
align_counts = comics_df['ALIGN'].value_counts().reset_index()
align_counts.columns = ['Alignment', 'Count']
 
fig_align_bar = px.bar(
    align_counts,
    x='Alignment',
    y='Count',
    title='Distribución de la Alineación de Personajes',
    labels={'Alignment': 'Alineación', 'Count': 'Número de Personajes'}
)
st.plotly_chart(fig_align_bar, use_container_width=True)
 
fig_align_pie = px.pie(
    align_counts,
    values='Count',
    names='Alignment',
    title='Proporción de la Alineación de Personajes',
    hole=0.3 # Para un gráfico de donut
)
fig_align_pie.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig_align_pie, use_container_width=True)
 
# --- 2. Distribución de Género (SEX) ---
st.header('2. Distribución de Género')
sex_counts = comics_df['SEX'].value_counts().reset_index()
sex_counts.columns = ['Gender', 'Count']
 
fig_sex_bar = px.bar(
    sex_counts,
    x='Gender',
    y='Count',
    title='Distribución de Género de Personajes',
    labels={'Gender': 'Género', 'Count': 'Número de Personajes'}
)
st.plotly_chart(fig_sex_bar, use_container_width=True)
 
fig_sex_pie = px.pie(
    sex_counts,
    values='Count',
    names='Gender',
    title='Proporción de Género de Personajes',
    hole=0.3
)
fig_sex_pie.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig_sex_pie, use_container_width=True)
 
# --- 3. Personajes por Año de Primera Aparición (YEAR) ---
st.header('3. Personajes por Año de Primera Aparición')
 
# Eliminar NaN para el conteo de años
year_data = comics_df['YEAR'].dropna()
 
fig_year_hist = px.histogram(
    year_data,
    nbins=len(year_data.unique()), # Un bin por cada año único
    title='Frecuencia de Personajes por Año de Primera Aparición',
    labels={'value': 'Año de Primera Aparición', 'count': 'Número de Personajes'}
)
fig_year_hist.update_xaxes(dtick=10) # Mostrar etiquetas cada 10 años para legibilidad
st.plotly_chart(fig_year_hist, use_container_width=True)
 
# También se puede mostrar como línea para ver la tendencia
year_counts = year_data.value_counts().sort_index().reset_index()
year_counts.columns = ['Year', 'Count']
 
fig_year_line = px.line(
    year_counts,
    x='Year',
    y='Count',
    title='Tendencia de Personajes por Año de Primera Aparición',
    labels={'Year': 'Año de Primera Aparición', 'Count': 'Número de Personajes'}
)
st.plotly_chart(fig_year_line, use_container_width=True)
 
# --- 4. Distribución del Número de Apariciones (APPEARANCES) ---
st.header('4. Distribución del Número de Apariciones')
 
# Eliminar NaN para el conteo de apariciones
appearances_data = comics_df['APPEARANCES'].dropna()
 
fig_appearances_hist = px.histogram(
    appearances_data,
    nbins=50, # Número de bins ajustable
    title='Distribución del Número de Apariciones de Personajes',
    labels={'value': 'Número de Apariciones', 'count': 'Número de Personajes'},
    log_y=True # Usar escala logarítmica para ver mejor la distribución con muchos valores bajos
)
st.plotly_chart(fig_appearances_hist, use_container_width=True)

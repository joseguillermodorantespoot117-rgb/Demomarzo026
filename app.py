import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configurar la página de Streamlit
st.set_page_config(layout="wide")
st.title('Mi Aplicación Streamlit con DataFrame y Gráfico de Líneas')

# Generar datos de ejemplo
data = {
    'Fecha': pd.to_datetime(pd.date_range(start='2023-01-01', periods=100, freq='D')),
    'Valor_A': np.random.rand(100).cumsum() * 100,
    'Valor_B': np.random.rand(100).cumsum() * 50 + 200,
    'Categoría': np.random.choice(['X', 'Y', 'Z'], 100, p=[0.4, 0.3, 0.3])
}
df = pd.DataFrame(data)

# Mostrar el DataFrame
st.subheader('Datos Aleatorios de Ejemplo')
st.dataframe(df)

# Crear un gráfico de líneas
st.subheader('Tendencia de Valores a lo largo del tiempo')

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df['Fecha'], df['Valor_A'], label='Valor A', color='skyblue', marker='o', markersize=3, linestyle='-')
ax.plot(df['Fecha'], df['Valor_B'], label='Valor B', color='salmon', marker='x', markersize=3, linestyle='--')
ax.set_title('Gráfico de Líneas de Valor A y Valor B')
ax.set_xlabel('Fecha')
ax.set_ylabel('Valores')
ax.legend()
ax.grid(True, linestyle=':', alpha=0.7)
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

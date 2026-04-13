import pandas as pd
import numpy as np

# Crear un DataFrame de ejemplo
data = {
    'Fecha': pd.to_datetime(pd.date_range(start='2023-01-01', periods=100)),
    'Valor': np.random.rand(100).cumsum() + 10,
    'Categoría': np.random.choice(['A', 'B', 'C'], 100)
}
df = pd.DataFrame(data)

# Guardar el código de Streamlit en un archivo 'app.py'
streamlit_code = '''
import streamlit as st
import pandas as pd
import plotly.express as px

# Título de la aplicación
st.title('Mi Aplicación de Streamlit con DataFrame y Gráfico de Línea')

# Mostrar el DataFrame
st.header('DataFrame de Ejemplo')
st.dataframe(df)

# Crear un gráfico de línea
st.header('Gráfico de Línea')
fig = px.line(df, x='Fecha', y='Valor', title='Tendencia de Valores a lo Largo del Tiempo')
st.plotly_chart(fig)

'''

with open('app.py', 'w') as f:
    f.write(streamlit_code.replace('df', 'pd.DataFrame(' + str(data) + ')')) # Pass data directly

print("Archivo 'app.py' creado con éxito.")

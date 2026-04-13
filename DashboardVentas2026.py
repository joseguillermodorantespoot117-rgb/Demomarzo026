import streamlit as st
import pandas as pd
import plotly.express as px

# To make sure Streamlit is installed, uncomment the line below and run it once
# !pip install streamlit pandas plotly

# This writes the content of this cell to a file named dashboard_ventas.py
# %%writefile dashboard_ventas.py

# --- Streamlit App --- (This part would go into dashboard_ventas.py)
st.set_page_config(layout='wide')
st.title('Sales Dashboard for USA Branches')

# Load Data (Assuming the file is in the same path as before)
@st.cache_data
def load_data():
    file_path = 'datos/SalidaVentas.xlsx'
    df = pd.read_excel(file_path)
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    return df

df = load_data()

st.header('Overview of Sales Data')
st.write(f"Total Sales Records: {len(df):,}")
st.write(df.head())

# 1. Sales over time
st.subheader('Sales Over Time')
fig_sales_time = px.line(df.sort_values('Order Date'), x='Order Date', y='Sales', title='Sales Over Time', height=400)
st.plotly_chart(fig_sales_time, use_container_width=True)

# 2. Sales by Region
st.subheader('Total Sales by Region')
sales_by_region = df.groupby('Region')['Sales'].sum().reset_index()
fig_sales_region = px.bar(sales_by_region, x='Region', y='Sales', title='Total Sales by Region', height=400)
st.plotly_chart(fig_sales_region, use_container_width=True)


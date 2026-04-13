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

# --- Instructions to run the Streamlit app in Colab --- (This part remains in the notebook cell)
# You need to install localtunnel to expose the Streamlit app publicly
# !npm install -g localtunnel

# Save the app content to a .py file
# This creates a file named dashboard_ventas.py in your Colab environment

# You can manually copy the Streamlit app code above into a file named 'dashboard_ventas.py'
# in your Colab environment's file explorer, or use the following commented-out code:
# with open('dashboard_ventas.py', 'w') as f:
#     f.write("""import streamlit as st\nimport pandas as pd\nimport plotly.express as px\n\nst.set_page_config(layout='wide')\nst.title('Sales Dashboard for USA Branches')\n\n@st.cache_data\ndef load_data():\n    file_path = '/content/drive/MyDrive/Practica 7/SalidaVentas.xlsx'\n    df = pd.read_excel(file_path)\n    df['Order Date'] = pd.to_datetime(df['Order Date'])\n    return df\n\ndf = load_data()\n\nst.header('Overview of Sales Data')\nst.write(f\"Total Sales Records: {len(df):,}\")\nst.write(df.head())\n\nst.subheader('Sales Over Time')\nfig_sales_time = px.line(df.sort_values('Order Date'), x='Order Date', y='Sales', title='Sales Over Time', height=400)\nst.plotly_chart(fig_sales_time, use_container_width=True)\n\nst.subheader('Total Sales by Region')\nsales_by_region = df.groupby('Region')['Sales'].sum().reset_index()\nfig_sales_region = px.bar(sales_by_region, x='Region', y='Sales', title='Total Sales by Region', height=400)\nst.plotly_chart(fig_sales_region, use_container_width=True)\n""")

# To run the Streamlit app, execute the following commands in separate cells or together after writing the file:
# !streamlit run dashboard_ventas.py & npx localtunnel --port 8501
# You might need to install localtunnel first: !npm install -g localtunnel

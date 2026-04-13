import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout='wide')
st.title('Sales Dashboard for USA Branches')

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

st.subheader('Sales Over Time')
fig_sales_time = px.line(df.sort_values('Order Date'), x='Order Date', y='Sales', title='Sales Over Time', height=400)
st.plotly_chart(fig_sales_time, use_container_width=True)

st.subheader('Total Sales by Region')
sales_by_region = df.groupby('Region')['Sales'].sum().reset_index()
fig_sales_region = px.bar(sales_by_region, x='Region', y='Sales', title='Total Sales by Region', height=400)
st.plotly_chart(fig_sales_region, use_container_width=True)

st.subheader('Total Sales by Category')
sales_by_category = df.groupby('Category')['Sales'].sum().reset_index()
fig_sales_category = px.pie(sales_by_category, values='Sales', names='Category', title='Total Sales by Category')
st.plotly_chart(fig_sales_category, use_container_width=True)

st.subheader('Top 10 Sales by Sub-Category')
sales_by_subcategory = df.groupby('Sub-Category')['Sales'].sum().nlargest(10).reset_index()
fig_sales_subcategory = px.bar(sales_by_subcategory, x='Sub-Category', y='Sales', title='Top 10 Sales by Sub-Category', height=400)
st.plotly_chart(fig_sales_subcategory, use_container_width=True)

st.subheader('Sales by State in USA')
sales_by_state = df.groupby('State')['Sales'].sum().reset_index()
fig_sales_state_map = px.choropleth(sales_by_state,
                                   locations='State',
                                   locationmode='USA-states',
                                   color='Sales',
                                   scope='usa',
                                   color_continuous_scale="Viridis",
                                   title='Total Sales by State',
                                   hover_name='State',
                                   height=600)
st.plotly_chart(fig_sales_state_map, use_container_width=True)

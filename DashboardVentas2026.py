import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np # Necesario para la transformación logarítmica

st.set_page_config(layout='wide')
st.title('Sales Dashboard for USA Branches')

@st.cache_data
def load_data():
    file_path = 'datos/SalidaVentas.xlsx'
    df = pd.read_excel(file_path)
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    return df

df = load_data()

# --- Custom Styling for Dark Grey Background ---
custom_template = "plotly_dark" # Usando un tema oscuro como base
bg_color = "#262626" # Color gris oscuro

# --- Sidebar for Filters ---
st.sidebar.header('Filter Data')

# Region filter
available_regions = df['Region'].unique()
selected_regions = st.sidebar.multiselect('Select Region(s)', available_regions, available_regions)

# Category filter
available_categories = df['Category'].unique()
selected_categories = st.sidebar.multiselect('Select Category(s)', available_categories, available_categories)

# Filter data based on selected regions and categories
filtered_df = df[df['Region'].isin(selected_regions) & df['Category'].isin(selected_categories)]

st.header('Overview of Sales Data (Filtered)')
st.write(f"Total Sales Records (filtered): {len(filtered_df):,}")
st.write(filtered_df.head())

st.subheader('Sales Over Time')
fig_sales_time = px.line(filtered_df.sort_values('Order Date'), x='Order Date', y='Sales', title='Sales Over Time', height=400,
                          template=custom_template)
fig_sales_time.update_layout(paper_bgcolor=bg_color, plot_bgcolor=bg_color)
st.plotly_chart(fig_sales_time, use_container_width=True)

st.subheader('Total Sales by Region')
sales_by_region = filtered_df.groupby('Region')['Sales'].sum().reset_index()
fig_sales_region = px.bar(sales_by_region, x='Region', y='Sales', title='Total Sales by Region', height=400,
                           template=custom_template)
fig_sales_region.update_layout(paper_bgcolor=bg_color, plot_bgcolor=bg_color)
st.plotly_chart(fig_sales_region, use_container_width=True)

st.subheader('Total Sales by Category')
sales_by_category = filtered_df.groupby('Category')['Sales'].sum().reset_index()
fig_sales_category = px.pie(sales_by_category, values='Sales', names='Category', title='Total Sales by Category',
                            template=custom_template)
fig_sales_category.update_layout(paper_bgcolor=bg_color, plot_bgcolor=bg_color)
st.plotly_chart(fig_sales_category, use_container_width=True)

st.subheader('Top 10 Sales by Sub-Category')
sales_by_subcategory = filtered_df.groupby('Sub-Category')['Sales'].sum().nlargest(10).reset_index()
fig_sales_subcategory = px.bar(sales_by_subcategory, x='Sub-Category', y='Sales', title='Top 10 Sales by Sub-Category', height=400,
                                template=custom_template)
fig_sales_subcategory.update_layout(paper_bgcolor=bg_color, plot_bgcolor=bg_color)
st.plotly_chart(fig_sales_subcategory, use_container_width=True)

# --- Sales by State Map (Choropleth Map with Logarithmic Scale and State Codes) ---
st.subheader('Ventas por Estado en USA')

# State abbreviations mapping
state_abbreviations = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'District of Columbia': 'DC',
    'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL',
    'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA',
    'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN',
    'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
    'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
    'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR',
    'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD',
    'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA',
    'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
}

sales_by_state = filtered_df.groupby('State')['Sales'].sum().reset_index()
sales_by_state['State_Code'] = sales_by_state['State'].map(state_abbreviations)

# Apply logarithmic transformation for better color distribution
sales_by_state['Log_Sales'] = np.log1p(sales_by_state['Sales']) # log1p(x) computes log(1+x)

fig_state = px.choropleth(
    sales_by_state,
    locations='State_Code', # Usar la columna 'State_Code' para las ubicaciones
    locationmode='USA-states',
    color='Log_Sales', # Usar la columna transformada logarítmicamente para el color
    scope='usa',
    color_continuous_scale='Plasma', # Escala de color cambiada para mejor contraste
    title='Ventas Totales por Estado en USA (Escala Logarítmica)',
    labels={'Log_Sales': 'Log de Ventas Totales', 'State': 'Estado'},
    hover_name='State', # Mostrar el nombre original del estado al pasar el cursor
    hover_data={'Sales': ':.2f', 'Log_Sales': False} # Mostrar el valor original de las ventas, ocultar log_sales
)
fig_state.update_layout(paper_bgcolor=bg_color, plot_bgcolor=bg_color, geo_scope='usa') # Asegura que el mapa esté centrado en USA
st.plotly_chart(fig_state, use_container_width=True)
st.markdown('---') # Separador visual

print("Streamlit app 'dashboard_ventas.py' has been updated with advanced map features and filtering.")

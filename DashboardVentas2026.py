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

# --- Custom Styling for Dark Grey Background ---
custom_template = "plotly_dark" # Using a dark template as a base
bg_color = "#262626" # Dark grey color

st.header('Overview of Sales Data')
st.write(f"Total Sales Records: {len(df):,}")
st.write(df.head())

st.subheader('Sales Over Time')
fig_sales_time = px.line(df.sort_values('Order Date'), x='Order Date', y='Sales', title='Sales Over Time', height=400,
                          template=custom_template)
fig_sales_time.update_layout(paper_bgcolor=bg_color, plot_bgcolor=bg_color)
st.plotly_chart(fig_sales_time, use_container_width=True)

st.subheader('Total Sales by Region')
sales_by_region = df.groupby('Region')['Sales'].sum().reset_index()
fig_sales_region = px.bar(sales_by_region, x='Region', y='Sales', title='Total Sales by Region', height=400,
                           template=custom_template)
fig_sales_region.update_layout(paper_bgcolor=bg_color, plot_bgcolor=bg_color)
st.plotly_chart(fig_sales_region, use_container_width=True)

st.subheader('Total Sales by Category')
sales_by_category = df.groupby('Category')['Sales'].sum().reset_index()
fig_sales_category = px.pie(sales_by_category, values='Sales', names='Category', title='Total Sales by Category',
                            template=custom_template)
fig_sales_category.update_layout(paper_bgcolor=bg_color, plot_bgcolor=bg_color)
st.plotly_chart(fig_sales_category, use_container_width=True)

st.subheader('Top 10 Sales by Sub-Category')
sales_by_subcategory = df.groupby('Sub-Category')['Sales'].sum().nlargest(10).reset_index()
fig_sales_subcategory = px.bar(sales_by_subcategory, x='Sub-Category', y='Sales', title='Top 10 Sales by Sub-Category', height=400,
                                template=custom_template)
fig_sales_subcategory.update_layout(paper_bgcolor=bg_color, plot_bgcolor=bg_color)
st.plotly_chart(fig_sales_subcategory, use_container_width=True)

# Add the Sales by State Choropleth Map with dark background and hover info
st.subheader('Sales by State in USA')
sales_by_state = df.groupby('State')['Sales'].sum().reset_index()

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

sales_by_state['State Abbreviation'] = sales_by_state['State'].map(state_abbreviations)

fig_sales_state_map = px.choropleth(sales_by_state,
                                   locations='State',
                                   locationmode='USA-states',
                                   color='Sales',
                                   scope='usa',
                                   color_continuous_scale="Plasma", # Changed to Plasma for better visibility
                                   title='Total Sales by State',
                                   hover_name='State',
                                   hover_data={'State Abbreviation': True, 'Sales': ':,.2f'},
                                   height=600,
                                   template=custom_template)
fig_sales_state_map.update_layout(paper_bgcolor=bg_color, plot_bgcolor=bg_color)
st.plotly_chart(fig_sales_state_map, use_container_width=True)

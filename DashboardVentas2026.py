import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout='wide')
st.title('Profit Dashboard for USA Branches')

@st.cache_data
def load_data():
    file_path = '/content/drive/MyDrive/Practica 7/SalidaVentas.xlsx'
    df = pd.read_excel(file_path)
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    return df

df = load_data()

# --- Custom Styling ---
custom_template = "plotly_white"
bg_color = "lightgrey"
line_color_single = "darkgrey" # For single line plots
discrete_colors = ['#88B04B', '#F7CAC9', '#92A8D1', '#9B2335', '#A2AB58', '#E6A29F', '#795548', '#FFB6C1', '#DDA0DD'] # A subdued palette

# --- Sidebar for Filters ---
st.sidebar.header('Filter Data')

# Region filter
available_regions = df['Region'].unique()
selected_regions = st.sidebar.multiselect('Select Region(s)', available_regions, available_regions)

# Filter data based on selected regions
filtered_df = df[df['Region'].isin(selected_regions)]

st.header('Overview of Profit Data')
st.write(f"Total Profit Records (filtered): {len(filtered_df):,}")
st.write(filtered_df.head())

st.subheader('Profit Over Time')
fig_profit_time = px.line(filtered_df.sort_values('Order Date'), x='Order Date', y='Profit', title='Profit Over Time', height=400,
                          template=custom_template,
                          line_color=line_color_single) # Using a single subdued color for the line
fig_profit_time.update_layout(paper_bgcolor=bg_color, plot_bgcolor=bg_color)
st.plotly_chart(fig_profit_time, use_container_width=True)

st.subheader('Total Profit by Region')
profit_by_region = filtered_df.groupby('Region')['Profit'].sum().reset_index()
fig_profit_region = px.bar(profit_by_region, x='Region', y='Profit', title='Total Profit by Region', height=400,
                           template=custom_template,
                           color='Region', # Color by region to use discrete_colors
                           color_discrete_sequence=discrete_colors)
fig_profit_region.update_layout(paper_bgcolor=bg_color, plot_bgcolor=bg_color)
st.plotly_chart(fig_profit_region, use_container_width=True)

st.subheader('Total Profit by Category')
profit_by_category = filtered_df.groupby('Category')['Profit'].sum().reset_index()
fig_profit_category = px.pie(profit_by_category, values='Profit', names='Category', title='Total Profit by Category',
                            template=custom_template,
                            color_discrete_sequence=discrete_colors)
fig_profit_category.update_layout(paper_bgcolor=bg_color, plot_bgcolor=bg_color)
st.plotly_chart(fig_profit_category, use_container_width=True)

st.subheader('Top 10 Profit by Sub-Category')
profit_by_subcategory = filtered_df.groupby('Sub-Category')['Profit'].sum().nlargest(10).reset_index()
fig_profit_subcategory = px.bar(profit_by_subcategory, x='Sub-Category', y='Profit', title='Top 10 Profit by Sub-Category', height=400,
                                template=custom_template,
                                color='Sub-Category', # Color by sub-category
                                color_discrete_sequence=discrete_colors)
fig_profit_subcategory.update_layout(paper_bgcolor=bg_color, plot_bgcolor=bg_color)
st.plotly_chart(fig_profit_subcategory, use_container_width=True)

st.subheader('Profit by State in USA')
profit_by_state = filtered_df.groupby('State')['Profit'].sum().reset_index()

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

profit_by_state['State Abbreviation'] = profit_by_state['State'].map(state_abbreviations)

fig_profit_state_map = px.choropleth(profit_by_state,
                                   locations='State',
                                   locationmode='USA-states',
                                   color='Profit',
                                   scope='usa',
                                   color_continuous_scale="Viridis", # Changed from Greys to Viridis for testing
                                   title='Total Profit by State',
                                   hover_name='State',
                                   hover_data={'State Abbreviation': True, 'Profit': ':,.2f'},
                                   height=600,
                                   template=custom_template)
fig_profit_state_map.update_layout(paper_bgcolor=bg_color, plot_bgcolor=bg_color)
st.plotly_chart(fig_profit_state_map, use_container_width=True)

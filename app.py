import pandas as pd
import streamlit as st
import plotly.express as px

df = pd.read_csv('/content/swiggy.csv')
st.set_page_config(page_title='Swiggy Dashboard', layout='wide')
st.title('Swiggy Dashboard')

# Sidebar for filters
st.sidebar.header('Filter Options')

# City filter
cities = df['City'].unique()
selected_city = st.sidebar.selectbox('Select City', ['All'] + list(cities))

# Area filter (dependent on city selection)
if selected_city != 'All':
    areas_in_city = df[df['City'] == selected_city]['Area'].unique()
    selected_area = st.sidebar.selectbox('Select Area', ['All'] + list(areas_in_city))
else:
    selected_area = st.sidebar.selectbox('Select Area', ['All'] + list(df['Area'].unique()))

# Restaurant Type filter (corrected to 'Food type')
restaurant_types = df['Food type'].unique()
selected_restaurant_type = st.sidebar.selectbox('Select Restaurant Type', ['All'] + list(restaurant_types))

# Apply filters
filtered_df = df.copy()
if selected_city != 'All':
    filtered_df = filtered_df[filtered_df['City'] == selected_city]
if selected_area != 'All':
    filtered_df = filtered_df[filtered_df['Area'] == selected_area]
if selected_restaurant_type != 'All':
    filtered_df = filtered_df[filtered_df['Food type'] == selected_restaurant_type]

st.write(f"Displaying data for: City='{selected_city}', Area='{selected_area}', Restaurant Type='{selected_restaurant_type}'")

# Display visualizations
st.subheader('Data Visualizations')

# Check if filtered_df is empty to avoid errors
if not filtered_df.empty:
    # Bar chart: Count of restaurants by Food Type
    food_type_counts = filtered_df['Food type'].value_counts().reset_index()
    food_type_counts.columns = ['Food type', 'Count']
    fig_food_type = px.bar(food_type_counts, x='Food type', y='Count', title='Number of Restaurants by Food Type')
    st.plotly_chart(fig_food_type, width='stretch') # Corrected here

    # Histogram: Distribution of Prices
    if 'Price' in filtered_df.columns:
        fig_price_dist = px.histogram(filtered_df, x='Price', nbins=20, title='Distribution of Restaurant Prices')
        st.plotly_chart(fig_price_dist, width='stretch') # Corrected here
    else:
        st.warning("Price column not found in the filtered data for visualization.")

else:
    st.warning("No data available for the selected filters.")

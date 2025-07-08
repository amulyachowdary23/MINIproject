import streamlit as st
import pandas as pd
import numpy as np
from data_processor import load_and_process_data
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Food Recommendations", layout="wide")

def get_similar_foods(df, food_name, n_recommendations=5):
    """Get similar foods based on nutritional content."""
    features = ['Calories', 'Protein', 'Fat', 'Carbs', 'Fiber']
    
    # Prepare feature matrix
    X = df[features].copy()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Calculate similarity
    similarity = cosine_similarity(X_scaled)
    
    # Get index of the selected food
    food_idx = df[df['Food'] == food_name].index[0]
    
    # Get similar foods
    similar_indices = similarity[food_idx].argsort()[::-1][1:n_recommendations+1]
    similar_foods = df.iloc[similar_indices]
    
    return similar_foods

def get_foods_by_nutrient(df, nutrient, min_value=None, max_value=None):
    """Get foods filtered by nutrient content."""
    filtered_df = df.copy()
    
    if min_value is not None:
        filtered_df = filtered_df[filtered_df[nutrient] >= min_value]
    if max_value is not None:
        filtered_df = filtered_df[filtered_df[nutrient] <= max_value]
    
    return filtered_df.sort_values(nutrient, ascending=False)

# Load data
df = load_and_process_data()

if df is not None:
    st.title("Food Recommendations")
    
    # Sidebar for recommendation type
    recommendation_type = st.sidebar.radio(
        "Select Recommendation Type",
        ["Similar Foods", "Nutrient-based Filtering"]
    )
    
    if recommendation_type == "Similar Foods":
        st.header("Find Similar Foods")
        st.markdown("""
        This tool helps you find foods with similar nutritional profiles to your selected food.
        """)
        
        selected_food = st.selectbox(
            "Select a Food",
            sorted(df["Food"].unique())
        )
        
        n_recommendations = st.slider(
            "Number of Recommendations",
            min_value=3,
            max_value=10,
            value=5
        )
        
        if st.button("Get Recommendations"):
            similar_foods = get_similar_foods(df, selected_food, n_recommendations)
            
            st.subheader(f"Foods similar to {selected_food}")
            for _, food in similar_foods.iterrows():
                with st.expander(food['Food']):
                    st.write(f"Category: {food['Category']}")
                    st.write(f"Calories: {food['Calories']:.1f}")
                    st.write(f"Protein: {food['Protein']:.1f}g")
                    st.write(f"Fat: {food['Fat']:.1f}g")
                    st.write(f"Carbs: {food['Carbs']:.1f}g")
    
    else:
        st.header("Filter Foods by Nutrient Content")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nutrient = st.selectbox(
                "Select Nutrient",
                ["Calories", "Protein", "Fat", "Carbs", "Fiber"]
            )
            
        with col2:
            min_value = st.number_input(
                f"Minimum {nutrient}",
                value=float(df[nutrient].min()),
                step=1.0
            )
            max_value = st.number_input(
                f"Maximum {nutrient}",
                value=float(df[nutrient].max()),
                step=1.0
            )
        
        if st.button("Find Foods"):
            filtered_foods = get_foods_by_nutrient(df, nutrient, min_value, max_value)
            
            st.subheader(f"Foods matching your criteria")
            st.dataframe(
                filtered_foods[['Food', 'Category', nutrient]]
                .head(10)
                .style.highlight_max(nutrient, color='lightgreen')
            )
else:
    st.error("Error loading the dataset. Please check the data file and try again.")

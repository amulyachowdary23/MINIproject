import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from data_processor import load_and_process_data
from visualizations import create_correlation_plot, create_category_comparison
import pandas as pd
st.set_page_config(page_title="Advanced Analytics", layout="wide")

# Load data
df = load_and_process_data()

if df is not None:
    st.title("Advanced Analytics & Correlations")
    
    # Correlation Analysis
    st.header("Nutrient Correlation Analysis")
    nutrients = ["Calories", "Protein", "Fat", "Carbs", "Fiber"]
    
    try:
        corr_plot = create_correlation_plot(df[nutrients])
        st.plotly_chart(corr_plot, use_container_width=True)
    except Exception as e:
        st.error(f"Error creating correlation plot: {str(e)}")
    
    # Category Comparison
    st.header("Category-wise Nutrient Comparison")
    try:
        comp_plot = create_category_comparison(df, nutrients)
        st.plotly_chart(comp_plot, use_container_width=True)
    except Exception as e:
        st.error(f"Error creating category comparison: {str(e)}")
    
    # Nutrient Comparison Tool
    st.header("Food Comparison Tool")
    col1, col2 = st.columns(2)
    
    with col1:
        food1 = st.selectbox("Select First Food", sorted(df["Food"].unique()), key="food1")
        food1_data = df[df["Food"] == food1].iloc[0]
    
    with col2:
        food2 = st.selectbox("Select Second Food", sorted(df["Food"].unique()), key="food2")
        food2_data = df[df["Food"] == food2].iloc[0]
    
    comparison_data = pd.DataFrame({
        'Nutrient': nutrients,
        food1: [food1_data[nutrient] for nutrient in nutrients],
        food2: [food2_data[nutrient] for nutrient in nutrients]
    })
    
    fig = px.bar(comparison_data, x='Nutrient', y=[food1, food2], barmode='group',
                 title=f"Nutrient Comparison: {food1} vs {food2}")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("Error loading the dataset. Please check the data file and try again.")

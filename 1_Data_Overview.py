import streamlit as st
import plotly.express as px
from data_processor import load_and_process_data

st.set_page_config(page_title="Nutritional Composition Analysis", layout="wide")

# Load data
df = load_and_process_data()

if df is not None:
    st.title("Nutritional Composition Analysis")

    st.markdown("""
    This section provides a detailed analysis of the nutritional composition of various food items.
    The analysis focuses on key nutrients that impact health outcomes.
    """)

    # Sidebar filters
    st.sidebar.header("Analysis Filters")

    # Category filter
    selected_category = st.sidebar.selectbox(
        "Select Food Category",
        ["All"] + sorted(df["Category"].unique().tolist())
    )

    # Filter data based on selection
    filtered_df = df[df["Category"] == selected_category] if selected_category != "All" else df

    # Nutrient Composition Analysis
    st.header("Nutrient Composition Analysis")

    # Summary statistics for the selected category
    st.subheader("Statistical Summary")
    nutrients = ["Calories", "Protein", "Fat", "Carbs", "Fiber"]
    stats_df = filtered_df[nutrients].describe()
    st.dataframe(stats_df.style.format("{:.2f}"))

    # Nutrient Distribution
    st.header("Nutrient Distribution Analysis")
    selected_nutrient = st.selectbox("Select Nutrient for Analysis", nutrients)

    col1, col2 = st.columns(2)

    with col1:
        # Histogram
        fig_hist = px.histogram(
            filtered_df,
            x=selected_nutrient,
            title=f"Distribution of {selected_nutrient}"
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    with col2:
        # Box plot
        fig_box = px.box(
            filtered_df,
            y=selected_nutrient,
            title=f"Box Plot of {selected_nutrient}"
        )
        st.plotly_chart(fig_box, use_container_width=True)

    # Nutrient Composition by Category
    if selected_category == "All":
        st.header("Category-wise Nutrient Analysis")

        # Average nutrient content by category
        avg_by_category = df.groupby('Category')[nutrients].mean().reset_index()

        # Create a heatmap of average nutrient content
        fig_heatmap = px.imshow(
            avg_by_category[nutrients].T,
            x=avg_by_category['Category'],
            y=nutrients,
            title="Average Nutrient Content by Food Category",
            aspect="auto"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)

    # Raw Data Display
    st.header("Detailed Data View")
    st.dataframe(filtered_df)

else:
    st.error("Error loading the dataset. Please check the data file and try again.")
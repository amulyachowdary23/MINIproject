import streamlit as st
from data_processor import load_and_process_data
from ml_analysis import perform_kmeans_clustering, get_feature_importance

st.set_page_config(page_title="Machine Learning Insights", layout="wide")

# Load data
df = load_and_process_data()

if df is not None:
    st.title("Machine Learning Insights")
    
    # K-means clustering
    st.header("Food Clustering Analysis")
    st.markdown("""
    This analysis groups similar foods based on their nutritional content using K-means clustering.
    Adjust the number of clusters to see different groupings.
    """)
    
    n_clusters = st.slider("Number of Clusters", 2, 8, 4)
    
    try:
        cluster_fig, cluster_labels = perform_kmeans_clustering(df, n_clusters)
        st.plotly_chart(cluster_fig, use_container_width=True)
        
        # Display cluster information
        st.subheader("Cluster Analysis")
        for i in range(n_clusters):
            cluster_foods = df[cluster_labels == i]["Food"].tolist()
            with st.expander(f"Cluster {i+1} Foods"):
                st.write(", ".join(cluster_foods))
    except Exception as e:
        st.error(f"Error performing clustering: {str(e)}")
    
    # Feature importance
    st.header("Nutrient Importance Analysis")
    st.markdown("""
    This analysis shows how different nutrients contribute to the overall caloric content of foods.
    """)
    
    try:
        importance_fig = get_feature_importance(df)
        st.plotly_chart(importance_fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error calculating feature importance: {str(e)}")
else:
    st.error("Error loading the dataset. Please check the data file and try again.")

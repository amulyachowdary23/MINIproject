import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import numpy as np

def perform_kmeans_clustering(df, n_clusters):
    """Perform K-means clustering on nutritional data."""
    try:
        # Select features for clustering
        features = ['Calories', 'Protein', 'Fat', 'Carbs', 'Fiber']
        X = df[features].copy()

        # Handle missing or invalid values
        X = X.fillna(X.mean())

        # Scale the features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Perform clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(X_scaled)

        # Create visualization
        df_plot = pd.DataFrame(X_scaled, columns=features)
        df_plot['Cluster'] = clusters
        df_plot['Food'] = df['Food']

        fig = px.scatter_3d(
            df_plot,
            x='Calories',
            y='Protein',
            z='Fat',
            color='Cluster',
            hover_data=['Food'],
            title="Food Clusters based on Nutritional Content"
        )

        return fig, clusters
    except Exception as e:
        print(f"Error in clustering: {str(e)}")
        raise

def get_feature_importance(df):
    """Calculate and visualize feature importance."""
    try:
        features = ['Protein', 'Fat', 'Carbs', 'Fiber']
        X = df[features].copy()
        y = df['Calories'].copy()

        # Handle missing values
        X = X.fillna(X.mean())
        y = y.fillna(y.mean())

        # Train random forest
        rf = RandomForestRegressor(n_estimators=100, random_state=42)
        rf.fit(X, y)

        # Create importance plot
        importance_df = pd.DataFrame({
            'Feature': features,
            'Importance': rf.feature_importances_
        }).sort_values('Importance', ascending=True)

        fig = px.bar(
            importance_df,
            x='Importance',
            y='Feature',
            orientation='h',
            title="Nutrient Importance for Calorie Content"
        )

        return fig
    except Exception as e:
        print(f"Error in feature importance: {str(e)}")
        raise
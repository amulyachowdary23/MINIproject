import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def create_distribution_plot(df, nutrient):
    """Create distribution plot for a given nutrient."""
    try:
        fig = px.histogram(
            df, 
            x=nutrient,
            nbins=30,
            title=f"Distribution of {nutrient}",
            labels={nutrient: f"{nutrient} Content"}
        )
        fig.update_layout(
            showlegend=False,
            xaxis_title=f"{nutrient} Content",
            yaxis_title="Count"
        )
        return fig
    except Exception as e:
        print(f"Error in create_distribution_plot: {str(e)}")
        return None

def create_correlation_plot(df):
    """Create correlation heatmap for nutrients."""
    try:
        # Calculate correlation matrix
        corr = df.corr()

        fig = go.Figure(data=go.Heatmap(
            z=corr,
            x=corr.columns,
            y=corr.columns,
            colorscale='RdBu',
            zmin=-1,
            zmax=1
        ))

        fig.update_layout(
            title="Nutrient Correlation Matrix",
            width=600,
            height=600,
            xaxis_tickangle=-45
        )

        return fig
    except Exception as e:
        print(f"Error in create_correlation_plot: {str(e)}")
        return None

def create_category_comparison(df, nutrients):
    """Create category-wise nutrient comparison plot."""
    try:
        # Calculate mean values for each category and nutrient
        category_means = df.groupby('Category')[nutrients].mean().reset_index()

        # Melt the dataframe for plotting
        melted_df = category_means.melt(
            id_vars=['Category'],
            value_vars=nutrients,
            var_name='Nutrient',
            value_name='Value'
        )

        fig = px.box(
            df,
            x='Category',
            y=nutrients,
            title="Nutrient Distribution by Food Category",
            points="all"
        )

        fig.update_layout(
            xaxis_tickangle=-45,
            height=600,
            showlegend=True
        )

        return fig
    except Exception as e:
        print(f"Error in create_category_comparison: {str(e)}")
        return None

def create_scatter_matrix(df, nutrients):
    """Create scatter matrix for selected nutrients."""
    try:
        fig = px.scatter_matrix(
            df,
            dimensions=nutrients,
            title="Nutrient Relationships Matrix"
        )

        fig.update_layout(
            width=800,
            height=800
        )

        return fig
    except Exception as e:
        print(f"Error in create_scatter_matrix: {str(e)}")
        return None
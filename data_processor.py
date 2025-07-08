import pandas as pd
import numpy as np

def load_and_process_data():
    """Load and preprocess the nutritional data."""
    try:
        # Load data
        df = pd.read_csv("attached_assets/nutrients_csvfile.csv")

        # Clean column names
        df.columns = df.columns.str.strip()

        # Convert numeric columns
        numeric_columns = ['Grams', 'Calories', 'Protein', 'Fat', 'Sat.Fat', 'Fiber', 'Carbs']

        for col in numeric_columns:
            # Handle 't' values and remove commas
            df[col] = pd.to_numeric(
                df[col].replace(['t', 'T'], '0')
                .astype(str)
                .str.replace(',', '')
                .str.replace('$', '')
                .str.strip(),
                errors='coerce'
            )

        # Fill missing values with 0
        df = df.fillna(0)

        # Remove rows where all numeric columns are 0
        df = df[~(df[numeric_columns] == 0).all(axis=1)]

        return df
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return None

def get_nutrient_stats(df, nutrient):
    """Calculate basic statistics for a given nutrient."""
    if df is None or nutrient not in df.columns:
        return None

    stats = {
        'mean': df[nutrient].mean(),
        'median': df[nutrient].median(),
        'std': df[nutrient].std(),
        'min': df[nutrient].min(),
        'max': df[nutrient].max()
    }
    return stats
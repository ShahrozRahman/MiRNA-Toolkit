import pandas as pd


def build_feature_matrix(expression_df: pd.DataFrame, label_column: str):
    """Split expression table into X features and y labels."""
    if label_column not in expression_df.columns:
        raise KeyError(f"{label_column} not found in expression dataframe")

    y = expression_df[label_column].copy()
    x = expression_df.drop(columns=[label_column]).copy()
    return x, y

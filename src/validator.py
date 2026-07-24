import pandas as pd


def validate_data(df):
    """
    Perform basic data validation.
    """
    if df.empty:
        raise ValueError("Dataset is empty.")

    if df.isnull().sum().sum() > 0:
        print("Warning: Missing values detected.")

    return df
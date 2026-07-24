import pandas as pd


def load_purchase_data(csv_path):
    """
    Load purchase records from a CSV file.
    """
    return pd.read_csv(csv_path)


def load_finance_data(excel_path):
    """
    Load finance records from an Excel file.
    """
    return pd.read_excel(excel_path, engine="openpyxl")
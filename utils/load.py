import pandas as pd


def save_to_csv(dataframe: pd.DataFrame, file_name: str = "products.csv") -> bool:
    try:
        dataframe.to_csv(file_name, index=False)
        return True
    except Exception as error:
        print(f"Error saving to CSV: {error}")
        return False
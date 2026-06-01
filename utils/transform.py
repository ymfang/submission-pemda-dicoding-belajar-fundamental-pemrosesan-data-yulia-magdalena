import re
import pandas as pd


EXCHANGE_RATE = 16000


def clean_title(value):
    try:
        if pd.isna(value):
            return None

        value = str(value).strip()
        if value == "" or value == "Unknown Product":
            return None

        return value
    except Exception as error:
        print(f"Error cleaning title: {error}")
        return None


def clean_price(value):
    try:
        if pd.isna(value):
            return None

        value = str(value).strip()

        if value == "" or value == "Price Unavailable":
            return None

        number = value.replace("$", "").replace(",", "").strip()
        return float(number) * EXCHANGE_RATE
    except Exception as error:
        print(f"Error cleaning price: {error}")
        return None


def clean_rating(value):
    try:
        if pd.isna(value):
            return None

        value = str(value).strip()

        if "Invalid Rating" in value or "Not Rated" in value:
            return None

        match = re.search(r"(\d+(\.\d+)?)\s*/\s*5", value)
        if not match:
            return None

        return float(match.group(1))
    except Exception as error:
        print(f"Error cleaning rating: {error}")
        return None


def clean_colors(value):
    try:
        if pd.isna(value):
            return None

        value = str(value).strip()
        match = re.search(r"(\d+)", value)

        if not match:
            return None

        return int(match.group(1))
    except Exception as error:
        print(f"Error cleaning colors: {error}")
        return None


def clean_size(value):
    try:
        if pd.isna(value):
            return None

        value = str(value).replace("Size:", "").strip()

        if value == "":
            return None

        return value
    except Exception as error:
        print(f"Error cleaning size: {error}")
        return None


def clean_gender(value):
    try:
        if pd.isna(value):
            return None

        value = str(value).replace("Gender:", "").strip()

        if value == "":
            return None

        return value
    except Exception as error:
        print(f"Error cleaning gender: {error}")
        return None


def transform_data(data):
    try:
        dataframe = pd.DataFrame(data).copy()

        if dataframe.empty:
            return dataframe

        dataframe["Title"] = dataframe["Title"].apply(clean_title)
        dataframe["Price"] = dataframe["Price"].apply(clean_price)
        dataframe["Rating"] = dataframe["Rating"].apply(clean_rating)
        dataframe["Colors"] = dataframe["Colors"].apply(clean_colors)
        dataframe["Size"] = dataframe["Size"].apply(clean_size)
        dataframe["Gender"] = dataframe["Gender"].apply(clean_gender)

        dataframe = dataframe.dropna()
        dataframe = dataframe.drop_duplicates().reset_index(drop=True)

        dataframe["Price"] = dataframe["Price"].astype(float)
        dataframe["Rating"] = dataframe["Rating"].astype(float)
        dataframe["Colors"] = dataframe["Colors"].astype(int)
        dataframe["Size"] = dataframe["Size"].astype("object")
        dataframe["Gender"] = dataframe["Gender"].astype("object")
        dataframe["timestamp"] = dataframe["timestamp"].astype("object")

        return dataframe
    except Exception as error:
        print(f"Error transforming data: {error}")
        return pd.DataFrame()
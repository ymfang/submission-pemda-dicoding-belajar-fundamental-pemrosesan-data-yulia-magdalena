import pandas as pd

from utils.transform import (
    clean_title,
    clean_price,
    clean_rating,
    clean_colors,
    clean_size,
    clean_gender,
    transform_data,
)


def test_clean_title():
    assert clean_title("T-shirt 2") == "T-shirt 2"
    assert clean_title("Unknown Product") is None


def test_clean_price():
    assert clean_price("$102.15") == 1634400.0
    assert clean_price("Price Unavailable") is None


def test_clean_rating():
    assert clean_rating("Rating: ⭐ 3.9 / 5") == 3.9
    assert clean_rating("Rating: Not Rated") is None
    assert clean_rating("Rating: ⭐ Invalid Rating / 5") is None


def test_clean_colors():
    assert clean_colors("3 Colors") == 3


def test_clean_size():
    assert clean_size("Size: XL") == "XL"


def test_clean_gender():
    assert clean_gender("Gender: Women") == "Women"


def test_transform_data_removes_invalid_and_duplicates():
    raw_data = [
        {
            "Title": "Unknown Product",
            "Price": "$100.00",
            "Rating": "Rating: ⭐ Invalid Rating / 5",
            "Colors": "5 Colors",
            "Size": "Size: M",
            "Gender": "Gender: Men",
            "timestamp": "2026-06-01T17:13:33.527605",
        },
        {
            "Title": "T-shirt 2",
            "Price": "$102.15",
            "Rating": "Rating: ⭐ 3.9 / 5",
            "Colors": "3 Colors",
            "Size": "Size: M",
            "Gender": "Gender: Women",
            "timestamp": "2026-06-01T17:13:33.527605",
        },
        {
            "Title": "T-shirt 2",
            "Price": "$102.15",
            "Rating": "Rating: ⭐ 3.9 / 5",
            "Colors": "3 Colors",
            "Size": "Size: M",
            "Gender": "Gender: Women",
            "timestamp": "2026-06-01T17:13:33.527605",
        },
        {
            "Title": "Pants 16",
            "Price": "Price Unavailable",
            "Rating": "Rating: Not Rated",
            "Colors": "8 Colors",
            "Size": "Size: S",
            "Gender": "Gender: Men",
            "timestamp": "2026-06-01T17:13:33.527605",
        },
    ]

    dataframe = transform_data(raw_data)

    assert len(dataframe) == 1
    assert dataframe.iloc[0]["Title"] == "T-shirt 2"
    assert dataframe.iloc[0]["Price"] == 1634400.0
    assert dataframe.iloc[0]["Rating"] == 3.9
    assert dataframe.iloc[0]["Colors"] == 3
    assert dataframe.iloc[0]["Size"] == "M"
    assert dataframe.iloc[0]["Gender"] == "Women"


def test_transform_data_output_dtypes():
    raw_data = [
        {
            "Title": "Jacket 6",
            "Price": "$153.37",
            "Rating": "Rating: ⭐ 3.3 / 5",
            "Colors": "3 Colors",
            "Size": "Size: S",
            "Gender": "Gender: Unisex",
            "timestamp": "2026-06-01T17:13:33.527605",
        }
    ]

    dataframe = transform_data(raw_data)

    assert dataframe["Price"].dtype == "float64"
    assert dataframe["Rating"].dtype == "float64"
    assert dataframe["Colors"].dtype == "int64"
    assert dataframe["Size"].dtype == "object"
    assert dataframe["Gender"].dtype == "object"
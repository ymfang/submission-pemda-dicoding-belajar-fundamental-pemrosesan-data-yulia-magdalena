from unittest.mock import patch
import pandas as pd

from utils.load import save_to_csv


def test_save_to_csv_success(tmp_path):
    dataframe = pd.DataFrame(
        [
            {
                "Title": "T-shirt 2",
                "Price": 1634400.0,
                "Rating": 3.9,
                "Colors": 3,
                "Size": "M",
                "Gender": "Women",
                "timestamp": "2026-06-01T17:13:33.527605",
            }
        ]
    )

    file_path = tmp_path / "products.csv"
    result = save_to_csv(dataframe, str(file_path))

    assert result is True
    assert file_path.exists()

    saved_dataframe = pd.read_csv(file_path)
    assert len(saved_dataframe) == 1
    assert saved_dataframe.iloc[0]["Title"] == "T-shirt 2"


def test_save_to_csv_failed():
    dataframe = pd.DataFrame(
        [
            {
                "Title": "T-shirt 2",
                "Price": 1634400.0,
            }
        ]
    )

    with patch.object(pd.DataFrame, "to_csv", side_effect=Exception("write error")):
        result = save_to_csv(dataframe, "products.csv")

    assert result is False
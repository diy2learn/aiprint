import pandas as pd

from aiprint.core import hightlight_dataframe


def test_hightlight_dataframe():
    raw = {}
    for idx in range(5):
        col = f"col_{idx}"
        raw[col] = [1, 2, 3, 4, 5]
    data = pd.DataFrame(raw)
    hightlight_dataframe(data, "col_1 % 2 == 0")

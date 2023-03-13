import pandas as pd

from aiprint.core import highlight_dict, highlight_text, hightlight_dataframe


def test_hightlight_dataframe():
    raw = {}
    for idx in range(5):
        col = f"col_{idx}"
        raw[col] = [1, 2, 3, 4, 5]
    data = pd.DataFrame(raw)
    hightlight_dataframe(data, "col_1 % 2 == 0")


def test_highlight_dict():
    data = {"success": False, "other_field": 123}
    highlight_dict(data, "success")


def test_highlight_text():
    logs = "Model status: failed. Cause: corrupted input data. All-other-related-stuffs"
    highlight_text(logs, "status")

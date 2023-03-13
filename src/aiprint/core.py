"""Core functions"""
from typing import Any

import pandas as pd
from termcolor import colored

from aiprint.helper import add_color, extract_status


def hightlight_dataframe(data: pd.DataFrame, condition: str, color: str = "red"):
    """Highlight rows in a dataframe based-on a given condition

    Examples
    --------
    import pandas as pd
    data = pd.DataFrame({"val": [7, 8, 9, 10], "col1": [10, 20, 30, 40], "col2": [1, 2, 3, 4]})

    # check one condition
    hightlight_dataframe(data, "val % 2 == 0")

    # check multiple conditions
    hightlight_dataframe(data, "col1 >= 20 & col2 <= 3")


    # check very large dataframe with fragmented print
    raw = {}
    for idx in range(30):
        col = f"col_{idx}"
        raw[col] = [1, 2, 3, 4, 5]
    data = pd.DataFrame(raw)
    hightlight_dataframe(data, "col_1 % 2 == 0")
    """
    mask = data.eval(condition)
    matched_idx = data.index[mask].tolist()
    partitioned_lines = str(data).split("\n\n")

    # to handle when very large dataframe is printed into more than 2 sections
    # , one parasite [n row x m col] is added
    if len(partitioned_lines) > 2:
        partitioned_lines = partitioned_lines[:-1]
    colored_lines = []
    for partitioned_str in partitioned_lines:
        lines = partitioned_str.split("\n")
        for idx in matched_idx:
            idx_line = idx + 1
            lines[idx_line] = colored(lines[idx_line], color)
        colored_lines.append("\n".join(lines))
    print("\n\n".join(colored_lines))


def highlight_dict(data: dict, key: str):
    """Highlight a given field of the dictionary

    Examples
    --------
    data = {"success": False,
            "other_field": 123}
    highlight_dict(data, "success")
    """
    data_str = str(data).replace("'", '"')
    pattern = f'"{key}": (\w+)'
    status = extract_status(data_str, pattern)
    filled_pattern = pattern.replace("(\w+)", status)
    print(add_color(data_str, filled_pattern, status))


def highlight_text(data: dict, key: str):
    """Highlight a given field of the dictionary

    Examples
    --------
    logs = "Model status: failed. Cause: corrupted input data.
            All-other-related-stuffs"
    highlight_text(logs, "status")
    """
    data_str = str(data).replace("'", '"')
    pattern = f"{key}: (\w+)"
    status = extract_status(data_str, pattern)
    filled_pattern = pattern.replace("(\w+)", status)
    print(add_color(data_str, filled_pattern, status))


def cprint(data: Any, key: str):
    """print with colorcode for queried key"""
    mapper = {pd.DataFrame: hightlight_dataframe, dict: highlight_dict, str: highlight_text}
    mapper[type(data)](data, key)

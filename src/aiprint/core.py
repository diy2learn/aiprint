"""Core functions"""
from typing import Any

import pandas as pd
from logzero import logger
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
    to_extract = "(\s?\w+)"
    pattern = f'"{key}":{to_extract}'
    try:
        status = extract_status(data_str, pattern)
        filled_pattern = pattern.replace(to_extract, status)
        print(add_color(data_str, filled_pattern, status))
    except TypeError:
        logger.debug("in dict-item highlight mode.")
        highlight_dict_item(data, key)


def highlight_dict_item(data: dict, key: str, color: str = "yellow"):
    """Highlight a given item of the dictionary"""
    data_str = str(data)
    item = data[key]
    to_colors = [f"'{key}':", str(item)]
    colored_text = [colored(txt, color) for txt in to_colors]
    mapper = zip(to_colors, colored_text)
    for to_color, colored_txt in mapper:
        data_str = data_str.replace(to_color, colored_txt)
    print(data_str)


def highlight_text(data: dict, key: str):
    """Highlight a given field of the dictionary

    Examples
    --------
    logs = "Model status: failed. Cause: corrupted input data.
            All-other-related-stuffs"
    highlight_text(logs, "status")
    """
    data_str = str(data).replace("'", '"')
    to_extract = "\w+"
    sep = "[:=]?"
    query = f"(\s?{sep}\s?{to_extract})"
    pattern = f"{key}{query}"
    extracted = extract_status(data_str, pattern)
    status = split_status(extracted, [":", "="])
    filled_pattern = pattern.replace(query, extracted)
    print(add_color(data_str, filled_pattern, status))


def split_status(text: str, separators: None):
    """Split status from `sep`"""
    default_seps = [":", "="]
    seps = separators if separators else default_seps
    for sep in seps:
        text = text.split(sep)[-1]
    return text


def cprint(data: Any, key: str):
    """print with colorcode for queried key"""
    mapper = {pd.DataFrame: hightlight_dataframe, dict: highlight_dict, str: highlight_text}
    mapper[type(data)](data, key)

"""helper functions"""


import re

from logzero import logger
from termcolor import colored


def str2bool(v):
    """convert string to boolean"""
    return v.strip().lower() in ("yes", "true", "t", "1", "ok")


def extract_status(data_str: str, pattern: str):
    """

    Examples
    --------
    data_str = {"success": false,
                "other_field": 123}
    """
    extracted = re.findall(pattern, data_str)
    if len(extracted) == 0:
        logger.debug("Can not extract status from key")
    else:
        return extracted[0]


def add_color(data_str: str, pattern: str, status: str):
    color = "green" if str2bool(status) else "red"
    colored_txt = colored(pattern, color)
    return data_str.replace(pattern, colored_txt)

"""
Constant for prj
"""

import pandas as pd


TOKEN = pd.read_parquet(r"./Bot/resources/env_var.kzd")['Token'].values[0]


def add_var(name_var: str, value_var: str | int | float | pd.Timestamp) -> None:
    """
    Add custom variables for prj to file
    :param name: Name var
    :param value: Value var
    :return: None
    """
    df = pd.read_parquet("env_var.kzd")
    cols = df.columns.tolist()
    if name_var in cols:
        raise KeyError(f"Name {name_var} already exist")
    df[name_var] = [value_var]
    df.to_parquet("env_var.kzd")


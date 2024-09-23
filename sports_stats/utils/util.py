import re
from pandas import DataFrame
from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def to_int(string: str):
    try:
        string = int(string.replace('.', ''))
        return string
    except ValueError:
        raise ValueError(f'Value "{string}" cannot be coerced to type integer.')


def clean_table(raw_df: DataFrame, post=False) -> DataFrame:
    df = raw_df.copy()
    if len(df.columns) > 0 and (type(df.columns[0]) != str) and len(df.columns[0]) > 1:
        new_cols = [(re.sub("Unnamed: [0-9]*_level_[0-9]*", "Misc", col[0]) + "_" + col[1]).rstrip('_') for col in df.columns if "Unnamed" not in col[1]]
        df.columns = df.columns.droplevel()
        idx = [i for i, col in enumerate(df.columns) if "Unnamed" not in col]
        df = df.iloc[:, idx]
        df.columns = [col.replace(" ", "-") for col in new_cols]
    if post:
        if "Year" in df.columns:
            df = df[df.Year.apply(lambda x: type(to_int(x)) == int)].reset_index(inplace=False).drop(columns=["index"])
        elif "Misc_Result" in df.columns:
            # keep row only if W/L/T, not something else (missed game)
            df = df[df.Misc_Result.apply(lambda x: (len(x) > 1 and x[:2] in ["W ", "L ", "T "]))].reset_index(inplace=False).drop(columns=["index"])
    return df


import pandas as pd

from .config import RSRC_DIR

COLS = ["Account", "Value"]


def build_is():
    DATA_DIR = RSRC_DIR / "income_statement"

    # Income
    df_inc = pd.read_csv(DATA_DIR / "income.csv")
    df_inc = pd.concat(
        [
            pd.DataFrame([["Income", inc := df_inc.Value.sum()]], columns=COLS),
            df_inc,
        ]
    )

    # Living Expenses
    df_liv = pd.read_csv(DATA_DIR / "living_expenses.csv")
    df_liv["Value"] = df_liv.Value.map(lambda val: -val if val > 0 else val)
    df_liv = pd.concat(
        [
            pd.DataFrame(
                [["Living Expenses", liv_exp := df_liv.Value.sum()]], columns=COLS
            ),
            df_liv,
        ]
    )

    # Income before Interest and Tithe
    ibit = inc + liv_exp

    # Interest Expenses
    df_int = pd.read_csv(DATA_DIR / "interest_expenses.csv")
    df_int["Value"] = df_int.Value.map(lambda val: -val if val > 0 else val)
    df_int = pd.concat([df_int, pd.DataFrame([["Tithe", ibit * -0.1]], columns=COLS)])
    df_int = pd.concat(
        [
            pd.DataFrame(
                [["Living Expenses", int_exp := df_int.Value.sum()]], columns=COLS
            ),
            df_int,
        ]
    )

    # Other Gain & Loss
    df_oth = pd.read_csv(DATA_DIR / "other_gnl.csv")
    df_oth = pd.concat(
        [
            pd.DataFrame(
                [["Living Expenses", oth_gnl := df_oth.Value.sum()]], columns=COLS
            ),
            df_oth,
        ]
    )

    # Net Income
    net_inc = ibit + int_exp + oth_gnl

    # Build Income Statement
    df_is = pd.concat(
        [
            df_inc,
            df_liv,
            df_int,
            df_oth,
            pd.DataFrame([["Net Income", net_inc]], columns=COLS),
        ],
    )
    df_is["Value"] = df_is.Value.map(lambda val: int(val * 1e4))
    return df_is


def build_bs():
    DATA_DIR = RSRC_DIR / "balance_sheet"

    # Net Cash

    # Riskless Assets

    # Risky Assets

    # Real Estate

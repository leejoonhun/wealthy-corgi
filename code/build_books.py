import pandas as pd
import yaml

from config import RSRC_DIR
from utils import get_gold_price

COLS = ["Account", "Value"]


def build_is():
    DATA_DIR = RSRC_DIR / "income_statement"

    # Income
    with open(DATA_DIR / "income.yml") as f:
        df_inc = pd.DataFrame(yaml.safe_load(f).items(), columns=COLS)
        df_inc[COLS[0]] = df_inc[COLS[0]].map(lambda acct: f"  {acct}")
    df_inc = pd.concat(
        [
            pd.DataFrame([["Income", inc := df_inc[COLS[-1]].sum()]], columns=COLS),
            df_inc,
        ],
    )

    # Living Expenses
    with open(DATA_DIR / "living_expenses.yml") as f:
        df_liv_exp = pd.DataFrame(yaml.safe_load(f).items(), columns=COLS)
        df_liv_exp[COLS[0]] = df_liv_exp[COLS[0]].map(lambda acct: f"  {acct}")
        df_liv_exp[COLS[-1]] = df_liv_exp[COLS[-1]].map(lambda val: -abs(val))
    df_liv_exp = pd.concat(
        [
            pd.DataFrame(
                [["Living Expenses", liv_exp := df_liv_exp[COLS[-1]].sum()]],
                columns=COLS,
            ),
            df_liv_exp,
        ],
    )

    # Income before Interest and Tithe
    ibit = inc + liv_exp

    # Interest Expenses
    with open(DATA_DIR / "interest_expenses.yml") as f:
        df_int_exp = pd.DataFrame(yaml.safe_load(f).items(), columns=COLS)
        df_int_exp[COLS[0]] = df_int_exp[COLS[0]].map(lambda acct: f"  {acct}")
        df_int_exp[COLS[-1]] = df_int_exp[COLS[-1]].map(lambda val: -abs(val))
    df_int_exp = pd.concat(
        [df_int_exp, pd.DataFrame([["Tithe", ibit * -0.1]], columns=COLS)]
    )
    df_int_exp = pd.concat(
        [
            pd.DataFrame(
                [["Living Expenses", int_exp := df_int_exp[COLS[-1]].sum()]],
                columns=COLS,
            ),
            df_int_exp,
        ],
    )

    # Other Gain & Loss
    with open(DATA_DIR / "other_gnl.yml") as f:
        df_oth_gnl = pd.DataFrame(yaml.safe_load(f).items(), columns=COLS)
        df_oth_gnl[COLS[0]] = df_oth_gnl[COLS[0]].map(lambda acct: f"  {acct}")
    df_oth_gnl = pd.concat(
        [
            pd.DataFrame(
                [["Living Expenses", oth_gnl := df_oth_gnl[COLS[-1]].sum()]],
                columns=COLS,
            ),
            df_oth_gnl,
        ],
    )

    # Net Income
    net_inc = ibit + int_exp + oth_gnl

    # Build Income Statement
    df_is = pd.concat(
        [
            df_inc,
            df_liv_exp,
            df_int_exp,
            df_oth_gnl,
            pd.DataFrame([["Net Income", net_inc]], columns=COLS),
        ],
        ignore_index=True,
    )
    df_is[COLS[-1]] = df_is[COLS[-1]].map(lambda val: int(val * 1e4))
    return df_is


def build_bs(include_dets: bool = False):
    DATA_DIR = RSRC_DIR / "balance_sheet"

    # Net Cash
    ## Deposits and Reserves
    with open(DATA_DIR / "cash.yml") as f:
        df_cash = pd.DataFrame(yaml.safe_load(f).items(), columns=COLS)
        df_cash[COLS[0]] = df_cash[COLS[0]].map(lambda acct: f"  {acct}")
        df_cash[COLS[-1]] = df_cash[COLS[-1]].map(lambda val: val * 1e4)

    depo, resv = df_cash[COLS[-1]]

    ## Current Liabilities
    with open(DATA_DIR / "current_liabilities.yml") as f:
        df_liab_dets = pd.DataFrame(yaml.safe_load(f).items(), columns=COLS)
        df_cash[COLS[0]] = df_cash[COLS[0]].map(lambda acct: f"    {acct}")
        df_liab_dets[COLS[-1]] = df_liab_dets[COLS[-1]].map(lambda val: -abs(val) * 1e4)
    df_liab_dets = pd.concat(
        [
            df_cur_liab := pd.DataFrame(
                [["  Current Liabilities", cur_liab := df_liab_dets[COLS[-1]].sum()]],
                columns=COLS,
            ),
            df_liab_dets,
        ]
    )

    df_net_cash = pd.concat(
        [
            pd.DataFrame(
                [["Net Cash", net_cash := depo + resv + cur_liab]], columns=COLS
            ),
            df_cash,
            df_liab_dets if include_dets else df_cur_liab,
        ]
    )

    # Riskless Assets
    ## Installments
    with open(DATA_DIR / "installments.yml") as f:
        df_inst_dets = pd.DataFrame(yaml.safe_load(f).items(), columns=COLS)
        df_inst_dets[COLS[0]] = df_inst_dets[COLS[0]].map(lambda acct: f"    {acct}")
        df_inst_dets[COLS[-1]] = df_inst_dets[COLS[-1]].map(lambda val: int(val * 1e4))
    df_inst_dets = pd.concat(
        [
            df_inst := pd.DataFrame(
                [["  Installments", inst := df_inst_dets[COLS[-1]].sum()]],
                columns=COLS,
            ),
            df_inst_dets,
        ]
    )

    ## Gold
    p_gold = get_gold_price()
    with open(DATA_DIR / "gold_spots.yml") as f:
        df_gold_spot = pd.DataFrame(yaml.safe_load(f).items(), columns=COLS)
        df_gold_spot[COLS[0]] = df_gold_spot[COLS[0]].map(lambda acct: f"    {acct}")
        df_gold_spot[COLS[-1]] = df_gold_spot[COLS[-1]].map(lambda val: val * p_gold)

    with open(DATA_DIR / "gold_tradables.yml") as f:
        df_gold_trad = pd.DataFrame(yaml.safe_load(f).items(), columns=COLS)
        df_gold_trad[COLS[0]] = df_gold_trad[COLS[0]].map(lambda acct: f"    {acct}")
        # TODO: import IAU and IAUM price to adjust
        df_gold_trad[COLS[-1]] = df_gold_trad[COLS[-1]].map(lambda val: val * p_gold)

    df_gold_dets = pd.concat([df_gold_spot, df_gold_trad])
    df_gold_dets = pd.concat(
        [
            df_gold := pd.DataFrame(
                [["  Gold", gold := df_gold_dets[COLS[-1]].sum()]],
                columns=COLS,
            ),
            df_gold_dets,
        ]
    )

    ## Bonds
    with open(DATA_DIR / "bonds.yml") as f:
        df_bond_dets = pd.DataFrame(yaml.safe_load(f).items(), columns=COLS)
        df_bond_dets[COLS[0]] = df_bond_dets[COLS[0]].map(lambda acct: f"    {acct}")
        df_bond_dets[COLS[-1]] = df_bond_dets[COLS[-1]].map(lambda val: int(val * 1e4))
    df_bond_dets = pd.concat(
        [
            df_bond := pd.DataFrame(
                [["  Bonds", bond := df_bond_dets[COLS[-1]].sum()]],
                columns=COLS,
            ),
            df_bond_dets,
        ]
    )

    df_less = pd.concat(
        [
            pd.DataFrame(
                [["Riskless Assets", less := inst + gold + bond]], columns=COLS
            ),
            df_inst_dets if include_dets else df_inst,
            df_gold_dets if include_dets else df_gold,
            df_bond_dets if include_dets else df_bond,
        ]
    )

    # Risky Assets
    ## Stocks
    with open(DATA_DIR / "stocks.yml") as f:
        data_stok = yaml.safe_load(f)
        df_ko_stok_dets = pd.DataFrame(data_stok["Korean"].items(), columns=COLS)
        df_us_stok_dets = pd.DataFrame(data_stok["American"].items(), columns=COLS)
        df_eu_stock_dets = pd.DataFrame(data_stok["European"].items(), columns=COLS)

    ## Mutual Funds
    with open(DATA_DIR / "mutual_funds.yml") as f:  # TODO: daily update
        data_fund = yaml.safe_load(f)
        df_robo_dets = pd.DataFrame(data_fund["Robo-advisors"].items(), columns=COLS)
        df_pef_dets = pd.DataFrame(
            data_fund["Private Equity Funds"].items(), columns=COLS
        )
        df_hf_dets = pd.DataFrame(data_fund["Hedge Funds"].items(), columns=COLS)
        df_robo_dets[COLS[0]] = df_robo_dets[COLS[0]].map(lambda acct: f"    {acct}")
        df_pef_dets[COLS[0]] = df_pef_dets[COLS[0]].map(lambda acct: f"    {acct}")
        df_hf_dets[COLS[0]] = df_hf_dets[COLS[0]].map(lambda acct: f"    {acct}")
    df_robo_dets = pd.concat(
        [
            pd.DataFrame(
                [["  Robo-advisors", robo := df_robo_dets[COLS[-1]].sum()]],
                columns=COLS,
            ),
            df_robo_dets,
        ]
    )
    df_pef_dets = pd.concat(
        [
            pd.DataFrame(
                [["  Private Equity Funds", pef := df_pef_dets[COLS[-1]].sum()]],
                columns=COLS,
            ),
            df_pef_dets,
        ]
    )
    df_hf_dets = pd.concat(
        [
            pd.DataFrame(
                [["  Hedge Funds", hf := df_hf_dets[COLS[-1]].sum()]],
                columns=COLS,
            ),
            df_hf_dets,
        ]
    )

    df_fund_dets = pd.concat([df_robo_dets, df_pef_dets, df_hf_dets])
    df_fund_dets = pd.concat(
        [
            df_fund := pd.DataFrame(
                [["  Mutual Funds", fund := robo + pef + hf]],
                columns=COLS,
            ),
            df_fund_dets,
        ]
    )

    ## Private Equity
    with open(DATA_DIR / "private_equity.yml") as f:
        data_priv = yaml.safe_load(f)
        df_ko_priv_dets = pd.DataFrame(data_priv["Korean"].items(), columns=COLS)
        df_us_priv_dets = pd.DataFrame(data_priv["American"].items(), columns=COLS)
        df_ko_priv_dets[COLS[0]] = df_ko_priv_dets[COLS[0]].map(
            lambda acct: f"    {acct}"
        )
        df_us_priv_dets[COLS[0]] = df_us_priv_dets[COLS[0]].map(
            lambda acct: f"    {acct}"
        )

    ## Cryptocurrencies

    df_risky = pd.concat(
        [
            pd.DataFrame(
                [["Risky Assets", risky := stok + fund + priv + cryp]], columns=COLS
            ),
            df_stok_dets if include_dets else df_stok,
            df_fund_dets if include_dets else df_fund,
            df_priv_dets if include_dets else df_priv,
            df_cryp_dets if include_dets else df_cryp,
        ]
    )

    # Real Estate
    ## Residentials & Commercials
    with open(DATA_DIR / "real_estate.yml") as f:
        data_re = yaml.safe_load(f)
        df_resi_dets = pd.DataFrame(data_re["Residentials"].items(), columns=COLS)
        df_comr_dets = pd.DataFrame(data_re["Commercials"].items(), columns=COLS)
    # TODO: add apt price

    ## Tradables
    with open(DATA_DIR / "real_estate_tradables.yml") as f:
        df_rtrad_dets = pd.DataFrame(yaml.safe_load(f).items(), columns=COLS)

    df_re = pd.concat(
        [
            pd.DataFrame([["  Real Estate", re := resi + comr + trad]], columns=COLS),
            df_resi_dets if include_dets else df_resi,
            df_comr_dets if include_dets else df_comr,
            df_trad_dets if include_dets else df_trad,
        ]
    )

    # Net Assets
    net_ast = net_cash + less + risky + re

    # Build Balance Sheet
    df_bs = pd.concat(
        [
            df_net_cash,
            df_less,
            df_risky,
            df_re,
            pd.DataFrame([["Net Assets", net_ast]], columns=COLS),
        ],
        ignore_index=True,
    )
    df_bs[COLS[-1]] = df_bs[COLS[-1]].astype(int)
    return df_bs

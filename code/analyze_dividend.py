import pandas as pd
import pandas_datareader as pdr


def calc_next_div(ticker):
    df_act = pdr.get_data_yahoo_actions(ticker)
    df_div = df_act[df_act["action"] == "DIVIDEND"]

    last_div = df_div.iloc[0]["value"]
    div_gr_rate = (
        df_div.value.pct_change().map(lambda g: 1 - g).prod()
        ** (365 / (df_div.index[0] - df_div.index[-1]).days)
        - 1
    )
    days_from_last_div = (pd.Timestamp.today() - df_div.index[0]).days
    next_div = last_div * (1 + div_gr_rate) ** days_from_last_div
    return next_div

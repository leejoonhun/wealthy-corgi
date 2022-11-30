from typing import Iterable

import pandas as pd
import pandas_datareader as pdr


def get_df_act(ticker, time_range: Iterable = None):
    if time_range:
        start, end = time_range
        return pdr.get_data_yahoo_actions(ticker, start=start, end=end)
    else:
        return pdr.get_data_yahoo_actions(ticker)


def calc_next_div(df_act):
    df_div = df_act[df_act["action"] == "DIVIDEND"]

    first_div, last_div = df_div.value[-1], df_div.value[0]
    div_gr_rate = (last_div / first_div) ** (
        365 / (df_div.index[0] - df_div.index[-1]).days
    ) - 1
    days_from_last_div = (pd.Timestamp.today() - df_div.index[0]).days

    next_div = last_div * (1 + div_gr_rate) ** days_from_last_div
    return next_div

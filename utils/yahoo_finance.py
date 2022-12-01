import pandas_datareader as pdr
import yaml

from config import RSRC_DIR

with open(RSRC_DIR / "name2ticker.yml", "r") as f:
    name2ticker = yaml.safe_load(f)


def get_us_stock_prices(names: list):
    dfs = {}
    for name in names:
        dfs[name] = pdr.get_data_yahoo(name2ticker[name])
    return dfs

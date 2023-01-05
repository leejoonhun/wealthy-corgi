import pandas_datareader.data as web
import yaml

from config import RSRC_DIR

with open(RSRC_DIR / "name2ticker.yml", "r") as f:
    name2ticker = yaml.safe_load(f)


def get_ko_stock_prices(names: str):
    dfs = {}
    for name in names:
        dfs[name] = web.DataReader(name2ticker[name], "naver")
    return

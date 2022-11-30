import pandas_datareader.data as web
import requests
import yaml

from config import RSRC_DIR

with open(RSRC_DIR / "api_keys.yml", "r") as f:
    API_KEY = yaml.safe_load(f)["Alpha Vantage"]


def get_xr(quote: str, base: str = "KRW"):
    return (
        web.DataReader(f"{quote}/{base}", "av-forex", api_key=API_KEY)
        .loc["Exchange Rate"]
        .values[0]
    )


def get_crypto_price(quote: str):
    return (
        web.DataReader(f"{quote}/KRW", "av-forex", api_key=API_KEY)
        .loc["Exchange Rate"]
        .values[0]
    )


def get_ty(year: int = 10):
    assert year in [2, 5, 10, 30], "Year must be 2, 5, 10, or 30"
    url = f"https://www.alphavantage.co/query?function=TREASURY_YIELD&maturity={year}year&apikey={API_KEY}"
    data = requests.get(url).json()
    return float(data["data"][0]["value"]) / 100


def get_sector_perf():
    return web.get_sector_performance_av(api_key=API_KEY)

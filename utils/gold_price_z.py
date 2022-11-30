import pandas as pd


def get_gold_price():
    url = "http://goldpricez.com/kr/gram"
    data = pd.read_html(url)
    return int(
        data[1]
        .iloc[0, 1]
        .replace("₩", "")
        .replace(",", "")
        .replace(" ", "")
        .replace("KRW", "")
    )

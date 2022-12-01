import pandas as pd

url = "http://goldpricez.com/kr/gram"


def get_gold_price():
    data = pd.read_html(url)
    return int(
        data[1]
        .iloc[0, 1]
        .replace("₩", "")
        .replace(",", "")
        .replace(" ", "")
        .replace("KRW", "")
    )

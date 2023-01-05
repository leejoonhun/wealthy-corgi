import pandas as pd

url = "https://www.neonet.co.kr/novo-rebank/view/offerings/OfferingsList.neo?"


def get_apt_price(req):
    return int(
        pd.read_html(url + req)[0]
        .iloc[0, 1]
        .replace(",", "")
        .replace(" ", "")
        .replace("만원", "0000")
    )

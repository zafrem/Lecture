import requests
import json


def get_altcoin_list():
    api_request = requests.get('https://api.binance.com/api/v3/ticker/price')
    api = json.loads(api_request.content)
    lst = []
    for x in api:
        lst.append(x['symbol'])
    return lst


def get_altcoin_current_price(altcoin):
    api_request = requests.get('https://api.binance.com/api/v3/ticker/price')
    api = json.loads(api_request.content)

    price = 0

    for x in api:
        if x['symbol'] == altcoin:
            price = float(x['price'])
    return price


if __name__ == '__main__':
    print(get_altcoin_list())
    print(get_altcoin_current_price('BTCUSDC'))
import requests
import json


def get_altcoin_data():
    api_request = requests.get('https://api.binance.com/api/v3/ticker/price')
    _api = json.loads(api_request.content)
    return _api


if "__main__" == __name__ :
    api = get_altcoin_data()
    for x in api:
        print(x['symbol'], "${0:.4f}".format(float(x['price'])))

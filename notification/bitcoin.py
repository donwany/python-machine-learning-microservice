import requests
from SECRETS import bit_coin_keys


def bitcoin_price(symbol):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'symbol': symbol
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': bit_coin_keys
    }

    response = requests.get(url, headers=headers, params=parameters)

    data = response.json()

    last_updated = data['data'][symbol]['last_updated']
    price = data['data'][symbol]['quote']['USD']['price']

    return last_updated, price

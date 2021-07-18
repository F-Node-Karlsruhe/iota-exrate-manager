from requests import Session
import json
from .utils import get_comma_separated_values

def coingecko(currencies):

    url = 'https://api.coingecko.com/api/v3/simple/price'

    parameters = {
    'ids':'iota',
    'vs_currencies': get_comma_separated_values(currencies)
    }

    headers = {
    'Accepts': 'application/json'
    }

    session = Session()

    session.headers.update(headers)

    try:

        response = session.get(url, params=parameters)

        return json.loads(response.text)['iota']

    except Exception as e:

        print(e)

    return None





def cmc(currencies, api_key):

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

    parameters = {
    'slug':'iota',
    'convert': get_comma_separated_values(currencies)
    }

    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': api_key,
    }

    session = Session()
    session.headers.update(headers)

    update = {}

    try:
        response = session.get(url, params=parameters)

        data = json.loads(response.text)['data']['1720']['quote']

        for c in currencies:

            update[c] = data[c.upper()]['price']

    except Exception as e:

        print(e)

    return update




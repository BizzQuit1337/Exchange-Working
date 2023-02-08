import hmac, hashlib
from datetime import datetime, timedelta
import requests
import pandas as pd

def signature(endpoint, expires, api_secret):
    query_string = 'GET' + endpoint + str(expires)
    sign = hmac.new(
            api_secret.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256
        ).hexdigest()
    return sign


def signed_request(endpoint,api_key, api_secret):
    base_url = 'https://www.bitmex.com'
    verb = 'GET'
    now = datetime.now()+timedelta(minutes=1)
    expires = int(datetime.timestamp(now))
    s = signature(endpoint, expires, api_secret)
    headers = {'api-expires':str(expires),
         'api-key':api_key,
         'api-signature':s}
    url = base_url + endpoint
    response = requests.get(url, headers=headers)
    return response.json()

def get_current_price(symbol):
    payload={'symbol':symbol, 'reverse':True}
    response = requests.get('https://www.bitmex.com/api/v1/trade', params=payload)
    r = response.json()
    return r[0]['price']


def get_bitmex_wallet(api_key, api_secret):
    endpoint = '/api/v1/user/margin?currency=all'
    r = signed_request(endpoint,api_key, api_secret)
    return r
    
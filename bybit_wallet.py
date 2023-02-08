import requests, hmac, hashlib, time
from urllib.parse import quote_plus

def bybit_signature(segreta_bybit, params):
    #timestamp = int(time.time() * 10 ** 3)
    param_str = ''
    for key in sorted(params.keys()):
        v = params[key]
        if isinstance(params[key], bool):
            if params[key]:
                v = 'true'
            else :
                v = 'false'
        param_str += key + '=' + v + '&'
    param_str = param_str[:-1]
    hash = hmac.new(segreta_bybit.encode("utf-8"), param_str.encode("utf-8"), hashlib.sha256)
    signature = hash.hexdigest()
    sign_real = {
        "sign": signature
    }
    param_str = quote_plus(param_str, safe="=&")
    full_param_str = f"{param_str}&sign={sign_real['sign']}"
    return full_param_str

def get_bybit_current_price(symbol):
    BASE_URL = 'https://api.bybit.com'
    enpoint = '/v2/public/tickers'
    params = {'symbol':symbol}
    url = BASE_URL + enpoint
    response = requests.get(url, params=params)
    r = response.json()
    return float(r['result'][0]['last_price'])

def signed_request(chiave_bybit, segreta_bybit, endpoint):
    BASE_URL = 'https://api.bybit.com'
    enpoint = endpoint
    timestamp = int(time.time() * 10 ** 3)
    params={'api_key':chiave_bybit,
                'timestamp': str(timestamp),
                'recv_window': '5000'}
    full_param_str = bybit_signature(segreta_bybit, params)
    url = BASE_URL + enpoint + '?' + full_param_str
    response = requests.get(url)
    r = response.json()
    return r
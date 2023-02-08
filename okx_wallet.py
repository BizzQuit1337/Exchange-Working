import requests, base64, hmac
import pandas as pd
from datetime import datetime

def okx_get_header(endpoint, api_key, api_secret, api_pass):
    body = {}
    current_time = current_time_okx()
    header = {
        'CONTENT_TYPE':'application/json',
        'OK-ACCESS-KEY':api_key,
        'OK-ACCESS-SIGN':okx_signature(current_time, endpoint, body, api_secret),
        'OK-ACCESS-TIMESTAMP':current_time,
        'OK-ACCESS-PASSPHRASE':api_pass
    }
    return header

def okx_signature(timestamp, request_path, body, api_secret):
    if str(body) == '{}' or str(body) == 'None':
        body = ''
    message = str(timestamp) + 'GET' + request_path + str(body)
    mac = hmac.new(bytes(api_secret, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
    d = mac.digest()
    return base64.b64encode(d)

def current_time_okx():
    now = datetime.utcnow()
    t = now.isoformat("T", "milliseconds")
    return t + "Z"

def get_okx_trading_wallet(api_key, api_secret, api_pass):
    ## Trading wallet
    url = '/api/v5/account/balance'
    header = okx_get_header(url, api_key, api_secret, api_pass)
    response = requests.get('http://www.okex.com' + url, headers=header)
    r = response.json()
    return r

def get_okx_funding_wallet(api_key, api_secret, api_pass):
    url = '/api/v5/asset/balances'
    header = okx_get_header(url, api_key, api_secret, api_pass)
    response = requests.get('http://www.okex.com' + url, headers=header)
    r = response.json()
    w = pd.DataFrame(columns=['Qty', 'USD Value'])
    return r

def okx_send_unsigned_request(url_path, payload={}):
    BASE_URL = 'https://www.okx.com'
    url = BASE_URL + url_path
    response = requests.get(url)
    return response.json()

def get_okx_current_price(base, quote):
    res = okx_send_unsigned_request("/api/v5/market/ticker?instId=" + base+'-'+quote, payload={})
    return float(res['data'][0]['last'])

def trying():
    url = '/api/v5/finance/staking-defi/orders-active'
    header = okx_get_header(url, 'b31868f6-5da1-4632-807a-5c11461fb885', 'DBE05EDEF38A320C9DBE64CD91BFE651', 'qju2wgy6dkqRZM7qyt')
    response = requests.get('http://www.okex.com' + url, headers=header)
    r = response.json()
    w = pd.DataFrame(columns=['Qty', 'USD Value'])
    return response

def get_positions(api_key, api_secret, api_pass):
    url = '/api/v5/account/positions'
    header = okx_get_header(url, api_key, api_secret, api_pass)
    response = requests.get('http://www.okex.com' + url, headers=header)
    r = response.json()
    return r

def get_contract(api_key, api_secret, api_pass, instType):
    url = '/api/v5/public/instruments?instType='+instType
    header = okx_get_header(url, api_key, api_secret, api_pass)
    response = requests.get('http://www.okex.com' + url, headers=header)
    r = response.json()
    return r

def get_earn(api_key, api_secret, api_pass):
    url = '/api/v5/finance/staking-defi/orders-active'
    header = okx_get_header(url, api_key, api_secret, api_pass)
    response = requests.get('http://www.okex.com' + url, headers=header)
    r = response.json()
    return r





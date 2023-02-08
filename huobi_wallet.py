import requests, hmac, config, hashlib, base64
from urllib.parse import urlencode
from datetime import datetime
import pandas as pd
import numpy as np

def get_huobi_current_price(base, quote):
    symbol = base+quote
    endpoint = '/market/detail/merged'
    base_uri = 'api.huobi.pro'
    method = 'GET'
    url = 'https://' + base_uri + endpoint + '?symbol=' + symbol.lower()
    response = requests.request(method, url)
    r = response.json()
    pr = (r['tick']['bid'][0] + r['tick']['ask'][0])/2
    return pr

def huobi_send_signed_request(chiave_huobi, segreta_huobi, endpoint, method, base_uri):
    timestamp = str(datetime.utcnow().isoformat())[0:19]
    params = urlencode({'AccessKeyId': chiave_huobi,
                        'SignatureMethod': 'HmacSHA256',
                        'SignatureVersion': '2',
                        'Timestamp': timestamp
                       })
    pre_signed_text = method + '\n' + base_uri + '\n' + endpoint + '\n' + params
    hash_code = hmac.new(segreta_huobi.encode(), pre_signed_text.encode(), hashlib.sha256).digest()
    signature = urlencode({'Signature': base64.b64encode(hash_code).decode()})
    url = 'https://' + base_uri + endpoint + '?' + params + '&' + signature
    response = requests.request(method, url)
    return response.json()

def huobi_send_signed_request_usdM(chiave_huobi, segreta_huobi, endpoint, method, base_uri):
    timestamp = str(datetime.utcnow().isoformat())[0:19]
    params = urlencode({'AccessKeyId': chiave_huobi,
                        'SignatureMethod': 'HmacSHA256',
                        'SignatureVersion': '2',
                        'Timestamp': timestamp,
                       })
    pre_signed_text = method + '\n' + base_uri + '\n' + endpoint + '\n' + params
    hash_code = hmac.new(segreta_huobi.encode(), pre_signed_text.encode(), hashlib.sha256).digest()
    signature = urlencode({'Signature': base64.b64encode(hash_code).decode()})
    url = 'https://' + base_uri + endpoint + '?' + params + '&' + signature
    response = requests.request(method, url, json={'valuation_asset': 'USDT'})
    return response.json()

def get_contract_size(symbol):
    endpoint = '/swap-api/v1/swap_contract_info?contract_code='+symbol
    base_uri = 'api.hbdm.com'
    method = 'GET'
    url = 'https://' + base_uri + endpoint
    response = requests.request(method, url)
    resp = response.json()
    r = resp['data'][0]['contract_size']
    return r
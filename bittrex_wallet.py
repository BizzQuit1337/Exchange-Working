import time, hashlib, hmac, requests
import pandas as pd

def bittrex_wallet_request(api_key, api_secret):
    url = "https://api.bittrex.com/v3/balances"
    method = "GET"
    nonce = int(time.time() * 1000)
    params = {}
    content = ""
    contenthash = hashlib.sha512(content.encode()).hexdigest()
    paramsstring = ""
    message = str(nonce) + url + paramsstring + method + contenthash
    signature = hmac.new(api_secret.encode(),
                         message.encode(), hashlib.sha512).hexdigest()
    headers = {
        'Accept': 'application/json',
        'Api-Key': api_key,
        'Api-Signature': signature,
        'Api-Timestamp': str(nonce),
        'Api-Content-Hash': contenthash
    }
    response = requests.request(method, url, headers=headers, params=params)
    r = response.json()
    return r

def get_price(symbol:str):
    url = 'https://api.bittrex.com/v3/markets/' + symbol + '/ticker'
    response = requests.get(url)
    r = response.json()
    return r

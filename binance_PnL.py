import requests
from urllib.parse import urlencode
import pandas as pd
import time
import hmac
import hashlib
import numpy as np

def binance_send_signed_request(BASE_URL, http_method, url_path, chiave_binance, segreta_binance, payload={}):
    query_string = urlencode(payload, True)
    if query_string:
        query_string = "{}&timestamp={}".format(query_string, binance_get_timestamp())
    else:
        query_string = "timestamp={}".format(binance_get_timestamp())

    url = (
        BASE_URL + url_path + "?" + query_string + "&signature=" + binance_hashing(query_string, segreta_binance)
    )
    params = {"url": url, "params": {}}
    response = binance_dispatch_request(http_method, chiave_binance)(**params)
    return response.json()

def binance_dispatch_request(http_method, chiave_binance=''):
    session = requests.Session()
    session.headers.update(
        {"Content-Type": "application/json;charset=utf-8", "X-MBX-APIKEY": chiave_binance}
    )
    return {
        "GET": session.get,
        "DELETE": session.delete,
        "PUT": session.put,
        "POST": session.post,
    }.get(http_method, "GET")

def get_binance_current_price(base, quote):
    BASE_URL = "https://api.binance.com"
    pr = binance_send_public_request(BASE_URL, '/api/v3/ticker/price', payload={'symbol':base+quote})['price']
    return float(pr)

def binance_get_timestamp():
    return int(time.time() * 1000)

def binance_hashing(query_string, segreta_binance):
    return hmac.new(
        segreta_binance.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256
    ).hexdigest()

def binance_send_public_request(BASE_URL, url_path, payload={}):
    query_string = urlencode(payload, True)
    url = BASE_URL + url_path
    if query_string:
        url = url + "?" + query_string
    response = binance_dispatch_request("GET")(url=url)
    return response.json()



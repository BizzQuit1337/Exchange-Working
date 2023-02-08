import time, hashlib, hmac, requests
import config

def signature(method, url, chiave_gate, segreta_gate, query_string=None, payload_string=None):
    key = chiave_gate
    secret = segreta_gate
    t = time.time()
    m = hashlib.sha512()
    m.update((payload_string or "").encode('utf-8'))
    hashed_payload = m.hexdigest()
    s = '%s\n%s\n%s\n%s\n%s' % (method, url, query_string or "", hashed_payload, t)
    sign = hmac.new(secret.encode('utf-8'), s.encode('utf-8'), hashlib.sha512).hexdigest()
    return {'KEY': key, 'Timestamp': str(t), 'SIGN': sign}
    

def send_signed_request(url, chiave_gate, segreta_gate):
    host = "https://api.gateio.ws"
    prefix = "/api/v4"
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    query_param = ''
    # for `gen_sign` implementation, refer to section `Authentication` above
    sign_headers = signature('GET', prefix + url, chiave_gate, segreta_gate, query_param)
    headers.update(sign_headers)
    r = requests.request('GET', host + prefix + url, headers=headers)
    return r.json()

def current_price(base, quote):
    host = "https://api.gateio.ws"
    prefix = "/api/v4"
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    url = '/spot/tickers'
    query_param = 'currency_pair=' + base + '_' + quote
    r = requests.request('GET', host + prefix + url + "?" + query_param, headers=headers)
    return float(r.json()[0]['last'])
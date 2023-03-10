import requests
import hmac
import hashlib
import base64
import time
from uuid import uuid1
import urllib.parse
import sys
from typing import List

def rest_kraken_wallet(chiave_kraken, segreta_kraken):
    resp = kraken_request('/0/private/Balance', {
        "nonce": str(int(1000 * time.time()))
    }, chiave_kraken, segreta_kraken)
    r = resp.json()
    return r

def kraken_request(uri_path, data, api_key, api_sec):
    api_url = "https://api.kraken.com"
    headers = {}
    headers['API-Key'] = api_key
    # get_kraken_signature() as defined in the 'Authentication' section
    headers['API-Sign'] = get_kraken_signature(uri_path, data, api_sec)
    req = requests.post((api_url + uri_path), headers=headers, data=data)
    return req

def get_kraken_signature(urlpath, data, secret):
    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()
    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()

def get_kraken_current_price(base, quote):
    symbol = base + '/' + quote
    resp = requests.get('https://api.kraken.com/0/public/Ticker?pair=' + symbol)
    r = resp.json()
    sy = list(r['result'].keys())[0]
    pr = float(r['result'][sy]['c'][0])
    return pr

try:
    from exceptions import KrakenExceptions
except ModuleNotFoundError:
    print('USING LOCAL MODULE')
    sys.path.append('/Users/benjamin/repositories/Trading/python-kraken-sdk')
    from exceptions import KrakenExceptions

class KrakenErrorHandler():
    '''Class used to raise an Error or return the response'''

    def __init__(self):
        self.__kexceptions = KrakenExceptions()

    def __get_exception(self, msg):
        return self.__kexceptions.get_exception(msg)

    def check(self, data: dict) -> dict:
        '''Check if the error message is a known Kraken error response
            than raise a custom exception or return the data containing the 'error'
        '''
        if len(data.get('error', [])) == 0 and 'result' in data: return data['result']

        exception = self.__get_exception(data['error'])
        if exception: raise exception(data)
        return data

    def check_send_status(self, data: dict) -> dict:
        '''Used for futures REST responses'''
        if 'sendStatus' in data and 'status' in data['sendStatus']:
            exception = self.__get_exception(data['sendStatus']['status'])
            if exception: raise exception(data)
            return data
        return data

    def check_batch_status(self, data: List[dict]) -> dict:
        '''Used for futures REST batch order responses'''
        if 'batchStatus' in data:
            batch_status = data['batchStatus']
            for status in batch_status:
                if 'status' in status:
                    exception = self.__get_exception(status['status'])
                    if exception: raise exception(data)
        return data

class KrakenBaseFuturesAPI():
    ''' Base class for all Spot clients

        Handles un/signed requests and returns exception handled results

        ====== P A R A M E T E R S ======
        key: str, defualt: ''
            Spot API public key
        secret: str, default: ''
            Spot API secret key
        url: str, default: 'https://api.kraken.com'
            optional url
        sandbox: bool, default: False
            not used so far
    '''

    URL = 'https://api.kraken.com'
    API_V = '/0'


    def __init__(self, key: str='', secret: str='', url: str='', sandbox: bool=False):
        if sandbox: raise ValueError('Sandbox not availabel for Kraken Spot trading.')
        if url != '': self.url = url
        else: self.url = self.URL
        
        self.__nonce = 0
        self.__key = key
        self.__secret = secret
        self.__err_handler = KrakenErrorHandler()
        self.__session = requests.Session()
        self.__session.headers.update({'User-Agent': 'python-kraken-sdk'})

    def _request(self,
        method: str,
        uri: str,
        timeout: int=10,
        auth: bool=True,
        params: dict=None,
        do_json: bool=False,
        return_raw: bool=False
    ) -> dict:
        if params is None: params = {}
        method = method.upper()
        data_json = ''
        if method in ['GET', 'DELETE']:
            if params:
                strl = []
                for key in sorted(params): strl.append(f'{key}={params[key]}')
                data_json += '&'.join(strl)
                uri += f'?{data_json}'.replace(' ', '%20')

        headers = { }
        if auth:
            if not self.__key or self.__key == '' or not self.__secret or self.__secret == '': raise ValueError('Missing credentials.')
            self.__nonce = (self.__nonce + 1) % 1
            params['nonce'] = str(int(time.time() * 1000)) + str(self.__nonce).zfill(4)
            headers.update({
                'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
                'API-Key': self.__key,
                'API-Sign': self.get_kraken_signature(f'{self.API_V}{uri}', params)
            })

        url = f'{self.url}{self.API_V}{uri}'
        if method in ['GET', 'DELETE']:
            return self.__check_response_data(
                self.__session.request(method=method, url=url, headers=headers, timeout=timeout),
                return_raw
            )
        if do_json:
            return self.__check_response_data(
                self.__session.request(method=method, url=url, headers=headers, json=params, timeout=timeout),
                return_raw
            )
        return self.__check_response_data(
            self.__session.request(method=method, url=url, headers=headers, data=params, timeout=timeout),
            return_raw
        )

    def get_kraken_signature(self, urlpath: str, data: dict) -> str:
        '''Returns the signed data'''
        return base64.b64encode(
            hmac.new(
                base64.b64decode(self.__secret),
                urlpath.encode() + hashlib.sha256((str(data['nonce']) + urllib.parse.urlencode(data)).encode()).digest(),
                hashlib.sha512
            ).digest()
        ).decode()

    def __check_response_data(self, response_data, return_raw: bool=False) -> dict:
        '''checkes the response, handles the error and returns the data'''
        if response_data.status_code in [ '200', 200 ]:
            if return_raw: return response_data
            try: data = response_data.json()
            except ValueError as exc: raise ValueError(response_data.content) from exc
            else:
                if 'error' in data: return self.__err_handler.check(data)
                return data
        raise Exception(f'{response_data.status_code} - {response_data.text}')

    @property
    def return_unique_id(self) -> str:
        '''Returns a unique id str'''
        return ''.join(str(uuid1()).split('-'))

    def _to_str_list(self, value) -> str:
        '''Converts a list to a comme separated str'''
        if isinstance(value, str): return value
        if isinstance(value, list): return ','.join(value)
        raise ValueError('a must be type of str or list of strings')

class KrakenBaseFuturesAPI():
    ''' Base class for all Futures clients

        Handles un/signed requests and returns exception handled results

        ====== P A R A M E T E R S ======
        key: str, defualt: ''
            Futures API public key
        secret: str, default: ''
            Futures API secret key
        url: str, default: 'https://futures.kraken.com'
            optional url
        sandbox: bool, default: False
            if set to true the url will be 'https://demo-futures.kraken.com'

        ====== N O T E S ======
        If the sandbox environment is chosen, the keys must be generated here:
            https://demo-futures.kraken.com/settings/api
    '''

    URL = 'https://futures.kraken.com'
    SANDBOX_URL = 'https://demo-futures.kraken.com'

    def __init__(self, key: str='', secret: str='', url: str='', sandbox: bool=False):

        self.sandbox = sandbox
        if url: self.url = url
        elif self.sandbox: self.url = self.SANDBOX_URL
        else: self.url = self.URL

        self.__key = key
        self.__secret = secret
        self.__nonce = 0

        self.__err_handler = KrakenErrorHandler()
        self.__session = requests.Session()
        self.__session.headers.update({'User-Agent': 'python-kraken-sdk'})

    def _request(self,
        method: str,
        uri: str,
        timeout: int=10,
        auth: bool=True,
        post_params: dict=None,
        query_params: dict=None,
        return_raw: bool=False
    ) -> dict:
        method = method.upper()

        post_string: str = ''
        if post_params is not None:
            strl: List[str] = []
            for key in sorted(post_params): strl.append(f'{key}={post_params[key]}')
            post_string = '&'.join(strl)
        else: post_params = {}

        query_string: str = ''
        if query_params is not None:
            strl: List[str] = []
            for key in sorted(query_params): strl.append(f'{key}={query_params[key]}')
            query_string = '&'.join(strl).replace(' ', '%20')
        else: query_params = {}

        headers = { }
        if auth:
            if not self.__key or self.__key == '' or not self.__secret or self.__secret == '': raise ValueError('Missing credentials')
            self.__nonce = (self.__nonce + 1) % 1
            nonce = str(int(time.time() * 1000)) + str(self.__nonce).zfill(4)
            headers.update({
                'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
                'Nonce': nonce,
                'APIKey': self.__key,
                'Authent': self.get_kraken_futures_signature(uri, query_string + post_string, nonce)
            })

        if method in ['GET', 'DELETE']:
            return self.__check_response_data(
                self.__session.request(
                    method=method,
                    url=f'{self.url}{uri}' if query_string == '' else f'{self.url}{uri}?{query_string}',
                    headers=headers,
                    timeout=timeout
                ),
                return_raw
            )
        if method == 'PUT':
            return self.__check_response_data(
                self.__session.request(
                method=method,
                url=f'{self.url}{uri}',
                params=str.encode(query_string),
                headers=headers,
                timeout=timeout
                ),
                return_raw
            )

        return self.__check_response_data(
            self.__session.request(
                method=method,
                url=f'{self.url}{uri}?{post_string}',
                data=str.encode(post_string),
                headers=headers,
                timeout=timeout
            ), return_raw
        )

    def get_kraken_futures_signature(self, endpoint: str, data: str, nonce: str) -> str:
        '''
            Returns the signed data/message
            reference: https://github.com/CryptoFacilities/REST-v3-Python/blob/ee89b9b324335d5246e2f3da6b52485eb8391d50/cfRestApiV3.py#L295-L296
        '''
        if endpoint.startswith('/derivatives'): endpoint = endpoint[len('/derivatives'):]
        sha256_hash = hashlib.sha256()
        sha256_hash.update((data + nonce + endpoint).encode('utf8'))
        return base64.b64encode(
            hmac.new(
                base64.b64decode(self.__secret),
                sha256_hash.digest(),
                hashlib.sha512
            ).digest()
        )

    def __check_response_data(self, response_data, return_raw: bool=False) -> dict:
        if response_data.status_code in [ '200', 200 ]:
            if return_raw: return response_data
            try: data = response_data.json()
            except ValueError as exc: raise ValueError(response_data.content) from exc
            else:
                if 'error' in data: return self.__err_handler.check(data)
                if 'sendStatus' in data: return self.__err_handler.check_send_status(data)
                if 'batchStatus' in data: return self.__err_handler.check_batch_status(data)
                return data
        else: raise Exception(f'{response_data.status_code} - {response_data.text}')

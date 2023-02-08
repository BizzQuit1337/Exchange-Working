import kraken_wallet as kw
import shared_Functions as sf
import config

def get_usdt_pos(api_key, api_secret, exchange):
    client = kw.KrakenBaseFuturesAPI(api_key, api_secret, "https://futures.kraken.com")
    usdtPos = client._request('GET', '/derivatives/api/v3/openpositions')
    tickers = client._request('GET', '/derivatives/api/v3/tickers')

    assets = []

    for i in usdtPos['openPositions']:
        if i['size'] != 0:
            for j in tickers['tickers']:
                if i['symbol'] == j['symbol']:
                    coin_price = float(j['markPrice'])
                    coin = j['pair'].split(':')[0]
            position = float(i['size'])
            USD_Value = position*coin_price
            if i['side'] == 'short':
                asset = {
                        'Coin':coin,
                        'Contract':i['symbol'],
                        'QTY':round(position*-1,6),
                        'USD Value':round((USD_Value*-1),2),
                        'Exchange':exchange,
                        'Account':'USDT-M',
                        'Leverage':1,
                        'Mark Price':1,
                        'Liq Price':1,
                        'Liq Risk %':1
                    }
                assets.append(asset)
            else:
                asset = {
                        'Coin':coin,
                        'Contract':i['symbol'],
                        'QTY':round(position*-1,6),
                        'USD Value':round((USD_Value*-1),2),
                        'Exchange':exchange,
                        'Account':'USDT-M',
                        'Leverage':1,
                        'Mark Price':1,
                        'Liq Price':1,
                        'Liq Risk %':1
                    }
                assets.append(asset)

    return assets



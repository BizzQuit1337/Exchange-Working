import bitmex_wallet as bw
import shared_Functions as sf
import config

def get_usdt_pos(api_key, api_secret, exchange):
    usdtPos = bw.signed_request('/api/v1/position', api_key, api_secret)

    assets = []

    posAbsolute = 0
    posUSDValue = 0

    for i in usdtPos:
        if float(i['homeNotional']) != 0:
            position = float(i['homeNotional'])
            USD_Value = position*float(i['markPrice'])
            try:
                asset = {
                        'Coin':i['underlying'],
                        'Contract':i['symbol'],
                        'QTY':round(position,6),
                        'USD Value':round(USD_Value,2),
                        'Exchange':exchange,
                        'Account':i['currency'],
                        'Leverage':i['leverage'],
                        'Mark Price':round(float(i['markPrice']),2),
                        'Liq Price':round(float(i['liquidationPrice']),2),
                        'Liq Risk %':(float(i['liquidationPrice'])-float(i['markPrice']))/float(i['markPrice'])
                    }
                assets.append(asset)

                posAbsolute += abs(USD_Value)
                posUSDValue += USD_Value
            except:
                asset = {
                        'Coin':i['underlying'],
                        'Contract':i['symbol'],
                        'QTY':round(position,6),
                        'USD Value':round(USD_Value,2),
                        'Exchange':exchange,
                        'Account':i['currency'],
                        'Leverage':i['leverage'],
                        'Mark Price':round(float(i['markPrice']),2),
                        'Liq Price':'Null',
                        'Liq Risk %':'Null'
                    }
                assets.append(asset)

                posAbsolute += abs(USD_Value)
                posUSDValue += USD_Value

    bitmex = {'assets':assets, 'posValue':[posAbsolute, posUSDValue, 'USDT']}

    return bitmex

def leverValues(api_key, api_secret, exchange):
    leverValue = []

    for i in [get_usdt_pos(api_key, api_secret,exchange)]:
        lever = {'absolute':i['posValue'][0], 'USD Value':i['posValue'][1], 'Account':i['posValue'][2], 'exchange':'Bitmex'}
        leverValue.append(lever)

    return leverValue
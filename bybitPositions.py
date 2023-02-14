import bybit_wallet as bw
import shared_Functions as sf

def get_usdt_pos(api_key, api_secret, exchange):
    usdtPos = bw.signed_request(api_key, api_secret, '/private/linear/position/list')

    assets = []

    posAbsolute = 0
    posUSDValue = 0

    for i in usdtPos['result']:
        if i['data']['size'] != 0:
            currentPrice = bw.get_bybit_current_price(i['data']['symbol'])
            position = float(i['data']['size'])
            USD_Value = position*float(currentPrice)
            try:
                if i['data']['side'] == 'Sell':
                    asset = {
                            'Coin':i['data']['symbol'][:-4],
                            'Contract':i['data']['symbol'],
                            'QTY':round(position*-1,6),
                            'USD Value':round(USD_Value*-1,2),
                            'Exchange':exchange,
                            'Account':'USDT-M',
                            'Leverage':i['data']['leverage'],
                            'Mark Price':round(currentPrice,2),
                            'Liq Price':round(float(i['data']['liq_price']),2),
                            'Liq Risk %':(float(i['data']['liq_price'])-float(currentPrice))/float(currentPrice)
                        }
                    assets.append(asset)

                    posAbsolute += abs(USD_Value)
                    posUSDValue += USD_Value*-1
                else:
                    asset = {
                            'Coin':i['data']['symbol'][:-4],
                            'Contract':i['data']['symbol'],
                            'QTY':round(position,6),
                            'USD Value':round(USD_Value,2),
                            'Exchange':exchange,
                            'Account':'USDT-M',
                            'Leverage':i['data']['leverage'],
                            'Mark Price':round(currentPrice,2),
                            'Liq Price':round(float(i['data']['liq_price']),2),
                            'Liq Risk %':(float(currentPrice)-float(i['data']['liq_price']))/float(currentPrice)
                        }
                    assets.append(asset)

                    posAbsolute += abs(USD_Value)
                    posUSDValue += USD_Value
            except:
                if i['data']['side'] == 'Sell':
                    asset = {
                            'Coin':i['data']['symbol'][:-4],
                            'Contract':i['data']['symbol'],
                            'QTY':round(position*-1,6),
                            'USD Value':round(USD_Value*-1,2),
                            'Exchange':exchange,
                            'Account':'USDT-M',
                            'Leverage':i['data']['leverage'],
                            'Mark Price':round(currentPrice,2),
                            'Liq Price':'Null',
                            'Liq Risk %':'Null'
                        }
                    assets.append(asset)

                    posAbsolute += abs(USD_Value)
                    posUSDValue += USD_Value*-1
                else:
                    asset = {
                            'Coin':i['data']['symbol'][:-4],
                            'Contract':i['data']['symbol'],
                            'QTY':round(position,6),
                            'USD Value':round(USD_Value,2),
                            'Exchange':exchange,
                            'Account':'USDT-M',
                            'Leverage':i['data']['leverage'],
                            'Mark Price':round(currentPrice,2),
                            'Liq Price':'Null',
                            'Liq Risk %':'Null'
                        }
                    assets.append(asset)

                    posAbsolute += abs(USD_Value)
                    posUSDValue += USD_Value

    bybit = {'assets':assets, 'posValue':[posAbsolute, posUSDValue, 'Trading']}

    return bybit

def leverValues(api_key, api_secret, exchange):
    leverValue = []

    for i in [get_usdt_pos(api_key, api_secret, exchange)]:
        lever = {'absolute':i['posValue'][0], 'USD Value':i['posValue'][1], 'Account':'futures', 'exchange':'Bybit'}
        leverValue.append(lever)

    return leverValue

    
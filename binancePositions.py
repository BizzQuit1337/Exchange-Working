import binance_PnL as bp
import shared_Functions as sf
import config 

def get_usdt_pos(api_key, api_secret, exchange):
    usdtPos = bp.binance_send_signed_request("https://fapi.binance.com", 'GET', '/fapi/v2/positionRisk', api_key, api_secret, payload={})

    assets = []

    posAbsolute = 0
    posUSDValue = 0

    for i in usdtPos:
        if float(i['positionAmt']) != 0.0:
            position = float(i['positionAmt'])
            USD_Value = position*float(i['markPrice'])
            try:
                if i['pos'][:-(len(i['pos'])-1)] == '-':
                    liq_risk = (float(i['liquidationPrice'])-float(i['markPrice']))/float(i['markPrice'])
                else:
                    liq_risk = (float(i['markPrice'])-float(i['liquidationPrice']))/float(i['markPrice'])
                if i['symbol'][:4] == '1000':  
                    asset = {
                            'Coin':i['symbol'][4:-4],
                            'Contract':i['symbol'],
                            'QTY':round(position*1000,6),
                            'USD Value':round(USD_Value,2),
                            'Exchange':exchange,
                            'Account':'USDT-M',
                            'Leverage':i['leverage'],
                            'Mark Price':round(float(i['markPrice']),2),
                            'Liq Price':round(float(i['liquidationPrice']),2),
                            'Liq Risk %':liq_risk
                        }
                    assets.append(asset)

                    posAbsolute += abs(USD_Value)
                    posUSDValue += USD_Value
                else:
                    asset = {
                            'Coin':i['symbol'].split('_')[0][:-4],
                            'Contract':i['symbol'],
                            'QTY':round(position,6),
                            'USD Value':round(USD_Value,2),
                            'Exchange':exchange,
                            'Account':'USDT-M',
                            'Leverage':i['leverage'],
                            'Mark Price':round(float(i['markPrice']),2),
                            'Liq Price':round(float(i['liquidationPrice']),2),
                            'Liq Risk %':(float(i['liquidationPrice'])-float(i['markPrice']))/float(i['markPrice'])
                        }
                    assets.append(asset)

                    posAbsolute += abs(USD_Value)
                    posUSDValue += USD_Value
            except:
                if i['symbol'][:4] == '1000':  
                    asset = {
                            'Coin':i['symbol'][4:-4],
                            'Contract':i['symbol'],
                            'QTY':round(position*1000,6),
                            'USD Value':round(USD_Value,2),
                            'Exchange':exchange,
                            'Account':'USDT-M',
                            'Leverage':i['leverage'],
                            'Mark Price':round(float(i['markPrice']),2),
                            'Liq Price':'Null',
                            'Liq Risk %':'Null'
                        }
                    assets.append(asset)

                    posAbsolute += abs(USD_Value)
                    posUSDValue += USD_Value
                else:
                    asset = {
                            'Coin':i['symbol'].split('_')[0][:-4],
                            'Contract':i['symbol'],
                            'QTY':round(position,6),
                            'USD Value':round(USD_Value,2),
                            'Exchange':exchange,
                            'Account':'USDT-M',
                            'Leverage':i['leverage'],
                            'Mark Price':round(float(i['markPrice']),2),
                            'Liq Price':'Null',
                            'Liq Risk %':'Null'
                        }
                    assets.append(asset)

                    posAbsolute += abs(USD_Value)
                    posUSDValue += USD_Value

    binance = {'assets':assets, 'posValue':[posAbsolute, posUSDValue, 'USDT-M']}

    return binance

def get_coinM_pos(api_key, api_secret, exchange):
    coinMPos = bp.binance_send_signed_request("https://dapi.binance.com", 'GET', '/dapi/v1/positionRisk', api_key, api_secret, payload={})

    assets = []

    posAbsolute = 0
    posUSDValue = 0

    for i in coinMPos:
        if float(i['positionAmt']) != 0:
            position = float(i['notionalValue'])
            USD_Value = position*float(i['markPrice'])
            try:
                if i['pos'][:-(len(i['pos'])-1)] == '-':
                    asset = {
                            'Coin':i['symbol'].split('_')[0][:-3],
                            'Contract':i['symbol'],
                            'QTY':round(position,6),
                            'USD Value':round(USD_Value,2),
                            'Exchange':exchange,
                            'Account':'COIN-M',
                            'Leverage':i['leverage'],
                            'Mark Price':round(float(i['markPrice']),2),
                            'Liq Price':round(float(i['liquidationPrice']),2),
                            'Liq Risk %':(float(i['liquidationPrice'])-float(i['markPrice']))/float(i['markPrice'])
                        }
                else:
                    asset = {
                            'Coin':i['symbol'].split('_')[0][:-3],
                            'Contract':i['symbol'],
                            'QTY':round(position,6),
                            'USD Value':round(USD_Value,2),
                            'Exchange':exchange,
                            'Account':'COIN-M',
                            'Leverage':i['leverage'],
                            'Mark Price':round(float(i['markPrice']),2),
                            'Liq Price':round(float(i['liquidationPrice']),2),
                            'Liq Risk %':(float(i['markPrice'])-float(i['liquidationPrice']))/float(i['markPrice'])
                        }
                assets.append(asset)

                posAbsolute += abs(USD_Value)
                posUSDValue += USD_Value
            except:
                asset = {
                        'Coin':i['symbol'].split('_')[0][:-3],
                        'Contract':i['symbol'],
                        'QTY':round(position,6),
                        'USD Value':round(USD_Value,2),
                        'Exchange':exchange,
                        'Account':'COIN-M',
                        'Leverage':i['leverage'],
                        'Mark Price':round(float(i['markPrice']),2),
                        'Liq Price':'Null',
                        'Liq Risk %':'Null'
                    }
                assets.append(asset)

                posAbsolute += abs(USD_Value)
                posUSDValue += USD_Value

    binance = {'assets':assets, 'posValue':[posAbsolute, posUSDValue, 'Coin-M']}

    return binance

def all_positions(api_key, api_secret, exchange):
    assets = []

    for i in [get_coinM_pos(api_key, api_secret, exchange), get_usdt_pos(api_key, api_secret, exchange)]:
        assets.append(i['assets'])

    return assets

def leverValues(api_key, api_secret, exchange):
    leverValue = []

    for i in [get_coinM_pos(api_key, api_secret, exchange), get_usdt_pos(api_key, api_secret, exchange)]:
        lever = {'absolute':i['posValue'][0], 'USD Value':i['posValue'][1], 'Account':i['posValue'][2], 'exchange':'Binance'}
        leverValue.append(lever)

    return leverValue

get_coinM_pos(config.binance_key, config.binance_secret, 'blah blah')
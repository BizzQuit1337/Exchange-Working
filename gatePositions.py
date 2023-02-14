import Gate_wallet as gw
import shared_Functions as sf
import config_ocar

def get_usdt_pos(api_key, api_secret, exchange):
    usdtPos = gw.send_signed_request('/futures/usdt/positions', api_key, api_secret)

    assets = []

    posAbsolute = 0
    posUSDValue = 0

    for i in usdtPos:
        if i['size'] != 0:
            position = float(i['value'])/float(i['mark_price'])
            USD_Value = float(i['value'])
            try:
                asset = {
                        'Coin':'When can see output add coin name here',
                        'Contract':'When can see output add contract name here',
                        'QTY':round(position,6),
                        'USD Value':round(USD_Value,2),
                        'Exchange':exchange,
                        'Account':'USDT-M',
                        'Leverage':i["leverage"],
                        'Mark Price':round(float(i["mark_price"]),2),
                        'Liq Price':round(float(i["liq_price"]),2),
                        'Liq Risk %':(float(i["liq_price"])-float(i["mark_price"]))/float(i["mark_price"])
                    }
                assets.append(asset)

                posAbsolute += abs(USD_Value)
                posUSDValue += USD_Value
            except:
                asset = {
                        'Coin':'When can see output add coin name here',
                        'Contract':'When can see output add contract name here',
                        'QTY':round(position,6),
                        'USD Value':round(USD_Value,2),
                        'Exchange':exchange,
                        'Account':'USDT-M',
                        'Leverage':i["leverage"],
                        'Mark Price':round(float(i["mark_price"]),2),
                        'Liq Price':'Null',
                        'Liq Risk %':'Null'
                    }
                assets.append(asset)

                posAbsolute += abs(USD_Value)
                posUSDValue += USD_Value

    Gate = {'assets':assets, 'posValue':[posAbsolute, posUSDValue, 'Future']}

    return Gate

def leverValues(api_key, api_secret, exchange):
    leverValue = []

    for i in [get_usdt_pos(api_key, api_secret, exchange)]:
        lever = {'absolute':i['posValue'][0], 'USD Value':i['posValue'][1], 'Account':i['posValue'][2], 'exchange':'Gate'}
        leverValue.append(lever)

    return leverValue

get_usdt_pos(config_ocar.gate_key, config_ocar.gate_secret, 'gatesteing')
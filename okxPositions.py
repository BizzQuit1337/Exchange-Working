import config_ocar
import okx_wallet as ow
import shared_Functions as sf

def get_usdt_pos(api_key, api_secret, api_pass, exchange):
    usdtPos = ow.get_positions(api_key, api_secret, api_pass)
    contract_size = ow.get_contract(api_key, api_secret, api_pass, 'SWAP')

    assets = []

    posAbsolute = 0
    posUSDValue = 0

    for i in usdtPos['data']:
        for j in contract_size['data']:
            if j['instId'] == i['instId']:
                position = float(j['ctVal'])*float(i['pos'])
                USD_Value = position*float(i['markPx'])
                liq = i['liqPx']
                try:
                    
                    if i['pos'][:-(len(i['pos'])-1)] == '-':
                        asset = {
                            'Coin':i['instId'].split('-')[0],
                            'Contract':i['instId'],
                            'QTY':round(position,6),
                            'USD Value':round(USD_Value,2),
                            'Exchange':exchange,
                            'Account':'USDT-M',
                            'Leverage':i['lever'],
                            'Mark Price':round(float(i['markPx']),2),
                            'Liq Price':round(float(i['liqPx']),2),
                            'Liq Risk %':(float(liq)-float(i['markPx']))/float(i['markPx'])
                        }
                    else:
                        asset = {
                            'Coin':i['instId'].split('-')[0],
                            'Contract':i['instId'],
                            'QTY':round(position,6),
                            'USD Value':round(USD_Value,2),
                            'Exchange':exchange,
                            'Account':'USDT-M',
                            'Leverage':i['lever'],
                            'Mark Price':round(float(i['markPx']),2),
                            'Liq Price':round(float(i['liqPx']),2),
                            'Liq Risk %':(float(i['markPx'])-float(liq))/float(i['markPx'])
                        }
                    assets.append(asset)

                    posAbsolute += abs(USD_Value)
                    posUSDValue += USD_Value
                except:
                    asset = {
                        'Coin':i['instId'].split('-')[0],
                        'Contract':i['instId'],
                        'QTY':round(position,6),
                        'USD Value':round(USD_Value,2),
                        'Exchange':exchange,
                        'Account':'USDT-M',
                        'Leverage':i['lever'],
                        'Mark Price':round(float(i['markPx']),2),
                        'Liq Price':'Null',
                        'Liq Risk %':'Null'
                    }
                    assets.append(asset)

                    posAbsolute += abs(USD_Value)
                    posUSDValue += USD_Value

    OKX = {'assets':assets, 'posValue':[posAbsolute, posUSDValue, 'Earn']}

    return OKX

def leverValues(api_key, api_secret, api_pass, exchange):
    leverValue = []

    for i in [get_usdt_pos(api_key, api_secret, api_pass, exchange)]:
        lever = {'absolute':i['posValue'][0], 'USD Value':i['posValue'][1], 'Account':'USDT-M', 'exchange':'OKX'}
        leverValue.append(lever)

    return leverValue

#get_usdt_pos(config_ocar.okx_key, config_ocar.okx_secret, config_ocar.okx_passphrase, 'shit stain')
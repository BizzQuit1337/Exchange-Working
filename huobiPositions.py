import config
import huobi_wallet as hw
import shared_Functions as sf

def get_usdtM_pos(api_key, api_secret, exchange):
    usdtMPos = hw.huobi_send_signed_request(api_key, api_secret, '/linear-swap-api/v1/swap_cross_position_info', 'POST', 'api.hbdm.com')
    get_cont_size=hw.huobi_send_signed_request(api_key, api_secret, '/linear-swap-api/v1/swap_contract_info', 'GET', 'api.hbdm.com')
    liq_price = hw.huobi_send_signed_request(api_key, api_secret, '/linear-swap-api/v1/swap_cross_account_info', 'POST', 'api.hbdm.com')
    
    assets = []    

    posAbsolute = 0
    posUSDValue = 0  

    for i in usdtMPos['data']:
        for j in get_cont_size['data']:
            for k in liq_price['data'][0]['contract_detail']:
                if j['symbol'] == i['symbol'] and i['symbol'] == k['symbol']:
                    position = j['contract_size']*i['volume']
                    USD_Value = position*i['last_price']
                    try:
                        liq = float(k['liquidation_price'])
                        if i['direction'] == 'sell':
                            asset = {
                                'Coin':i['symbol'],
                                'Contract':i['contract_code'],
                                'QTY':round(position*-1,6),
                                'USD Value':round(USD_Value*-1,2),
                                'Exchange':exchange,
                                'Account':'USDT-M',
                                'Leverage':i['lever_rate'],
                                'Mark Price':round(float(i['last_price']),2),
                                'Liq Price':round(liq,2),
                                'Liq Risk %':(liq-float(i['last_price']))/float(i['last_price'])
                            }
                            assets.append(asset)

                            posAbsolute += abs(USD_Value)
                            posUSDValue += (USD_Value*-1)
                        else:
                            asset = {
                                'Coin':i['symbol'],
                                'Contract':i['contract_code'],
                                'QTY':round(position,6),
                                'USD Value':round(USD_Value,2),
                                'Exchange':exchange,
                                'Account':'USDT-M',
                                'Leverage':i['lever_rate'],
                                'Mark Price':round(float(i['last_price']),2),
                                'Liq Price':round(liq,2),
                                'Liq Risk %':(float(i['last_price'])-liq)/float(i['last_price'])
                            }
                            assets.append(asset)

                            posAbsolute += abs(USD_Value)
                            posUSDValue += USD_Value
                    except:
                        liq = 'Null'
                        if i['direction'] == 'sell':
                            asset = {
                                'Coin':i['symbol'],
                                'Contract':i['contract_code'],
                                'QTY':round(position*-1,6),
                                'USD Value':round(USD_Value*-1,2),
                                'Exchange':exchange,
                                'Account':'USDT-M',
                                'Leverage':i['lever_rate'],
                                'Mark Price':round(float(i['last_price']),2),
                                'Liq Price':liq,
                                'Liq Risk %':liq
                            }
                            assets.append(asset)

                            posAbsolute += abs(USD_Value)
                            posUSDValue += (USD_Value*-1)
                        else:
                            asset = {
                                'Coin':i['symbol'],
                                'Contract':i['contract_code'],
                                'QTY':round(position,6),
                                'USD Value':round(USD_Value,2),
                                'Exchange':exchange,
                                'Account':'USDT-M',
                                'Leverage':i['lever_rate'],
                                'Mark Price':round(float(i['last_price']),2),
                                'Liq Price':liq,
                                'Liq Risk %':liq
                            }
                            assets.append(asset)

                            posAbsolute += abs(USD_Value)
                            posUSDValue += USD_Value
    huobi = {'assets':assets, 'posValue':[posAbsolute, posUSDValue, 'USDT-M']}

    return huobi

def get_coinM_pos(api_key, api_secret, exchange):
    coinMPos = hw.huobi_send_signed_request(api_key, api_secret, '/swap-api/v1/swap_position_info', 'POST', 'api.hbdm.com')
    liqPrice = hw.huobi_send_signed_request(api_key, api_secret, '/swap-api/v1/swap_account_info', 'POST', 'api.hbdm.com')

    assets = []     

    posAbsolute = 0
    posUSDValue = 0 

    for i in coinMPos['data']:
        if i['volume'] != 0:
            for j in liqPrice['data']:
                if j['symbol'] == i['symbol']:
                    cont_Size = hw.get_contract_size(i['contract_code'])
                    USD_Value = float(i['volume'])*float(cont_Size)
                    position = USD_Value/float(i['last_price'])
                    try:
                        liq = float(j['liquidation_price'])
                        if i['direction'] == 'sell':
                            asset = {
                                    'Coin':i['symbol'],
                                    'Contract':i['contract_code'],
                                    'QTY':round(position*-1,6),
                                    'USD Value':round(USD_Value*-1,2),
                                    'Exchange':exchange,
                                    'Account':'Coin-M',
                                    'Leverage':i['lever_rate'],
                                    'Mark Price':round(float(i['last_price']),2),
                                    'Liq Price':round(liq,2), #Need to find this or an alternative
                                    'Liq Risk %':(liq-float(i['last_price']))/float(i['last_price'])
                                }
                            assets.append(asset)

                            posAbsolute += abs(USD_Value)
                            posUSDValue += (USD_Value*-1)
                        else:
                            asset = {
                                    'Coin':i['symbol'],
                                    'Contract':i['contract_code'],
                                    'QTY':round(position,6),
                                    'USD Value':round(USD_Value,2),
                                    'Exchange':exchange,
                                    'Account':'Coin-M',
                                    'Leverage':i['lever_rate'],
                                    'Mark Price':round(float(i['last_price']),2),
                                    'Liq Price':round(liq,2), #Need to find this or an alternative
                                    'Liq Risk %':(float(i['last_price'])-liq)/float(i['last_price'])
                                }
                            assets.append(asset)

                            posAbsolute += abs(USD_Value)
                            posUSDValue += USD_Value
                    except:
                        liq = 'Null'
                        if i['direction'] == 'sell':
                            asset = {
                                    'Coin':i['symbol'],
                                    'Contract':i['contract_code'],
                                    'QTY':round(position*-1,6),
                                    'USD Value':round(USD_Value*-1,2),
                                    'Exchange':exchange,
                                    'Account':'Coin-M',
                                    'Leverage':i['lever_rate'],
                                    'Mark Price':round(float(i['last_price']),2),
                                    'Liq Price':liq, #Need to find this or an alternative
                                    'Liq Risk %':liq
                                }
                            assets.append(asset)

                            posAbsolute += abs(USD_Value)
                            posUSDValue += (USD_Value*-1)
                        else:
                            asset = {
                                    'Coin':i['symbol'],
                                    'Contract':i['contract_code'],
                                    'QTY':round(position,6),
                                    'USD Value':round(USD_Value,2),
                                    'Exchange':exchange,
                                    'Account':'Coin-M',
                                    'Leverage':i['lever_rate'],
                                    'Mark Price':round(float(i['last_price']),2),
                                    'Liq Price':liq, #Need to find this or an alternative
                                    'Liq Risk %':liq
                                }
                            assets.append(asset)

                            posAbsolute += abs(USD_Value)
                            posUSDValue += USD_Value

    huobi = {'assets':assets, 'posValue':[posAbsolute, posUSDValue, 'Coin-M']}

    return huobi

def get_all_positions(api_key, api_secret, exchange):
    assets = []

    for i in [get_coinM_pos(api_key, api_secret, exchange), get_usdtM_pos(api_key, api_secret, exchange)]:
        assets.append(i['assets'])

    return assets

def leverValues(api_key, api_secret, exchange):
    leverValue = []

    for i in [get_coinM_pos(api_key, api_secret, exchange), get_usdtM_pos(api_key, api_secret, exchange)]:
        lever = {'absolute':i['posValue'][0], 'USD Value':i['posValue'][1], 'Account':i['posValue'][2], 'exchange':'Huobi'}
        leverValue.append(lever)

    return leverValue

#x = leverValues(config.huobi_key, config.huobi_secret, 'jj')

#sf.displayDataFrame(x, True)
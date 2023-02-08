import bybit_wallet as bw
import pandas as pd
import shared_Functions as sf
import config

def bybit_futures_wallet(api_key, api_secret, exchange):
    futures_wallet = bw.signed_request(api_key, api_secret, '/v2/private/wallet/balance')
    total_balance = 0
    assets = []

    #sf.saveExcel('bybit_fut.xlsx', futures_wallet['result'])

    for i in futures_wallet['result']:
        if futures_wallet['result'][i]['equity'] != 0:
            coin_price = 1
            total = float(futures_wallet['result'][i]['equity'])*float(coin_price)
            total_balance += futures_wallet['result'][i]['equity']
            if round(total,2) != 0:
                coin_asset = {
                    'Coin':i, 
                    'Contract':i,
                    'QTY':round(float(futures_wallet['result'][i]['equity']),6), 
                    'USD Value':round(total,2),
                    'Exchange':exchange, 
                    'Account':'USD-M'}
                assets.append(coin_asset)

    return [total_balance, 'Future', assets]

def bybit_spot_wallet(api_key, api_secret, exchange):
    spot_wallet = bw.signed_request(api_key, api_secret, '/spot/v3/private/account')
    total_balance =0 
    assets = []

    for i in range(0, len(spot_wallet['result']['balances'])):
        try:
            coin_price = bw.get_bybit_current_price(symbol=(spot_wallet['result']['balances'][i]['coin']+'USDT'))
            total = float(spot_wallet['result']['balances'][i]['total'])*float(coin_price)
            total_balance += total
            if round(total,2) != 0:
                coin_asset = {
                    'Coin':spot_wallet['result']['balances'][i]['coin'], 
                    'Contract':spot_wallet['result']['balances'][i]['coin'],
                    'QTY':round(float(spot_wallet['result']['balances'][i]['total']),6), 
                    'USD Value':round(total,2),
                    'Exchange':exchange, 
                    'Account':'SPOT'}
                assets.append(coin_asset)
        except:
            total_balance += float(spot_wallet['result']['balances'][i]['total'])
            if round(float(spot_wallet['result']['balances'][i]['total']),2) != 0:
                coin_asset = {
                    'Coin':spot_wallet['result']['balances'][i]['coin'], 
                    'Contract':spot_wallet['result']['balances'][i]['coin'],
                    'QTY':round(float(spot_wallet['result']['balances'][i]['total']),6), 
                    'USD Value':round(float(spot_wallet['result']['balances'][i]['total']),2),
                    'Exchange':exchange, 
                    'Account':'SPOT'}
                assets.append(coin_asset)

    
    return [total_balance, 'SPOT', assets]

def total_bybit_balance(api_key, api_secret, exchange, breakdown):
    total_balance = 0
    assets = []
    coin_assets = []
    balance_break = []
    for i in [bybit_spot_wallet(api_key, api_secret, exchange), bybit_futures_wallet(api_key, api_secret, exchange)]:
        assets.append(i)
        total_balance += i[0]
        coin_assets.append(i[2])
        balance = {'Exchange':exchange, i[1]:i[0]}
        balance_break.append(balance)

    
    #print(coin_assets)
    #print(pd.DataFrame(assets), '\nTotal Bybit balance: ', total_balance)

    if breakdown:
        sf.displayDataFrame(balance_break, True, False)
        print('Total',f"{total_balance:,.2f}")
    bybit = {'total':total_balance, 'coins':coin_assets}

    return bybit

def bybitLeaverage(api_key, api_secret, exchange):
    leverageValue = []

    for i in [bybit_futures_wallet(api_key, api_secret, exchange)]:
        lever = {'USD Value':i[0], 'Account':'futures', 'exchange':'Bybit'}
        leverageValue.append(lever)

    return leverageValue

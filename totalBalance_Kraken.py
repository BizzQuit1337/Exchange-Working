import kraken_wallet as kw
import config_ocar, re
import pandas as pd
import shared_Functions as sf

exchange = 'Kraken'

def kraken_spot_wallet_balance(api_key, api_secret):
    spot_wallet = kw.rest_kraken_wallet(api_key, api_secret)
    total_balance = 0
    assets = []

    for i in spot_wallet['result']:
        try:
            if len(i.split('.')) == 2:
                i == i.split('.')[0]
            coin_price = kw.get_kraken_current_price(i, 'USD')
            #print(i, spot_wallet['result'][i], 'cp')
            total = float(spot_wallet['result'][i])*float(coin_price)
            total_balance += total
            if round(total,2) != 0:
                asset = {
                    'Coin':i, 
                    'Contract':i,
                    'QTY':round(float(spot_wallet['result'][i]),2), 
                    'USD Value':round(total,2),
                    'Exchange':exchange, 
                    'Account':'SPOT'}
                assets.append(asset)
        except:
            #print(i, spot_wallet['result'][i])
            total_balance += float(spot_wallet['result'][i])
            if round(float(spot_wallet['result'][i]),2) != 0:
                if len(i.split('.')) > 1:
                    x = i.split('.')
                    pattern = r'[0-9]'
                    y = re.sub(pattern, '', x[0])
                    try:
                        coin_price = kw.get_kraken_current_price(y, 'USD')
                        total = float(spot_wallet['result'][i])*float(coin_price)
                        asset = {
                        'Coin':y, 
                        'Contract':i,
                        'QTY':round(float(spot_wallet['result'][i]),2), 
                        'USD Value':total,
                        'Exchange':exchange, 
                        'Account':'SPOT'}
                        assets.append(asset)
                    except:
                        asset = {
                            'Coin':y, 
                            'Contract':i,
                            'QTY':round(float(spot_wallet['result'][i]),2), 
                            'USD Value':round(float(spot_wallet['result'][i]),2),
                            'Exchange':exchange, 
                            'Account':'SPOT'}
                        assets.append(asset)
                else:
                    asset = {
                        'Coin':i, 
                        'Contract':i,
                        'QTY':round(float(spot_wallet['result'][i]),2), 
                        'USD Value':round(float(spot_wallet['result'][i]),2),
                        'Exchange':exchange, 
                        'Account':'SPOT'}
                    assets.append(asset)

    return [total_balance, 'SPOT', assets]

def kraken_futures_wallet_balance(api_key, api_secret):
    client = kw.KrakenBaseFuturesAPI(api_key, api_secret, "https://futures.kraken.com")
    futures_wallet = client._request('get', '/derivatives/api/v3/accounts')
    flex_wallet = futures_wallet['accounts']['flex']
    total_balance = 0
    assets = []

    #sf.saveExcel('futures Kraken.xlsx', futures_wallet['accounts'])

    ###

    for i in futures_wallet['accounts']['cash']['balances']:
        if futures_wallet['accounts']['cash']['balances'][i] != 0:
            try:
                coin_price = kw.get_kraken_current_price(i, 'USD')
                total = float(futures_wallet['accounts']['cash']['balances'][i])*float(coin_price)
                #print(i, total)
                total_balance += total
                if round(total,2) != 0:
                    asset = {
                        'Coin':i, 
                        'Contract':i,
                        'QTY':round(float(futures_wallet['accounts']['cash']['balances'][i]),2), 
                        'USD Value':round(total,2),
                        'Exchange':exchange, 
                        'Account':'SPOT'}
                    assets.append(asset)
            except:
                total = float(futures_wallet['accounts']['cash']['balances'][i])
                #print(i, futures_wallet['accounts']['cash']['balances'][i])
                total_balance += total
                if round(float(futures_wallet['accounts']['cash']['balances'][i]),2) != 0:
                    asset = {
                        'Coin':i, 
                        'Contract':i, 
                        'QTY':round(float(futures_wallet['accounts']['cash']['balances'][i]),2), 
                        'USD Value':round(float(futures_wallet['accounts']['cash']['balances'][i]),2),
                        'Exchange':exchange, 
                        'Account':'SPOT'}
                    assets.append(asset)

    for i in flex_wallet['currencies']:
        QTY = flex_wallet['currencies'][i]['quantity']
        try:
            coin_price = coin_price = kw.get_kraken_current_price(i, 'USD')
        except:
            coin_price = 1
        total_balance += float(QTY)*float(coin_price)
        asset = {
            'Coin':i, 
            'Contract':i,
            'QTY':round(QTY,6), 
            'USD Value':round(float(QTY)*float(coin_price),2),
            'Exchange':exchange, 
            'Account':'SPOT'}
        assets.append(asset)

        
    return [total_balance, 'USD-Margin', assets]

def total_kraken_balance(api_key_f, api_secret_f, api_key_s, api_secret_s, breakdown):
    total_balance = 0
    assets = []
    coin_assets = []
    balance_break = []

    for i in [kraken_futures_wallet_balance(api_key_f, api_secret_f), kraken_spot_wallet_balance(api_key_s, api_secret_s)]:
        total_balance += i[0]
        asset = {'Account':i[1], 'USD_Value':i[0]}
        assets.append(asset)
        coin_assets.append(i[2])
        balance = {'Exchange':'Kraken', i[1]:i[0]}
        balance_break.append(balance)

    #print(pd.DataFrame(assets), '\nTotal kraken balance: ', total_balance)

    if breakdown:
        newList = sf.singleDict(balance_break)
        sf.displayDataFrame(newList, True, False)
        print('Total',f"{total_balance:,.2f}")
    kraken = {'total':total_balance, 'coins':coin_assets}

    return kraken

#print(total_kraken_balance(config.kraken_futures_key, config.kraken_futures_secret, config.kraken_key, config.kraken_secret, False))
#kraken_futures_wallet_balance(config.kraken_futures_key, config.kraken_futures_secret)
#total_kraken_balance(config.kraken_futures_key, config.kraken_futures_secret, config.kraken_key, config.kraken_secret, False)

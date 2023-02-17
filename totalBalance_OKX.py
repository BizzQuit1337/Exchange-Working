import okx_wallet as ow
import config_ocar
import pandas as pd
import shared_Functions as sf

def okx_funding_wallet_balance(api_key, api_secret, api_pass, exchange):
    funding_wallet = ow.get_okx_funding_wallet(api_key, api_secret, api_pass)
    total_balance = 0
    assets = []
    
    for i in range(0, len(funding_wallet['data'])):
        try:
            coin_price = ow.get_okx_current_price(funding_wallet['data'][i]['ccy'], 'USDT')
            total = float(funding_wallet['data'][i]['bal'])*float(coin_price)
            total_balance += total
            if round(total,2) != 0:
                asset = {
                    'Coin':funding_wallet['data'][i]['ccy'], 
                    'Contract':funding_wallet['data'][i]['ccy'],
                    'QTY':round(float(funding_wallet['data'][i]['bal']),6), 
                    'USD Value':round(total,2),
                    'Exchange':exchange, 
                    'Account':'Spot'}
                assets.append(asset)
        except:
            total_balance += funding_wallet['data'][i]['bal']
            if round(float(funding_wallet['data'][i]['bal']),2) != 0:
                asset = {
                    'Coin':funding_wallet['data'][i]['ccy'], 
                    'Contract':funding_wallet['data'][i]['ccy'],
                    'QTY':round(float(funding_wallet['data'][i]['bal']),6), 
                    'USD Value':round(float(funding_wallet['data'][i]['eqUsd']),2),
                    'Exchange':exchange, 
                    'Account':'Spot'}
                assets.append(asset)

    return [total_balance, 'Spot', assets]

def okx_trading_wallet_balance(api_key, api_secret, api_pass, exchange):
    trading_wallet = ow.get_okx_trading_wallet(api_key, api_secret, api_pass)
    total_balance = 0
    assets = []

    #print('trading: ', trading_wallet['data'][0]['details'])

    for i in range(0, len(trading_wallet['data'][0]['details'])):
        total_balance += float(trading_wallet['data'][0]['details'][i]['eqUsd'])
        #print(trading_wallet['data'][0]['details'][i]['ccy'],trading_wallet['data'][0]['details'][i]['eqUsd'])
        if round(float(trading_wallet['data'][0]['details'][i]['eqUsd']),2) != 0:
            asset = {
                'Coin':trading_wallet['data'][0]['details'][i]['ccy'], 
                'Contract':trading_wallet['data'][0]['details'][i]['ccy'],
                'QTY':round(float(trading_wallet['data'][0]['details'][i]['cashBal']),6), 
                'USD Value':round(float(trading_wallet['data'][0]['details'][i]['eqUsd']),2),
                'Exchange':exchange, 
                'Account':'USDT-M'}
            assets.append(asset)

    return [total_balance, 'USDT-M', assets]

def get_earn_balance(api_key, api_secret, api_pass, exchange):
    earn_wallet = ow.get_earn(api_key, api_secret, api_pass)
    total_balance = 0
    assets = []

    for i in earn_wallet['data']:
        qty =float(i['investData'][0]['amt'])
        try:
            coin_price = ow.get_okx_current_price(i['investData'][0]['ccy'], 'USDT')
            usd = qty*float(coin_price)
            asset = {
                    'Coin':i['investData'][0]['ccy'], 
                    'Contract':i['investData'][0]['ccy'],
                    'QTY':round(qty,6), 
                    'USD Value':round(usd, 2),
                    'Exchange':exchange, 
                    'Account':'Earn'}
            assets.append(asset)
            total_balance += usd
        except:
            usd = qty*1
            asset = {
                    'Coin':i['investData'][0]['ccy'], 
                    'Contract':i['investData'][0]['ccy'],
                    'QTY':round(qty,6), 
                    'USD Value':round(usd, 2),
                    'Exchange':exchange, 
                    'Account':'Earn'}
            assets.append(asset)
            total_balance += usd

    return [total_balance, 'Earn', assets]


def okx_wallet_total(api_key, api_secret, api_pass, exchange, breakdown):
    all_asset = []
    total_balance = 0
    coin_assets = []
    balance_break = []

    for i in [okx_trading_wallet_balance(api_key, api_secret, api_pass, exchange), okx_funding_wallet_balance(api_key, api_secret, api_pass, exchange), get_earn_balance(api_key, api_secret, api_pass, exchange)]:
        asset = {'Account':i[1],'USD Value':i[0]}
        all_asset.append(asset)
        total_balance += i[0]
        coin_assets.append(i[2])
        balance = {'Exchange':exchange, i[1]:i[0]}
        balance_break.append(balance)

    if breakdown:
        newList = sf.singleDict(balance_break)
        sf.displayDataFrame(newList, True, False)
        print('Total',f"{total_balance:,.2f}")
    okx = {'total':total_balance, 'coins':coin_assets}

    #print(pd.DataFrame(okx['coins'][2]))
    #print(total_balance)

    return okx

def okxLeaverage(api_key, api_secret, api_pass, exchange):
    leverageValue = []

    for i in [okx_trading_wallet_balance(api_key, api_secret, api_pass, exchange)]:
        for j in i[2]:
            if j['Coin'] == 'USDT':
                lever = {'USD Value':j['USD Value'], 'Account':'USDT-M', 'exchange':'OKX'}
                leverageValue.append(lever)
    return leverageValue

#print(okxLeaverage(config_ocar.okx_key, config_ocar.okx_secret, config_ocar.okx_passphrase, 'll'))

#okx_wallet_total(config_ocar.okx_key, config_ocar.okx_secret, config_ocar.okx_passphrase, 'popadour', False)
#get_earn_balance(config_ocar.okx_key, config_ocar.okx_secret, config_ocar.okx_passphrase, 'popadour')

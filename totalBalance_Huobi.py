import config
import huobi_wallet as hw
import pandas as pd
import requests
import shared_Functions as sf

def huobi_usdM_wallet_balance(api_key, api_secret, exchange):
    huobi_usdM_wallet = hw.huobi_send_signed_request_usdM(api_key, api_secret, '/linear-swap-api/v1/swap_balance_valuation', 'POST', 'api.hbdm.com')
    total_balance = 0                                             
    assets = []

    #print(huobi_usdM_wallet)
    #sf.saveExcel('huobi_btc.xlsx', huobi_usdM_wallet['data'])

    for i in range(0, len(huobi_usdM_wallet['data'])):
        if huobi_usdM_wallet['data'][i]['balance'] != 0:
            total_balance += float(huobi_usdM_wallet['data'][i]['balance'])
            if round(float(huobi_usdM_wallet['data'][i]['balance']),2) != 0:
                asset = {
                    'Coin':huobi_usdM_wallet['data'][i]['valuation_asset'].upper(), 
                    'Contract':huobi_usdM_wallet['data'][i]['valuation_asset'].upper(), 
                    'QTY':round(float(huobi_usdM_wallet['data'][i]['balance']),6), 
                    'USD Value':round(float(huobi_usdM_wallet['data'][i]['balance']),2),
                    'Exchange':exchange, 
                    'Account':'USD-M'}
                assets.append(asset)

    return [total_balance, 'USDT-M', assets]

def huobi_coinM_wallet_balance(api_key, api_secret, exchange):
    coinM_wallet = hw.huobi_send_signed_request(api_key, api_secret, '/swap-api/v1/swap_account_info', 'POST', 'api.hbdm.com')
    total_balance = 0 
    assets = []

    for i in range(0, len(coinM_wallet['data'])):
        if coinM_wallet['data'][i]['margin_balance'] != 0:
            try:
                coin_price = hw.get_huobi_current_price(coinM_wallet['data'][i]['symbol'], 'USDT')
                total = float(coinM_wallet['data'][i]['margin_balance'])*float(coin_price)
                total_balance += total
                if round(total,2) != 0:
                    asset = {
                        'Coin':coinM_wallet['data'][i]['symbol'].upper(), 
                        'Contract':coinM_wallet['data'][i]['symbol'].upper(), 
                        'QTY':round(float(coinM_wallet['data'][i]['margin_balance']),6), 
                        'USD Value':round(total,2),
                        'Exchange':exchange, 
                        'Account':'Coin-M'}
                    assets.append(asset)
            except:
                total_balance += coinM_wallet['data'][i]['margin_balance']
                if round(float(coinM_wallet['data'][i]['margin_balance']),2) != 0:
                    asset = {
                        'Coin':coinM_wallet['data'][i]['symbol'].upper(), 
                        'Contract':coinM_wallet['data'][i]['symbol'].upper(), 
                        'QTY':round(float(coinM_wallet['data'][i]['margin_balance']),6), 
                        'USD Value':round(float(coinM_wallet['data'][i]['margin_balance']),2),
                        'Exchange':exchange, 
                        'Account':'Coin-M'}
                    assets.append(asset)
    
    return [total_balance, 'Coin-M', assets]

def rest_huobi_spot_wallet(chiave_huobi, segreta_huobi, huobi_spot_account_id, exchange):
    endpoint = '/v1/account/accounts/{}/balance'.format(huobi_spot_account_id)
    r = hw.huobi_send_signed_request(chiave_huobi, segreta_huobi, endpoint, 'GET', 'api.huobi.pro')
    total_balance = 0
    assets = []

    for i in r['data']['list']:
        if i['balance'] != '0':
            if 'usd' in i['currency']:
                total_balance += float(i['balance'])
                if round(float(i['balance']),2) != 0:
                    asset = {
                        'Coin':i['currency'].upper(), 
                        'Contract':i['currency'].upper(), 
                        'QTY':round(float(i['balance']),6), 
                        'USD Value':round(float(i['balance']),2),
                        'Exchange':exchange, 
                        'Account':'SPOT'}
                    assets.append(asset)
            else:
                coin_price = hw.get_huobi_current_price(i['currency'], 'usdt')
                total_balance += float(i['balance'])*coin_price
                if round((float(i['balance'])*float(coin_price)),2) != 0:
                    asset = {
                        'Coin':i['currency'].upper(), 
                        'Contract':i['currency'].upper(), 
                        'QTY':round(float(i['balance']),6), 
                        'USD Value':round((float(i['balance'])*float(coin_price)),2),
                        'Exchange':exchange, 
                        'Account':'SPOT'}
                    assets.append(asset)

    return [total_balance, 'SPOT', assets]

def total_huobi_balance(api_key, api_secret, api_id, exchange, breakdown):
    total_balance = 0
    assets = []
    coin_assets = []
    balance_break = []

    for i in [huobi_coinM_wallet_balance(api_key, api_secret, exchange), huobi_usdM_wallet_balance(api_key, api_secret, exchange), rest_huobi_spot_wallet(api_key, api_secret, api_id, exchange)]:
        total_balance += i[0]
        asset = {'Account':i[1], 'USD Value':i[0]}
        assets.append(asset)
        coin_assets.append(i[2])
        balance = {'Exchange':exchange, i[1]:i[0]}
        balance_break.append(balance)

    #print(coin_assets)
    #print(pd.DataFrame(assets), '\nTotal Huobi balance: ', total_balance)

    if breakdown:
        sf.displayDataFrame(balance_break, True, False)
        print('Total',f"{total_balance:,.2f}")
    huobi = {'total':total_balance, 'coins':coin_assets}

    return huobi

def huobiLeaverage(api_key, api_secret, exchange):
    leverageValue = []

    for i in [huobi_usdM_wallet_balance(api_key, api_secret, exchange), huobi_coinM_wallet_balance(api_key, api_secret, exchange)]:
        lever = {'USD Value':i[0], 'Account':i[1], 'exchange':'Huobi'}
        leverageValue.append(lever)

    return leverageValue


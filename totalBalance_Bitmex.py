import bitmex_wallet as bw
import config
import pandas as pd
import shared_Functions as sf

exchange = 'Bitmex'

def bitmex_wallet(api_key, api_secret, breakdown):
    wallet = bw.get_bitmex_wallet(api_key, api_secret)
    total_balance = 0
    total_unrealisedPnL = 0
    assets = []
    coin_assets = []
    balance_break = []

    for i in range(0, len(wallet)):
        if wallet[i] != 0:
            if wallet[i]['currency'].upper() == 'XBT':
                coin_price = bw.get_current_price(wallet[i]['currency'].upper())
                satoshi_convert = float(wallet[i]['walletBalance'])*0.00000001
                total = satoshi_convert*coin_price
                total_balance += total
                if round(total,2) != 0:
                    asset={
                        'Coin':'BTC', 
                        'Contract':'BTC', 
                        'QTY':round(satoshi_convert,6), 
                        'USD Value':round(total,2),
                        'Exchange':exchange, 
                        'Account':'SPOT'}
                    coin_assets.append(asset)
                #print(wallet[i]['unrealisedPnl'])
            elif wallet[i]['currency'] == 'BMEx':
                coin_price = bw.get_current_price(wallet[i]['currency'].upper())
                satoshi_convert = float(wallet[i]['walletBalance'])*0.000001
                total = satoshi_convert*coin_price
                total_balance += satoshi_convert
                total_unrealisedPnL += wallet[i]['unrealisedPnl']
                if round(total,2) != 0:
                    asset={
                        'Coin':'BMEX', 
                        'Contract':'BMEX',
                        'QTY':round(satoshi_convert,6), 
                        'USD Value':round(total,2),
                        'Exchange':exchange, 
                        'Account':'SPOT'}
                    coin_assets.append(asset)

    asset = {'Account':'SPOT', 'USD Value':total_balance}
    pnl = {'Account':'UnrealPnL', 'USD Value': total_unrealisedPnL}
    balance = {'Exchange':'Bitmex', 'SPOT':total_balance}
    balance_break.append(balance)
    assets.append(asset)
    assets.append(pnl)
    #print(pd.DataFrame(coin_assets))
    #sf.saveExcel('bitmex.xlsx', coin_assets)
    #print(pd.DataFrame(assets), '\nTotal Bitmex balance: ', total_balance)

    if breakdown:
        sf.displayDataFrame(balance_break, True, False)
        print('Total',f"{total_balance:,.2f}")
    bitmex = {'total':total_balance, 'coins':coin_assets}
     
    return bitmex

def bitmexLeaverage(api_key, api_secret):
    leverageValue = []

    for i in [bitmex_wallet(api_key, api_secret, False)]:
        lever = {'USD Value':i['total'], 'Account':'USDT', 'exchange':'Bitmex'}
        leverageValue.append(lever)

    return leverageValue
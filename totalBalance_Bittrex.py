import bittrex_wallet as bw
import pandas as pd
import config
import shared_Functions as sf

exchange = 'Bittrex'

def bittrex_balance(api_key, api_secret, breakdown):
    bittrex_wallet = bw.bittrex_wallet_request(api_key, api_secret)
    total_balance = 0
    assets = []
    coin_assets = []

    for i in range(0, len(bittrex_wallet)):
        if bittrex_wallet[i]['currencySymbol'] == 'EUR':
            coin_price = bw.get_price('USD-'+bittrex_wallet[i]['currencySymbol'])
            total = float(bittrex_wallet[i]['total'])/float(coin_price['lastTradeRate'])
            total_balance += total
            asset = {'Account':bittrex_wallet[i]['currencySymbol'], 'USD Value':total}
            assets.append(asset)
            if round(total,2) != 0:
                coin_asset = {
                    'Coin':bittrex_wallet[i]['currencySymbol'], 
                    'Contract':bittrex_wallet[i]['currencySymbol'],
                    'QTY':round(float(bittrex_wallet[i]['total']),6), 
                    'USD Value':round(total,2),'Exchange':exchange, 
                    'Account':'SPOT'}
                coin_assets.append(coin_asset)
        else:
            try:
                coin_price = bw.get_price(bittrex_wallet[i]['currencySymbol']+'-USD')
                #print(coin_price)
                total = float(bittrex_wallet[i]['total'])*float(coin_price)
                total_balance += total 
                asset = {'Account':bittrex_wallet[i]['currencySymbol'], 'USD Value':total}
                assets.append(asset)
                if round(total,2) != 0:
                    coin_asset = {
                        'Coin':bittrex_wallet[i]['currencySymbol'], 
                        'Contract':bittrex_wallet[i]['currencySymbol'],
                        'QTY':round(float(bittrex_wallet[i]['total']),6), 
                        'USD Value':round(total,2),
                        'Exchange':exchange, 
                        'Account':'SPOT'}
                    coin_assets.append(coin_asset)
            except:
                total = float(bittrex_wallet[i]['total'])* 0
                total_balance += total 
                asset = {'Account':bittrex_wallet[i]['currencySymbol'], 'USD Value':total}
                assets.append(asset)
                if round(total,2) != 0:
                    coin_asset = {
                        'Coin':bittrex_wallet[i]['currencySymbol'], 
                        'Contract':bittrex_wallet[i]['currencySymbol'], 
                        'QTY':round(float(bittrex_wallet[i]['total']),6), 
                        'USD Value':round(total,2),
                        'Exchange':exchange, 
                        'Account':'SPOT'}
                    coin_assets.append(coin_asset)

    #print(pd.DataFrame(assets), '\nTotal Bittrex balance: ', total_balance)
    #print(pd.DataFrame(coin_assets))
    balance_break = []
    if breakdown:
        balance = {'Exchange':'Bittrex', 'SPOT':total_balance}
        balance_break.append(balance)
        newList = sf.singleDict(balance_break)
        sf.displayDataFrame(newList, True, False)
        print('Total',f"{total_balance:,.2f}")
    bittrex = {'total':total_balance, 'coins':coin_assets}

    return bittrex
    

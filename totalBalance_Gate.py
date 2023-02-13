import Gate_wallet as gw
import config
import pandas as pd
import shared_Functions as sf

exchange = 'Gate'


def gate_swap_balance(api_key, api_secret):
    gate_wallet = gw.send_signed_request('/futures/usdt/accounts', api_key, api_secret)
    unrealPnL = gate_wallet['unrealised_pnl'] 
    total_balance = float(gate_wallet['total']) + float(unrealPnL)
    #sf.saveExcel('hh.xlsx',gate_wallet)
    asset = {'Account':'Futures', 'USD Value':total_balance}
    if round(total_balance,2) != 0:
        coin_asset = {
            'Coin':gate_wallet['currency'], 
            'Contract':gate_wallet['currency'], 
            'QTY':round(float(gate_wallet['total']),6), 
            'USD Value':round(total_balance,2),
            'Exchange':exchange, 
            'Account':'USDT-M'}
        return [total_balance, 'USDT-M', coin_asset]
    else:
        coin_asset = {
            'Coin':gate_wallet['currency'], 
            'Contract':gate_wallet['currency'], 
            'QTY':round(float(gate_wallet['total']),6), 
            'USD Value':round(total_balance,2),
            'Exchange':exchange, 
            'Account':'USDT-M'}
        return [total_balance, 'USDT-M', coin_asset]

def gate_spot_balance(api_key, api_secret):
    gate_wallet = gw.send_signed_request('/spot/accounts', api_key, api_secret)
    total_balance = 0
    assets = []

    #sf.saveExcel('d.xlsx', gate_wallet)

    for i in range(0, len(gate_wallet)):
        try:
            coin_price = gw.current_price(gate_wallet[i]['currency'], 'USDT')
            total_pre_price = float(gate_wallet[i]['available'])+float(gate_wallet[i]['locked'])
            total = total_pre_price * coin_price
            total_balance += total
            if round(total,2) != 0:
                asset = {
                    'Coin':gate_wallet[i]['currency'], 
                    'Contract':gate_wallet[i]['currency'], 
                    'QTY':round(float(gate_wallet[i]['available']),6), 
                    'USD Value':round(total,2),
                    'Exchange':exchange, 
                    'Account':'SPOT'}
                assets.append(asset)
        except:
            if gate_wallet[i]['currency'] == 'BTTOLD':
                total = float(gate_wallet[i]['available'])+float(gate_wallet[i]['locked'])
                total_balance += 0
                usd = 0
                if usd != 0:
                    asset = {
                        'Coin':gate_wallet[i]['currency'], 
                        'Contract':gate_wallet[i]['currency'],
                        'QTY':round(float(gate_wallet[i]['available']),6), 
                        'USD Value':0,
                        'Exchange':exchange, 
                        'Account':'SPOT'}
                    assets.append(asset)
            else:
                total = float(gate_wallet[i]['available'])+float(gate_wallet[i]['locked'])
                total_balance += total
                if round(total,2) != 0:
                    asset = {
                        'Coin':gate_wallet[i]['currency'], 
                        'Contract':gate_wallet[i]['currency'], 
                        'QTY':round(float(gate_wallet[i]['available']),6), 
                        'USD Value':round(total,2),
                        'Exchange':exchange, 
                        'Account':'SPOT'}
                    assets.append(asset)

    return [total_balance, 'SPOT', assets]

def gate_total_balance(api_key, api_secret, breakdown):
    total_balance = 0
    assets = []
    coin_assets = []
    skips = 0
    balance_break = []

    for i in [gate_swap_balance(api_key, api_secret), gate_spot_balance(api_key, api_secret)]:
        assets.append(i)
        try:
            total_balance += float(i[0])
            coin_assets.append(i[2])
            balance = {'Exchange':'Gate', i[1]:i[0]}
            balance_break.append(balance)
        except:
            total_balance += float(i[0])
            balance = {'Exchange':'Gate', i[1]:i[0]}
            balance_break.append(balance)
            skips += 1

    #print(coin_assets)
    #print(pd.DataFrame(assets), '\nTotal Gate balance: ', total_balance)

    if breakdown:
        newList = sf.singleDict(balance_break)
        sf.displayDataFrame(newList, True, False)
        print('Total',f"{total_balance:,.2f}")
    gate = {'total':total_balance, 'coins':coin_assets}

    return gate

def gateLeaverage(api_key, api_secret):
    leverageValue = []

    for i in [gate_swap_balance(api_key, api_secret)]:
        lever = {'USD Value':i[0], 'Account':'USDT-M', 'exchange':'Gate'}
        leverageValue.append(lever)
        if lever['USD Value'] <= 0.01:
            lever['USD Value'] = 0

    return leverageValue

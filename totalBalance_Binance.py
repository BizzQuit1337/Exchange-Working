import binance_PnL as bp  #This is a customs requests package to get the futures data from binace correctly, the binance api function was not returning correctly
import config
import pandas as pd
import shared_Functions as sf


def binance_future_wallet_balance(api_key, api_secret, exchange):
    futures_wallet = bp.binance_send_signed_request("https://fapi.binance.com", 'GET', '/fapi/v2/balance', api_key, api_secret, payload={})
    total_balance = 0
    assets = []

    

    for i in range(0, len(futures_wallet)):
        if futures_wallet[i]['balance'] != '0.00000000':
            try:
                coin_price = bp.binance_send_public_request("https://api.binance.com", '/api/v3/ticker/price', payload={'symbol': (futures_wallet[i]['asset']+'USDT')})
                total = (float(futures_wallet[i]['balance']) + float(futures_wallet[i]['crossUnPnl']))*float(coin_price['price'])
                total_balance += total
                if round(total,2) != 0:
                    asset={
                        'Coin':futures_wallet[i]['asset'],
                        'Contract':futures_wallet[i]['asset'],
                        'QTY':round((float(futures_wallet[i]['balance']) + float(futures_wallet[i]['crossUnPnl'])), 6),
                        'USD Value':round(total,2),
                        'Exchange':exchange, 
                        'Account':'USD-M'
                        }
                    assets.append(asset)
            except:
                total = float(futures_wallet[i]['balance']) + float(futures_wallet[i]['crossUnPnl'])
                total_balance += total
                if round(total,2) != 0:
                    asset={
                        'Coin':futures_wallet[i]['asset'], 
                        'Contract':futures_wallet[i]['asset'],
                        'QTY':round(total, 6), 
                        'USD Value':round(total,2),
                        'Exchange':exchange, 
                        'Account':'USD-M'}
                    assets.append(asset)

    return [total_balance, 'USDT-M', assets]

def binance_m_wallet_balance(api_key, api_secret, exchange):
    m_wallet = bp.binance_send_signed_request('https://dapi.binance.com', "GET", '/dapi/v1/balance', api_key, api_secret, payload={})
    total_balance = 0
    assets = []

    for i in range(0, len(m_wallet)):
        if  float(m_wallet[i]['balance']) != 0:
            try:
                coin_price = bp.binance_send_public_request("https://api.binance.com", '/api/v3/ticker/price', payload={'symbol': (m_wallet[i]['asset']+'USDT')})
                total = (float(m_wallet[i]['balance'])+ float(m_wallet[i]['crossUnPnl']))*float(coin_price['price'])
                total_balance += total
                if round(total,2) != 0:
                    asset={
                        'Coin':m_wallet[i]['asset'], 
                        'Contract':m_wallet[i]['asset'],
                        'QTY':round((float(m_wallet[i]['balance'])+ float(m_wallet[i]['crossUnPnl'])),6), 
                        'USD Value':round(total,2),
                        'Exchange':exchange, 
                        'Account':'Coin-M'}
                    assets.append(asset)
            except:
                total = float(m_wallet[i]['balance']) + float(m_wallet[i]['crossUnPnl'])
                total_balance += total
                if round(total,2) != 0:
                    asset={
                        'Coin':m_wallet[i]['asset'], 
                        'Contract':m_wallet[i]['asset'],
                        'QTY':round(total,6), 
                        'USD Value':round(total,2),
                        'Exchange':exchange, 
                        'Account':'Coin-M'}
                    assets.append(asset)

    return [total_balance, 'Coin-M', assets]

def binance_spot_wallet_balance(api_key, api_secret, exchange):
    spot_wallet = bp.binance_send_signed_request('https://api.binance.com', "GET", "/sapi/v1/capital/config/getall", api_key, api_secret, payload={'type': 'SPOT'})
    total_balance = 0
    assets = []

    for i in range(0, len(spot_wallet)):
        if spot_wallet[i]['free'] != '0':#'USDT':
            try:
                total = float(spot_wallet[i]['free'])+float(spot_wallet[i]['locked'])
                coin_price = bp.binance_send_public_request("https://api.binance.com", '/api/v3/ticker/price', payload={'symbol': (spot_wallet[i]['coin']+'USDT')})
                total_usd = float(coin_price['price']) * total
                total_balance += total_usd
                if round(total_usd,2) != 0:
                    asset={
                        'Coin':spot_wallet[i]['coin'],
                        'Contract':spot_wallet[i]['coin'], 
                        'QTY':round(total,6), 
                        'USD Value':round(total_usd,2),
                        'Exchange':exchange, 
                        'Account':'SPOT'}
                    assets.append(asset)       
            except:
                try:
                    total = float(spot_wallet[i]['free'])+float(spot_wallet[i]['locked'])
                    coin_price = bp.binance_send_public_request("https://api.binance.com", '/api/v3/ticker/price', payload={'symbol': (spot_wallet[i]['coin']+'BUSD')})
                    total_usd = float(coin_price['price']) * total
                    total_balance += total_usd
                    if round(total_usd,2) != 0:
                        asset={
                            'Coin':spot_wallet[i]['coin'], 
                            'Contract':spot_wallet[i]['coin'], 
                            'QTY':round(total,6), 
                            'USD Value':round(total_usd,2),
                            'Exchange':exchange, 
                            'Account':'SPOT'}
                        assets.append(asset)
                except:
                    total = float(spot_wallet[i]['free'])+float(spot_wallet[i]['locked'])
                    total_balance += total
                    if round(total,2) != 0:
                        asset={
                            'Coin':spot_wallet[i]['coin'], 
                            'Contract':spot_wallet[i]['coin'],
                            'QTY':round(total,6), 
                            'USD Value':round(total,2),
                            'Exchange':exchange, 
                            'Account':'SPOT'}
                        assets.append(asset)
                    
    return [total_balance, 'SPOT', assets]

def binance_margin_wallet_balance(api_key, api_secret, exchange):
        margin_wallet = bp.binance_send_signed_request('https://api.binance.com', "GET", "/sapi/v1/margin/account", api_key, api_secret, payload={})
        total_balance = 0
        assets = []

        isolated_margin = bp.binance_send_signed_request("https://api.binance.com", 'GET', '/sapi/v1/margin/isolated/account', api_key, api_secret, payload={})

        for i in isolated_margin['assets']:
            if i['baseAsset']['borrowed'] != 0:
                try:
                    coin_price = bp.binance_send_public_request("https://api.binance.com", '/api/v3/ticker/price', payload={'symbol': (i['baseAsset']['asset']+'USDT')})
                    total = (float(i['baseAsset']['netAsset'])*float(coin_price['price']))
                    asset={
                            'Coin':i['baseAsset']['asset'], 
                            'Contract':i['baseAsset']['asset'],
                            'QTY':i['baseAsset']['netAsset'], 
                            'USD Value':total,
                            'Exchange':exchange, 
                            'Account':'Margin-Isolated'}
                    if float(i['baseAsset']['netAsset']) != 0:
                        assets.append(asset)
                        total_balance += total
                except:
                    asset={
                            'Coin':i['baseAsset']['asset'], 
                            'Contract':i['baseAsset']['asset'],
                            'QTY':i['baseAsset']['netAsset'], 
                            'USD Value':i['baseAsset']['netAsset'],
                            'Exchange':exchange, 
                            'Account':'Margin-Isolated'}
                    if float(i['baseAsset']['netAsset']) != 0:
                        assets.append(asset)
                        total_balance += float(i['baseAsset']['netAsset'])

        for i in isolated_margin['assets']:
            if i['quoteAsset']['netAsset'] != 0:
                try:
                    coin_price = bp.binance_send_public_request("https://api.binance.com", '/api/v3/ticker/price', payload={'symbol': (i['quoteAsset']['asset']+'USDT')})
                    total = (float(i['baseAsset']['netAsset'])*float(coin_price['price']))
                    asset={
                            'Coin':i['quoteAsset']['asset'], 
                            'Contract':i['quoteAsset']['asset'],
                            'QTY':i['quoteAsset']['netAsset'], 
                            'USD Value':total,
                            'Exchange':exchange, 
                            'Account':'Margin-Isolated-quote'}
                    if float(i['quoteAsset']['netAsset']) != 0:
                        assets.append(asset)
                        total_balance += total
                except:
                    asset={
                            'Coin':i['quoteAsset']['asset'], 
                            'Contract':i['quoteAsset']['asset'],
                            'QTY':i['quoteAsset']['netAsset'], 
                            'USD Value':i['quoteAsset']['netAsset'],
                            'Exchange':exchange, 
                            'Account':'Margin-Isolated-quote'}
                    if float(i['baseAsset']['netAsset']) != 0:
                        assets.append(asset)
                        total_balance += float(i['quoteAsset']['netAsset'])

        for i in range(0, len(margin_wallet['userAssets'])):
            if margin_wallet['userAssets'][i]['free'] != '0':
                try:
                    coin_price = bp.binance_send_public_request("https://api.binance.com", '/api/v3/ticker/price', payload={'symbol': (margin_wallet['userAssets'][i]['asset']+'USDT')})
                    total = (float(margin_wallet['userAssets'][i]['free'])+float(margin_wallet['userAssets'][i]['locked']))*float(coin_price['price'])
                    total_balance += total
                    if round(total,2) != 0:
                        asset={
                            'Coin':margin_wallet['userAssets'][i]['asset'], 
                            'Contract':margin_wallet['userAssets'][i]['asset'],
                            'QTY':round((float(margin_wallet['userAssets'][i]['free'])+float(margin_wallet['userAssets'][i]['locked'])),6), 
                            'USD Value':round(total,2),
                            'Exchange':exchange, 
                            'Account':'Margin'}
                        assets.append(asset)
                except:
                    total = float(margin_wallet['userAssets'][i]['free'])+float(margin_wallet['userAssets'][i]['locked'])
                    total_balance += total
                    if round(total,2) != 0:
                        asset={
                            'Coin':['userAssets'][i]['asset'], 
                            'Contract':['userAssets'][i]['asset'],
                            'QTY':round(total,6), 'USD Value':round(total,2),
                            'Exchange':exchange, 
                            'Account':'Margin'}
                        assets.append(asset)

        return [total_balance, 'Margin', assets]

def binance_earn_wallet_balance(api_key, api_secret, exchange):
    total_balance = 0
    staking = bp.binance_send_signed_request('https://api.binance.com', "GET", "/sapi/v1/staking/position",api_key, api_secret, payload={'product': 'STAKING'})
    saving = bp.binance_send_signed_request('https://api.binance.com', "GET", "/sapi/v1/lending/union/account", api_key, api_secret)
    assets = []

    for i in range(0, len(staking)):
        if staking[i]['amount'] != '0':
            coin_price = bp.binance_send_public_request("https://api.binance.com", '/api/v3/ticker/price', payload={'symbol': (staking[i]['asset']+'USDT')})
            total = float(staking[i]['amount'])*float(coin_price['price'])
            total_balance += total
            if round(float(staking[i]['amount']),2) != 0:
                asset={
                    'Coin':staking[i]['asset'], 
                    'Contract':staking[i]['asset'],
                    'QTY':round(float(staking[i]['amount']),6), 
                    'USD Value':round(total,2),
                    'Exchange':exchange, 
                    'Account':'Earn'}
                assets.append(asset)

    for j in range(0, len(saving['positionAmountVos'])):
        if saving['positionAmountVos'][j]['amountInUSDT'] != '0':
            total = saving['positionAmountVos'][j]['amountInUSDT']
            total_balance += total
            if round(total,2) != 0:
                asset={
                    'Coin':saving['positionAmountVos'][j]['asset'], 
                    'Contract':saving['positionAmountVos'][j]['asset'],
                    'QTY':round(total,6), 
                    'USD Value':round(total,2),
                    'Exchange':exchange, 
                    'Account':'Earn'}
                assets.append(asset)
        else:
            total_balance += 0

    return [total_balance, 'Earn', assets]

def total_binance_balance(api_key, api_secret, exchange, breakdown):
    all_asset = []
    coin_assets = []
    balance_break = []
    total_balance = 0

    for i in [binance_future_wallet_balance(api_key, api_secret, exchange), binance_spot_wallet_balance(api_key, api_secret, exchange), binance_margin_wallet_balance(api_key, api_secret, exchange), binance_earn_wallet_balance(api_key, api_secret, exchange), binance_m_wallet_balance(api_key, api_secret, exchange) ]:
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
    binance = {'total':total_balance, 'coins':coin_assets}
    
    return binance

def binanceLeaverage(api_key, api_secret, exchange):
    leverageValue = []

    for i in [binance_future_wallet_balance(api_key, api_secret, exchange), binance_m_wallet_balance(api_key, api_secret, exchange)]:
        lever = {'USD Value':i[0], 'Account':i[1], 'exchange':'Binance'}
        leverageValue.append(lever)
        
    return leverageValue

#x = binance_margin_wallet_balance(config.binance_key, config.binance_secret, 'Binance')
#print(x)
#binance_margin_wallet_balance(config.binance_key, config.binance_secret, 'Binance')
#total_binance_balance(config.binance_key, config.binance_secret, 'Binance', False)

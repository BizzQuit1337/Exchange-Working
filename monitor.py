import binancePositions, bitmexPostions, bybitPositions, gatePositions, huobiPositions, krakenPositions, okxPositions
import config
import pandas as pd
import shared_Functions as sf
import all_balances as ab
import all_positions as ap
import totalBalance_Binance, totalBalance_Kraken, totalBalance_OKX, totalBalance_Huobi, totalBalance_Bitmex, totalBalance_Gate, totalBalance_Bittrex, totalBalance_Bybit

def get_all_positions():
    positions = []
    errorCount = 0
    total_USD = 0
    for i in [binancePositions.all_positions(config.binance_key, config.binance_secret, 'Binance'), bitmexPostions.get_usdt_pos(config.bitmex_key, config.bitmex_secret, 'Bitmex')['assets'], bybitPositions.get_usdt_pos(config.bybit_key, config.bybit_secret, 'Bybit')['assets'], gatePositions.get_usdt_pos(config.gate_key, config.gate_secret, 'Gate')['assets'], huobiPositions.get_all_positions(config.huobi_key, config.huobi_secret, 'Huobi'), krakenPositions.get_usdt_pos(config.kraken_futures_key, config.kraken_futures_secret, 'Kraken'), okxPositions.get_usdt_pos(config.okx_key, config.okx_secret, config.okx_passphrase, 'OKX')['assets'], binancePositions.all_positions(config.binance_sub_key, config.binance_sub_secret, 'Binance-sub'), bybitPositions.get_usdt_pos(config.bybit_sub_key, config.bybit_sub_secret, 'Bybit-sub')['assets'], okxPositions.get_usdt_pos(config.okx_key_sub, config.okx_secret_sub, config.okx_pass_sub, 'OKX-sub')['assets'], huobiPositions.get_all_positions(config.huobi_key_sub, config.huobi_secret_sub, 'Huobi-sub')]:
        if str(type(i)) == "<class 'dict'>":
            total_USD += i['USD Value']
            positions.append(i)
        else:
            for j in i:
                if str(type(j)) == "<class 'dict'>":
                    total_USD += j['USD Value']
                    positions.append(j)
                else:
                    for k in j:
                        if str(type(k)) == "<class 'dict'>":
                            total_USD += k['USD Value']
                            positions.append(k)
                        else:
                            errorCount += 1
    sorted_positions = sorted(positions, key=lambda d: d['Coin'])  

    return sorted_positions

def get_total_balance():
    balances = []
    total_total_balance = 0
    sub_total_balance = 0
    total_total_balance +=  totalBalance_OKX.okx_wallet_total(config.okx_key, config.okx_secret, config.okx_passphrase, 'OKX', True)['total']
    sub_total_balance +=  totalBalance_OKX.okx_wallet_total(config.okx_key_sub, config.okx_secret_sub, config.okx_pass_sub, 'OKX-sub', True)['total']
    total_total_balance += totalBalance_Binance.total_binance_balance(config.binance_key, config.binance_secret, 'Binance', True)['total']
    sub_total_balance += totalBalance_Binance.total_binance_balance(config.binance_sub_key, config.binance_sub_secret, 'Binance-sub', True)['total']
    total_total_balance += totalBalance_Kraken.total_kraken_balance(config.kraken_futures_key, config.kraken_futures_secret, config.kraken_key, config.kraken_secret, True)['total']
    total_total_balance += totalBalance_Huobi.total_huobi_balance(config.huobi_key, config.huobi_secret, config.huobi_spot_id, 'Huobi', True)['total']
    sub_total_balance += totalBalance_Huobi.total_huobi_balance(config.huobi_key_sub, config.huobi_secret_sub, config.huobi_spot_id_sub, 'Huobi-sub', True)['total']
    total_total_balance += totalBalance_Bitmex.bitmex_wallet(config.bitmex_key, config.bitmex_secret, True)['total']
    total_total_balance += totalBalance_Gate.gate_total_balance(config.gate_key, config.gate_secret, True)['total']
    total_total_balance += totalBalance_Bittrex.bittrex_balance(config.bittrex_key, config.bittrex_secret, True)['total']
    total_total_balance += totalBalance_Bybit.total_bybit_balance(config.bybit_key, config.bybit_secret, 'Bybit', True)['total']
    sub_total_balance += totalBalance_Bybit.total_bybit_balance(config.bybit_sub_key, config.bybit_sub_secret, 'Bybit-sub', True)['total']
    overall_total = sub_total_balance + total_total_balance
    total = [{'Total balance no sub':round(total_total_balance, 2), 'Total sub balance':round(sub_total_balance, 2),'Overall Total balance':round(overall_total, 2)}]
    return total

def get_all_assets():
    all_coins = []

    for i in [totalBalance_OKX.okx_wallet_total(config.okx_key, config.okx_secret, config.okx_passphrase, 'OKX', False)['coins'], totalBalance_OKX.okx_wallet_total(config.okx_key_sub, config.okx_secret_sub, config.okx_pass_sub, 'OKX-sub', False)['coins'], totalBalance_Binance.total_binance_balance(config.binance_key, config.binance_secret, 'Binance', False)['coins'], totalBalance_Binance.total_binance_balance(config.binance_sub_key, config.binance_sub_secret, 'Binance-sub', False)['coins'], totalBalance_Kraken.total_kraken_balance(config.kraken_futures_key, config.kraken_futures_secret, config.kraken_key, config.kraken_secret, False)['coins'], totalBalance_Huobi.total_huobi_balance(config.huobi_key, config.huobi_secret, config.huobi_spot_id, 'Huobi', False)['coins'], totalBalance_Huobi.total_huobi_balance(config.huobi_key_sub, config.huobi_secret_sub, config.huobi_spot_id_sub, 'Huobi-sub', False)['coins'], totalBalance_Bitmex.bitmex_wallet(config.bitmex_key, config.bitmex_secret, False)['coins'], totalBalance_Gate.gate_total_balance(config.gate_key, config.gate_secret, False)['coins'], totalBalance_Bittrex.bittrex_balance(config.bittrex_key, config.bittrex_secret, False)['coins'], totalBalance_Bybit.total_bybit_balance(config.bybit_key, config.bybit_secret, 'Bybit', False)['coins'], totalBalance_Bybit.total_bybit_balance(config.bybit_sub_key, config.bybit_sub_secret, 'Bybit-sub', False)['coins']]:
        if str(type(i)) == "<class 'dict'>":
            all_coins.append(i)
        else:
            for j in i:
                if str(type(j)) == "<class 'dict'>":
                    all_coins.append(j)
                else:
                    for k in j:
                        if str(type(k)) == "<class 'dict'>":
                            all_coins.append(k)
                        else:
                            print('gone to deep bud')
                            
    sorted_assets = sorted(all_coins, key=lambda d: d['Coin'])
    return sorted_assets

def usdt_Value():
    total_assets = []

    assets = get_all_assets()
    positions = get_all_positions()

    #sf.saveExcel('positionings.xlsx', positions)

    for i in positions:
        total_assets.append(i)
    for i in assets:
        total_assets.append(i)

    sorted_assets = sorted(total_assets, key=lambda d: d['Coin'])

    #sf.displayDataFrame(sorted_assets)

    #for i in sorted_assets:
    #    if i['Exchange'] == 'OKX-sub':
    #        print(i)

    breakAsset = {
        'Coin':'BREAK',
        'USD Value':0,
        'QTY':0
    }

    sorted_assets.append(breakAsset)

    #sf.saveExcel('sorted_assets.xlsx', sorted_assets)


    coinUSD = 0
    coinQTY = 0
    cond_assets = []
    cond_currency = []

    for i in sorted_assets:
        try:
            if preCoin == i['Coin']:
                coinUSD += i['USD Value']
                coinQTY += i['QTY']
            else:
                if preCoin == 'USD' or preCoin == 'USDT' or preCoin == 'USDC' or preCoin == 'EUR' or preCoin == 'BUSD':
                    currency = {
                        'Coin':preCoin,
                        'QTY':coinQTY,
                        'USD Value':round(coinUSD,2)
                    }
                    cond_currency.append(currency)
                else:
                    asset = {
                        'Coin':preCoin,
                        'QTY':coinQTY,
                        'USD Value':coinUSD
                    }
                    cond_assets.append(asset)
                preCoin = i['Coin']
                coinUSD = i['USD Value']
                coinQTY = i['QTY']
        except:
            preCoin = i['Coin']
            coinUSD += i['USD Value']
            coinQTY += i['QTY']

    #sf.saveExcel('cond_assets.xlsx', cond_assets)

    return [cond_assets, cond_currency]

def Leverage():
    
    asset_bal = ab.leaverageAssets()
    bbdf = sf.displayDataFrame(asset_bal, False, True)
    asset_pos = ap.get_leverageValue()
    bpdf = sf.displayDataFrame(asset_pos, False, True)

    levers = []

    for i in bbdf:
        for j in bpdf:
            if i['Account'] == j['Account'] and i['exchange'] == j['exchange']:
                try:
                    lever = {
                        'Exchange':i['exchange'],
                        'Account':i['Account'],
                        'Wallet USD Value':i['USD Value'],
                        'Position Absolute':j['absolute'],
                        'Position USD Value':j['USD Value'],
                        'Leverage':round((float(j['absolute'])/float(i['USD Value'])),2)
                    }
                    levers.append(lever)
                except:
                    lever = {
                        'Exchange':i['exchange'],
                        'Account':i['Account'],
                        'Wallet USD Value':i['USD Value'],
                        'Position Absolute':j['absolute'],
                        'Position USD Value':j['USD Value'],
                        'Leverage':0
                    }
                    levers.append(lever)
    return levers

import all_balances as ab
import all_positions as ap
import config, time
import pandas as pd
import shared_Functions as sf
start = time.time()
total_assets = []

assets = ab.get_all_assets()
positions = ap.get_all_positions(config.binance_key, config.bitmex_key, config.bybit_key, config.gate_key, config.huobi_key, config.kraken_futures_key, config.okx_key, config.binance_secret, config.bitmex_secret, config.bybit_secret, config.gate_secret, config.huobi_secret, config.kraken_futures_secret, config.okx_secret, config.okx_passphrase)

#sf.saveExcel('positionings.xlsx', positions)

for i in positions:
    total_assets.append(i)
for i in assets:
    total_assets.append(i)

sorted_assets = sorted(total_assets, key=lambda d: d['Coin'])

#sf.displayDataFrame(sorted_assets)

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
                    'USD Value':coinUSD
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

print(pd.DataFrame(cond_assets), '\n#####\n', pd.DataFrame(cond_currency))
end = time.time()
print('Taken: ', (end-start))


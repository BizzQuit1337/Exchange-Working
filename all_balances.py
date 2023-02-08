import config
import pandas as pd
import config, totalBalance_Binance, totalBalance_Kraken, totalBalance_OKX, totalBalance_Huobi, totalBalance_Bitmex, totalBalance_Gate, totalBalance_Bittrex, totalBalance_Bybit
import shared_Functions as sf

def leaverageAssets():
    all_assets = []
    for i in [totalBalance_OKX.okxLeaverage(config.okx_key, config.okx_secret, config.okx_passphrase, 'OKX'), totalBalance_Binance.binanceLeaverage(config.binance_key, config.binance_secret, 'Binance'), totalBalance_Huobi.huobiLeaverage(config.huobi_key, config.huobi_secret, 'Huobi'), totalBalance_Bybit.bybitLeaverage(config.bybit_key, config.bybit_secret, 'Bybit'), totalBalance_Gate.gateLeaverage(config.gate_key, config.gate_secret), totalBalance_Bitmex.bitmexLeaverage(config.bitmex_key, config.bitmex_secret)]:
        df = sf.displayDataFrame(i, False, True)
        all_assets.append(df)
    
    return all_assets

#print(leaverageAssets())
#print(get_all_assets())
#print('#################')
#print(get_total_balance())
#x=leaverageAssets()
#print(pd.DataFrame(x))
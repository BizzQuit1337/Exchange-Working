import config_ocar
import pandas as pd
import config_ocar, totalBalance_Binance, totalBalance_Kraken, totalBalance_OKX, totalBalance_Huobi, totalBalance_Bitmex, totalBalance_Gate, totalBalance_Bittrex, totalBalance_Bybit
import shared_Functions as sf

def leaverageAssets():
    all_assets = []
    for i in [totalBalance_OKX.okxLeaverage(config_ocar.okx_key, config_ocar.okx_secret, config_ocar.okx_passphrase, 'OKX'), totalBalance_Binance.binanceLeaverage(config_ocar.binance_key, config_ocar.binance_secret, 'Binance'), totalBalance_Huobi.huobiLeaverage(config_ocar.huobi_key, config_ocar.huobi_secret, 'Huobi'), totalBalance_Bybit.bybitLeaverage(config_ocar.bybit_key, config_ocar.bybit_secret, 'Bybit'), totalBalance_Gate.gateLeaverage(config_ocar.gate_key, config_ocar.gate_secret), totalBalance_Bitmex.bitmexLeaverage(config_ocar.bitmex_key, config_ocar.bitmex_secret)]:
        df = sf.displayDataFrame(i, False, True)
        all_assets.append(df)
    
    return all_assets

#print(leaverageAssets())
#print(get_all_assets())
#print('#################')
#print(get_total_balance())
#x=leaverageAssets()
#print(pd.DataFrame(x))s
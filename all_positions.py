import binancePositions, bitmexPostions, bybitPositions, gatePositions, huobiPositions, krakenPositions, okxPositions
import config
import pandas as pd
import shared_Functions as sf

def get_leverageValue():
    all_positions = []
    for i in [binancePositions.leverValues(config.binance_key, config.binance_secret, 'Binance'), huobiPositions.leverValues(config.huobi_key, config.huobi_secret, 'Huobi'), okxPositions.leverValues(config.okx_key, config.okx_secret, config.okx_passphrase, 'OKX'), bybitPositions.leverValues(config.bybit_key, config.bybit_secret, 'Bybit'), gatePositions.leverValues(config.gate_key, config.gate_secret, 'Gate'), bitmexPostions.leverValues(config.bitmex_key, config.bitmex_secret, 'Bitmex')]:
        df = sf.displayDataFrame(i, False, True)
        all_positions.append(df)
    return all_positions
            
#x = get_all_positions(config.binance_key, config.bitmex_key, config.bybit_key, config.gate_key, config.huobi_key, config.kraken_futures_key, config.okx_key, config.binance_secret, config.bitmex_secret, config.bybit_secret, config.gate_secret, config.huobi_secret, config.kraken_futures_secret, config.okx_secret, config.okx_passphrase)
#sf.displayDataFrame(x, True, False)
#print(pd.DataFrame(x))
#print(get_leverageValue())

#sf.saveExcel('positions.xlsx', x)
#end = time.time()
#print('Taken: ', (end-start))
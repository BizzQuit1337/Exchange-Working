import binancePositions, bitmexPostions, bybitPositions, gatePositions, huobiPositions, krakenPositions, okxPositions
import config_ocar
import pandas as pd
import shared_Functions as sf

def get_leverageValue():
    all_positions = []
    for i in [binancePositions.leverValues(config_ocar.binance_key, config_ocar.binance_secret, 'Binance'), huobiPositions.leverValues(config_ocar.huobi_key, config_ocar.huobi_secret, 'Huobi'), okxPositions.leverValues(config_ocar.okx_key, config_ocar.okx_secret, config_ocar.okx_passphrase, 'OKX'), bybitPositions.leverValues(config_ocar.bybit_key, config_ocar.bybit_secret, 'Bybit'), gatePositions.leverValues(config_ocar.gate_key, config_ocar.gate_secret, 'Gate'), bitmexPostions.leverValues(config_ocar.bitmex_key, config_ocar.bitmex_secret, 'Bitmex')]:#, binancePositions.leverValues(config_ocar.binance_sub_key, config_ocar.binance_sub_secret, 'Binance-sub'), bybitPositions.leverValues(config_ocar.bybit_sub_key, config_ocar.bybit_sub_secret, 'Bybit-sub'), huobiPositions.leverValues(config_ocar.huobi_key_sub, config_ocar.huobi_secret_sub, 'Huobi-sub'), okxPositions.leverValues(config_ocar.okx_key_sub, config_ocar.okx_secret_sub, config_ocar.okx_pass_sub, 'OKX-sub')]:
        df = sf.displayDataFrame(i, False, True)
        all_positions.append(df)
    return all_positions
            
#x = get_all_positions(config_ocar.binance_key, config_ocar.bitmex_key, config_ocar.bybit_key, config_ocar.gate_key, config_ocar.huobi_key, config_ocar.kraken_futures_key, config_ocar.okx_key, config_ocar.binance_secret, config_ocar.bitmex_secret, config_ocar.bybit_secret, config_ocar.gate_secret, config_ocar.huobi_secret, config_ocar.kraken_futures_secret, config_ocar.okx_secret, config_ocar.okx_passphrase)
#sf.displayDataFrame(x, True, False)
#print(pd.DataFrame(x))
#print(get_leverageValue())

#sf.saveExcel('positions.xlsx', x)
#end = time.time()
#print('Taken: ', (end-start))
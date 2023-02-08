import all_balances as ab
import all_positions as ap
import config, time
import pandas as pd
import shared_Functions as sf

start = time.time()

def Leverage():
    
    asset_bal = ab.leaverageAssets()
    bbdf = sf.displayDataFrame(asset_bal, False)
    asset_pos = ap.get_leverageValue()
    bpdf = sf.displayDataFrame(asset_pos, False)

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
                        'Leverage':float(j['absolute'])/float(i['USD Value'])
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

x = Leverage()

sf.displayDataFrame(x, True)

end = time.time()
print('Taken: ', (end-start))
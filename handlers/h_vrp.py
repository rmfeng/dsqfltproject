"""
handler for VRP data
"""
import pandas as pd
import numpy as np
import datetime as dt
from statsmodels.tsa.arima_model import ARMA
from handlers.BaseProcessor import BaseProcessor


class VRPProcessor(BaseProcessor):
    # specifications for raw file path and out path:
    NAME = "VRP"
    RAW_PATHS = ['raw_data/^GSPC.csv',
                'raw_data/^VIX.csv']
    OUT_PATH = 'pkl_data/VRP.pkl'


    def __init__(self):
        super().__init__(self.RAW_PATHS, self.OUT_PATH)

    def load_raw(self):
        print("Loading data for %s ... " % self.NAME)
        self.row_data['sp500']=pd.read_csv(self.RAW_PATH[0])
        self.row_data['vix'] = pd.read_csv(self.RAW_PATHS[1])

    def wrangle(self):
        print("Wrangling data for %s ... " % self.NAME)
        sp500=self.row_data['sp500']
        vix=self.row_data['vix']
        
        sp500['o']=np.log(sp500['Open'])-np.log(sp500['Close'].shift(1))
        sp500['u']=np.log(sp500['High'])-np.log(sp500['Open'])
        sp500['d']=np.log(sp500['Low'])-np.log(sp500['Open'])
        sp500['c']=np.log(sp500['Close'])-np.log(sp500['Open'])

        #suppose n=20
        n=20
        sp500['rs']=sp500['u']*(sp500['u']-sp500['c'])+sp500['d']*(sp500['d']-sp500['c'])
        sp500['V_rs']=sp500['rs'].rolling(window=n).sum()/n
        series_vo=(sp500['o']-sp500['o'].rolling(window=n).mean())**2
        sp500['V_o']=series_vo.rolling(window=n).sum()/(n-1)
        series_vc=(sp500['c']-sp500['c'].rolling(window=20).mean())**2
        sp500['V_c']=series_vc.rolling(window=n).sum()/(n-1)

        k=0.34/(1.34+(n+1)/(n-1))
        sp500['V']=sp500['V_o']+k*sp500['V_c']+(1-k)*sp500['V_rs']

        #GARCH style, actually is ARMA to variance
        model=ARMA(sp500['V'][39:],order=(1,1)).fit()

        vix=vix.iloc[78:]
        vix['forecast']=np.sqrt(model.predict()*252)*100

        vix['VRP']=vix['Close']-vix['forecast']
        vix=vix[(vix['Date']>='1990-06-08')&(vix['Date']<='2019-11-05')]
        vix=vix.set_index('Date')
        vix.index=pd.to_datetime(vix.index)

        self.wrangled_data = vix[['VRP']]


# testing
if __name__ == '__main__':
    # running this as of higher dir
    import os
    os.chdir('..')

    p = PCRProcessor()
    p.load_raw()
    p.wrangle()
    p.save_pickle()
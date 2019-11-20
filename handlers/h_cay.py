"""
handler for CAY data
"""
import pandas as pd
import numpy as np
import datetime as dt
from scipy import signal
import statsmodels.api as sm
from handlers.BaseProcessor import BaseProcessor


class CAYProcessor(BaseProcessor):
    # specifications for raw file path and out path:
    NAME = "CAY"
    RAW_PATHS = ['raw_data/UNAC-ECE_USA.csv','raw_data/FRED-HNOTLNQ027S.csv','raw_data/FED-FU156010001_Q.csv','raw_data/RATEINF-CPI_USA.csv']
    OUT_PATH = 'pkl_data/CAY.pkl'

    def __init__(self):
        super().__init__(self.RAW_PATHS, self.OUT_PATH)

    def load_raw(self):
        print("Loading data for %s ... " % self.NAME)
        self.raw_data['consumption'] = pd.read_csv(self.RAW_PATHS[0])
        self.raw_data['asset'] = pd.read_csv(self.RAW_PATHS[1])
        self.raw_data['wealth'] = pd.read_csv(self.RAW_PATHS[2])
        self.raw_data['CPI'] = pd.read_csv(self.RAW_PATHS[3])

    def wrangle(self):
        print("Wrangling data for %s ... " % self.NAME)
        consumption = self.raw_data['consumption']
        asset=self.raw_data['asset']
        wealth=self.raw_data['wealth']
        CPI=self.raw_data['CPI']
        
        consumption['consumption']=consumption['Equals: Total actual individual consumption (US dollar; series 1000)']-consumption['Clothing and footwear (US dollar; series 1000)']
        consumption=consumption[['Date','consumption']]

        asset=asset.rename(columns={'Value':'asset'})
        wealth=wealth.rename(columns={'Value':'wealth'})
        data=pd.merge(consumption,asset,on='Date',how='outer')
        data=pd.merge(data,wealth,on='Date',how='outer')

        #CPI adjustment
        CPI=CPI.rename(columns={'Value':'CPI'})

        data=data[data.Date>='1989-12-01']
        CPI=CPI[CPI.Date>='1989-12-01']
        data=pd.merge(data,CPI,on='Date',how='outer')

        data['consumption']=data['consumption']/data['CPI']*141.900
        data['asset']=data['asset']/data['CPI']*141.900
        data['wealth']=data['wealth']/data['CPI']*141.900

        #interpolate yearly consumption to quarterly data
        data=data.sort_values(by='Date')
        data.head()

        data['consumption']=data['consumption'].ffill()
        data['asset']=data['asset'].ffill()
        data['wealth']=data['wealth'].ffill()

        #log,detrend and cointegration
        data['consumption']=np.log(data['consumption'])
        data['asset']=np.log(data['asset'])
        data['wealth']=np.log(data['wealth'])
        data=data.set_index('Date')

        #detrend
        data['consumption_norm']=signal.detrend(data['consumption'],type='linear')
        data['asset_norm']=signal.detrend(data['asset'],type='linear')
        data['wealth_norm']=signal.detrend(data['wealth'],type='linear')


        model = sm.OLS(data['consumption'], sm.add_constant(data[['asset','wealth']]))
        results = model.fit()

        data['resid']=results.resid
        
        data.index=pd.to_datetime(data.index)
        
        self.wrangled_data = data[['resid']]


# testing
if __name__ == '__main__':
    # running this as of higher dir
    import os
    os.chdir('..')

    p = CPIProcessor()
    p.load_raw()
    p.wrangle()
    p.save_pickle()

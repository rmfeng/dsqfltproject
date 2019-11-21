"""
handler for SPX data
"""
import pandas as pd
import numpy as np
import datetime as dt
from handlers.BaseProcessor import BaseProcessor


class SPXProcessor(BaseProcessor):
    # specifications for raw file path and out path:
    NAME = "SPX"
    RAW_PATHS = ['raw_data/spx/SP500_prices.csv']
    OUT_PATH = 'pkl_data/SPX.pkl'

    def __init__(self):
        super().__init__(self.RAW_PATHS, self.OUT_PATH)

    def load_raw(self):
        print("Loading data for %s ... " % self.NAME)

        # obtain data
        self.raw_data = pd.read_csv(self.RAW_PATHS[0])

    def wrangle(self):
        print("Wrangling data for %s ... " % self.NAME)
        SP500 = self.raw_data
        SP500.drop(columns=['Open','High','Low','Close','Volume'],inplace=True)
        SP500.columns = ['DATE','Adj Close']
        SP500.set_index('DATE',drop=True,inplace=True)
        SP500.index=pd.to_datetime(SP500.index)
        SP500 = SP500.resample('D').ffill().dropna()
        SP500 = SP500.loc[(SP500.index>='1990-06-07') & (SP500.index<='2019-09-30')]
        SP500['Adj Close'] = SP500['Adj Close'].astype(float)
        SP500.columns = ['SPX']
        self.wrangled_data = SP500.pct_change().dropna()







# testing
if __name__ == '__main__':
    # running this as of higher dir
    import os
    os.chdir('..')

    p = SPXProcessor()
    p.load_raw()
    p.wrangle()
    p.save_pickle()

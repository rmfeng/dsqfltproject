"""
handler for MA data
"""
import pandas as pd
import numpy as np
import datetime as dt
from handlers.BaseProcessor import BaseProcessor


class MAProcessor(BaseProcessor):
    # specifications for raw file path and out path:
    NAME = "MA"
    RAW_PATHS = ['raw_data/^GSPC.csv']
    OUT_PATH = 'pkl_data/MA.pkl'

    def __init__(self):
        super().__init__(self.RAW_PATHS, self.OUT_PATH)

    def load_raw(self):
        print("Loading data for %s ... " % self.NAME)

        # obtain data
        self.raw_data = pd.read_csv(self.RAW_PATHS[0])

    def wrangle(self):
        print("Wrangling data for %s ... " % self.NAME)
        spx= self.raw_data
        spx=spx.set_index('Date')[['Adj Close']]
        spx.index=pd.to_datetime(spx.index)
        
        spx['rolling_mean']=spx['Adj Close'].rolling('304d').mean()
        spx['high']=spx['Adj Close']>spx['rolling_mean']
        spx['MA']=spx['high'].apply(lambda x:1 if x else 0)
        
        self.wrangled_data = spx[['MA']][spx.index>='1990-06-08']







# testing
if __name__ == '__main__':
    # running this as of higher dir
    import os
    os.chdir('..')

    p = SPXProcessor()
    p.load_raw()
    p.wrangle()
    p.save_pickle()

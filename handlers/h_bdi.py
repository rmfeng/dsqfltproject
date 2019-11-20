"""
handler for BDI data
"""
import pandas as pd
import numpy as np
import datetime as dt
from handlers.BaseProcessor import BaseProcessor


class BDIProcessor(BaseProcessor):
    # specifications for raw file path and out path:
    NAME = "BDI"
    RAW_PATHS = ['raw_data/Baltic Dry Index Historical Data.csv',
                 'raw_data/equity_mkt_timing_2018/BDI_GSCI.csv']
    OUT_PATH = 'pkl_data/BDI.pkl'

    GSCI_COL = 'Baltic Exchange Dry Index (BDI) - PRICE INDEX'

    def __init__(self):
        super().__init__(self.RAW_PATHS, self.OUT_PATH)

    def load_raw(self):
        print("Loading data for %s ... " % self.NAME)
        print("1")
        self.row_data['BDI1']=pd.read_csv(self.RAW_PATH[0])
        self.row_data['BDI2'] = pd.read_csv(self.RAW_PATHS[1])

    def wrangle(self):
        print("Wrangling data for %s ... " % self.NAME)
        BDI1=self.row_data['BDI1']
        BDI2=self.row_data['BDI2']
        
        BDI2['Date']=pd.to_datetime(BDI2['Name']).astype(str)
        BDI2=BDI2[(BDI2['Date']>='1990-06-08')&(BDI2['Date']<'2012-07-04')]
        BDI2=BDI2.rename(columns={'Baltic Exchange Dry Index (BDI) - PRICE INDEX':'BDI'})
        BDI1=BDI1.rename(columns={'Price':'BDI'})
        
        BDI2=BDI2.sort_values(by='Date',ascending=True).set_index('Date')[['BDI']]
        BDI1=BDI1.sort_values(by='Date',ascending=True).set_index('Date')[['BDI']]
        
        BDI1['BDI']=BDI1['BDI'].apply(lambda x: float(x.replace(',','')))
        BDI=pd.concat([BDI2,BDI1])
        BDI.index=BDI.index.todatetime

        self.wrangled_data = BDI[['PCR']]


# testing
if __name__ == '__main__':
    # running this as of higher dir
    import os
    os.chdir('..')

    p = PCRProcessor()
    p.load_raw()
    p.wrangle()
    p.save_pickle()
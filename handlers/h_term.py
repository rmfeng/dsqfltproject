"""
handler for TERM data
"""
import pandas as pd
import numpy as np
import datetime as dt
from handlers.BaseProcessor import BaseProcessor


class TERMProcessor(BaseProcessor):
    # specifications for raw file path and out path:
    NAME = "TERM"
    RAW_PATHS = ['raw_data/USTREASURY-YIELD.csv']
    OUT_PATH = 'pkl_data/TERM.pkl'

    def __init__(self):
        super().__init__(self.RAW_PATHS, self.OUT_PATH)

    def load_raw(self):
        print("Loading data for %s ... " % self.NAME)
        self.raw_data = pd.read_csv(self.RAW_PATHS[0])

    def wrangle(self):
        print("Wrangling data for %s ... " % self.NAME)
        treasury=self.raw_data
        treasury=treasury[treasury['Date']>='1990-06-08']
        treasury=treasury.sort_values(by='Date',ascending=True)
        treasury['TERM']=treasury['10 YR']-treasury['3 MO']
        treasury.index=pd.to_datetime(treasury['Date'])
        
        self.wrangled_data =treasury[['TERM']] 
        


# testing
if __name__ == '__main__':
    # running this as of higher dir
    import os
    os.chdir('..')

    p = CPIProcessor()
    p.load_raw()
    p.wrangle()
    p.save_pickle()

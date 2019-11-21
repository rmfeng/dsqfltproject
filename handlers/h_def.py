"""
handler for DEF data
"""
import pandas as pd
import numpy as np
import datetime as dt
from handlers.BaseProcessor import BaseProcessor



class DEFProcessor(BaseProcessor):
    # specifications for raw file path and out path:
    NAME = "DEF"
    RAW_PATHS = ['raw_data/FRED-BAA10YM.csv','raw_data/FRED-AAA10YM.csv']
    OUT_PATH = 'pkl_data/DEF.pkl'

    def __init__(self):
        super().__init__(self.RAW_PATHS, self.OUT_PATH)

    def load_raw(self):
        print("Loading data for %s ... " % self.NAME)

        # obtain data
        df1 = pd.read_csv(self.RAW_PATHS[0])
        df2 = pd.read_csv(self.RAW_PATHS[1])
        self.raw_data = pd.DataFrame()
        self.raw_data['DEF'] = df1['Value']-df2['Value']

        # obtain dates
        self.raw_data['DATE'] = df1['Date']
        self.raw_data.set_index('DATE',drop=True,inplace=True)
        self.raw_data.index=pd.to_datetime(self.raw_data.index)
        self.raw_data = self.raw_data.iloc[::-1]
        self.raw_data = self.raw_data.iloc[self.raw_data.index >= '1990-06-08']

    def wrangle(self):
        print("Wrangling data for %s ... " % self.NAME)
        df_DEF = self.raw_data
        df_DEF_re = df_DEF.resample('D').ffill().dropna()
        self.wrangled_data = df_DEF_re



# testing
if __name__ == '__main__':
    # running this as of higher dir
    import os
    os.chdir('..')

    p = DEFProcessor()
    p.load_raw()
    p.wrangle()
    p.save_pickle()

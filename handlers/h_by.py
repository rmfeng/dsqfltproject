"""
handler for BY data
"""
import pandas as pd
import numpy as np
import datetime as dt
import requests
from bs4 import BeautifulSoup
from handlers.BaseProcessor import BaseProcessor


class BYProcessor(BaseProcessor):
    # specifications for raw file path and out path:
    NAME = "BY"
    RAW_PATHS = ['raw_data/FRED-DGS10.csv']
    OUT_PATH = 'pkl_data/BY.pkl'

    def __init__(self):
        super().__init__(self.RAW_PATHS, self.OUT_PATH)

    def load_raw(self):
        print("Loading data for %s ... " % self.NAME)

        # obtain data
        self.raw_data = pd.read_csv(self.RAW_PATHS[0])
        self.raw_data = self.raw_data.iloc[::-1]
        self.raw_data.reset_index(drop=True,inplace=True)
        self.raw_data.columns = ['DATE','Y']
        self.raw_data.set_index('DATE',drop=True,inplace=True)
        self.raw_data.index=pd.to_datetime(self.raw_data.index)


    def wrangle(self):
        print("Wrangling data for %s ... " % self.NAME)
        df_BY = self.raw_data.loc[self.raw_data.index >= '1989-06-08']
        df_BY_re = df_BY.resample('D').ffill().dropna()

        # compute 12 months EMA
        EMA = df_BY_re.ewm(span=12*30).mean().dropna()
        EMA = EMA.loc[EMA.index >= '1990-06-08']
        df_BY_re = df_BY_re.loc[df_BY_re.index >= '1990-06-08']

        fun = lambda t: df_BY_re['Y'][t]/EMA['Y'][t]
        BY=[fun(t) for t in range(df_BY_re.shape[0])]
        df_BY_re['BY'] = BY
        df_BY_re.drop(columns=['Y'],inplace=True)
        self.wrangled_data = df_BY_re

# testing
if __name__ == '__main__':
    # running this as of higher dir
    import os
    os.chdir('..')

    p = BYProcessor()
    p.load_raw()
    p.wrangle()
    p.save_pickle()

"""
handler for NOS data
"""
import pandas as pd
import numpy as np
import datetime as dt
from handlers.BaseProcessor import BaseProcessor


class OILProcessor(BaseProcessor):
    # specifications for raw file path and out path:
    NAME = "OIL"
    RAW_PATHS = ['raw_data/futures_data/CL_ohlcv.pkl']
    OUT_PATH = 'pkl_data/OIL.pkl'

    def __init__(self):
        super().__init__(self.RAW_PATHS, self.OUT_PATH)

    def load_raw(self):
        print("Loading data for %s ... " % self.NAME)
        self.raw_data['oil'] = pd.read_pickle(self.RAW_PATHS[0])

    def wrangle(self):
        print("Wrangling data for %s ... " % self.NAME)
        df = self.raw_data['oil']
        df = df[['Settle']].reset_index()
        df['Expiration'] = df['Expiration'].astype('datetime64[ns]')
        df['Date'] = df['Date'].astype('datetime64[ns]')
        df['days_exp'] = (df['Expiration'] - df['Date']).apply(lambda x: x.days)
        df['months'] = np.ceil(df['days_exp'] / 365 * 12)
        df_unique = df.groupby(['Date', 'months'])[['Settle']].first()
        df_by_month = df_unique.reset_index().pivot(columns='months', index='Date', values='Settle')
        df_14 = df_by_month[[1, 4]].dropna()
        df_res = pd.DataFrame(np.log(df_14[1] / df_14[4].shift(90)).dropna(), columns=['PCR'])
        self.wrangled_data = df_res


# testing
if __name__ == '__main__':
    # running this as of higher dir
    import os
    os.chdir('..')

    p = OILProcessor()
    p.load_raw()
    p.wrangle()
    p.save_pickle()

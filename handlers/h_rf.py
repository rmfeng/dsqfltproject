"""
handler for 3 month treasury bill data
"""
import pandas as pd
import numpy as np
import datetime as dt
from handlers.BaseProcessor import BaseProcessor


class RFProcessor(BaseProcessor):
    # specifications for raw file path and out path:
    NAME = "RF"
    RAW_PATHS = ['raw_data/DTB3.csv']
    OUT_PATH = 'pkl_data/RF.pkl'

    def __init__(self):
        super().__init__(self.RAW_PATHS, self.OUT_PATH)

    def load_raw(self):
        print("Loading data for %s ... " % self.NAME)

        # obtain data
        self.raw_data = pd.read_csv(self.RAW_PATHS[0])

        # obtain dates
        self.raw_data.set_index('DATE',drop=True,inplace=True)
        self.raw_data.index=pd.to_datetime(self.raw_data.index)


    def wrangle(self):
        print("Wrangling data for %s ... " % self.NAME)
        df_RF = self.raw_data
        df_RF_re = df_RF.resample('D').ffill().dropna()
        df_RF_re = df_RF_re.iloc[df_RF_re.index >= '2000-01-01']
        self.wrangled_data = df_RF_re






# testing
if __name__ == '__main__':
    # running this as of higher dir
    import os
    os.chdir('..')

    p = RFProcessor()
    p.load_raw()
    p.wrangle()
    p.save_pickle()

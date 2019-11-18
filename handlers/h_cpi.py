"""
handler for NOS data
"""
import pandas as pd
import numpy as np
import datetime as dt
from handlers.BaseProcessor import BaseProcessor


class CPIProcessor(BaseProcessor):
    # specifications for raw file path and out path:
    NAME = "CPI"
    RAW_PATHS = ['raw_data/cpi/CPIAUCSL.csv']
    OUT_PATH = 'pkl_data/CPI.pkl'

    def __init__(self):
        super().__init__(self.RAW_PATHS, self.OUT_PATH)

    def load_raw(self):
        print("Loading data for %s ... " % self.NAME)
        self.raw_data = pd.read_csv(self.RAW_PATHS[0], parse_dates=['DATE'], index_col='DATE')

    def wrangle(self):
        print("Wrangling data for %s ... " % self.NAME)
        df_cpi = self.raw_data
        df_cpi_re = df_cpi.resample('D').ffill().dropna()
        df_cpi_out = (df_cpi_re / df_cpi_re.shift(365) - 1).dropna()
        self.wrangled_data = df_cpi_out


# testing
if __name__ == '__main__':
    # running this as of higher dir
    import os
    os.chdir('..')

    nos = CPIProcessor()
    nos.load_raw()
    nos.wrangle()
    nos.save_pickle()

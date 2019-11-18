"""
handler for NOS data
"""
import pandas as pd
import numpy as np
from handlers.BaseProcessor import BaseProcessor


class SIProcessor(BaseProcessor):
    # specifications for raw file path and out path:
    NAME = "SI"
    RAW_PATHS = ['raw_data/si/Short_Interest.csv']
    OUT_PATH = 'pkl_data/SI.pkl'

    def __init__(self):
        super().__init__(self.RAW_PATHS, self.OUT_PATH)

    def load_raw(self):
        print("Loading data for %s ... " % self.NAME)
        self.raw_data['si'] = pd.read_csv(self.RAW_PATHS[0], parse_dates=['Date'], index_col='Date').sort_index()

    def wrangle(self):
        print("Wrangling data for %s ... " % self.NAME)
        df = self.raw_data['si']
        si = pd.DataFrame((df['ShortVolume'] / df.rolling(30)['TotalVolume'].mean()).dropna(), columns=['SI'])
        self.wrangled_data = si


# testing
if __name__ == '__main__':
    # running this as of higher dir
    import os
    os.chdir('..')

    p = SIProcessor()
    p.load_raw()
    p.wrangle()
    p.save_pickle()

"""
handler for NOS data
"""
import pandas as pd
import numpy as np
import datetime as dt
from handlers.BaseProcessor import BaseProcessor


class PCRProcessor(BaseProcessor):
    # specifications for raw file path and out path:
    NAME = "PCR"
    RAW_PATHS = ['raw_data/gsci/BDI_GSCI.csv',
                 'raw_data/spx/SP500_prices.csv']
    OUT_PATH = 'pkl_data/PCR.pkl'

    GSCI_COL = 'S&P GSCI Commodity Total Return - RETURN IND. (OFCL)'

    def __init__(self):
        super().__init__(self.RAW_PATHS, self.OUT_PATH)

    def load_raw(self):
        print("Loading data for %s ... " % self.NAME)
        self.raw_data['gsci'] = pd.read_csv(self.RAW_PATHS[0],
                                            parse_dates=['Name'],
                                            index_col='Name')[[self.GSCI_COL]]

        self.raw_data['spx'] = pd.read_csv(self.RAW_PATHS[1],
                                           parse_dates=['Date'],
                                           index_col='Date')[['Close']]

    def wrangle(self):
        print("Wrangling data for %s ... " % self.NAME)
        df1 = self.raw_data['gsci'].resample('D').ffill()
        df2 = self.raw_data['spx'].resample('D').ffill()

        dfj = df1.join(df2, how='inner')
        dfj['PCR'] = np.log(dfj['Close'] / dfj[self.GSCI_COL])

        self.wrangled_data = dfj[['PCR']]


# testing
if __name__ == '__main__':
    # running this as of higher dir
    import os
    os.chdir('..')

    p = PCRProcessor()
    p.load_raw()
    p.wrangle()
    p.save_pickle()

"""
handler for IC data
"""
import pandas as pd
import numpy as np
import datetime as dt
from handlers.BaseProcessor import BaseProcessor


class ICProcessor(BaseProcessor):
    # specifications for raw file path and out path:
    NAME = "IC"
    RAW_PATHS = ['raw_data/implied_correlation_hist.csv']
    OUT_PATH = 'pkl_data/IC.pkl'

    def __init__(self):
        super().__init__(self.RAW_PATHS, self.OUT_PATH)

    def load_raw(self):
        print("Loading data for %s ... " % self.NAME)
        self.row_data['IC']=pd.read_csv(RAW_PATHS[0],skiprows=1)

    def wrangle(self):
        print("Wrangling data for %s ... " % self.NAME)
        IC1=self.row_data['IC']
        del IC1['SPX']
        del IC1['VIX']
        IC1['DATE']=pd.to_datetime(IC1['DATE']).astype(str)
        IC1=IC1[IC1.DATE<='2019-11-05']
        IC1=IC1.set_index('DATE')

        def firstIC(row):
            for i in row:
                try:
                    if(np.isnan(i)):
                        continue
                    else:
                        return i
                except:
                    return
        IC1['IC']=IC1.apply(firstIC,axis=1)

        IC1.index=pd.to_datetime(IC1.index)

        self.wrangled_data = IC1[['IC']]


# testing
if __name__ == '__main__':
    # running this as of higher dir
    import os
    os.chdir('..')

    p = PCRProcessor()
    p.load_raw()
    p.wrangle()
    p.save_pickle()
"""
handler for SIM data
"""
import pandas as pd
import numpy as np
import datetime as dt
from handlers.BaseProcessor import BaseProcessor


class SIMProcessor(BaseProcessor):
    # specifications for raw file path and out path:
    NAME = "SIM"
    RAW_PATHS = ['raw_data/dates.pkl']
    OUT_PATH = 'pkl_data/SIM.pkl'


    def __init__(self):
        super().__init__(self.RAW_PATHS, self.OUT_PATH)

    def load_raw(self):
        print("Loading data for %s ... " % self.NAME)
        self.raw_data['sim'] = pd.read_pickle(self.RAW_PATHS[0])

    def wrangle(self):
        print("Wrangling data for %s ... " % self.NAME)
        # shipping
        dates=self.raw_data['sim']
        dates['Year']=dates.index.strftime('%Y')
        dates['Month']=dates.index.strftime('%m')
        start=dates.groupby(['Year','Month']).apply(lambda x: x.index[1]).reset_index()
        start=start[start['Month']=='05'] #second business day in May
        start=start.set_index('Year')
        start.loc['1990']=['05',pd.to_datetime('1990-05-02')]#insert manually 1990 data

        end=dates[dates['Month']=='10']
        end=end.groupby(['Year','Month']).apply(lambda x: x.index[14]).reset_index() #15th business day in October
        end=end.set_index('Year')

        dates['start']=dates['Year'].apply(lambda x: start.loc[x,0])
        dates['end']=dates['Year'].apply(lambda x: end.loc[x,0])
        dates['in']=(dates.index<=dates['end'])&(dates.index>=dates['start'])

        dates['SIM']=dates['in'].rolling(130).sum().shift(-130)
        self.wrangled_data = dates[['SIM']]


# testing
if __name__ == '__main__':
    # running this as of higher dir
    import os
    os.chdir('..')

    p = NOSProcessor()
    p.load_raw()
    p.wrangle()
    p.save_pickle()

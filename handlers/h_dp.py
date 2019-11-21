"""
handler for DP data from multpl
"""
import pandas as pd
import numpy as np
import datetime as dt
import requests
from bs4 import BeautifulSoup
from handlers.BaseProcessor import BaseProcessor


class DPProcessor(BaseProcessor):
    # specifications for raw file path and out path:
    NAME = "DP"
    RAW_PATHS = ['https://www.multpl.com/s-p-500-dividend/table/by-month','raw_data/spx/SP500_prices.csv']
    OUT_PATH = 'pkl_data/DP.pkl'

    def __init__(self):
        super().__init__(self.RAW_PATHS, self.OUT_PATH)

    def load_raw(self):
        print("Loading data for %s ... " % self.NAME)

        # parse website
        r = requests.get(self.RAW_PATHS[0])
        soup = BeautifulSoup(r.content, 'html5lib')

        # obtain earnings and dates
        DY = [val.text[:5].split('\n')[0] for val in soup.find_all('td', attrs = {'class':'right'})]
        D = [val.text for val in soup.find_all('td', attrs = {'class':'left'})]

        # crate dataframe of earnings
        self.raw_data = pd.DataFrame()
        self.raw_data['D'] = DY
        self.raw_data['DATE'] = D
        self.raw_data.set_index('DATE',drop=True,inplace=True)
        self.raw_data.index=pd.to_datetime(self.raw_data.index)


    def wrangle(self):
        print("Wrangling data for %s ... " % self.NAME)

        # use SP500 prices to obtain PE
        SP500 = pd.read_csv(self.RAW_PATHS[1])
        SP500.drop(columns=['Open','High','Low','Close','Volume'],inplace=True)
        SP500.columns = ['DATE','Adj Close']
        SP500.set_index('DATE',drop=True,inplace=True)
        SP500.index=pd.to_datetime(SP500.index)
        SP500 = SP500.resample('D').ffill().dropna()
        SP500 = SP500.loc[(SP500.index>='1990-06-08') & (SP500.index<='2019-09-30')]
        SP500['Adj Close'] = SP500['Adj Close'].astype(float)

        # forward fill
        df_DP = self.raw_data
        df_DP_re = df_DP.resample('D').ffill().dropna()
        df_DP_re = df_DP_re.loc[df_DP_re.index>='1990-06-08']
        df_DP_re['D'] = df_DP_re['D'].astype(float)

        # compute dividend/price
        fun = lambda t: df_DP_re['D'][t]/SP500['Adj Close'][t]
        DP=[fun(t) for t in range(SP500.shape[0])]
        df_DP_re['DP'] = DP
        df_DP_re.drop(columns=['D'],inplace=True)
        self.wrangled_data = df_DP_re

# testing
if __name__ == '__main__':
    # running this as of higher dir
    import os
    os.chdir('..')

    p = DPProcessor()
    p.load_raw()
    p.wrangle()
    p.save_pickle()

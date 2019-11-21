"""
handler for CAPE data from multpl
"""
import pandas as pd
import numpy as np
import datetime as dt
import requests
from bs4 import BeautifulSoup
from handlers.BaseProcessor import BaseProcessor


class CAPEProcessor(BaseProcessor):
    # specifications for raw file path and out path:
    NAME = "CAPE"
    RAW_PATHS = ['https://www.multpl.com/s-p-500-earnings/table/by-year','raw_data/spx/SP500_prices.csv']
    OUT_PATH = 'pkl_data/CAPE.pkl'

    def __init__(self):
        super().__init__(self.RAW_PATHS, self.OUT_PATH)

    def load_raw(self):
        print("Loading data for %s ... " % self.NAME)

        # parse website
        r = requests.get(self.RAW_PATHS[0])
        soup = BeautifulSoup(r.content, 'html5lib')

        # obtain earnings and dates
        EY = [float(val.text[:7].split('\n')[0]) for val in soup.find_all('td', attrs = {'class':'right'})]
        D = [val.text for val in soup.find_all('td', attrs = {'class':'left'})]

        # crate dataframe of earnings
        self.raw_data = pd.DataFrame()
        self.raw_data['EY'] = EY
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
        SP500 = SP500.loc[(SP500.index>='1990-06-08') & (SP500.index<='2019-06-30')]
        SP500['Adj Close'] = SP500['Adj Close'].astype(float)


        # compute earnings over last 10 years then ffill
        df_CAPE = self.raw_data.iloc[::-1]
        df_CAPE['EY'] = df_CAPE['EY'].rolling(10).sum().dropna()

        df_CAPE_re = df_CAPE.resample('D').ffill().dropna()
        df_CAPE_re = df_CAPE_re.loc[df_CAPE_re.index >= '1990-06-08']

        print(df_CAPE_re.head())

        # compute price/average last 10 years earnings
        fun = lambda t: SP500['Adj Close'][t]/(df_CAPE_re['EY'][t]/10)
        CAPE=[fun(t) for t in range(SP500.shape[0])]
        df_CAPE_re['CAPE'] = CAPE
        df_CAPE_re.drop(columns=['EY'],inplace=True)
        self.wrangled_data = df_CAPE_re

# testing
if __name__ == '__main__':
    # running this as of higher dir
    import os
    os.chdir('..')

    p = CAPEProcessor()
    p.load_raw()
    p.wrangle()
    p.save_pickle()

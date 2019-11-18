"""
handler for NOS data
"""
import pandas as pd
import numpy as np
import datetime as dt
from handlers.BaseProcessor import BaseProcessor


class NOSProcessor(BaseProcessor):
    # specifications for raw file path and out path:
    NAME = "NOS"
    RAW_PATHS = ['raw_data/nos/naicsvsp.xls',
                 'raw_data/nos/vsp.xls',
                 'raw_data/nos/naicsnop.xls',
                 'raw_data/nos/nop.xls']
    OUT_PATH = 'pkl_data/NOS.pkl'

    # other constants to use
    DATA_COLUMNS = ['ticker', 'year'] + list(range(1, 13))

    def __init__(self):
        super().__init__(self.RAW_PATHS, self.OUT_PATH)

    def load_raw(self):
        print("Loading data for %s ... " % self.NAME)
        self.raw_data['vsp'] = pd.read_excel(self.RAW_PATHS[0], header=None)
        self.raw_data['vsp'].columns = self.DATA_COLUMNS
        self.raw_data['vsp_old'] = pd.read_excel(self.RAW_PATHS[1], header=None)
        self.raw_data['vsp_old'].columns = self.DATA_COLUMNS
        self.raw_data['nop'] = pd.read_excel(self.RAW_PATHS[2], header=None)
        self.raw_data['nop'].columns = self.DATA_COLUMNS
        self.raw_data['nop_old'] = pd.read_excel(self.RAW_PATHS[3], header=None)
        self.raw_data['nop_old'].columns = self.DATA_COLUMNS

    def wrangle(self):
        print("Wrangling data for %s ... " % self.NAME)
        # shipping
        df_nos_ship = self.raw_data['vsp']
        df_nos_mdm = df_nos_ship[df_nos_ship['ticker'] == 'AMDMVS'].drop('ticker', axis=1)
        df_nos_mt = df_nos_mdm.melt(id_vars=['year'])
        df_nos_mt['knowledge_dt'] = df_nos_mt.apply(lambda row:
                                                    get_knowledge_dt(row['year'], row['variable']),
                                                    axis=1)
        df_ship_res = df_nos_mt.set_index('knowledge_dt')[['value']].rename(columns={'value':
                                                                                     'shipments'}).sort_index()

        # old shipping
        df_old_ship = self.raw_data['vsp_old']
        df_old_mdm = df_old_ship[df_old_ship['ticker'] == 'AMDMVS'].drop('ticker', axis=1)
        df_old_mt = df_old_mdm.melt(id_vars=['year'])
        df_old_mt['knowledge_dt'] = df_old_mt.apply(lambda row:
                                                    get_knowledge_dt(row['year'], row['variable']),
                                                    axis=1)
        df_old_res = df_old_mt.set_index('knowledge_dt')[['value']].rename(columns={'value':
                                                                                    'old_shipments'}).sort_index()

        # combining
        df_ship_combined = df_old_res.join(df_ship_res, how='outer')
        df_ship_combined['filled_shipments'] = df_ship_combined.apply(lambda row:
                                                                      row['old_shipments']
                                                                      if pd.isnull(row['shipments'])
                                                                      else row['shipments'],
                                                                      axis=1)

        # orders
        df_nos_orders = self.raw_data['nop']
        df_order_mdm = df_nos_orders[df_nos_orders['ticker'] == 'AMDMNO'].drop('ticker', axis=1)
        df_order_mt = df_order_mdm.melt(id_vars=['year'])
        df_order_mt['knowledge_dt'] = df_order_mt.apply(lambda row:
                                                        get_knowledge_dt(row['year'], row['variable']),
                                                        axis=1)
        df_order_res = df_order_mt.set_index('knowledge_dt')[['value']].rename(columns={'value':
                                                                                        'orders'}).sort_index()

        # old orders
        df_old_order = self.raw_data['nop_old']
        df_old_mdm_order = df_old_order[df_old_order['ticker'] == 'AMDMNO'].drop('ticker', axis=1)
        df_omdo = df_old_mdm_order.melt(id_vars=['year'])
        df_omdo['knowledge_dt'] = df_omdo.apply(lambda row:
                                                get_knowledge_dt(row['year'], row['variable']),
                                                axis=1)
        df_or_order = df_omdo.set_index('knowledge_dt')[['value']].rename(columns={'value':
                                                                                   'old_orders'}).sort_index()

        df_order_combined = df_order_res.join(df_or_order, how='outer')

        df_order_combined['filled_orders'] = df_order_combined.apply(lambda row:
                                                                     row['old_orders']
                                                                     if pd.isnull(row['orders'])
                                                                     else row['orders'],
                                                                     axis=1)

        # final df
        df_comb_final = df_order_combined[['filled_orders']].join(df_ship_combined[['filled_shipments']]).dropna()
        df_comb_final['nos'] = np.log(df_comb_final['filled_orders'] / df_comb_final['filled_shipments'])
        self.wrangled_data = df_comb_final[['nos']]


def get_knowledge_dt(year, month):
    if month != 12:
        return dt.date(year, month + 1, 25)
    else:
        return dt.date(year + 1, 1, 25)


# testing
if __name__ == '__main__':
    # running this as of higher dir
    import os
    os.chdir('..')

    nos = NOSProcessor()
    nos.load_raw()
    nos.wrangle()
    nos.save_pickle()

"""
handler for PCAPrice data
"""
import pandas as pd
import numpy as np
import datetime as dt
from handlers.BaseProcessor import BaseProcessor
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


class PCAPriceProcessor(BaseProcessor):
    # specifications for raw file path and out path:
    NAME = "PCAPrice"
    RAW_PATHS = ['pkl_data/DP.pkl','pkl_data/PE.pkl','pkl_data/BM.pkl','pkl_data/CAPE.pkl']
    OUT_PATH = 'pkl_data/PCAPrice.pkl'

    def __init__(self):
        super().__init__(self.RAW_PATHS, self.OUT_PATH)

    def load_raw(self):
        print("Loading data for %s ... " % self.NAME)

        # obtain data for DP, PE, BM, CAPE
        df_DP = pd.read_pickle(self.RAW_PATHS[0])
        df_PE = pd.read_pickle(self.RAW_PATHS[1])
        df_BM = pd.read_pickle(self.RAW_PATHS[2])
        df_CAPE = pd.read_pickle(self.RAW_PATHS[3])
        self.raw_data = pd.concat([df_DP,df_PE,df_BM,df_CAPE],axis=1)


    def wrangle(self):
        print("Wrangling data for %s ... " % self.NAME)

        # proceed to PCA
        features = ['DP','PE','BM','CAPE']
        x = self.raw_data[features].fillna(0)
        x = StandardScaler().fit_transform(x)
        pca = PCA(n_components=1)
        principalComponents = pca.fit_transform(x)
        self.wrangled_data = pd.DataFrame(data = principalComponents,columns = ['PCAPrice'])
        self.wrangled_data.index = self.raw_data.index




# testing
if __name__ == '__main__':
    # running this as of higher dir
    import os
    os.chdir('..')

    p = PCAPriceProcessor()
    p.load_raw()
    p.wrangle()
    p.save_pickle()

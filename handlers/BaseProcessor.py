"""
Parent Class for processing raw data

each handler will take raw data from the raw_data folder and wrangle it into the required format,
then save it into out_data folder
"""
import pandas as pd
from abc import ABC, abstractmethod

DATE_COL = 'AsOfDate'


class BaseProcessor(ABC):
    NAME = 'BASE'

    def __init__(self, raw_data_paths, out_path):
        """
        takes data from the raw_data_path, wrangles it and saves it to the out_path
        :param raw_data_paths:
        :param out_path:
        """
        self.raw_data_paths = raw_data_paths
        self.out_path = out_path
        self.raw_data = {}
        self.wrangled_data = None

    def run(self):
        """ executes self containing logic """
        self.load_raw()
        self.wrangle()
        self.save_pickle()

    @abstractmethod
    def load_raw(self):
        """ loads data and puts it into .raw_data for use in the .wrangle method """
        pass

    @abstractmethod
    def wrangle(self):
        """ wrangles all of the data and puts only to-export results into the .wrangled_data dataframe """
        pass

    def run_all(self):
        """ load, wrangle and save data """
        self.load_raw()
        self.wrangle()
        self.save_pickle()

    def save_pickle(self):
        """ standardize the index and column names """
        if self.wrangled_data is None:
            print("Unable to save pickle, the data has not been wrangled, try running the .wrangle() method ...")
        self.wrangled_data.index.name = DATE_COL  # consistent index name
        self.wrangled_data.index = pd.DatetimeIndex(self.wrangled_data.index)
        self.wrangled_data.columns = [self.NAME]
        self.wrangled_data.to_pickle(self.out_path)

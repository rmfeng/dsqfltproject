"""
main class for the management of all of the timeseries data
"""
import pandas as pd
import handlers
from handlers.BaseProcessor import DATE_COL  # string name of the date column to enforce consistency


class TSManager:
    OUR_DIR = 'pkl_data/'
    DATE_PKL = 'dates.pkl'

    def __init__(self):
        self.handlers = {}
        self._load_handlers()
        self.data = None

    def load(self):
        """ loads all of the resulting data from the handlers """
        self.data = pd.read_pickle(self.DATE_PKL)
        self.data.index.name = DATE_COL

        for hname, h in self.handlers.items():
            print("Loading %s" % hname)
            cur_out = h.out_path
            df = pd.read_pickle(cur_out).resample('D').ffill()  # make daily and forward fill the values
            if hname in self.data.columns:
                # getting to a distinct column:
                i = 2
                while "%s_%s" % (hname, i) in self.data.columns:
                    i += 1
                print("warning: %s was already in the data set, instead we merged new column as %s" %
                      (hname, hname + '_%s' % i))
                self.data = self.data.join(df, how='left', rsuffix="_%s" % i)
            else:
                self.data = self.data.join(df, how='left')

    def _load_handlers(self):
        for h in handlers.ALL_HANDLERS:
            self.handlers[h.NAME] = h

    def rewrangle_data(self, to_wrangle=None):
        """ reprocess the data for a specific handler, or if to_wrangle is None, then all of them """
        if to_wrangle is None:
            for hname, h in self.handlers.items():
                h.run_all()
        elif to_wrangle in self.handlers.keys():
            self.handlers[to_wrangle].run_all()
        else:
            print("Cannot wrangle %s as the handler was not found in self.handlers" % to_wrangle)


if __name__ == '__main__':
    for handle in handlers.ALL_HANDLERS:
        print(handle.NAME)

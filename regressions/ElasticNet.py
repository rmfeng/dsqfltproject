import handlers
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import ElasticNet

class _ElasticNet:

    def __init__(self, _alpha=0.001, _l1_ratio=0.25, _max_iter=10000, R_130=None):
        self.en = ElasticNet(alpha=_alpha, l1_ratio=_l1_ratio, max_iter=_max_iter)
        self.si = SimpleImputer(strategy='median')

    def fit(self,X,y):
        self.en.fit(X, y)

    def predict(self,X):
        X = self.si.fit_transform(X)
        return self.en.predict(X)


class ENPredictor:

    def __init__(self, data, _alpha=0.001, _l1_ratio=0.25, _max_iter=10000):

        self.data = data
        si = SimpleImputer(strategy='median')
        self.X = si.fit_transform(np.array(data[[handle.NAME for handle in handlers.ALL_HANDLERS if handle.NAME not in ['SPX','RF','spx_tp130']]]))
        self.y = si.fit_transform(np.array(data[['spx_tp130']]))

    def predict(self,nb_periods):

        p = []
        sft = [self.X.shape[1] for k in range(nb_periods)]
        for t in range(nb_periods):

            X = self.X[20*t:(2520+20*t),:]
            next_X = self.X[(2520+20*t):(2540+20*t),:]
            y = self.y[20*t:(2520+20*t)]

            EN = _ElasticNet(_alpha=0.001, _l1_ratio=0.25, _max_iter=10000)
            EN.fit(X,y)

            for el in EN.predict(next_X):
                p.append(el)

        return p,self.y[2520:(2540+20*(nb_periods-1))],sft

    def plot_predict(self,nb_periods):

        p,ytrue,sft = self.predict(nb_periods)

        plt.figure(figsize=(15,5))
        plt.plot(self.data.index[2520:(2520+nb_periods*20)],np.cumsum(p),label='Elastic Net')
        plt.plot(self.data.index[2520:(2520+nb_periods*20)],np.cumsum(ytrue),label='True')
        plt.title('Linear regression for predicting forward 130-day returns')
        plt.legend()
        plt.show()

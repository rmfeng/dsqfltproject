import handlers
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.impute import SimpleImputer

class KitchenSinkRegressions:

    def __init__(self,threshold=0.1,R_130=None):
        self.threshold = threshold
        self.R_130 = R_130
        self.si = SimpleImputer(strategy='median')

    def fit(self,X,y):
        self.reg = LinearRegression().fit(X, y)

    def predict(self,X):
        X = self.si.fit_transform(X)
        return self.reg.predict(X)


class KSPredictor:

    def __init__(self,data,threshold=0.1):

        self.threshold = threshold
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

            KSR = KitchenSinkRegressions(self.threshold)
            KSR.fit(X,y)

            for el in KSR.predict(next_X):
                p.append(el[0])

        return p,self.y[2520:(2540+20*(nb_periods-1))],sft

    def plot_predict(self,nb_periods):

        p,ytrue,sft = self.predict(nb_periods)

        plt.figure(figsize=(15,5))
        plt.plot(self.data.index[2520:(2520+nb_periods*20)],np.cumsum(p),label='Kitchen Sink')
        plt.plot(self.data.index[2520:(2520+nb_periods*20)],np.cumsum(ytrue),label='True')
        plt.title('Linear regression for predicting forward 130-day returns')
        plt.legend()
        plt.show()

    def plot_screened_ft(self,nb_periods):

        p,ytrue,sft = self.predict(nb_periods)
        msft = [self.X.shape[1] for k in range(nb_periods*20)]
        plt.figure(figsize=(15,5))
        plt.plot(self.data.index[2520:(2520+nb_periods*20)],msft,label='Screened Features')
        plt.ylim(3,20)
        plt.title('Number of features used')
        plt.legend()
        plt.show()

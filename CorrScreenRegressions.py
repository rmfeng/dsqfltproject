import handlers
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

class CorrScreenRegressions:

    def __init__(self,threshold=0.1,R_130=None):
        self.threshold = threshold
        self.R_130 = R_130

    def fit(self,X,y):

        X = X.T

        # screen variables: measure pairwise correlation between X(t) and y(t+130)
        if self.R_130 is None:
            self.R_130 = [y[i:i+130].sum() for i in range(X.shape[1]-130)]

        screened_ft = [i for i in range(X.shape[0]) if abs(np.corrcoef(np.array([X[i,:-130],self.R_130]))[0,1])>self.threshold]
        self.screened_ft = screened_ft

        # fit
        self.reg = LinearRegression().fit(X[screened_ft,:].T, y)

    def predict(self,X):
        X = X.T
        return self.reg.predict(X[self.screened_ft,:].T)

    def return_screened_ft(self):
        return self.screened_ft

class CorrScreenPredictor:

    def __init__(self,data,threshold=0.1):
        self.threshold = threshold
        self.data = data
        self.X = np.array(data[[handle.NAME for handle in handlers.ALL_HANDLERS if handle.NAME != 'SPX']])
        self.y = np.array(data[['SPX']])

    def predict(self,nb_periods):

        p = []
        sft = []

        for t in range(nb_periods):

            X = self.X[20*t:(2520+20*t),:]
            next_X = self.X[(2520+20*t):(2540+20*t),:]
            y = self.y[20*t:(2520+20*t)]

            CSR = CorrScreenRegressions(self.threshold)
            CSR.fit(X,y)
            sft.append(CSR.return_screened_ft())

            for el in CSR.predict(next_X):
                p.append(el[0])

        return p,self.y[2520:(2540+20*(nb_periods-1))],sft

    def plot_predict(self,nb_periods):

        p,ytrue,sft = self.predict(nb_periods)

        plt.figure(figsize=(15,5))
        plt.plot(self.data.index[2520:(2520+nbp*20)],np.cumsum(p),label='screened ft')
        plt.plot(self.data.index[2520:(2520+nbp*20)],np.cumsum(ytrue),label='true')
        plt.title('linear regression for predicting returns')
        plt.legend()
        plt.show()

    def plot_screened_ft(self,nb_periods):

        p,ytrue,sft = self.predict(nb_periods)
        msft = []
        for i in range(nb_periods):
            for k in range(20):
                msft.append(len(sft[i]))
        plt.figure(figsize=(15,5))
        plt.plot(self.data.index[2520:(2520+nbp*20)],msft,label='screened ft')
        plt.ylim(0,17)
        plt.title('Number of features used')
        plt.legend()
        plt.show()

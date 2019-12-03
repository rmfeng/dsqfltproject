import handlers
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import pandas as pd

class CorrScreenRegressions:

    def __init__(self,threshold=0.1,R_130=None):
        self.threshold = threshold
        self.R_130 = R_130

    def fit(self,X,y):

        X = X.T

        # screen variables: measure pairwise correlation between X(t) and y(t+130)
        if self.R_130 is None:
            self.R_130 = pd.DataFrame(y).dropna().iloc[:,0].tolist()

        screened_ft = [i for i in range(X.shape[0]) if abs(np.corrcoef(np.array([X[i,:],self.R_130]))[0,1])>self.threshold]
        self.screened_ft = screened_ft

        # fit
        self.reg = LinearRegression().fit(X[screened_ft,:].T, y)

    def predict(self,X):
        X = X.T
        return self.reg.predict(X[self.screened_ft,:].T)

    def return_screened_ft(self):
        return self.screened_ft

class CorrScreenPredictor:

    def __init__(self,data,RealTime=False,threshold=0.1):

        self.threshold = threshold
        self.data = data
        self.RealTime = RealTime
        self.X = np.array(self.data[[handle.NAME for handle in handlers.ALL_HANDLERS if handle.NAME not in ['SPX','RF','spx_tp130']]])
        self.y = np.array(self.data[['spx_tp130']])

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

    def predictRT(self,nb_periods):

        # same method as predict but with the following constraints

        # constraints:
        # BDI has been known at least since January 2011 <=> t > 5184
        # NOS was discovered in December 2008 <=> t > 4658
        # OIL was first mentioned as a predictor of equity returns in 2005 <=> t > 3673
        # PCR was found in late 2014 <=> t > 6105
        # PCA-tech was first used as a return predictor in 2010 <=> t > 4932


        p = []
        sft = []

        for t in range(nb_periods):

            ft_to_use = self.RTfeatures(2520+20*t)

            X = self.X[20*t:(2520+20*t),ft_to_use]
            next_X = self.X[(2520+20*t):(2540+20*t),ft_to_use]
            y = self.y[20*t:(2520+20*t)]

            CSR = CorrScreenRegressions(self.threshold)
            CSR.fit(X,y)
            sft.append(CSR.return_screened_ft())

            for el in CSR.predict(next_X):
                p.append(el[0])

        return p,self.y[2520:(2540+20*(nb_periods-1))],sft

    def RTfeatures(self,idx):

        # splits the periods in order to use only
        # features available at the current time

        # periods: 0 > 3673 > 4658 > 4932 > 5184 > 6105

        all_ft = self.data[[handle.NAME for handle in handlers.ALL_HANDLERS if handle.NAME not in ['SPX','RF','spx_tp130']]].columns.tolist()

        if idx <= 3673:
            # PCR, BDI, PCA-tech, NOS and OIL still unknown
            ix = [all_ft.index('PCR'),all_ft.index('BDI'),all_ft.index('NOS'),all_ft.index('OIL')]
        elif (idx > 3673) and (idx <= 4658):
            # PCR, BDI, PCA-tech and NOS still unknown
            ix = [all_ft.index('PCR'),all_ft.index('BDI'),all_ft.index('NOS'),all_ft.index('OIL')]
        elif (idx > 4658) and (idx <= 4932):
            # PCR, BDI and PCA-tech still unknown
            ix = [all_ft.index('PCR'),all_ft.index('BDI'),all_ft.index('NOS')]
        elif (idx > 4932) and (idx <= 5184):
            # PCR and BDI still unknown
            ix = [all_ft.index('PCR'),all_ft.index('BDI')]
        elif (idx > 5184) and (idx <= 6105):
            # PCR still unknown
            ix = [all_ft.index('PCR')]
        else:
            # all ft discovered
            ix = []

        return [k for k in range(self.X.shape[1]) if k not in ix]


    def plot_predict(self,nb_periods):

        if not self.RealTime:
            p,ytrue,sft = self.predict(nb_periods)
            lbl = 'Correlation Screening'
        else:
            p,ytrue,sft = self.predictRT(nb_periods)
            lbl = 'Real Time Correlation Screening'

        plt.figure(figsize=(15,5))
        plt.plot(self.data.index[2520:(2520+nb_periods*20)],np.cumsum(p),label=lbl)
        plt.plot(self.data.index[2520:(2520+nb_periods*20)],np.cumsum(ytrue),label='True')
        plt.title('Linear regression for predicting forward 130-day returns')
        plt.legend()
        plt.show()

    def plot_screened_ft(self,nb_periods):

        if not self.RealTime:
            p,ytrue,sft = self.predict(nb_periods)
            lbl = 'Correlation Screening'
        else:
            p,ytrue,sft = self.predictRT(nb_periods)
            lbl = 'Real Time Correlation Screening'

        msft = []
        for i in range(nb_periods):
            for k in range(20):
                msft.append(len(sft[i]))
        fig = plt.figure(figsize=(15,5))
        plt.plot(self.data.index[2520:(2520+nb_periods*20)],msft,label=lbl)
        plt.ylim(0,17)
        plt.title('Number of features used')
        plt.legend()
        fig.savefig('../images/'+lbl.replace(' ','')+'_features.png', dpi=fig.dpi)
        plt.show()

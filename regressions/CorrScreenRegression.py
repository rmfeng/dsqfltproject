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

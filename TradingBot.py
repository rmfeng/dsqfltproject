import handlers
from CorrScreen import CorrScreenPredictor
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class TradingBot:

    # index:             daily positions in SPX
    # update frequency:  positions are adjusted each time the return forecast change exceeds 10%
    # size:              eight times expected equity premium
    # caps:              strategy caped at 150% long / 50% short

    def __init__(self,data,threshold=0.1):
        self.threshold = threshold
        self.data = data
        rf = data['RF'][2520:].dropna().tolist()
        rf = filter(lambda s: s != '.', rf)
        self.rf = [float(s) for s in rf]
        #self.rf = [float(s)*20/252 for s in rf]


    def _rf(self,nb_periods):
        #
        # used to compute equity risk premium (predicted_return - 90-day Treasury Bill)
        #
        return self.rf[:20*nb_periods]

    def cap_pos(self,pos_list):
        #
        # bounds positions in [-0.5,1.5]
        #
        for i in range(len(pos_list)):
            if pos_list[i]>1.5:
                pos_list[i]=1.5
            elif pos_list[i]<-0.5:
                pos_list[i]=-0.5
        return pos_list

    def create_pos(self,predictions,nb_periods):
        #
        # creates positions as eight times expected premium
        # > positions are rounded to the nearest 10% (see appendix B) using round(*,1)
        #

        # compute risk free rate
        rf = self._rf(nb_periods)

        # return eight times expected premium, rounded to the nearest 10%
        return [round(8*(predictions[i]-rf[i]),1) for i in range(len(predictions))]

    def comp_stats(self,spx_buy_hold,strat_rt,nb_periods):
        years = nb_periods*20/252
        annual_return = 100*(strat_rt.iloc[-1,0]/strat_rt.iloc[0,0] - 1)/years
        annual_return_spx = 100*(spx_buy_hold[-1]/spx_buy_hold[0])/years
        print('------------------------------')
        print('number of years    :',round(years,2))
        print('annual return SPX  :',round(annual_return_spx,2),'%')
        print('annual return strat:',round(annual_return,2),'%')
        print('------------------------------')


    def CS_pos(self,nb_periods):

        #
        # computes positions for correlation screening
        #

        # compute predictions
        CSP = CorrScreenPredictor(self.data,self.threshold)
        __p,ytrue,sft = CSP.predict(nb_periods)

        # log returns to returns
        _p = np.exp(__p)

        #plt.hist(_p,bins=50)
        #plt.title('returns distribution')
        #plt.plot(self.data.index[2520:(2520+nb_periods*20)],_p)
        #plt.show()

        #plt.hist(p,bins=50)
        #plt.title('premium distribution')
        #plt.plot(self.data.index[2520:(2520+nb_periods*20)],p)
        #plt.show()

        # create positions
        pos = self.create_pos(_p,nb_periods)

        # cap positions
        return self.cap_pos(pos)

    def plot_wealth_CS(self,nb_periods):

        # compute positions
        CS_pos = self.CS_pos(nb_periods)

        # timeline
        timeline = self.data.index[2520:(2520+nb_periods*20)]

        # spx buy and hold
        spx_buy_hold = np.exp(self.data['SPX'][2520:(2520+nb_periods*20)].cumsum())

        # strategy
        strat_rt = pd.DataFrame([1 + (CS_pos[i] * (np.exp(self.data['SPX'][2520:(2520+nb_periods*20)][i]) - 1)) for i in range(len(CS_pos))]).cumprod()

        # print stats
        self.comp_stats(spx_buy_hold,strat_rt,nb_periods)

        # plot
        plt.figure(figsize=(15,5))
        plt.plot(timeline,strat_rt,label='Correlation Screening')
        plt.plot(timeline,spx_buy_hold,label='SPX buy and hold')
        plt.title('Comparison between strategy and SPX')
        plt.legend()
        plt.show()

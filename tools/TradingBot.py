import handlers
from CorrScreen import CorrScreenPredictor
from KitchenSink import KSPredictor
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
        self.rf = self.data['RF'][2520:].tolist()

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

        fact = (130/90)*(1/100)

        # return eight times expected premium, rounded to the nearest 10%
        # log returns are first transformed to returns by np.exp(*)-1
        return [round(8*((np.exp(predictions[i])-1)-(np.exp(rf[i])-1)*fact),1) for i in range(len(predictions))]

    def comp_stats(self,spx_buy_hold,strat_rt,nb_periods):

        # time
        years = nb_periods*20/252

        # returns
        annual_return = 100*(strat_rt.iloc[-1,0]-1)/years
        annual_return_spx = 100*(spx_buy_hold[-1]-1)/years

        # bond returns (first switch log returns to returns)
        bond_rt = np.exp(pd.DataFrame(self._rf(nb_periods),columns=['rt'])) - 1
        bond_rt = bond_rt.dropna().iloc[:,0].tolist()

        # spx premium computation (first switch log returns to retruns)
        spx_rt = np.exp(self.data['SPX'][2520:(2520+nb_periods*20)])-1
        spx_rt = spx_rt.dropna().tolist()
        spx_prem = [spx_rt[i]-bond_rt[i] for i in range(len(bond_rt))]

        # strategy premium
        strat_rt = np.exp(strat_rt) - 1
        strat_rt = strat_rt.dropna().iloc[:,0].tolist()
        strat_prem = [strat_rt[i]-bond_rt[i] for i in range(len(bond_rt))]

        # sharpe
        spx_sharpe = np.mean(spx_prem)/np.std(spx_rt)
        strat_sharpe = np.mean(strat_prem)/np.std(strat_rt)

        # disp
        print('-----------------------------------------------')
        print('number of years    :',round(years,2))
        print('annual return SPX  :',round(annual_return_spx,2),'%  |  Sharpe:',round(spx_sharpe,2))
        print('annual return strat:',round(annual_return,2),'%  |  Sharpe:',round(strat_sharpe,2))
        print('-----------------------------------------------')


    def KS_pos(self,nb_periods):

        #
        # computes positions for kitchen sink regression
        #

        # compute predictions
        KSP = KSPredictor(self.data,self.threshold)
        _p,ytrue,sft = KSP.predict(nb_periods)

        # create positions
        pos = self.create_pos(_p,nb_periods)

        # cap positions
        return self.cap_pos(pos)

    def plot_wealth_KS(self,nb_periods):

        # compute positions
        KS_pos = self.KS_pos(nb_periods)

        # timeline
        timeline = self.data.index[2520:(2520+nb_periods*20)]

        # spx buy and hold
        spx_buy_hold = np.exp(self.data['SPX'][2520:(2520+nb_periods*20)]).cumprod()

        # strategy
        strat_rt = pd.DataFrame([1 + (KS_pos[i] * (np.exp(self.data['SPX'][2520:(2520+nb_periods*20)][i]) - 1)) for i in range(len(KS_pos))]).cumprod()

        # print stats
        self.comp_stats(spx_buy_hold,strat_rt,nb_periods)

        # plot
        plt.figure(figsize=(15,5))
        plt.plot(timeline,strat_rt,label='Kitchen Sink')
        plt.plot(timeline,spx_buy_hold,label='SPX buy and hold')
        plt.title('Comparison between Kitchen Sink and buy-and-hold SPX')
        plt.legend()
        plt.show()


    def CS_pos(self,nb_periods,RealTime=False):

        #
        # computes positions for correlation screening
        #

        # compute predictions
        CSP = CorrScreenPredictor(self.data,RealTime,self.threshold)

        if not RealTime:
            p,ytrue,sft = CSP.predict(nb_periods)
        else:
            p,ytrue,sft = CSP.predictRT(nb_periods)

        # create positions
        pos = self.create_pos(p,nb_periods)

        # cap positions
        return self.cap_pos(pos)

    def plot_wealth_CS(self,nb_periods,RealTime=False):

        # compute positions
        CS_pos = self.CS_pos(nb_periods,RealTime)

        # timeline
        timeline = self.data.index[2520:(2520+nb_periods*20)]

        # spx buy and hold
        spx_buy_hold = np.exp(self.data['SPX'][2520:(2520+nb_periods*20)]).cumprod()

        # strategy
        strat_rt = pd.DataFrame([1 + (CS_pos[i] * (np.exp(self.data['SPX'][2520:(2520+nb_periods*20)][i]) - 1)) for i in range(len(CS_pos))]).cumprod()

        # print stats
        self.comp_stats(spx_buy_hold,strat_rt,nb_periods)

        # plot
        lbl = 'Correlation Screening'
        if RealTime:
            lbl = 'Real Time '+lbl
        plt.figure(figsize=(15,5))
        plt.plot(timeline,strat_rt,label=lbl)
        plt.plot(timeline,spx_buy_hold,label='SPX buy and hold')
        plt.title('Comparison between '+lbl+' and buy-and-hold SPX')
        plt.legend()
        plt.show()

    def plot_wealth_all(self,nb_periods):

        # compute positions
        KS_pos = self.KS_pos(nb_periods)
        CS_pos = self.CS_pos(nb_periods)
        RTCS_pos = self.CS_pos(nb_periods,RealTime=True)

        # timeline
        timeline = self.data.index[2520:(2520+nb_periods*20)]

        # spx buy and hold
        spx_buy_hold = np.exp(self.data['SPX'][2520:(2520+nb_periods*20)]).cumprod()

        # strategy
        ks = pd.DataFrame([1 + (KS_pos[i] * (np.exp(self.data['SPX'][2520:(2520+nb_periods*20)][i]) - 1)) for i in range(len(KS_pos))]).cumprod()
        cs = pd.DataFrame([1 + (CS_pos[i] * (np.exp(self.data['SPX'][2520:(2520+nb_periods*20)][i]) - 1)) for i in range(len(CS_pos))]).cumprod()
        rtcs = pd.DataFrame([1 + (RTCS_pos[i] * (np.exp(self.data['SPX'][2520:(2520+nb_periods*20)][i]) - 1)) for i in range(len(RTCS_pos))]).cumprod()

        # plot
        plt.figure(figsize=(15,5))
        plt.plot(timeline,ks,label='Kitchen Sink')
        plt.plot(timeline,cs,label='Correlation Screening')
        plt.plot(timeline,rtcs,label='Real Time Correlation Screening')
        plt.plot(timeline,spx_buy_hold,label='SPX buy and hold')
        plt.title('Comparison between all strategies and buy-and-hold SPX')
        plt.legend()
        plt.show()

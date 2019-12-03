# Market Timing Strategy

### Team members
- Jialu Xie
- Rong Feng
- Karl Dessenne (karld@nyu.edu)

### Files 
- The handlers folder contains scripts that load and wrangle the raw data (either from .csv files saved in the raw_data folder or scraped online from a number of websites) and saved the wrangled data in .pkl format in the pkl_data folder
- The pkl_data folder contains all features described in section 2 of Hull and Qiao independently pickled, resulting from running handlers
- The tools folder contains tools used to run handlers (TSManager) and compute positions and P&Ls of the different strategies (TradingBot)


### Fields 
- ***pkl_data/train_prepared.pkl*** is the pickled dataframe containing engineered features used in the following methods, the fields are named according to what thet represent, the descriptions can be found in section 2 of Hull and Qiao
- ***pkl_data/test_prepared.pkl*** is of the same format but concerns an ulterior period (from 2015)

### Running solutions
- The folder /notebooks contains different notebooks that rely on the infrastructure mentioned above to plot statistics on the features as well as positions and wealth accumulations for the different models
- ***corr_screening_regression.ipynb*** runs the kitchen sink regression, as well as the (real time) correlation screening regression(s) showing features used, positions, and compounded wealth


# Analyst Earnings Forecasts

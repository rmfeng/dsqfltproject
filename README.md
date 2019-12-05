### Team members
- Jialu Xie
- Rong Feng
- Karl Dessenne (karld@nyu.edu)

# Market Timing Strategy

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

### Files 
- The handlers folder contains scripts that load and wrangle the raw data (either from .csv files saved in the raw_data folder or scraped online from a number of websites) and saved the wrangled data in .pkl format in the pkl_data folder


### Fields 
- ***pkl_data_2/before_1989.pkl*** is the pickled dataframe containing price time series from -30 to 30 days after erning announcements. Prices are normalized that price at erning announcement date is 1. Index of the dataframe is [ticker, announcement date, quarter number].
- ***pkl_data_2/after_1989.pkl*** is of the same format but concerns periods after 1989
- ***pkl_data_2/df_forecast.pkl*** is the pickled dataframe containing analysts' erning forecast, indexed with [ticker, accounting period, quarter number, analyst id]
- ***pkl_data_2/df_actual.pkl*** is the pickled dataframe containing actual return, also including erning surprice metrics and forecast distribution metrics. The definition of these metrics are commentted in part2_data_analysis.ipynb. Indexed with [ticker, accounting period, quarter number, analyst id]
- ***pkl_data_2/merged_data.pkl*** is the pickled dataframe, merged from df_actual and price time series (before_1989.pkl and after_1989.pkl). Records with either missing prices or missing forecasts are dropped.

### Running solutions
- The part2_data_analysis.ipynb in notebooks folder contains data process and analysis, including definitions of different erning surprise metrics and forecast distribution metrics.

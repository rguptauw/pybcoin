"""
    Module name: btc_model
    Description: Module for predicting bitcoin price direction based on
    external regressors and bitcoin time series.
"""

# importing modules
import pandas as pd
import numpy as np
from fbprophet import Prophet
from sklearn.linear_model import LinearRegression
import datetime
import csv

# suppressing pandas warnings
pd.options.mode.chained_assignment = None

# defining BTC prediction class object


class BtcModelPrediction(object):

    """
        Class object for predicting bitcoin prices from 2 techniques:
            1. Time Series prediction
            2. Linear Regression
        The prediction is done taking into account all the historical data.
            :member attributes: in_path_btc: input path for BTC prices
                                in_path_comm: input path for commodity prices
                                in_path_gtrends: input path for Google search
                                                trends
                                out_path: output path for writing to a csv file
    """

    # constructor function
    def __init__(self, params):
        self.in_path_btc = dic_temp['in_path_btc']
        self.in_path_comm = dic_temp['in_path_comm']
        self.in_path_gtrends = dic_temp['in_path_gtrends']
        self.out_path = dic_temp['out_path']

    # function to create a time series prediction
    def time_prediction(self):
        """
            Method to predict the BTC price for one day based on historical
            prices. Uses a library 'prophet' made open-source by Facebook.
            The library gives a confidence interval, and seperately provides
            trend and seasonality.
            : param self
            :return future['yhat'](float)
                    error_val(int)
        """
        error_val = -1
        try:
            btc_data = pd.read_csv(self.in_path_btc + 'btc_price.csv')

            # creating a current btc price for later use
            self.curr_price = btc_data['btc_price'].iloc[-1]

            # today's date for further use
            self.today_date = btc_data['utc_time'].iloc[-1]

            # training from fbprophet
            # prophet module requires columns ds (date) and y (value)
            candles = btc_data.rename(columns={'utc_time': 'ds',
                                               'btc_price': 'y'})
            m = Prophet(yearly_seasonality=True, daily_seasonality=False,
                        changepoint_prior_scale=0.001)
            m.fit(candles)

            # making the predictions
            future = m.make_future_dataframe(periods=1, include_history=False)
            future = m.predict(future)
            ts_res = future['yhat'][0]
            return ts_res

        except Exception as e:
            print (e)
            return error_val

    # function to create a linear regression model
    def linear_prediction(self):
        """
            Method to predict BTC price for next day on external regressors:
                1. Oil Price
                2. Google trends
            Uses scikit learn library to run linear regression.

            : param self
            : return pred_reg(float)
                     error_val(int)
        """
        error_val = -1
        try:
            oil_data = pd.read_csv(self.in_path_comm + 'oil_price.csv')
            google_data = pd.read_csv(self.in_path_gtrends
                                      + 'GTrendsData_old.csv')
            btc_data = pd.read_csv(self.in_path_btc + 'btc_price.csv')

            # merging all the datasets
            df = pd.merge(btc_data, oil_data, left_on='utc_time',
                          right_on='Date')
            del df['Date']
            df = pd.merge(df, google_data, left_on='utc_time',
                          right_on='date')
            del df['date']
            df['google_hits'] = df['btc'] + df['bitcoin'] + df['btc usd']
            + df['btcusd']

            # selecting only relevant columns
            df = df[['utc_time', 'oil_price', 'google_hits', 'btc_price']]

            # shifting the btc price by +1 day, want to predict for next day
            df['btc_price_next'] = 0
            for i in range(0, len(df) - 1):
                df['btc_price_next'].iloc[i] = df['btc_price'].iloc[i + 1]

            # preparing the dataset for linear regression
            df_lin = df[['oil_price', 'google_hits', 'btc_price_next']]

            # response index number
            resp_idx = df_lin.shape[1] - 1

            # last row are the new features with which prediction is to be made
            feature_day = df_lin.iloc[-1]
            del feature_day['btc_price_next']
            X_day = feature_day.as_matrix()
            X_day = X_day.reshape(1, -1)

            # training the linear regression model
            df_lin = df_lin.drop(df_lin.index[[-1]])

            # preparing the features and the response variables
            X = df_lin.iloc[:, :-1].values
            y = df_lin.iloc[:, resp_idx].values

            # training the regression model
            regressor = LinearRegression()
            regressor.fit(X, y)
            pred_reg = regressor.predict(X_day)[0]
            return pred_reg
        except Exception as e:
            print (e)
            return error_val

    # defining a function to create a composite prediction
    def final_prediction(self):
        """
            Method to create a composite prediction by taking inputs from
            both time-series and linear regression model.
            Writes a row to the csv that is read by the UI component.
            : param self
            : return error_val(int)
        """
        error_val = -1
        try:
            final_yhat = (self.time_prediction() + self.linear_prediction())/2
            # predicted direction
            res_dir = final_yhat - self.curr_price
            res = 1 if np.sign(res_dir) == 1.0 else 0
            # confidence calculation
            ci = np.absolute(res_dir)/self.curr_price
            ci_f = round(ci*10, 2)
            # creating the row to append finally
            today_date = datetime.datetime.strptime(self.today_date,
                                                    '%Y-%m-%d')
            pred_date = today_date + datetime.timedelta(days=1)
            pred_date = pred_date.strftime("%m/%d/%Y")

            app_list = [pred_date]
            app_list.append(res)
            app_list.append(ci_f)

            # writing to the file
            with open(self.out_path + 'BitcoinPrice.csv', 'ab') as f:
                writer = csv.writer(f)
                writer.writerow(app_list)
        except Exception as e:
            print (e)
            return error_val


# creating a temporary dictionary
dic_temp = {'in_path_btc': './data/btc/',
            'in_path_comm': './data/commodity/',
            'in_path_gtrends': './data/gtrends/',
            'out_path': './data/'}

# running the object
test = BtcModelPrediction(dic_temp)
result = test.final_prediction()
print result

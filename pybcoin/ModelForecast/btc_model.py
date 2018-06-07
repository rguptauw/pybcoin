"""
    Module name: btc_model
    Description: Module for predicting bitcoin price direction based on
    external regressors and time series.
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

        self.in_path_btc = params['Forecast']['in_path_btc']
        self.in_path_comm = params['Forecast']['in_path_comm']
        self.in_path_gtrends = params['Forecast']['in_path_gtrends']
        self.in_path_social = params['Forecast']['in_path_social']
        self.path_time_pred = params['Forecast']['path_time_pred']
        self.out_path = params['Forecast']['out_path']

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
            btc_data = pd.read_csv(self.in_path_btc + 'btc_prices.csv')
            btc_data['Date'] = pd.to_datetime(btc_data['Date']
                                              ).dt.strftime('%Y-%m-%d')

            # creating a current btc price for later use
            self.curr_price = btc_data['btc_price'].iloc[-1]

            # today's date for further use
            self.today_date = btc_data['Date'].iloc[-1]

            # training from fbprophet
            # prophet module requires columns ds (date) and y (value)
            candles = btc_data.rename(columns={'Date': 'ds',
                                      'btc_price': 'y'})
            m = Prophet(yearly_seasonality=True, daily_seasonality=False,
                        changepoint_prior_scale=0.001)
            m.fit(candles)

            # making the predictions
            future = m.make_future_dataframe(periods=1, include_history=False)
            future = m.predict(future)
            # creating the row to append to the time series dataset
            today_date = datetime.datetime.strptime(self.today_date,
                                                    '%Y-%m-%d')
            pred_date = today_date + datetime.timedelta(days=1)
            pred_date = pred_date.strftime("%Y-%m-%d")

            app_list = [pred_date]
            app_list.append(future['yhat'][0])

            # writing to the file
            with open(self.path_time_pred + 'predicted_time.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(app_list)

            return future['yhat']

        except Exception as e:
            print(e)
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
            oil_data['Date'] = pd.to_datetime(oil_data['Date']
                                              ).dt.strftime('%Y-%m-%d')
            google_data = pd.read_csv(self.in_path_gtrends + 'GTrendsData.csv')
            google_data['Date'] = pd.to_datetime(google_data['Date']
                                                 ).dt.strftime('%Y-%m-%d')
            btc_data = pd.read_csv(self.in_path_btc + 'btc_prices.csv')
            btc_data['Date'] = pd.to_datetime(btc_data['Date']
                                              ).dt.strftime('%Y-%m-%d')
            twitter_sentiment = pd.read_csv(self.in_path_social +
                                            'tweets_sentiment.csv')
            twitter_sentiment['Date'] = pd.to_datetime(
                twitter_sentiment['Date']).dt.strftime('%Y-%m-%d')
            reddit_sentiment = pd.read_csv(self.in_path_social +
                                           'reddit_comments_sentiment.csv')
            reddit_sentiment['Date'] = pd.to_datetime(reddit_sentiment['Date']
                                                      ).dt.strftime('%Y-%m-%d')

            # merging all the datasets
            df = pd.merge(btc_data, oil_data, on='Date')
            df = pd.merge(df, google_data, on='Date')
            df = pd.merge(df, twitter_sentiment, on='Date')

            # renaming columns name for twitter
            df = df.rename(columns={'Negative': 'twitter_negative'})
            df = df.rename(columns={'Positive': 'twitter_positive'})
            df = pd.merge(df, reddit_sentiment, on='Date')

            # renaming columns name for reddit
            df = df.rename(columns={'Negative': 'reddit_negative'})
            df = df.rename(columns={'Positive': 'reddit_positive'})

            # getting relevant computations from social data
            df['google_hits'] = (df['btc'] + df['bitcoin'] +
                                 df['btc usd'] + df['btcusd'])
            df['twitter'] = (df['twitter_positive'] / (df['twitter_positive'] +
                             df['twitter_negative']))
            df['reddit'] = (df['reddit_positive'] / (df['reddit_positive'] +
                            df['reddit_negative']))

            # selecting only relevant columns
            df = df[['Date', 'oil_price', 'google_hits', 'twitter',
                    'reddit', 'btc_price']]

            # initializing the columns of price deltas
            df['btc_delta'] = 0
            df['oil_delta'] = 0
            df['google_delta'] = 0
            df['twitter_delta'] = 0
            df['reddit_delta'] = 0

            # computing the percentage change for all rows
            for i in range(1, len(df)):
                df['btc_delta'].iloc[i] = ((df['btc_price'].iloc[i] -
                                            df['btc_price'].iloc[i - 1]) /
                                           df['btc_price'].iloc[i - 1])
                df['oil_delta'].iloc[i] = ((df['oil_price'].iloc[i] -
                                            df['oil_price'].iloc[i - 1]) /
                                           df['oil_price'].iloc[i - 1])
                df['google_delta'].iloc[i] = ((df['google_hits'].iloc[i] -
                                               df['google_hits'].iloc[i - 1]) /
                                              df['google_hits'].iloc[i - 1])
                df['twitter_delta'].iloc[i] = ((df['twitter'].iloc[i] -
                                                df['twitter'].iloc[i - 1]) /
                                               df['twitter'].iloc[i - 1])
                df['reddit_delta'].iloc[i] = ((df['reddit'].iloc[i] -
                                               df['reddit'].iloc[i - 1]) /
                                              df['reddit'].iloc[i - 1])

            # shifting the btc price by +1 day, want to predict for  next day
            df['btc_delta_pred'] = 0
            for i in range(0, len(df) - 1):
                df['btc_delta_pred'].iloc[i] = df['btc_delta'].iloc[i + 1]

            # selecting only relevant columns
            df = df[['Date', 'oil_delta', 'google_delta', 'twitter_delta',
                     'reddit_delta', 'btc_price', 'btc_delta',
                     'btc_delta_pred']]

            # preparing the dataset for linear regression
            df_lin = df[['oil_delta', 'google_delta', 'twitter_delta',
                        'reddit_delta', 'btc_delta_pred']]

            # response index number
            resp_idx = df_lin.shape[1] - 1

            # last row are the new features with which prediction is to be made
            feature_day = df_lin.iloc[-1]
            del feature_day['btc_delta_pred']
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
            print(e)
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
            time_data = pd.read_csv(self.path_time_pred + 'predicted_time.csv')
            time_data['Date'] = pd.to_datetime(time_data['Date']
                                               ).dt.strftime('%Y-%m-%d')

            price_old = time_data['predicted_price_time'].iloc[-2]
            time_ratio = (self.time_prediction() - price_old) / price_old
            reg_ratio = self.linear_prediction()

            final_yhat = (reg_ratio * 0.8) + (time_ratio * 0.2)

            # predicted direction
            res = 1 if np.sign(final_yhat)[0] == 1.0 else 0

            # confidence calculation
            ci = round((np.absolute(final_yhat[0]) / 0.05), 2)
            ci_f = ci if ci < 1 else 1
            # creating the row to append finally
            today_date = datetime.datetime.strptime(self.today_date,
                                                    '%Y-%m-%d')
            pred_date = today_date + datetime.timedelta(days=1)
            pred_date = pred_date.strftime("%Y-%m-%d")

            app_list = [pred_date]
            app_list.append(res)
            app_list.append(ci_f)

            # writing to the file
            final_df = pd.read_csv(self.out_path + 'BitcoinPrice.csv')
            app_list = pd.DataFrame(app_list)
            app_list = app_list.transpose()
            app_list.columns = ['date', 'move', 'confidence']
            final_df = final_df.append(app_list)
            final_df.to_csv(self.out_path + 'BitcoinPrice.csv', index=False)

            return final_yhat[0]

        except Exception as e:
            print(e)
            return error_val

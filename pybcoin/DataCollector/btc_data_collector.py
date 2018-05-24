"""
    Module name: btc_data_collector
    Description: Module for collecting day level Bitcoin specific data
    like, price, number of tweets, volume of buy and sell transactions.
"""

from datetime import datetime, timedelta
import logging

import pandas as pd
import requests
import quandl
from forex_python.bitcoin import BtcConverter


class BtcDataCollector(object):

    """
        The object for retrieving daily data for bitcoin specific
        factors.The prices are retreived once a day at a predefined
        time. If the current for the current day is not available,
        latest available data is used.
            :member attributes: logger: logger instance
                                api_key: Quandl API key
                                tweet_count_url: Url to retrieve
                                                tweets count

            :member functions:  fetch_btc_price
                                fetch_tweet_counts
                                fetch_transaction_volume
    """

    def __init__(self, params):
        self.logger = logging.getLogger('simpleExample')
        self.api_key = params['Quandl']['quandl-key']
        self.tweet_count_url = params['Twitter']['tweet-count-url']

    def fetch_btc_price(self):
        """
            Method to fetch the current bitcoin price.
            The price is in USD and is retreived from
            the CoinDesk index.
            : param self
            : return btc_price(float)
                     error_val(int)
        """
        error_val = -1
        try:
            today = datetime.now()
            start_date = today - timedelta(days=1)
            btc_price = pd.DataFrame([{
                'Date': start_date.strftime("%Y-%m-%d"),
                'btc_price': BtcConverter().get_previous_price(
                                                'USD', start_date)}])
            return btc_price.set_index('Date')
        except Exception as e:
            # self.logger.error(e)
            print(e)
            return error_val

    def fetch_tweet_counts(self):
        """
            Method to fetch the daily estimated number of tweets
            with bitcoin related hastags. The function parses the
            HTML page to retrieve the tweet counts.

            : param self
            : return tweet_count(pandas Dataframes)
                     error_val(int)
        """
        error_val = -1
        try:
            day_count = 1
            today = datetime.now()
            start_date = today - timedelta(days=day_count)
            url = self.tweet_count_url
            page = requests.get(url)
            first = '[new Date("'+start_date.strftime("%Y/%m/%d")+'"),'
            last = ']'
            start = page.text.rindex(first) + len(first)
            end = page.text.find(last, start)
            val = page.text[start:end]
            if val == 'null':
                count = 0
            else:
                count = int(page.text[start:end])
            tweet_count = pd.DataFrame({
                            'Date': [start_date.strftime("%Y/%m/%d")],
                            'tweet_count': [count]
                            })
            return tweet_count.set_index('Date')
        except Exception as e:
            # self.logger.error(e)
            print(e)
            return error_val

    def fetch_transaction_volume(self):
        """
            Method to fetch the daily bitcoin transaction
            volume in USD.
            : param self
            : return nyse_index(pandas Dataframe)
                     error_val(int)
        """
        error_val = -1
        try:
            day_count = 1
            today = datetime.now()
            start_date = today - timedelta(days=day_count)
            volume = quandl.get("BCHAIN/ETRVU",
                                start_date=start_date.strftime("%Y-%m-%d"),
                                api_key=self.api_key)
            return volume
        except Exception as e:
            # self.logger.error(e)
            print(e)
            return error_val

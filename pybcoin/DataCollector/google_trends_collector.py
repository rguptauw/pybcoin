"""
    Module name: google_trends_collector
    Description: Module for collecting data on how bitcoin
    is trending on google.
"""

from datetime import datetime, timedelta
import logging

import pandas as pd
from pytrends.request import TrendReq


class GTrendsDataCollector(object):

    """
        The object for retrieving current day level data from google
        trends.
            :member attributes: logger: logger instance
            :member functions:  fetch_trends

    """

    def __init__(self, params=None):
        self.logger = logging.getLogger('simpleExample')

    def fetch_trends(self, params=None):
        """
            Method to fetch the google trends data for bitcoin
            and related keywords, for the given date.
            : param self
            : return google_trend(DataFrame)
                     error_val(int)
        """
        error_val = -1
        try:
            pytrends = TrendReq(hl='en-US', tz=360)
            day_count = 5
            kw_lists = ["btc", "bitcoin", "btc usd", "btcusd", "cypto",
                        "cryptocurrency", "eth", "ethereum", "blockchain"]
            df_final = pd.DataFrame()
            today = datetime.now()
            start_date = today - timedelta(days=day_count)
            date_range = start_date.strftime("%Y-%m-%d")\
                + ' ' + today.strftime("%Y-%m-%d")
            for wordlist in kw_lists:
                pytrends.build_payload([wordlist], cat=0,
                                       timeframe=date_range,
                                       geo='', gprop='')
                df_final = pd.concat([df_final,
                                     pytrends.interest_over_time()], axis=1)
            df_final.index = pd.to_datetime(df_final.index).date
            df_final.index.name = 'Date'
            return df_final[kw_lists].tail(n=1)
        except Exception as e:
            # self.logger.error(e)
            print(e)
            return error_val

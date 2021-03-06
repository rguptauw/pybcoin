"""
    Module name: market_data_collector
    Description: Module for collecting day level data for general
    market indicators like crude oil prices, USD/EURO exchange rates,
    NYSE composite index.
"""
from datetime import datetime, timedelta

import quandl
import pandas as pd
from googlefinance.client import get_prices_data
from forex_python.converter import CurrencyRates

DATE_FORMAT = "%Y-%m-%d"
INDEX = 'Date'
OIL_INDEX = "OPEC/ORB"


class MarketDataCollector(object):
    """

       The object for retrieving daily data for market indicators.
       The prices are retreived once a day at a predefined time. If
       the current for the current day is not available, latest available
       data is used.
            :member functions:  fetch_usd_exrate
                                fetch_oil_price
                                fetch_nyse_index

    """

    def __init__(self):
        pass

    def fetch_usd_exrate(self):
        """
            Method to fetch the daily USD-EURO exchange rate.
            The rates are according to the European Central Bank scale.
            : param self
            : return usd_eur_rate(pandas Dataframes)
                     error_val(int)
        """
        error_val = -1
        try:
            day_count = 1
            src_curr = 'USD'
            dst_curr = 'EUR'
            today = datetime.now()
            start_date = today - timedelta(days=day_count)
            usd_eur_rate = pd.DataFrame([{
                'Date': start_date.strftime(DATE_FORMAT),
                'forex_rate': CurrencyRates().get_rate(src_curr, dst_curr)}])
            return usd_eur_rate.set_index(INDEX)
        except Exception as e:
            # self.logger.error(e)
            print(e)
            return error_val

    def fetch_oil_price(self):
        """
            Method to fetch the daily crude oil prices.
            The rates are according to the OPEC Basket index.
            : param self
            : return oil_price(pandas Dataframes)
                     error_val(int)
        """
        error_val = -1
        try:
            day_count = 5
            today = datetime.now()
            start_date = today - timedelta(days=day_count)

            oil_price = quandl.get(OIL_INDEX,
                                   start_date=start_date.strftime(DATE_FORMAT))
            oil_price = oil_price.rename(columns={'Value': 'oil_price'})
            oil_price.index = pd.to_datetime(oil_price.index).date
            oil_price.index.name = INDEX
            return oil_price.tail(n=1)
        except Exception as e:
            # self.logger.error(e)
            print(e)
            return error_val

    def fetch_nyse_index(self):
        """
            Method to fetch the daily NYSE index.
            : param self
            : return nyse_index(pandas Dataframe)
                     error_val(int)
        """
        error_val = -1
        try:
            params = [
                # NYSE COMPOSITE (DJ)
                {
                    'q': "NYA",
                    'x': "INDEXNYSEGIS",
                }
            ]
            period = "5d"
            nyse_index = get_prices_data(params, period)
            nyse_index.index.name = INDEX
            return nyse_index.tail(n=1)
        except Exception as e:
            print(e)
            return error_val

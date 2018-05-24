"""
    Module name: controller_collector
    Description: Controller module for all data collection.
"""
import logging

from btc_data_collector import BtcDataCollector
from google_trends_collector import GTrendsDataCollector
from market_data_collector import MarketDataCollector
from reddit_comment_collector import RedditDataCollector
from tweets_collector import TwitterDataCollector

from configparser import SafeConfigParser


class ControllerCollector(object):

    """
        The controller object for data collection pipeline. Responsible
        for triggering and monitoring the daily streaming data collection
        from all data sources.
            :member attributes: logger: logger instance
                                config: config file path

            :member functions: data_collect_pipeline
    """

    def __init__(self, config_file):
        self.logger = logging.getLogger('simpleExample')
        self.config = SafeConfigParser()
        self.config.read(config_file)

    def data_collection_pipeline(self):
        """
            Method to call the data collector modules to retreive latest
            data.
            : param self
            : return ret_val(int)

        """
        collection_complete = False
        try:
            # Collecting latest BTC price.
            collector = BtcDataCollector(self.config)
            data = collector.fetch_btc_price()
            if data == -1:
                return collection_complete
            data.to_csv('./data/latest/btc_prices.csv')

            # Collecting BTC Tweet Count
            data = collector.fetch_tweet_counts()
            if data == -1:
                return collection_complete
            data.to_csv('./data/latest/tweet_counts.csv')

            # Collecting BTC Volume
            data = collector.fetch_transaction_volume()
            if data == -1:
                return collection_complete
            data.to_csv('./data/latest/btc_volume.csv')

            # Collecting Google trends.
            collector = GTrendsDataCollector()
            data = collector.fetch_trends()
            if data == -1:
                return collection_complete
            data.to_csv('./data/latest/gtrends.csv')

            # Collecting USD/EURO forex rate
            collector = MarketDataCollector()
            data = collector.fetch_usd_exrate()
            if data == -1:
                return collection_complete
            data.to_csv('./data/latest/usd_exchrate.csv')

            # Collecting NYSE composite index
            data = collector.fetch_nyse_index()
            if data == -1:
                return collection_complete
            data.to_csv('./data/commodity/nyse_index.csv')

            # Collecting Crude Oil Price
            data = collector.fetch_oil_price()
            if data == -1:
                return collection_complete
            data.to_csv('./data/latest/oil_price.csv')

            # Collecting Tweets
            collector = TwitterDataCollector(self.config)
            data = collector.fetch_tweets()
            if data == -1:
                return collection_complete
            data.to_csv('./data/latest/tweets.csv')

            # Collecting Tweets
            collector = RedditDataCollector(self.config)
            data = collector.fetch_reddit_comments()
            if data == -1:
                return collection_complete
            data.to_csv('./data/latest/reddit_comments.csv')

            collection_complete = True
            print('Data Collection complete')
            return collection_complete
        except Exception as e:
            # self.logger.error(e)
            print(e)
            return collection_complete


controller = ControllerCollector('./pybcoin/config/config.ini')
val = controller.data_collection_pipeline()
print(val)

import logging
import numpy as np
import os
import pandas as pd
import sys

__directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__directory + "/..")
sys.path.append(__directory + "/../..")

from utils.pre_processing import pre_process_data # noqa
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer # noqa


class SentimentAnalyzer(object):
    """
        The controller object for Sentiment Analysis pipeline. Responsible
        for providing daily sentiment count.
            :member attributes: logger: logger instance
                                config: config file path
            :member functions: sentiment_scorer
    """
    def __init__(self, config):
        self.logger = logging.getLogger('simpleExample')
        self.analyzer = SentimentIntensityAnalyzer()
        self.path = config['Sentiment']['text_csv_path']

    def __sentiment_count__(self, grouped_Data):
        """
            Method to convert sentiment as features.
            : param self
            : return grouped_sentiment(pandas Dataframes)
        """
        pos_count = np.sum(grouped_Data['Sentiment'] > 0)
        neg_count = np.sum(grouped_Data['Sentiment'] < 0)
        grouped_sentiment = pd.DataFrame({
            'pos_count': [pos_count],
            'neg_count': [neg_count]
        })
        return grouped_sentiment

    def sentiment_scorer(self, keyword='tweets'):
        """
            Method to Return Daily Positive and Negative sentiment
            : param self
                    keyword: keywords specifying tweets or reddit_comments
            : return text_df(pandas Dataframes)
        """
        text_data = pre_process_data(self.path + keyword + '.csv')
        sentiment = []
        date = []

        for i in range(0, len(text_data)):
            sentiment.append(self.analyzer.polarity_scores(
                             text_data.iloc[i]['text'])['compound'])
            date.append(pd.to_datetime(text_data.iloc[i]['Date']).date())

        text_df = pd.DataFrame({'Date': date,
                                'Sentiment': sentiment
                                })

        text_df = text_df.groupby(['Date']).apply(
            self.__sentiment_count__).reset_index().drop(['level_1'], axis=1)
        text_df.to_csv(self.path + keyword + '_sentiment.csv', index=False)

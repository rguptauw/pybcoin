#requests, vaderSentiment, nltk
import pandas as pd
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import logging
import sys
import os
__directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__directory + "/..")
# sys.path.append(__directory + "/../..")
from utils.pre_processing import pre_process_data

class SentimentAnalyzer(object):

    """
        The controller object for data collection pipeline. Responsible
        for triggering and monitoring the daily streaming data collection
        from all data sources.
            :member attributes: logger: logger instance
                                config: config file path
            :member functions: data_collect_pipeline
    """
    def __init__(self):
        self.logger = logging.getLogger('simpleExample')
        self.analyzer = SentimentIntensityAnalyzer()

    def sentiment_scorer(self, path, keyword = 'twitter'):

        def sentiment_count(grp):
            pos_count = np.sum(grp['Sentiment']>0)
            neg_count = np.sum(grp['Sentiment']<0)
            return pd.DataFrame({
                'pos_count':[pos_count],
                'neg_count':[neg_count]
            })

        text_data = pre_process_data(path)
        sentiment = []
        date = []

        for i in range(0, len(text_data)):
            sentiment.append(self.analyzer.polarity_scores(text_data.iloc[i]['text'])['compound'])
            date.append(pd.to_datetime(text_data.iloc[i]['Date']).date())
            # date.append(text_data.iloc[i]['Date'])
        text_df = pd.DataFrame({'Date' : date,
                                'Sentiment': sentiment
                               })
        #text_df['Sentiment'] = np.where(text_df['Sentiment']>0, 'Positive', 'Negative')

        text_df = text_df.groupby(['Date']).apply(sentiment_count).reset_index().drop(['level_1'],axis = 1)
        text_df.to_csv('./data/latest/' + keyword + '_sentiment.csv',index=True)

analyzer = SentimentAnalyzer()
analyzer.sentiment_scorer(r'./data/latest/tweets.csv')

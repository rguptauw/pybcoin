from collections import Counter
import os
import glob

import nltk
from nltk.corpus import stopwords

import pandas as pd
import re
# nltk.download('stopwords')
stops = set(stopwords.words("english"))
stops.update(['http','https','www','com'])

def read_data():
    file_list = glob.glob("output_file*")
    raw_data = pd.DataFrame()
    dfs = []
    for file_ in file_list:
        df = pd.read_table(file_, delimiter=None)
        dfs.append(df)
    raw_data = pd.concat(dfs)

    semi_counts = raw_data[raw_data.columns[0]].apply(_count_semi)
    clean_raw_data = raw_data[raw_data.columns[0]][semi_counts == 9]

    clean_raw_data_split = clean_raw_data.str.split(";").tolist()

    return pd.DataFrame(clean_raw_data_split, columns=raw_data.columns[0].split(";"))


def _count_semi(tweet):
    return Counter(str(tweet))[';']


def clean_tweet(tweet):
    '''
    Utility function to clean the text in a tweet by removing
    links and special characters using regex.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


def remove_stopwords(tweet):
    # Removing all the stopwords
    filtered_words = [word for word in tweet.split() if word not in stops]
    return " ".join(filtered_words)


if __name__ == '__main__':
    twitter_data = read_data()
    twitter_data['text'] = twitter_data['text'].apply(str.lower)
    twitter_data['text'] = twitter_data['text'].apply(clean_tweet)
    twitter_data['text'] = twitter_data['text'].apply(remove_stopwords)
    twitter_data.to_csv('processed_data.csv', index=False)

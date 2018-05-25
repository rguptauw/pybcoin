from collections import Counter
import os
import glob

import nltk
from nltk.corpus import stopwords

import pandas as pd
import re
import string

# nltk.download('stopwords')
stops = set(stopwords.words("english"))
stops.update(['http','https','www','com'])

def read_data(path):
    df = pd.read_csv(path)
    df['text'] = df['text'].astype(str)
    return df

def remove_urls(tweet):
    tweet = re.sub(r"http\S+", "", tweet)
    tweet = re.sub(r'(?:(?:http|https|https://www|https://|http://|):\/\/)'
                   '?([-a-zA-Z0-9.]{2,256}\.[a-z]{2,4})\b(?:\/[-a-zA-Z0-9@:'
                   '%_\+.~#?&//=]*)?',"",tweet,flags=re.MULTILINE)
    tweet = '\n'.join([a for a in tweet.split("\n") if a.strip()])
    return tweet

def clean_tweet(tweet):
    tweet = tweet.lower()
    tweet = re.sub('@$[^\s]+','',tweet)
    tweet = re.sub('[\s]+', ' ', tweet)
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    tweet = tweet.strip('\'"')
    tweet = re.sub(r'[^\x00-\x7f]',r'', tweet)
    tweet = re.sub('[0-9]+', '', tweet)
    return tweet


def remove_stopwords(tweet):
    # Removing all the stopwords
    filtered_words = [word for word in tweet.split() if word not in stops]
    return " ".join(filtered_words)

def remove_delimiters(tweet):
    delimiters = ",.!?/&-:;@'+% =>_..."
    return ' '.join(w for w in re.split("["+"\\".join(delimiters)+"]", tweet) if w)

def remove_lessthantwo(tweet):
    return ' '.join( [w for w in tweet.split() if len(w)>2] )

def pre_process_data(path):
    twitter_data = read_data(path)
    twitter_data['text'] = twitter_data['text'].apply(remove_urls)
    twitter_data['text'] = twitter_data['text'].apply(str.lower)
    twitter_data['text'] = twitter_data['text'].apply(clean_tweet)
    twitter_data['text'] = twitter_data['text'].apply(remove_stopwords)
    twitter_data['text'] = twitter_data['text'].apply(remove_delimiters)
    twitter_data['text'] = twitter_data['text'].apply(remove_lessthantwo)
    return twitter_data

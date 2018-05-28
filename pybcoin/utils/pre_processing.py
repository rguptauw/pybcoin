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
<<<<<<< HEAD
    """
        Utility function to read csv for text pre-processing.
        : param path
        : return text_data(pandas Dataframes)
    """
    text_data = pd.read_csv(path)
    text_data['text'] = text_data['text'].astype(str)
    return text_data

def remove_urls(text):
    """
        Utility function to clean the text by removing urls.
        : param path
        : return text(str)
    """
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r'(?:(?:http|https|https://www|https://|http://|):\/\/)'
                   '?([-a-zA-Z0-9.]{2,256}\.[a-z]{2,4})\b(?:\/[-a-zA-Z0-9@:'
                   '%_\+.~#?&//=]*)?',"",text,flags=re.MULTILINE)
    text = '\n'.join([a for a in tweet.split("\n") if a.strip()])
    return text

def clean_text(text):
    """
        Utility function to clean the text by removing special characters.
        : param text
        : return text(str)
    """
    text = text.lower()
    text = re.sub('@$[^\s]+','',text)
    text = re.sub('@$[^\s]+','',text)
    text = re.sub('[\s]+', ' ', text)
    text = re.sub(r'#([^\s]+)', r'\1', text)
    text = text.strip('\'"')
    text = re.sub(r'[^\x00-\x7f]',r'', text)
    text = re.sub('[0-9]+', '', text)
    return text
=======
    df = pd.read_csv(path)
    df['text'] = df['text'].astype(str)
    return df
>>>>>>> 478406a8d1433cffeadbf78924ca8d8e2c9cd221

def remove_urls(tweet):
    tweet = re.sub(r"http\S+", "", tweet)
    tweet = re.sub(r'(?:(?:http|https|https://www|https://|http://|):\/\/)'
                   '?([-a-zA-Z0-9.]{2,256}\.[a-z]{2,4})\b(?:\/[-a-zA-Z0-9@:'
                   '%_\+.~#?&//=]*)?',"",tweet,flags=re.MULTILINE)
    tweet = '\n'.join([a for a in tweet.split("\n") if a.strip()])
    return tweet

<<<<<<< HEAD
def remove_stopwords(text):
    """
        Utility function to clean the text in a tweet by removing english stopwords.
        : param text
        : return text(str)
    """
=======
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
>>>>>>> 478406a8d1433cffeadbf78924ca8d8e2c9cd221
    # Removing all the stopwords
    filtered_words = [word for word in text.split() if word not in stops]
    return " ".join(filtered_words)

<<<<<<< HEAD
def remove_delimiters(text):
    """
        Utility function to clean the text in a tweet by removing delimiters
        : param text
        : return text(str)
    """
    delimiters = ",.!?/&-:;@'+% =>_..."
    return ' '.join(w for w in re.split("["+"\\".join(delimiters)+"]", text) if w)

def remove_lessthanthree(text):
    """
        Utility function to clean the text in a tweet by removing less than less than three
        letter words.
        : param text
        : return text_data(pandas Dataframes)
    """
    return ' '.join( [w for w in text.split() if len(w)>2] )

def pre_process_data(path):
    """
        Utility function to clean the text.
        : param path
        : return text_data(pandas Dataframes)
    """
    text_data = read_data(path)
    text_data['text'] = text_data['text'].apply(remove_urls)
    text_data['text'] = text_data['text'].apply(str.lower)
    text_data['text'] = text_data['text'].apply(clean_text)
    text_data['text'] = text_data['text'].apply(remove_stopwords)
    text_data['text'] = text_data['text'].apply(remove_delimiters)
    text_data['text'] = text_data['text'].apply(remove_lessthantwo)
    return text_data
=======
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
>>>>>>> 478406a8d1433cffeadbf78924ca8d8e2c9cd221

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


def remove_stopwords(text):
    """
        Utility function to clean the text in a tweet by removing english stopwords.
        : param text
        : return text(str)
    """
    # Removing all the stopwords
    filtered_words = [word for word in text.split() if word not in stops]
    return " ".join(filtered_words)

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

"""
This module is for text pre-processing and formating data
for SentimenetAnalyzer module.
"""

import pandas as pd
import re

from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS
import matplotlib
matplotlib.use("Agg") # noqa
from matplotlib import pyplot as plt


# nltk.download('stopwords')
stops = set(stopwords.words("english"))
stops.update(['http', 'https', 'www', 'com', 'fuck', 'Nan'])


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
    url_pattern = r'(?:(?:http|https|https://www|https://|http://|):\/\/)' \
        '?([-a-zA-Z0-9.]{2,256}\.[a-z]{2,4})\b(?:\/[-a-zA-Z0-9@:' \
        '%_\+.~#?&//=]*)?'
    text = re.sub(r"http\S+", "", text)
    text = re.sub(url_pattern, "", text, flags=re.MULTILINE)
    text = '\n'.join([a for a in text.split("\n") if a.strip()])
    return text


def clean_text(text):
    """
        Utility function to clean the text by removing special characters.
        : param text
        : return text(str)
    """
    text = text.lower()
    text = re.sub('@$[^\s]+', '', text)
    text = re.sub('@$[^\s]+', '', text)
    text = re.sub('[\s]+', ' ', text)
    text = re.sub(r'#([^\s]+)', r'\1', text)
    text = text.strip('\'"')
    text = re.sub(r'[^\x00-\x7f]', r'', text)
    text = re.sub('[0-9]+', '', text)
    return text


def remove_stopwords(text):
    """
        Utility function to clean the text in a tweet by removing
        english stopwords.
        : param text
        : return text(str)
    """
    filtered_words = [word for word in text.split() if word not in stops]
    return " ".join(filtered_words)


def remove_delimiters(text):
    """
        Utility function to clean the text in a tweet by removing delimiters
        : param text
        : return text(str)
    """
    delimiters = ",.!?/&-:;@'+% =>_..."
    return ' '.join(w for w in re.split("[" + "\\".join(delimiters) + "]",
                    text) if w)


def remove_lessthanthree(text):
    """
        Utility function to clean the text in a tweet by removing
        less than less than three
        letter words.
        : param text
        : return text_data(pandas Dataframes)
    """
    return ' '.join([w for w in text.split() if len(w) > 2])


def create_word_cloud(text, date_generated):
    """
        Utility function to plot wordcloud
        letter words.
        : param text
        : return png(matplotlib image)
    """
    word_cloud_path = './pybcoin/static/date_'
    text = ' '.join(text)
    wordcloud = WordCloud(stopwords=STOPWORDS,
                          background_color='white',
                          width=2500,
                          height=2000
                          ).generate(text)
    plt.figure(1, figsize=(13, 13))
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.savefig(word_cloud_path + date_generated[0].replace('/', '-') +
                '.png', bbox_inches='tight')


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
    text_data['text'] = text_data['text'].apply(remove_lessthanthree)
    word_cloud_data = text_data[text_data['Date'] == max(text_data['Date'])]
    create_word_cloud(word_cloud_data['text'],
                      (word_cloud_data['Date'].unique()))
    return text_data

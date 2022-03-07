# gives a list of most frequent words in the recent tweets containing the title
# currently based on a naive approach and is slow
# search for brand's twitter id for more approriate results, e.g. @Microsoft

import argparse
import twint
import pandas as pd
import os

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re

import matplotlib.pyplot as plt
import seaborn as sns


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--title', type=str, default='@Microsoft')
    parser.add_argument('--tweet_count', type=int, default=500)
    return parser.parse_args()


def scrape_tweets(title, tweet_count):
    c = twint.Config()
    c.Search = title
    c.Limit = tweet_count
    c.Store_csv = True
    c.Output = title + ".csv"
    if os.path.exists(c.Output):
        os.remove(c.Output)
    c.Lang = "en"
    c.Hide_output = True
    twint.run.Search(c)


def tokenize(text):
    tokens = re.split('\W+', text)
    return tokens


def remove_stopword(text):
    text = [char for char in text if char not in stopwords]
    return text


def lemmatize(text):
    text = [wnl.lemmatize(word) for word in text]
    return text


def preprocess_tweets():
    # remove punctuations & also remove tweets with less than 3 chars
    df['tweet'] = df['tweet'].str.replace('[^a-zA-Z0-9]', ' ', regex=True)
    df['tweet'] = df['tweet'].apply(lambda x: ' '.join ([w for w in x.split() if len (w)>3]))
    # tokenize
    df['tweet'] = df['tweet'].apply(lambda x: tokenize(x.lower()))
    # remove stop words
    df['tweet'] = df['tweet'].apply(lambda x: remove_stopword(x))
    # lemmatize
    df['tweet'] = df['tweet'].apply(lambda x: lemmatize(x))



args = parse_args()

# scrape_tweets
title = args.title
tweet_count = args.tweet_count
scrape_tweets(title, tweet_count)
df = pd.read_csv(title + ".csv")

# preprocess tweets
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("omw-1.4")
stopwords = stopwords.words("english")
# ps = nltk.PorterStemmer()
wnl = WordNetLemmatizer()

preprocess_tweets()

# word frequency count
data_list = df.loc[:,"tweet"].to_list()
flat_data_list = [item for sublist in data_list for item in sublist]
data_count = pd.DataFrame(flat_data_list)
data_count = data_count[0].value_counts()

# remove "http" and the title from data_count
data_count = data_count.drop(["http", title.lower().replace('@', '')], axis=0)

# visualize the word frequency count
data_count = data_count[:20,]
plt.figure(figsize=(10,5))
sns.barplot(x = data_count.values, y = data_count.index)
plt.title("Most frequent words in tweets")
plt.ylabel("Word", fontsize=12)
plt.xlabel("Count", fontsize=12)
plt.show()
# gives a list of most frequent words in the recent tweets containing the title
# currently based on a naive approach and is slow
# search for brand's twitter id for more approriate results, e.g. @Microsoft

import argparse
from ast import keyword
import twint
import pandas as pd
import os

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re

from gensim.corpora import Dictionary
from gensim.models import LdaMulticore
from gensim.models import Phrases, phrases

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t','--title', type=str, default='@Microsoft')
    parser.add_argument('-n','--tweet_count', type=int, default=5000)
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

def stem(text):
    text = [ps.stem(word) for word in text]
    return text


def make_bigrams_trigrams():
    bigram = Phrases(df['tweet'], min_count=5, threshold=100) # higher threshold fewer phrases.
    trigram = Phrases(bigram[df['tweet']], threshold=100) 
    bigram_mod = phrases.Phraser(bigram)
    trigram_mod = phrases.Phraser(trigram)
    for tweet in df['tweet']:
        tweet = bigram_mod[tweet]
        tweet = trigram_mod[tweet]


def preprocess_tweets():
    # remove punctuations, urls & also remove tweets with less than 3 chars
    df['tweet'] = df['tweet'].str.replace(r'@[^\s]+', '', regex=True)
    df['tweet'] = df['tweet'].str.replace(r'http\S+', '', regex=True)
    df['tweet'] = df['tweet'].str.replace('[^a-zA-Z0-9]', ' ', regex=True)
    df['tweet'] = df['tweet'].apply(lambda x: ' '.join ([w for w in x.split() if len (w)>3]))
    # tokenize
    df['tweet'] = df['tweet'].apply(lambda x: tokenize(x.lower()))
    # remove stop words
    df['tweet'] = df['tweet'].apply(lambda x: remove_stopword(x))
    # lemmatize & stemming
    df['tweet'] = df['tweet'].apply(lambda x: lemmatize(x))
    # df['tweet'] = df['tweet'].apply(lambda x: stem(x))
    # make bigrams & trigrams
    make_bigrams_trigrams()


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
ps = nltk.PorterStemmer()
wnl = WordNetLemmatizer()

preprocess_tweets()

make_bigrams_trigrams()

# word frequency count
data_list = df.loc[:,"tweet"].to_list()
flat_data_list = [[item for sublist in data_list for item in sublist]]

# create bag of words - (word:count)
dictionary = Dictionary(df.tweet)
bow_corpus = [dictionary.doc2bow(tweet) for tweet in df['tweet']]

tweets_lda = LdaMulticore(bow_corpus, num_topics = 3, id2word = dictionary, random_state = 1, passes=10)
topics = tweets_lda.show_topics()
words = []
for topic in topics[:1]:
    keywords = topic[1].split(" + ")
    for word in keywords:
        if word[7:-1] not in args.title.lower():
            words.append(word[7:-1])
print(words)

# remove csv file after use
os.remove(title + ".csv")
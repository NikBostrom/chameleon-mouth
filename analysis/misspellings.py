# Python 3

import numpy as np
import pandas as pd
import nltk
import os
import enchant

d = enchant.Dict("en_US")

def convert(string):
    if len(string) < 3:
        return string.lower()
    s = string
    first = s[0]
    if not first.isalnum():
        if first != "#":
            s = s[1:]
    last = s[len(s) - 1]
    if not last.isalnum():
        s = s[:(len(s) - 1)]
    return s.lower()

def split_tweet(tweet):
    words = str(tweet).split(" ")
    words = [convert(word) for word in words if (len(word) > 0) and (word[0] != "@" and word[0] != "#" and ("http" not in word)) ]
    return words
    
def misspelled_sentence(row):
    tweet = row["text"]
    words = split_tweet(tweet)
    misspellings = 0
    for word in words:
        if not d.check(word):
            misspellings += 1
    return misspellings

def num_words(row):
    tweet = row["text"]
    words = split_tweet(tweet)
    return len(words)

filepath = "../data/dictionaries/"
files = os.listdir(filepath)
files = [file for file in files if file.split(".")[1] == "csv"]
people = list(map(lambda x: x.split("_")[0], files))

all_tweets = pd.read_csv("all_tweets.csv")

all_tweets["misspelled"] = all_tweets.apply(lambda row: misspelled_sentence(row), axis=1)
all_tweets["num_words"] = all_tweets.apply(lambda row: num_words(row), axis=1)
all_tweets["misspelled/word"] = all_tweets["misspelled"] / all_tweets["num_words"]

means = []
stds = []

for person in people:
    data = all_tweets[all_tweets["person"] == person]
    mean = np.mean(data["misspelled/word"])
    std = np.std(data["misspelled/word"])
    means.append(mean)
    stds.append(std)

distribution = pd.DataFrame(data = [people, means, stds]).transpose()
distribution.columns = ["person", "mean", "std"]
distribution.to_csv("misspelling_distribution.csv", index=False)

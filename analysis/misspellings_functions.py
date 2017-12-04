# Python 3

import numpy as np
import pandas as pd
import nltk
import os
import enchant
import scipy.stats

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
    
def misspelled_sentence(tweet):
    words = split_tweet(tweet)
    misspellings = 0
    for word in words:
        if not d.check(word):
            misspellings += 1
    return misspellings

def num_words(tweet):
    words = split_tweet(tweet)
    return len(words)

def misspelled_distributions(tweet):
    misspellings = misspelled_sentence(tweet)
    words = num_words(tweet)

    data = pd.read_csv("misspelling_distribution.csv")

    people = list(data["person"])

    feature = dict()

    for index, row in data.iterrows():
        person = row["person"]
        mean = row["mean"]
        std = row["std"]
        distribution = scipy.stats.norm(mean, std)
        probability = distribution.cdf((misspellings/words) + 0.001) - distribution.cdf((misspellings/words) - 0.001) 
        if person not in feature.keys():
            feature[person] = probability

    factor=1.0/sum(feature.values())
    for k in feature:
      feature[k] = feature[k]*factor

    return feature










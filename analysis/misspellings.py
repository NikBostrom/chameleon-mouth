# Python 3

import numpy as np
import pandas as pd
import nltk
import os
import enchant

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

d = enchant.Dict("en_US")

filepath = "../data/dictionaries/"
files = os.listdir(filepath)
files = [file for file in files if file.split(".")[1] == "csv"]
people = list(map(lambda x: x.split("_")[0], files))

all_tweets = pd.read_csv("all_tweets.csv")

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

all_tweets["misspelled"] = all_tweets.apply(lambda row: misspelled_sentence(row), axis=1)
all_tweets["num_words"] = all_tweets.apply(lambda row: num_words(row), axis=1)
all_tweets["misspelled/word"] = all_tweets["misspelled"] / all_tweets["num_words"]

for person in people:
    data = all_tweets[all_tweets["person"] == person]
    mean = np.mean(data["misspelled/word"])
    std = np.std(data["misspelled/word"])
    
    

#
#for person in people:
#    data = data[data["person"] == person]
#    
#
#print(people)
#tweets = []
#
#
#
#def misspellings(row):
#    word = row["word"]
#    if d.check(word):
#        return 0
#    else:
#        return row["freq"]
#
#percentage = {}
#
#for person, file in zip(people, files):
#    data = pd.read_csv(filepath + file, encoding="latin1")
#    data["num_missed"] = data.apply(lambda row: misspellings(row), axis=1)
#    percentage[person] = sum(list(data["num_missed"])) / sum(list(data["freq"]))

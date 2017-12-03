# Python 3

import numpy as np
import pandas as pd
import nltk
import os
import enchant

filepath = "../data/dictionaries/"
files = os.listdir(filepath)
files = [file for file in files if file.split(".")[1] == "csv"]
people = list(map(lambda x: x.split("_")[0], files))

all_tweets = pd.read_csv("aggregate_tweets/all_tweets.csv")

def misspelled_sentence(row):
    tweet = row["text"]
    words = text.split(" ")

for person in people:
    data = data[data["person"] == person]
    

print(people)
tweets = []

d = enchant.Dict("en_US")

def misspellings(row):
    word = row["word"]
    if d.check(word):
        return 0
    else:
        return row["freq"]

percentage = {}

for person, file in zip(people, files):
    data = pd.read_csv(filepath + file, encoding="latin1")
    data["num_missed"] = data.apply(lambda row: misspellings(row), axis=1)
    percentage[person] = sum(list(data["num_missed"])) / sum(list(data["freq"]))

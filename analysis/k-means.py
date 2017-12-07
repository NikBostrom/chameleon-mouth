# Python 3

import pandas as pd
#import bagofwords
import os

filepath = "../data/raw_tweets/"
files = os.listdir(filepath)
people = list(map(lambda x: x.split("_")[0], files))

tweets = []

for person, file in zip(people, files):
    data = pd.read_csv(filepath + file)
    data["person"] = person
    data = data[["text", "person"]]
    tweets.append(data)
    
tweets = pd.concat(tweets)
tweets.to_csv("aggregate_tweets/all_tweets.csv", index=False)

features = ["avg_tweet_length", "avg_word_length"]
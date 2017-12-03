# Python 3
# @author: nikbostrom

'''
Calculate the average word length and average number of hashtags used by a given person over all their tweets
'''

import os
import pandas as pd

dict_filepath = "../data/dictionaries/"
dict_files = [x for x in os.listdir(dict_filepath) if x.split(".")[1] == "csv"]

raw_tweet_filepath = "../data/raw_tweets/"
raw_tweet_files = os.listdir(raw_tweet_filepath)

people = list(map(lambda x: x.split("_")[0], dict_files))

ave_word_lengths = {}
ave_num_hashtags = {}
ave_num_words = {}

'''
Calculate the average word length and average number of hashtags used by a given person over all their tweets
'''
for person, file in zip(people, dict_files):
    
    data = pd.read_csv(dict_filepath + file, encoding='latin1')
    nwords = 0
    total_length = 0
    nhashtags = 0

    for i, row in data.iterrows():
        word = row["word"]
        try:
            nwords += 1
            total_length += len(word)
            if word == "#":
                nhashtags = row["freq"]
        except:
            print(text)

    if nwords > 0:
        ave_word_lengths[person] = total_length / nwords
        ave_num_hashtags[person] = nhashtags / nwords
    else:
        ave_word_lengths[person] = 0
        ave_num_hashtags[person] = 0

'''
Calculate average number of words per tweet
'''
for person, file in zip(people, raw_tweet_files):
    
    data = pd.read_csv(raw_tweet_filepath + file, encoding='latin1')
    total_words = 0
    num_tweets = 0
    
    for _, row in data.iterrows():
        tweet = row["text"]
        try:
            split_tweet = tweet.split(" ")
            num_tweets += 1
            total_words += len(split_tweet)
        except:
            print(tweet)

        ave_num_words[person] = total_words / num_tweets

print("Average length of words used:", ave_word_lengths)
print("Average number of hashtags used:", ave_num_hashtags)
print("Average number of words: ", ave_num_words)

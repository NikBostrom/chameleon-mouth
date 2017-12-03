# Python 3
# @author: nikbostrom

import os
import pandas as pd
import numpy as np

class Average:
    # Taken from BagOfWords
    def __init__(self, dataset=0, directory=None, extension=None):
        '''
        dataset: int
            A switch integer to determine what dataset we are using
            0 = dictionary (frequency of words)
            1 = parts of speech

        directory: string
            NOTE: Not needed if dataset has been specified.
            The file directory of the folder in which the data can be found.
            Omit the final backslash.

        extension: string
            NOTE: Not needed if dataset has been specified.
            The rest of the data file filenames; anything that comes after
            the person's name.
            Caution: this is not the same as the file extension, i.e. NOT ".csv"
        '''

        if directory != None and extension != None:
            self.directory = directory
            self.extension = extension
        elif dataset == 0:
            self.directory = "../data/dictionaries"
            self.extension = "_dictionary.csv"
        elif dataset == 1:
            self.directory = "../data/partsofspeech"
            self.extension = "_POS.csv"
        else:
            raise ValueError("Invalid dataset inputted")

        self.dict_filepath = "../data/dictionaries/"
        self.dict_files = [x for x in os.listdir(self.dict_filepath) if x.split(".")[1] == "csv"]

        self.raw_tweet_filepath = "../data/raw_tweets/"
        self.raw_tweet_files = os.listdir(self.raw_tweet_filepath)

        self.people = list(map(lambda x: x.split("_")[0], self.dict_files))

        self.ave_num_hashtags = {}
        self.ave_num_words = {}
        self.ave_word_lengths = {}
        self.stdev_ave_word_len_per_tweet = {}


    def ave_word_length(self):
        '''
        Calculate the average word length and average number of hashtags used by a given person over all their tweets
        '''
        for person, file in zip(self.people, self.dict_files):
            
            data = pd.read_csv(self.dict_filepath + file, encoding='latin1')
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
                self.ave_word_lengths[person] = total_length / nwords
                self.ave_num_hashtags[person] = nhashtags / nwords
            else:
                self.ave_word_lengths[person] = 0
                self.ave_num_hashtags[person] = 0

    def ave_nwords_per_tweet(self):
        '''
        Calculate average number of words per tweet and average length of word per tweet
        '''
        for person, file in zip(self.people, self.raw_tweet_files):
            
            data = pd.read_csv(self.raw_tweet_filepath + file, encoding='latin1')
            total_words = 0
            num_tweets = 0
            self.ave_word_lengths_per_tweet = []

            for _, row in data.iterrows():
                tweet = row["text"]
                try:
                    split_tweet = tweet.split(" ")
                    num_tweets += 1
                    total_words += len(split_tweet)
                     
                    sum_w_lengths = 0
                    for w in split_tweet:
                        sum_w_lengths += len(w)
                    ave_wd_ln = sum_w_lengths / len(split_tweet)
                    self.ave_word_lengths_per_tweet.append(ave_wd_ln)
                except:
                    print(tweet)

                self.ave_num_words[person] = total_words / num_tweets

            self.stdev_ave_word_len_per_tweet[person] = np.std(self.ave_word_lengths_per_tweet)


a = Average()
a.ave_nwords_per_tweet()
a.ave_word_length()

print("StDevs", self.stdev_ave_word_len_per_tweet)
print("Average length of words used:", a.ave_word_lengths)
print("Average number of hashtags used:", a.ave_num_hashtags)
print("Average number of words: ", a.ave_num_words)


'''
Now for of the above lists, treat the average values as means of Normal distributions for each person, calculate the probability of seeing the average value for the tweet in question based on said distribution(s), and normalize all such probabilities.
'''


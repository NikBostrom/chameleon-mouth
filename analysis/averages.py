# Python 3
# @author: nikbostrom

import os
import pandas as pd
import numpy as np
from scipy.stats import norm

class Average:
    # Taken from BagOfWords
    def __init__(self, dataset=0, directory=None, extension=None):
        '''
        ----------------------------------------------
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
        ----------------------------------------------
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

        self.ave_word_lengths = {}
        self.ave_num_hashtags = {}

        self.ave_num_words_per_tweet = {}

        self.ave_of_ave_word_lengths_per_tweet = {}
        self.stdev_ave_word_len_per_tweet = {}

        self.probs_given_new_tweet = {}


    def ave_word_length(self):
        '''
        ----------------------------------------------
        Calculate the average word length and average number of hashtags used by a given person over all their tweets
        ----------------------------------------------
        '''
        for person, file in zip(self.people, self.dict_files):
            
            data = pd.read_csv(self.dict_filepath + file, error_bad_lines=False, encoding='latin1')
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
        ----------------------------------------------
        Calculate average number of words per tweet and average length of word PER TWEET
        ----------------------------------------------
        '''
        for person, file in zip(self.people, self.raw_tweet_files):
            
            data = pd.read_csv(self.raw_tweet_filepath + file, error_bad_lines=False, encoding='latin1')
            total_words = 0
            num_tweets = 0
            ave_word_lengths_per_tweet = []

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
                    ave_word_lengths_per_tweet.append(ave_wd_ln)
                except:
                    print(tweet)

            self.ave_num_words_per_tweet[person] = total_words / num_tweets

            self.ave_of_ave_word_lengths_per_tweet[person] = np.mean(ave_word_lengths_per_tweet)

            self.stdev_ave_word_len_per_tweet[person] = np.std(ave_word_lengths_per_tweet)

    def prob_ave_wd_len(self, new_tweet):
        '''
        ----------------------------------------------
        Given a new tweet, calculate the probability that each person said the given tween, based only on the average lenght of the words in the tweet and the average lengths of words used byy each person across all their tweets
        ----------------------------------------------
        '''
        total_length = 0
        for w in new_tweet.split(" "):
            total_length += len(w)
        new_tweet_ave_wd_len = total_length / len(new_tweet.split(" "))

        lens_and_stds = {}

        for person, ave_len in self.ave_word_lengths.items():
            lens_and_stds[person] = (ave_len, self.stdev_ave_word_len_per_tweet[person])

        probs = {}
        for p, (ave_len, std) in lens_and_stds.items():
            temp_prob = norm.cdf(new_tweet_ave_wd_len + 0.00000001, ave_len, std) - norm.cdf(new_tweet_ave_wd_len - 0.00000001, ave_len, std) 
            probs[p] = temp_prob
        
        probs_sum = 0
        for person, prob in probs.items():
            probs_sum += prob

        for person, prob in probs.items():
            if probs_sum > 0:
                probs[person] /= probs_sum
            else:
                probs[person] = 0
        return probs


'''
----------------------------------------------
Code to create csv with average data. Commented out because once calculated, the data is stored in the csv file and need not be recalculated every time the code is run. If the data set(s) change(s), then this can be rerun once to calculate the appropriate values.
----------------------------------------------
a = Average()

a.ave_nwords_per_tweet()
a.ave_word_length()


people = a.ave_word_lengths.keys()

ave_hashtags = []
ave_ave_word_lengths_pt = []
std_ave_wlpt = []
ave_nwords_per_tweet = []

for p in people:
    ave_h = a.ave_num_hashtags[p]
    av_av_wd_len_pt = a.ave_of_ave_word_lengths_per_tweet[p]
    std_ave_w_l = a.stdev_ave_word_len_per_tweet[p]
    ave_wpt = a.ave_num_words_per_tweet[p]

    ave_hashtags.append(ave_h)
    ave_ave_word_lengths_pt.append(av_av_wd_len_pt)
    std_ave_wlpt.append(std_ave_w_l)
    ave_nwords_per_tweet.append(ave_wpt)

averages = pd.DataFrame(data = [people, ave_hashtags, ave_ave_word_lengths_pt, std_ave_wlpt, ave_nwords_per_tweet]).transpose()
averages.columns = ["person", "ave hashtags", "mean wlength per tweet", "std of mean wlength per tweet", "ave num words per tweet"]
averages.to_csv("average_data.csv", index=False)
'''


'''
TESTING
'''
# print("StDevs", a.stdev_ave_word_len_per_tweet)
# print("Average length of words used:", a.ave_word_lengths, "\n---------------")
# print("Average number of hashtags used:", a.ave_num_hashtags)
# print("Average number of words per tweet: ", a.ave_num_words_per_tweet)

# new_tweet = "Eight888"
# print("Probability each person said ", new_tweet, ":", a.prob_ave_wd_len(new_tweet))

# new_tweet2 = "TwelveTwelve"
# print("\nProbability each person said ", new_tweet2, ":", a.prob_ave_wd_len(new_tweet2))

# new_tweet3 = "Fourteen141414"
# print("\nProbability each person said ", new_tweet3, ":", a.prob_ave_wd_len(new_tweet3))
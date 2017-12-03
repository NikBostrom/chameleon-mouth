# Python 3

import numpy as np
import pandas as pd
import glob
import re
from math import log

class BagOfWords:

    def __init__(self):
        '''
        This naive Bayes is so naive, it doesn't know shit yet ...
        '''
        # Returns a list of pathnames that satisfy the input string, with "*" as a wildcard
        self.filenames = glob.glob("../data/dictionaries/*_dictionary.csv")

        # Storage for all people
        self.names_all = []
        self.data_all = []
        self.wordprob_all = []
        self.totalfreq_all = []

    def populate(self):
        '''
        Fill ALL the storage! (Now it knows shit.)
        '''
        for filename in self.filenames:
            
            # Extract the names of the people we are dealing with, from their dictionary.csv filenames  
            # e.g. >>> names_all
            #      ['trump', 'elon']
            m = re.search("../data/dictionaries/(.*)_dictionary.csv", filename)
            if m:
                name = m.group(1)
                self.names_all.append(name)

            # Store the word occurence data for each person
            # Data columns are (freq, word, prob, freq_iter, prob_iter), where
            #   freq_iter and prob_iter are the result of Laplace smoothing with
            #   increment of 1
            # e.g. >>> data[0]
            #      [1230, 'the', 0.050, 1231, 0.049]
            data = pd.read_csv(filename).as_matrix()

            wordprob = {} # (key: word), (value: probability)
            totalfreq = 0 # running total of frequencies

            # Get frequency and probability data for all words
            # Do not use Laplace smoothing
            for row in data:
                word, freq, prob = row[1], row[0], row[2]
                wordprob[word] = prob
                totalfreq += freq

            # Commit everything to global storage
            self.data_all.append(data)
            self.wordprob_all.append(wordprob)
            self.totalfreq_all.append(totalfreq)

    def getlogprobs(self, word):
        '''
        For a specific word, find the log probability of occurence, given each of the people
        '''
        # Storage of logprobs of the input word for each given person
        logprob_list = np.zeros(len(self.names_all))

        # For each person, get the dictionary of probabilities
        for i, wordprob in enumerate(self.wordprob_all):
            # If word exists, return the frequency
            if word in wordprob:
                prob = wordprob[word]
            # Otherwise, assign a small probability under Ge-Zhou-Bostrom smoothing assumptions
            else:
                prob = 1./sum(self.totalfreq_all)
            logprob_list[i] = log(prob)
        
        return logprob_list

    def parsetweet(self, tweet):
        '''
        Find the normalized probability that a tweet was written by each of the people
        '''
        # Initialize running count of individual logprobs
        logprobsums = np.zeros(len(self.names_all))

        # Go through words in tweet; sum up log probabilities for all people
        for word in tweet:
            logprobword = self.getlogprobs(word)
            try:
                logprobsums = logprobword + logprobsums
            except:
                print("Number of people mismatch?")

        # Subtract all values by max value
        logprobsums_scaled = logprobsums - max(logprobsums)

        # Take element-wise exponent
        probsums = [np.exp(x) for x in logprobsums_scaled]

        # Create a dictionary of (key: name), (value: probability of seeing tweet)
        probsums_norm = {}
        for i, probsum in enumerate(probsums):
            name = self.names_all[i]
            probsums_norm[name] = probsum/sum(probsums)

        return probsums_norm

    def run(self, tweet):
        self.populate()
        return self.parsetweet(tweet)
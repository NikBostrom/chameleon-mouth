# Python 3

import pandas as pd
import glob
import re
from math import log

class BagOfWords:

    # this naive Bayes is so naive, it doesn't know shit yet!
    def __init__(self):
        # returns a list of pathnames that satisfy the input string, with "*" as a wildcard
        self.filenames = glob.glob("../data/*_dictionary.csv")

        # storage
        self.names_all = []
        self.data_all = []
        self.wordprob_all = []
        self.totalfreq_all = []

    # fill ALL the storage!
    def populate(self):
        for filename in self.filenames:
            
            # extract the names of the people we are dealing with, from their dictionary.csv filenames  
            # e.g. >>> names_all
            #      ['trump', 'elon']
            m = re.search("../data/(.*)_dictionary.csv", filename)
            if m:
                name = m.group(1)
                self.names_all.append(name)

            # store the word occurence data for each person
            # data columns are (freq, word, prob, freq_iter, prob_iter), where
            #   freq_iter and prob_iter are the result of Laplace smoothing with
            #   increment of 1
            # e.g. >>> data[0]
            #      [1230, 'the', 0.050, 1231, 0.049]
            data = pd.read_csv(filename).as_matrix()

            wordprob = {} # key: word (string), value: probability (float)
            totalfreq = 0 # running total of frequencies (int)

            # get frequency and probability data for all words
            for row in data:
                word, freq, prob = row[1], row[3], row[4]
                wordprob[word] = prob
                totalfreq += freq

            # commit everything to global storage
            self.data_all.append(data)
            self.wordprob_all.append(wordprob)
            self.totalfreq_all.append(totalfreq)

    def getlogprobs(self, word):

        # storage of logprobs of the input word for each person
        logprob_list = []

        # for each person, get the dictionary of probabilities
        for i, wordprob in enumerate(wordprob_all):
            # if word exists, return the frequency
            if word in wordprob:
                prob = wordprob[word]
            # otherwise, assign a small probability under Laplace smoothing assumptions
            else:
                prob = 1/totalfreq_all[i]
            logprob_list.append(-log(prob))
        
        return logprob_list

    def 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Retrievs an equal amount of random tweets from each of the authors
Useful for k-nearest neighbors training when equal sample sizes are important
'''

import pandas as pd
import os
import nltk
from util import convert
import random

#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
#nltk.download("tagsets")
#nltk.help.upenn_tagset()

total_data = pd.read_csv("training_set.csv")

people = list(total_data.person.unique())
samples = []

for person in people:
	data_person = total_data[total_data["person"] == person]
	sample = data_person.sample(n=1000, random_state=10)
	samples.append(sample)

equal_sample = pd.concat(samples)
equal_sample.to_csv("knn_training_set.csv", index=False)

# total_data["random"] = [random.random() for _ in range(len(total_data))]
# test_set = total_data[total_data["random"] < 0.5]
# training_set = total_data[total_data["random"] >= 0.5]

# test_set.to_csv("test_set.csv", index=False)
# training_set.to_csv("training_set.csv", index=False)
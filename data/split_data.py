#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 10:30:32 2017

@author: jasonge
"""

import pandas as pd
import os
import nltk
from util import convert
import random

#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
#nltk.download("tagsets")
#nltk.help.upenn_tagset()

total_data = pd.read_csv("all_tweets.csv")
total_data["random"] = [random.random() for _ in range(len(total_data))]
test_set = total_data[total_data["random"] < 0.5]
training_set = total_data[total_data["random"] >= 0.5]

test_set.to_csv("test_set.csv", index=False)
training_set.to_csv("training_set.csv", index=False)
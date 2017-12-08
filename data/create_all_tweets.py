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

file_path = "raw_tweets/"

files = os.listdir(file_path)

data_files = []

for file in files:
	person = file.split("_")[0]
	data = pd.read_csv(file_path + file)
	data = data[["text"]]
	data["person"] = person
	data_files.append(data)

all_tweets = pd.concat(data_files)
all_tweets.to_csv("test.csv", index=False)

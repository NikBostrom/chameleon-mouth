#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 19:53:29 2017

@author: jasonge
"""

import pandas as pd

data = pd.read_csv("trump_tweets_new.csv")

trump_dict = dict()

for index, row in data.iterrows():
    text = row["text"]
    words = text.split(" ")
    for word in words:
        w = word.lower()
        
        
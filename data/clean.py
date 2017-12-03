#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 19:53:29 2017

@author: jasonge
"""

import pandas as pd
import csv

data = pd.read_csv("trump_tweets_new.csv")

trump_dict = dict()

for index, row in data.iterrows():
    text = row["text"]
    try:
        words = text.split(" ")
        for word in words:
            w = word.lower()
            if w not in trump_dict.keys():
                trump_dict[w] = 1
            else:
                trump_dict[w] += 1
    except:
        print(text)
        

dictionary = pd.DataFrame({"word": list(trump_dict.keys()), "freq": list(trump_dict.values())})
dictionary = dictionary.sort(columns=["freq"], ascending= False)
dictionary["probability"] = dictionary["freq"] / sum(dictionary["freq"])
dictionary.to_csv("trump_dictionary.csv", index = False)
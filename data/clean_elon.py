#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 21:21:48 2017

@author: jasonge
"""

import pandas as pd
import csv
import nltk

def adjust(row):
    text = row["raw"]
    return text[2:]

data = pd.read_csv('elonmusk_tweets.csv')

data["text"] = data.apply(lambda row: adjust(row), axis = 1)

elon_dict = dict()

for index, row in data.iterrows():
    text = row["text"]
    try:
        words = text.split(" ")
        for word in words:
            w = word.lower()
            if w not in elon_dict.keys():
                elon_dict[w] = 1
            else:
                elon_dict[w] += 1
    except:
        print(text)
        

dictionary = pd.DataFrame({"word": list(elon_dict.keys()), "freq": list(elon_dict.values())})
dictionary = dictionary.sort(columns=["freq"], ascending= False)
dictionary["probability"] = dictionary["freq"] / sum(dictionary["freq"])
dictionary.to_csv("elon_dictionary.csv", index = False)


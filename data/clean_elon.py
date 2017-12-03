#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 21:21:48 2017

@author: jasonge
"""

import pandas as pd
import csv
import nltk

def convert(string):
    if len(string) < 3:
        return string
    s = string
    first = s[0]
    if not first.isalnum():
        s = s[1:]
    last = s[len(s) - 1]
    if not last.isalnum():
        s = s[:(len(s) - 1)]
    return s

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
            w = convert(w)
            if w not in elon_dict.keys():
                elon_dict[w] = 1
            else:
                elon_dict[w] += 1
    except:
        print(text)
        

dictionary = pd.DataFrame({"word": list(elon_dict.keys()), "freq": list(elon_dict.values())})
dictionary = dictionary.sort_values(by=["freq"], ascending= False)
dictionary["probability"] = dictionary["freq"] / sum(dictionary["freq"])
dictionary["freq_iterated"] = dictionary["freq"] + 1
dictionary["probability_iterated"] = dictionary["freq_iterated"] / sum(dictionary["freq_iterated"])
dictionary.to_csv("elon_dictionary.csv", index = False)


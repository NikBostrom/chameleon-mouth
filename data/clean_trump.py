#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 19:53:29 2017

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

data = pd.read_csv("trump_tweets_new.csv")

trump_dict = dict()

for index, row in data.iterrows():
    text = row["text"]
    try:
        words = text.split(" ")
        for word in words:
            w = word.lower()
            w = convert(w)
            if w not in trump_dict.keys():
                trump_dict[w] = 1
            else:
                trump_dict[w] += 1
    except:
        print(text)
        

dictionary = pd.DataFrame({"word": list(trump_dict.keys()), "freq": list(trump_dict.values())})
dictionary = dictionary.sort_values(by=["freq"], ascending= False)
dictionary["probability"] = dictionary["freq"] / sum(dictionary["freq"])
dictionary["freq_iterated"] = dictionary["freq"] + 1
dictionary["probability_iterated"] = dictionary["freq_iterated"] / sum(dictionary["freq_iterated"])
dictionary.to_csv("trump_dictionary.csv", index = False)




#text = nltk.tokenize.word_tokenize("I went to the beach")
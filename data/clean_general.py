#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 10:30:32 2017

@author: jasonge
"""


import pandas as pd
import os
import nltk

def convert(string):
    if len(string) < 3:
        return string
    s = string
    first = s[0]
    if not first.isalnum():
        if first != "#":
            s = s[1:]
    last = s[len(s) - 1]
    if not last.isalnum():
        s = s[:(len(s) - 1)]
    return s

files = os.listdir("raw_tweets")
people = list(map(lambda x: x.split("_")[0], files))

for person, file in zip(people, files):
    
    data = pd.read_csv("raw_tweets/" + file)
    
    dict_item = dict()
    
    for index, row in data.iterrows():
        text = row["text"]
        try:
            words = text.split(" ")
            for word in words:
                w = word.lower()
                w = convert(w)
                if w not in dict_item.keys():
                    dict_item[w] = 1
                else:
                    dict_item[w] += 1
        except:
            print(text)
            
    
    dictionary = pd.DataFrame({"word": list(dict_item.keys()), "freq": list(dict_item.values())})
    dictionary = dictionary.sort_values(by=["freq"], ascending= False)
    dictionary["probability"] = dictionary["freq"] / sum(dictionary["freq"])
    dictionary["freq_iterated"] = dictionary["freq"] + 1
    dictionary["probability_iterated"] = dictionary["freq_iterated"] / sum(dictionary["freq_iterated"])
    dictionary.to_csv("dictionaries/" + person + "_dictionary.csv", index = False)

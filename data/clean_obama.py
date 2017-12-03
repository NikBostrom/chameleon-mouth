#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 21:36:07 2017

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
        if first != "#":
            s = s[1:]
    last = s[len(s) - 1]
    if not last.isalnum():
        s = s[:(len(s) - 1)]
    return s

person = "obama"

data = pd.read_csv('BarackObama.csv')

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
dictionary.to_csv(person + "_dictionary.csv", index = False)

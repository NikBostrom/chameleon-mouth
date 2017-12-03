#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 21:36:07 2017

@author: jasonge
"""

import pandas as pd
import csv
import nltk

person = "obama"

data = pd.read_csv('BarackObama.csv')

dict_item = dict()

for index, row in data.iterrows():
    text = row["text"]
    try:
        words = text.split(" ")
        for word in words:
            w = word.lower()
            if w not in dict_item.keys():
                dict_item[w] = 1
            else:
                dict_item[w] += 1
    except:
        print(text)
        

dictionary = pd.DataFrame({"word": list(dict_item.keys()), "freq": list(dict_item.values())})
dictionary = dictionary.sort(columns=["freq"], ascending= False)
dictionary["probability"] = dictionary["freq"] / sum(dictionary["freq"])
dictionary.to_csv(person + "_dictionary.csv", index = False)

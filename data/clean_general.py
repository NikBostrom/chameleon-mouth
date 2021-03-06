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

training_set = pd.read_csv("training_set.csv")

people = list(set(training_set["person"]))

for person in people:
    
    data = training_set[training_set["person"] == person]
    
    dict_item = dict()
    pos_dict = dict()
    
    for index, row in data.iterrows():
        text = row["text"]
        try:
            words = text.split(" ")
            words = [convert(word) for word in words]
            sentence = " ".join(words)
            text = nltk.word_tokenize(sentence)
            tagged_text = nltk.pos_tag(text)
            for (word, POS) in tagged_text:
                
                if word not in dict_item.keys():
                    dict_item[word] = 1
                else:
                    dict_item[word] += 1
                if POS not in pos_dict.keys():
                    pos_dict[POS] = 1
                else:
                    pos_dict[POS] += 1
        except:
            print(text)
            
    
    dictionary = pd.DataFrame({"word": list(dict_item.keys()), "freq": list(dict_item.values())})
    dictionary = dictionary[["word", "freq"]]
    dictionary = dictionary.sort_values(by=["freq"], ascending= False)
    dictionary["probability"] = dictionary["freq"] / sum(dictionary["freq"])
    dictionary["freq_iterated"] = dictionary["freq"] + 1
    dictionary["probability_iterated"] = dictionary["freq_iterated"] / sum(dictionary["freq_iterated"])
    dictionary.to_csv("dictionaries/" + person + "_dictionary.csv", index = False)
    pos = pd.DataFrame({"POS": list(pos_dict.keys()), "freq": list(pos_dict.values())})
    pos["probability"] = pos["freq"] / sum(pos["freq"])
    pos = pos.sort_values(by=["freq"], ascending = False)
    pos.to_csv("partsofspeech/" + person + "_POS.csv", index=False )
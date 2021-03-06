# Python 3
print()
print("Loading...")
print()

import bagofwords
import pandas as pd
import nltk
import time
import averages
from misspellings_functions import misspelled_distributions

aves = averages.Precalcd_Ave()
bag = bagofwords.BagOfWords()
pos = bagofwords.BagOfWords(dataset=1)
weights = list(pd.read_csv("optimal_weights.csv")["weights"])

def analyze(tweet):
    try:
        
        word_list = tweet.split(" ")
        
        text = nltk.word_tokenize(tweet)
        tagged_text = nltk.pos_tag(text)
        pos_list = list(list(zip(*tagged_text))[1])
    
        f_bag = bag.get(word_list)
        f_pos = pos.get(pos_list)
        f_misspelled = misspelled_distributions(tweet)
        f_length = aves.probs(tweet)
    
        features = [f_bag, f_pos, f_misspelled, f_length]
    
        f_w = zip(features, weights)
    
        people = f_bag.keys()
    
        final = dict()
        for feature, weight in f_w:
            for person in people:
                if person not in final.keys():
                    final[person] = feature[person] * weight
                else:
                    final[person] += feature[person] * weight
        
        p = max(final, key=final.get)
    except: 
        p = ("error", {})
    return (p, final)

while(True):
    user_input = input("Please Enter Your Tweet (Control-C to Quit): ")
    print()
    output = analyze(user_input)
    prediction = output[0]
    distribution = output[1]

    print("Prediction: " + prediction + "\n")
    print("Distribution: ")
    for key in distribution.keys():
        print(key + ": " + "{0:.0f}%".format(distribution[key] * 100))
    print()
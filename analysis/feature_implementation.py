# Python 3

import pandas as pd
import bagofwords
import nltk
import time
from multiprocessing.dummy import Pool

import averages

from misspellings_functions import misspelled_distributions

start = time.time()

aves = averages.Precalcd_Ave()
bag = bagofwords.BagOfWords()
pos = bagofwords.BagOfWords(dataset=1)


test_set = pd.read_csv("test_set_sample.csv")

weights = [0.7488068419804749, 0.25119315801952524, 0.0, 0.0]
#weights = [0.25, 0.25, 0.25, 0.25]

#weights = [0.5,0.5,0.0,0.0]
weights = [1.0, 0, 0, 0]

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
        p = "error"
    return p

tweets = list(test_set["text"])
predictions = [analyze(tweet) for tweet in tweets]


test_set["prediction"] = predictions
test_set["correct"] = test_set["prediction"] == test_set["person"]

correct = test_set[test_set["correct"] == True]
num_correct = len(correct)
test_set.to_csv("predictions_with_validation.csv", index=False)
num_total = len(test_set)
print("Percent Correct" + str(num_correct/num_total))

people = list(set(test_set["person"]))

for person in people:
    temp = test_set[test_set["person"] == person]
    num = len(temp)
    correct = temp[temp["correct"] == True]
    c = len(correct)
    print("Person: " + person)
    print("Tweets: " + str(num))
    print("Number Correct: " + str(c))
    print("Percentage Correct: " + str(c / num))
    print()
    
print(weights)

print(str(time.time() - start))

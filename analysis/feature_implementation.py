# Python 3

import pandas as pd
import bagofwords

import averages

from misspellings_functions import misspelled_distributions

f_1 = {"obama": 0.1, "trump": 0.3, "neil": 0.5, "kim": 0.05, "elon": 0.05}
f_2 = {"obama": 0.3, "trump": 0.1, "neil": 0.2, "kim": 0.3, "elon": 0.1}

# bag = bagofwords.BagOfWords()
# bag_data = bag.get(["trump"])
# print("Bag data:", bag_data)

tweet = "That special hat delivery will take place deep within the real, but fictional (of course), tunnel we are building under LA while you drive the giant machine blindfolded. This will actually happen."

aves = averages.Precalcd_Ave()

word_list = tweet.split(" ")

bag = bagofwords.BagOfWords()
f_bag = bag.get(word_list)
f_misspelled = misspelled_distributions(tweet)
f_length = aves.probs(tweet)

weights = [0.333,0.333,0.333]
features = [f_bag, f_misspelled, f_length]

f_w = zip(features, weights)

people = f_bag.keys()

final = dict()

for feature, weight in f_w:
    for person in people:
        if person not in final.keys():
            final[person] = feature[person] * weight
        else:
            final[person] += feature[person] * weight

print(final)



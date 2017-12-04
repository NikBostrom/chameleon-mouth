# Python 3

import pandas as pd
import bagofwords

import averages

from misspellings_functions 
import misspelled_distributions

f_1 = {"obama": 0.1, "trump": 0.3, "neil": 0.5, "kim": 0.05, "elon": 0.05}
f_2 = {"obama": 0.3, "trump": 0.1, "neil": 0.2, "kim": 0.3, "elon": 0.1}

# bag = bagofwords.BagOfWords()
# bag_data = bag.get(["trump"])
# print("Bag data:", bag_data)

aves = averages.Precalcd_Ave()
ave_hashtags = aves.ave_num_words_per_tweet
mean_word_lengths = aves.ave_of_ave_word_lengths_per_tweet
std_word_lengths = aves.stdev_ave_word_len_per_tweet

print(ave_hashtags, mean_word_lengths, std_word_lengths)

tweet = "STEM education needs to be funded"
word_list = tweet.split(" ")

bag = bagofwords.BagOfWords()
f_bag = bag.get(word_list)
f_misspelled = misspelled_distributions(tweet)

weights = [0.0, 1.0]
features = [f_bag, f_misspelled]

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



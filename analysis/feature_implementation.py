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

aves = averages.Precalcd_Ave()
bag = bagofwords.BagOfWords()

test_set = pd.read_csv("../data/test_set.csv")
test_set = test_set.sample(1000)
test_set = test_set.reset_index()

weights = [0.333,0.333,0.333]

predictions = []

num_total = len(test_set)

for index, row in test_set.iterrows():
    try:
        tweet = row["text"]
    
        word_list = tweet.split(" ")
    
        f_bag = bag.get(word_list)
        f_misspelled = misspelled_distributions(tweet)
        f_length = aves.probs(tweet)
    
    
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
        
        p = max(final, key=final.get)
    except:
        p = "error"
    predictions.append(p)
    print("prediction: " + p + " actual: " + row["person"] + " progress: " + str(index/num_total))
    
test_set["prediction"] = predictions
test_set["correct"] = test_set["prediction"] == test_set["person"]

correct = test_set[test_set["correct"] == True]
num_correct = len(correct)
test_set.to_csv("predictions.csv", index=False)
print("Percent Correct" + (num_correct/num_total))


#def prediction(row):
#
#    tweet = row["text"]
#
#    word_list = tweet.split(" ")
#
#    f_bag = bag.get(word_list)
#    f_misspelled = misspelled_distributions(tweet)
#    f_length = aves.probs(tweet)
#
#
#    features = [f_bag, f_misspelled, f_length]
#
#    f_w = zip(features, weights)
#
#    people = f_bag.keys()
#
#    final = dict()
#
#    for feature, weight in f_w:
#        for person in people:
#            if person not in final.keys():
#                final[person] = feature[person] * weight
#            else:
#                final[person] += feature[person] * weight
#
#    return max(final, key=final.get)

#test_set["prediction"] = data.apply(lambda row: prediction(row), axis = 1)




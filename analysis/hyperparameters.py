# Python 3

import pandas as pd
import bagofwords
import nltk
import time
from multiprocessing.dummy import Pool
from operator import add

import averages

from misspellings_functions import misspelled_distributions

validation_set = pd.read_csv("validation_set.csv")
validation_set = validation_set.reset_index()
validation_set = validation_set.head(1000)

aves = averages.Precalcd_Ave()
bag = bagofwords.BagOfWords()
pos = bagofwords.BagOfWords(dataset=1)

weights = [0.25,0.25,0.25,0.25]

alpha = 0.99
beta = 1.0

start = time.time()

for index, row in validation_set.iterrows():
    try:
        tweet = row["text"]
        word_list = tweet.split(" ")
        
        text = nltk.word_tokenize(tweet)
        tagged_text = nltk.pos_tag(text)
        pos_list = list(list(zip(*tagged_text))[1])
    
        f_bag = bag.get(word_list)
        f_pos = pos.get(pos_list)
        f_misspelled = misspelled_distributions(tweet)
        f_length = aves.probs(tweet)
    
        features = [f_bag, f_pos, f_misspelled, f_length]
    
        feature_results = list(map(lambda x: max(x, key=x.get), features))
    except:
        feature_results =[]
    if len(list(feature_results)) > 0:
        person = row["person"]
        results = []
        for result in feature_results:
            if result == person:
                results.append(0.01*beta)
            else:
                results.append(-0.01*beta)
        weights = list(map(add, weights, results))
        weights = [0 if i < 0 else i for i in weights]
        weights = [float(i)/sum(weights) for i in weights]
    beta = beta * alpha
    if index%50 == 0:
        print(index)
print(weights)
print(str(time.time() - start))

data = pd.Dataframe(weights, columns = ["weights"])
data.to_csv("optimal_weights.csv", index=False)









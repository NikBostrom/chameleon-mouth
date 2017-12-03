# Python 3

import pandas as pd
import bagofwords

f_1 = {"obama": 0.1, "trump": 0.3, "neil": 0.5, "kim": 0.1}
f_2 = {"obama": 0.3, "trump": 0.1, "neil": 0.2, "kim": 0.4}

# bag = bagofwords.BagOfWords()
# bag_data = bag.run(["trump"])
# print(bag_data)

weights = [0.3, 0.7]
features = [f_1, f_2]

f_w = zip(features, weights)

people = f_1.keys()

final = dict()

for feature, weight in f_w:
    for person in people:
        if person not in final.keys():
            final[person] = feature[person] * weight
        else:
            final[person] += feature[person] * weight

print(final)



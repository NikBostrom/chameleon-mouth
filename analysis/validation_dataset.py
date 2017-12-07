# Python 3

import pandas as pd
import bagofwords
import nltk
import time
from multiprocessing.dummy import Pool

import averages

from misspellings_functions import misspelled_distributions

df2 = pd.read_csv("test_set_sample.csv")
df2 = df2.drop(["prediction", "correct"], axis=1)

df1 = pd.read_csv("../data/test_set.csv")
df1["index"] = df1.index

print(len(df1))
df1 = df1[~df1["index"].isin(list(df2["index"]))]
print(len(df1))

validation_set = df1
validation_set_sample = validation_set.sample(n=1000, random_state=10)
validation_set_sample = validation_set_sample.drop("index", axis=1)
validation_set_sample.to_csv("validation_set.csv", index=False)



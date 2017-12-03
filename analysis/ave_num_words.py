# Python 3
# @author: nikbostrom

import os
import pandas as pd

filepath = "../data/dictionaries/"
files = os.listdir(filepath)
people = list(map(lambda x: x.split("_")[0], files))

print(files)
print(people)

ave_word_lengths = {}

for person, file in zip(people, files):
    
    data = pd.read_csv(filepath + file)
    nwords = 0
    total_length = 0
    
    for _, row in data.iterrows():
        word = row["word"]
        try:
            # print("Word:", word, "- Length:", len(word))
            nwords += 1
            total_length += len(word)
        except:
            print(text)

        ave_word_lengths[person] = total_length / nwords

print(ave_word_lengths)
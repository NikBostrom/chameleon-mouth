'''
For each person, outputs two csv files:
	1. The words of their tweets.
	2. The parts of speech of the words of their tweets,
where there exists one tweet per line, with entries (words/POS) separated by commas.
'''

from util import convert
import pandas as pd
import os
import nltk

files = os.listdir("raw_tweets")
people = list(map(lambda x: x.split("_")[0], files))

for person, file in zip(people, files):
    
    data = pd.read_csv("raw_tweets/" + file)
    

    for index, row in data.iterrows():
        text = row["text"]
        try:
            
            words = text.split(" ")
            words = [convert(word) for word in words]
            
            sentence = " ".join(words)
            text = nltk.word_tokenize(sentence)
            tagged_text = nltk.pos_tag(text)
            POSs = [tag[1] for tag in tagged_text]

            


        except:
            print(text)
            
    # dictionary = pd.DataFrame({"word": list(dict_item.keys()), "freq": list(dict_item.values())})
    # dictionary = dictionary[["word", "freq"]]
    # dictionary = dictionary.sort_values(by=["freq"], ascending= False)
    # dictionary["probability"] = dictionary["freq"] / sum(dictionary["freq"])
    # dictionary["freq_iterated"] = dictionary["freq"] + 1
    # dictionary["probability_iterated"] = dictionary["freq_iterated"] / sum(dictionary["freq_iterated"])
    # dictionary.to_csv("dictionaries/" + person + "_dictionary.csv", index = False)
    # pos = pd.DataFrame({"POS": list(pos_dict.keys()), "freq": list(pos_dict.values())})
    # pos["probability"] = pos["freq"] / sum(pos["freq"])
    # pos = pos.sort_values(by=["freq"], ascending = False)
    # pos.to_csv("partsofspeech/" + person + "_POS.csv", index=False )
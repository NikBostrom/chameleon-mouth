import pandas as pd
import os

# Converts a string to lowercase formatting
def convert(string):
    if len(string) < 3:
        return string.lower()
    s = string
    first = s[0]
    if not first.isalnum():
        if first != "#":
            s = s[1:]
    last = s[len(s) - 1]
    if not last.isalnum():
        s = s[:(len(s) - 1)]
    return s.lower()


# Gets all tweets and the POSs of all words in the tweets
def gettweetsandPOSs():

    files = os.listdir("raw_tweets")
    people = list(map(lambda x: x.split("_")[0], files))

    tweets_all = {}
    tweet_POSs_all = {}

    for person, file in zip(people, files):
        
        data = pd.read_csv("raw_tweets/" + file)
        
        tweets = []
        tweet_POSs = []

        for index, row in data.iterrows():
            text = row["text"]
            try:
                
                words = text.split(" ")
                tweet = [convert(word) for word in words]
                
                sentence = " ".join(tweet)
                text = nltk.word_tokenize(sentence)
                tagged_text = nltk.pos_tag(text)
                tweet_POSs = [tag[1] for tag in tagged_text]

                tweets.append(tweet)
                tweet_POSs.append(tweet_POSs)

            except:
                print(text)

        tweets_all[person] = tweets
        tweet_POSs_all[person] = tweet_POSs

    return tweets_all, tweet_POSs_all

'''
Generates dictionaries of (key: author), (value: list of their tweets), where
tweets are represented as lists of words. Gives two dictionaries: one for 
the words themselves, and one for the POS of those words
'''
def gettweetsbyauthorship(datafile="all_tweets.csv"):
    data = pd.read_csv(datafile)
    
    people = list(data.person.unique())
    
    tweets_all = {person: [] for person in people}
    tweets_POSs_all = {person: [] for person in people}

    for index, row in data.iterrows():
        text = str(row["text"])
        person = str(row["person"])
        
        try:
            words = text.split(" ")
            tweet = [convert(word) for word in words]
            
            sentence = " ".join(tweet)
            text = nltk.word_tokenize(sentence)
            tagged_text = nltk.pos_tag(text)
            tweet_POSs = [tag[1] for tag in tagged_text]

            tweets_all[person].append(tweet)
            tweets_POSs_all[person].append(tweet_POSs)
        except Exception as e:
            print(e)

    return tweets_all, tweets_POSs_all
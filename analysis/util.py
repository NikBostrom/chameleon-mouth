# utility functions

import pandas as pd
import numpy as np
import nltk

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
# Returns two dictionaries:
#   1. A dictionary of (key: person name), (value: list of tweets, where each tweet is a list of words)
#   2. A dictionary of (key: person name), (value: list of tweet POSs, where each tweet is a list of POSs)
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

# Gets all tweets and assigns authorship
# Returns a dictionary of (key: text of the tweet, as a string), (value: author, as a string)
def gettweets(datafile="all_tweets.csv"):
    data = pd.read_csv(datafile)
    
    text_to_author = {}
    text_to_wordlist = {}
    text_to_POSlist = {}

    wordfreq = {}
    POSfreq = {}

    people = list(data.person.unique())
    count = np.zeros(len(people))

    for index, row in data.iterrows():
        text = str(row["text"])
        person = str(row["person"])

        if len(text) < 300 and count[people.index(person)] < 5000:        
            try:

                text_to_author[text] = person

                wordlist = tweet_str_to_wordlist(text)
                POSlist = tweet_str_to_POSlist(text)

                for word in wordlist:
                    if word in wordfreq:
                        wordfreq[word] += 1
                    else:
                        wordfreq[word] = 1

                for POS in POSlist:
                    if POS in POSfreq:
                        POSfreq[POS] += 1
                    else:
                        POSfreq[POS] = 1

                text_to_wordlist[text] = wordlist
                text_to_POSlist[text] = POSlist

                count[people.index(person)] += 1
            except Exception as e:
                print(e)

    return text_to_author, text_to_wordlist, text_to_POSlist, wordfreq, POSfreq

# For k-NN
def getknntrainingtweets(datafile="knn_training_set.csv"):
    data = pd.read_csv(datafile)
    
    text_to_author = {}
    text_to_wordlist = {}
    text_to_POSlist = {}

    wordfreq = {}
    POSfreq = {}

    people = list(data.person.unique())

    for index, row in data.iterrows():
        text = str(row["text"])
        person = str(row["person"])

        if len(text) < 300:        
            try:

                text_to_author[text] = person

                wordlist = tweet_str_to_wordlist(text)
                POSlist = tweet_str_to_POSlist(text)

                for word in wordlist:
                    if word in wordfreq:
                        wordfreq[word] += 1
                    else:
                        wordfreq[word] = 1

                for POS in POSlist:
                    if POS in POSfreq:
                        POSfreq[POS] += 1
                    else:
                        POSfreq[POS] = 1

                text_to_wordlist[text] = wordlist
                text_to_POSlist[text] = POSlist

            except Exception as e:
                print(e)

    return text_to_author, text_to_wordlist, text_to_POSlist, wordfreq, POSfreq

# Converts a tweet, as a string, to a list of its words
# e.g. "This is a tweet" -> ["this", "is", "a", "string"]
def tweet_str_to_wordlist(tweet):
    words = tweet.split(" ")
    tweet_wordlist = [convert(word) for word in words if word != ""]
    return tweet_wordlist

# Converts a tweet, as a string, to a list of its POS tags
# e.g. "This is a tweet" -> ['DT', 'VBZ', 'DT', 'NN']
def tweet_str_to_POSlist(tweet):
    tweet_wordlist = tweet_str_to_wordlist(tweet)
    sentence = " ".join(tweet_wordlist)
    text = nltk.word_tokenize(sentence)
    tagged_text = nltk.pos_tag(text)
    tweet_POSlist = [tag[1] for tag in tagged_text]
    return tweet_POSlist
# Python 3

import util

class k_Nearest:
    def __init__(self, datafile="all_tweets.csv"):
    	self.tweets_all, self.tweets_POSs_all = util.gettweetsandPOSs()
    	self.people = self.tweets_all.keys()

    def wordsimilarity(self, tweet_new):
    	
    	occurrences_all = np.zeros(len(tweets_all.values()))
    	for i, tweet in enumerate(tweets_all.values()):
    		occurrences = 0
    		for word in tweet_new:
    			occurrences += tweet.count(word)
    		occurrences_all[i] = occurrences
    	
    	return occurrences_all

    def compare(self, tweet_new):
    	for 

print(convert("test"))
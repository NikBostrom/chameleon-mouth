# Python 3

import util

class k_Nearest:
    def __init__(self, datafile="all_tweets.csv"):
    	self.tweets_all, self.tweets_POSs_all = util.gettweetsandPOSs()
    	self.people = self.tweets_all.keys()

    def similarity(self, tweet_new, tweets_all_values):
    	
    	occurrences_all = np.zeros(len(tweets_all_values))
    	for i, tweet in enumerate(tweets_all.values()):
    		occurrences = 0
    		for word in tweet_new:
    			occurrences += tweet.count(word)
    		occurrences_all[i] = occurrences
    	
    	# Scale the values so that the maximum value is 1
    	occurrences_all_norm = [x/max(occurrences_all) for x in occurrences_all]

    	return occurrences_all_norm

    def word_similarity(self, tweet_words_new):
    	return similarity(tweet_words_new, self.tweets_all.values())

    def POS_similarity(self, tweet_POSs_new):
    	return similarity(tweet_POSs_new, self.tweets_POSs_all.values())

    def otherfeatures(self, tweet_words_new):
    	
    	lenoftweet_similarity = np.zeros(len(self.tweets_all.values()))
    	for i, tweet in enumerate(self.tweets_all.values()):
    		for word in tweet_words_new:

    # len of tweet
    # avg len of word
    # number of hashtags
    # number of links
    # number of @mentions
    def compare(self, tweet_new):
    	for 

print(convert("test"))
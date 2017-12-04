# Python 3

import util
import numpy as np

class k_Nearest:
    def __init__(self, datafile="all_tweets.csv"):
    	self.tweets_all, self.tweets_POSs_all = util.gettweetsandPOSs()
    	self.people = self.tweets_all.keys()

    # def occurence_similarity(self, tweet_new, tweets_all_values):
    	
    # 	occurrences_all = np.zeros(len(tweets_all_values))
    # 	for i, tweet_data in enumerate(tweets_all.values()):
    # 		occurrences = 0
    # 		for word in tweet_new:
    # 			occurrences += tweet_data.count(word)
    # 		occurrences_all[i] = occurrences
    	
    # 	# Scale the values so that the maximum value is 1
    # 	occurrences_all_norm = np.array([x/max(occurrences_all) for x in occurrences_all])

    # 	return occurrences_all_norm

    # def word_similarity(self, tweet_words_new):
    # 	'''
    # 	Call this if you want to calculate word occurrence similarity separately. Usually better to just call
    # 	all_wordbased_similarities since that also calculates this
    # 	'''
    # 	return occurence_similarity(tweet_words_new, self.tweets_all.values())

    # def POS_similarity(self, tweet_POSs_new):
    # 	return occurence_similarity(tweet_POSs_new, self.tweets_POSs_all.values())

    def all_similarities(self, tweet_new):

    	no_of_tweets = len(self.tweets_all.values())
    	if len(self.tweets_all.values()) != len(self.tweets_POSs_all.values()):
    		print("Warning! Mismatched number of dataset tweets")

    	# Arrays for storage of similarity scores
    	(wordoccurrence_similarity, POSoccurrence_similarity, lenoftweet_similarity, avglenofword_similarity, numhashtags_similarity, 
    		numlinks_similarity, nummentions_similarity) = (np.zeros(no_of_tweets) for _ in range(7))

    	# For each tweet in the dataset (i.e. tweet_data)
    	for i, tweet_data in enumerate(self.tweets_all.values()):
    		
    		# Calculate the number of times words in tweet_new occur in tweet_data
    		occurrences = sum([tweet_data.count(word) for word in tweet_new])
    		wordoccurrence_similarity[i] = occurrences

    		# Calculate how similar their tweet lengths are
    		# A negative exponential is used to map absolute separation, where 0 is most similar, to a similarity score, 
    		#   which ranges between 0 (least similar) and 1 (most similar)
    		lenoftweet_separation = len(tweet_data) - len(tweet_new)
    		lenoftweet_similarity[i] = np.exp(-0.1*abs(lenoftweet_separation))

    		# Calculate how similar their average word lengths are
    		avglenofword_separation = np.mean([len(word) for word in tweet_new]) - np.mean([len(word) for word in tweet_data])
    		avglenofword_similarity[i] = np.exp(-0.1*abs(avglenofword_separation))

    		# Calculate how similar their number of hashtags are
    		numhashtags_separation = sum([1 if word[0] == "#" else 0 for word in tweet_new]) - sum([1 if word[0] == "#" else 0 for word in tweet_data])
    		numhashtags_similarity[i] = np.exp(-0.1*abs(numhashtags_separation))

    		# Calculate how similar their number of links are
    		numlinks_separation = sum([1 if "http" in word else 0 for word in tweet_new]) - sum([1 if "http" in word else 0 for word in tweet_data])
    		numlinks_similarity[i] = np.exp(-0.1*abs(numlinks_separation))

    		# Calculate how similar their number of mentions are
			nummentions_separation = sum([1 if word[0] == "@" else 0 for word in tweet_new]) - sum([1 if word[0] == "@" else 0 for word in tweet_data])
    		nummentions_similarity[i] = np.exp(-0.1*abs(nummentions_separation))

    	for i, tweet_data_POS in enumerate(self.tweets_POSs_all.values()):
    		occurrences = sum([tweet_data_POS.count(word) for word in tweet_new])
    		POSoccurrence_similarity[i] = occurrences

		# Normalize the arrays for word and POS occurrences so all values are between 0 (least similar) and 1 (most similar)
    	wordoccurrence_similarity_norm = np.array([x/max(wordoccurrence_similarity) for x in wordoccurrence_similarity])
		POSoccurrence_similarity_norm = np.array([x/max(POSoccurrence_similarity) for x in POSoccurrence_similarity])
    		
    	return wordoccurrence_similarity_norm, POSoccurrence_similarity_norm, lenoftweet_similarity, avglenofword_similarity, numhashtags_similarity, numlinks_similarity, nummentions_similarity

    def get_k_nearest(self, tweet_new, k=5):

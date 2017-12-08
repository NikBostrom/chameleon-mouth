# Python 3

import util
import numpy as np
from collections import Counter
import pandas as pd

class k_Nearest:
    def __init__(self):

    	'''
		Get all training tweets and their authorship
    	'''
    	(self.text_to_author, self.text_to_wordlist, self.text_to_POSlist, 
    		self.wordfreq, self.POSfreq) = util.getknntrainingtweets()
    	self.all_tweet_texts = list(self.text_to_author.keys())
    	self.no_of_tweets = len(self.text_to_author.keys())

    def all_similarities(self, tweet_new):
    	# Arrays for storage of similarity scores
    	(wordoccurrence_similarities, POSoccurrence_similarities, 
    		lenoftweet_similarities, avglenofword_similarities, 
    		numhashtags_similarities, numlinks_similarities, nummentions_similarities) = (np.zeros(self.no_of_tweets) for _ in range(7))

    	# Convert tweet of interest to a wordlist and a POSlist
    	tweet_words_new = util.tweet_str_to_wordlist(tweet_new)
    	tweet_POSs_new = util.tweet_str_to_POSlist(tweet_new)

    	# Iterate over each tweet in the dataset (i.e. tweet_data)
    	for i, tweet_data_raw in enumerate(self.all_tweet_texts):

    		# Convert tweet in the training set to a wordlist and a POSlist
    		tweet_data = self.text_to_wordlist[tweet_data_raw]
    		tweet_data_POS = self.text_to_POSlist[tweet_data_raw]

    		# Calculate the number of times words in tweet_words_new occur in tweet_data
    		occurrences = sum([min(np.exp(-np.log(0.2*self.wordfreq[word])),1) for word in tweet_words_new if word in tweet_data])
    		wordoccurrence_similarities[i] = occurrences/(len(tweet_data)+len(tweet_words_new))

    		# Calcualte the number of times the same POS in tweet_POSs_new occurs in tweet_data
    		occurrences = sum([min(np.exp(-np.log(0.2*self.POSfreq[word])),1) for word in tweet_POSs_new if word in tweet_data_POS])
    		POSoccurrence_similarities[i] = occurrences/(len(tweet_data_POS) + len(tweet_POSs_new))

    		# Calculate how similar their tweet lengths are
    		# A negative exponential is used to map absolute separation, where 0 is most similar, to a similarity score, 
    		#   which ranges between 0 (least similar) and 1 (most similar)
    		lenoftweet_separation = len(tweet_data_raw) - len(tweet_new)
    		lenoftweet_similarities[i] = np.exp(-0.1*abs(lenoftweet_separation))

    		# Calculate how similar their average word lengths are
    		avglenofword_separation = (np.mean([len(word) for word in tweet_words_new]) 
    								 - np.mean([len(word) for word in tweet_data]))
    		avglenofword_similarities[i] = np.exp(-abs(avglenofword_separation))

    		# Calculate how similar their number of hashtags are
    		numhashtags_separation = (sum([1 for word in tweet_words_new if word[0] == "#"])
    								- sum([1 for word in tweet_data if word[0] == "#"]))
    		numhashtags_similarities[i] = np.exp(-abs(numhashtags_separation))

    		# Calculate how similar their number of links are
    		numlinks_separation = (sum([1 for word in tweet_words_new if "http" in word])
    							 - sum([1 for word in tweet_data if "http" in word]))
    		numlinks_similarities[i] = np.exp(-abs(numlinks_separation))

    		# Calculate how similar their number of mentions are
    		nummentions_separation = (sum([1 for word in tweet_words_new if word[0] == "@"])
    								- sum([1 for word in tweet_data if word[0] == "@"]))
    		nummentions_similarities[i] = np.exp(-abs(nummentions_separation))

    	# Normalize
    	if max(wordoccurrence_similarities) != 0:
    		wordoccurrence_similarities = wordoccurrence_similarities/max(wordoccurrence_similarities)
    	if max(POSoccurrence_similarities) != 0:
    		POSoccurrence_similarities = POSoccurrence_similarities/max(POSoccurrence_similarities)

    	return (wordoccurrence_similarities, POSoccurrence_similarities,
    		lenoftweet_similarities, avglenofword_similarities, 
    		numhashtags_similarities, numlinks_similarities, nummentions_similarities)

    def get_k_nearest(self, tweet_new, k=5):
    	
    	# Get the similarity vectors for each feature of interest
    	similarity_vectors = self.all_similarities(tweet_new)
    	
    	# The weightings of each feature
    	weights = np.array([0.75, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0])
    	
    	# Perform linear combination of feature vectors
    	overall_similarities = np.zeros(self.no_of_tweets)
    	for i in range(len(similarity_vectors)):
    		overall_similarities = overall_similarities + similarity_vectors[i] * weights[i]

    	# Get the indices of the k best tweets
    	ind = np.argpartition(-overall_similarities, k)[:k]

    	# Sort indices with most similar tweets first 
    	ind = sorted(ind, key= lambda x: overall_similarities[x], reverse=True)

    	# Get the text and authorship of the k bext tweets
    	tweets = [self.all_tweet_texts[i] for i in ind]
    	authors = [self.text_to_author[text] for text in tweets]

    	return tweets, authors

    def get_author_prediction(self, tweet, k):
    	_, authors = self.get_k_nearest(tweet, k)

    	# Count the authorship and return most common author
    	authors_count = Counter(authors)
    	most_frequent_author = authors_count.most_common(1)[0][0]

    	# Because there might be ties, we iterate through the counter and
    	# identify any other authors which might also have the maximal
    	# number of tweets, storing them in a list
    	most_frequent_authors = []
    	for author, count in authors_count.items():
    		if authors_count[most_frequent_author] == authors_count[author]:
    			most_frequent_authors.append(author)
    	# print("Most frequent authors: ", most_frequent_authors)

    	# If no tie, simply return the original most common author
    	if len(most_frequent_authors) == 1:
    		return most_frequent_authors[0]

    	# Else if there is a tie, loop through tweets and pick the most similar
    	# tweet that also has most common authorship. Return that author
    	else:
    		for author in authors:
    			if author in most_frequent_authors:
    				return author

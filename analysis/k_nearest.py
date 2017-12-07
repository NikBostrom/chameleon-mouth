# Python 3

import util
import numpy as np
from collections import Counter

class k_Nearest:
    def __init__(self, datafile="all_tweets.csv"):

    	'''
		Get all training tweets and their authorship
    	'''
    	(self.text_to_author, self.text_to_wordlist, self.text_to_POSlist, 
    		self.wordfreq, self.POSfreq) = util.gettweets()
    	self.all_tweet_texts = list(self.text_to_author.keys())
    	# self.tweets_all, self.tweets_POSs_all
    	self.no_of_tweets = len(self.text_to_author.keys())
    	# self.people = self.tweets_all.keys()

    def all_similarities(self, tweet_new):

    	# if len(self.tweets_all.values()) != len(self.tweets_POSs_all.values()):
    	# 	print("Warning! Mismatched number of dataset tweets")

    	# Arrays for storage of similarity scores
    	(wordoccurrence_similarities, POSoccurrence_similarities, 
    		lenoftweet_similarities, avglenofword_similarities, 
    		numhashtags_similarities, numlinks_similarities, nummentions_similarities) = (np.zeros(self.no_of_tweets) for _ in range(7))

    	# Convert tweet of interest to a wordlist and a POSlist
    	tweet_words_new = util.tweet_str_to_wordlist(tweet_new)
    	tweet_POSs_new = util.tweet_str_to_POSlist(tweet_new)

    	# Iterate over each tweet in the dataset (i.e. tweet_data)
    	for i, tweet_data_raw in enumerate(self.all_tweet_texts):
    		
    		# if (i % 1000) == 0:
    		# 	print(i)

    		# Convert tweet in the training set to a wordlist and a POSlist
    		tweet_data = self.text_to_wordlist[tweet_data_raw]
    		tweet_data_POS = self.text_to_POSlist[tweet_data_raw]

    		# if i == 10000:
    		# 	print(tweet_new)
    		# 	print(tweet_words_new)
    		# 	print(tweet_POSs_new)
    		# 	print(tweet_data_raw)
    		# 	print(tweet_data)
    		# 	print(tweet_data_POS)

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
    	wordoccurrence_similarities_norm = wordoccurrence_similarities/max(wordoccurrence_similarities)
    	POSoccurrence_similarities_norm = POSoccurrence_similarities/max(POSoccurrence_similarities)

    	return (wordoccurrence_similarities_norm, POSoccurrence_similarities_norm,
    		lenoftweet_similarities, avglenofword_similarities, 
    		numhashtags_similarities, numlinks_similarities, nummentions_similarities)

    def get_k_nearest(self, tweet_new, k=5):
    	
    	# Get the similarity vectors for each feature of interest
    	similarity_vectors = self.all_similarities(tweet_new)

    	# print(np.shape(similarity_vectors))
    	# print(max(similarity_vectors[0]))
    	
    	# The weightings of each feature
    	weights = np.array([0.5, 0.4, 0.1, 0.0, 0.0, 0.0, 0.0])
    	
    	# Perform linear combination of feature vectors
    	overall_similarities = np.zeros(self.no_of_tweets)
    	for i in range(len(similarity_vectors)):
    		overall_similarities = overall_similarities + similarity_vectors[i] * weights[i]

    	# Get the indices of the k best tweets
    	ind = np.argpartition(-overall_similarities, k)[:k]
    	
    	# for i in ind:
    	# 	print(overall_similarities[i])
    	# 	print(similarity_vectors[0][i])
    	# 	print(similarity_vectors[1][i])
    	# 	print(similarity_vectors[2][i])
    	# 	print(similarity_vectors[3][i])
    	# 	print(similarity_vectors[4][i])
    	# 	print(similarity_vectors[5][i])
    	# 	print(similarity_vectors[6][i])
    	# 	print(" ")


    	# tweets = [self.all_tweet_texts[i] for i in ind]
    	# print(tweets)
    	# print([self.text_to_author[text] for text in tweets])

    	# Sort indices with most similar tweets first 
    	ind = sorted(ind, key= lambda x: overall_similarities[x], reverse=True)

    	# Get the text and authorship of the k bext tweets
    	tweets = [self.all_tweet_texts[i] for i in ind]
    	authors = [self.text_to_author[text] for text in tweets]

    	# Count the authorship and return most common author
    	authors_count = Counter(authors)
    	print(authors_count)
    	most_frequent_author = authors_count.most_common(1)[0][0]
    	print("Most frequent author: ", most_frequent_author)

    	# Because there might be ties, we iterate through the counter and
    	# identify any other authors which might also have the maximal
    	# number of tweets, storing them in a list
    	most_frequent_authors = []
    	for author, count in authors_count.items():
    		if authors_count[most_frequent_author] == authors_count[author]:
    			most_frequent_authors.append(author)
    	print("Most frequent authors: ", most_frequent_authors)

    	# If no tie, simply return the original most common author
    	if len(most_frequent_authors) == 1:
    		return authors, most_frequent_authors[0]

    	# Else if there is a tie, loop through tweets and pick the most similar
    	# tweet that also has most common authorship. Return that author
    	else:
    		for author in authors:
    			if author in most_frequent_authors:
    				return authors, author


a = k_Nearest()
tweet = "Senate leaders' political games are handicapping the Supreme Court and judgeships across the country. http://ofa.bo/2dVVHno? #DoYourJob"
tweet1 = "With the great vote on Cutting Taxes, this could be a big day for the Stock Market - and YOU!"
tweet2 = "Putting Pelosi/Schumer Liberal Puppet Jones into office in Alabama would hurt our great Republican Agenda of low on taxes"
tweet3 = "Crest Velour Hoodie and Sweatpants http://thekidssupply.com "
b = a.get_k_nearest(tweet, k=12)
c = a.get_k_nearest(tweet1, k=12)
d = a.get_k_nearest(tweet2, k=12)
e = a.get_k_nearest(tweet3, k=12)

# 
print(b)
print(c)
print(d)
print(e)

# Python 3

import util
import numpy as np

class k_Nearest:
    def __init__(self, datafile="all_tweets.csv"):
    	self.text_to_author = util.get_text_to_author()
    	self.all_tweet_texts = list(self.text_to_author.keys())
    	# self.tweets_all, self.tweets_POSs_all
    	self.no_of_tweets = len(self.text_to_author.keys())
    	# self.people = self.tweets_all.keys()

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

    	# if len(self.tweets_all.values()) != len(self.tweets_POSs_all.values()):
    	# 	print("Warning! Mismatched number of dataset tweets")

    	# Arrays for storage of similarity scores
    	(wordoccurrence_similarities, POSoccurrence_similarities, 
    		lenoftweet_similarities, avglenofword_similarities, 
    		numhashtags_similarities, numlinks_similarities, nummentions_similarities) = (np.zeros(self.no_of_tweets) for _ in range(7))

    	tweet_words_new = util.tweet_str_to_wordlist(tweet_new)
    	tweet_POSs_new = util.tweet_str_to_POSlist(tweet_new)

    	print("I'm at checkpoint 1!")

    	# Iterate over each tweet in the dataset (i.e. tweet_data)
    	for i, tweet_data_raw in enumerate(self.all_tweet_texts):
    		
    		if (i % 1000) == 0:
    			print(i)

    		tweet_data = util.tweet_str_to_wordlist(tweet_data_raw)
    		tweet_data_POS = util.tweet_str_to_POSlist(tweet_data_raw)

    		# Calculate the number of times words in tweet_words_new occur in tweet_data
    		occurrences = sum([tweet_data.count(word) for word in tweet_words_new])
    		wordoccurrence_similarities[i] = occurrences

    		# Calcualte the number of times the same POS in tweet_POSs_new occurs in tweet_data
    		occurrences = sum([tweet_data_POS.count(word) for word in tweet_POSs_new])
    		POSoccurrence_similarities[i] = occurrences

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
    		numhashtags_separation = (sum([1 if word[0] == "#" else 0 for word in tweet_words_new])
    								- sum([1 if word[0] == "#" else 0 for word in tweet_data]))
    		numhashtags_similarities[i] = np.exp(-abs(numhashtags_separation))

    		# Calculate how similar their number of links are
    		numlinks_separation = (sum([1 if "http" in word else 0 for word in tweet_words_new])
    							 - sum([1 if "http" in word else 0 for word in tweet_data]))
    		numlinks_similarities[i] = np.exp(-abs(numlinks_separation))

    		# Calculate how similar their number of mentions are
    		nummentions_separation = (sum([1 if word[0] == "@" else 0 for word in tweet_words_new])
    								- sum([1 if word[0] == "@" else 0 for word in tweet_data]))
    		nummentions_similarities[i] = np.exp(-abs(nummentions_separation))

    	print(max(wordoccurrence_similarities))

    	wordoccurrence_similarities_norm = wordoccurrence_similarities/max(wordoccurrence_similarities)
    	POSoccurrence_similarities_norm = POSoccurrence_similarities/max(POSoccurrence_similarities)

    	return (wordoccurrence_similarities_norm, POSoccurrence_similarities_norm,
    		lenoftweet_similarities, avglenofword_similarities, 
    		numhashtags_similarities, numlinks_similarities, nummentions_similarities)

    def get_k_nearest(self, tweet_new, k=5):
    	
    	similarity_vectors = self.all_similarities(tweet_new)

    	print(np.shape(similarity_vectors))
    	print(max(similarity_vectors[0]))
    	
    	weights = np.array([0.375, 0.375, 0.05, 0.05, 0.05, 0.05, 0.05])
    	
    	overall_similarities = np.zeros(self.no_of_tweets)

    	for i in range(len(similarity_vectors)):
    		overall_similarities = overall_similarities + similarity_vectors[i] * weights[i]

    	# Get the indices of the k best tweets
    	ind = np.argpartition(-overall_similarities, k)[:k]
    	for i in ind:
    		print(overall_similarities[i])
    		print(similarity_vectors[0][i])
    	print(overall_similarities[ind[0] + 1])
    	tweets = [self.all_tweet_texts[i] for i in ind]
    	authors = [self.text_to_author[text] for text in tweets]

    	return tweets, authors

a = k_Nearest()
tweet = "Senate leaders' political games are handicapping the Supreme Court and judgeships across the country. http://ofa.bo/2dVVHno? #DoYourJob"
b = a.get_k_nearest(tweet, k=5)
# 
print(b)

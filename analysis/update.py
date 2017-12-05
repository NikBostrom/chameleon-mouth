import averages
import misspellings
import os
'''
Run this code if the data sets are updated
'''
a = averages.Average()

a.ave_nwords_per_tweet()
a.ave_word_length()

os.system("python misspellings.py")
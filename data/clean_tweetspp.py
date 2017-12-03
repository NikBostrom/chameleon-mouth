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

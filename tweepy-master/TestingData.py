# This Python file uses the following encoding: utf-8
import os, sys
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import mysql.connector
from mysql.connector import errorcode
import string
import time
import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from hashtags import FindHashTags
from accident import *
import bernoulli
import re
from trainedobj import *
from stringmatching import *

nltk.data.load('tokenizers/punkt/english.pickle')
stop_words = set(stopwords.words("english"))
filtered_tweet = []
hashtags = []

for num in range(1,100):
	tweettxt = raw_input()

	tweet = tweettxt.decode('utf-8').lower()
	# if re.match(r'#?([Aa]ccident)',tweet) is not None:
	tweet = ''.join([x for x in tweet if ord(x) < 128])

	exclude = set('!"$%&\'()*+,-./:;<=>?@[\]^_`{|}~')
	tweet = ''.join(ch for ch in tweet if ch not in exclude)
	hashtags = FindHashTags(tweet)
	tweet = tweet.replace("#","")	
	result = re.sub(r"http\S+", "", tweet)
	words = word_tokenize(result)
	for w in words:
	  if w not in stop_words:
		  filtered_tweet.append(w)
	tweetstr = ' '.join(filtered_tweet)
	if 'accident' in tweet:
		print "Tweet filtered..."
		print(tweetstr)
	
	
	
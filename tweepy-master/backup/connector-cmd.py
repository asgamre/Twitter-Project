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
from nltk.bernoulli import *
import re
from trainedobj import *
from stringmatching import *
import pickle
ckey="rWwXVqiCOYFxCUMIpcgJ2WIm2"
csecret="eHwyTGNvuSCtUkUHf68o23PuVCECxKckYLA5E2k1BrNaqLMxKP"
atoken="1926861750-Wxf4jWK2opPu5nNigottA229f5KeXoLPBW4jXzH"
asecret="OdvnAvPBqu8mrRGy7mKrtvaft1boGWznIDkhiAi0yE9CF"
nltk.data.load('tokenizers/punkt/english.pickle')
stop_words = set(stopwords.words("english"))
filtered_tweet = []
# hashtags = []
tweetduparray = []
words = []

class listener(StreamListener):
	#classifier = None
	#ber_obj = None
	
	def __init__(self):
		print "Training initiated..."
		trainingRequired = False

		if(trainingRequired):
			(self.ber_obj,self.classifier) = trainfunc()
			outfile = open('classifierDumpFile.p', 'wb') 
			pickle.dump((self.ber_obj,self.classifier) , outfile) 
			outfile.close()
			print "TrainingRequired:True"
		else: 
			f1 = open('classifierDumpFile.p') 
			if(f1): 
				(self.ber_obj,self.classifier) = pickle.load(f1) 
				f1.close() 
				print ("Loaded Trained Data")
		print "Training terminated..."
		
	def on_data(self, data):
		# all_data = json.loads(data)
		# list_class=["situational","non-situational"]
		# if 'text' in all_data:
			  # tweet = all_data["text"].encode('utf-8').lower()
			  tweet = raw_input().lower()
			  #if re.match(r'#?([Aa]ccident)',tweet) is not None:
				  # username = all_data["user"]["screen_name"]
				 	
			  tweet = ''.join([x for x in tweet if ord(x) < 128])
			  exclude = set('!"$%&\'()*+,-./:;<=>?@[\]^_`{|}~')
			  tweet = ''.join(ch for ch in tweet if ch not in exclude)
			  tweet = tweet.replace("#","")	
			  result = re.sub(r"http\S+", "", tweet)
			  words = word_tokenize(result)
			  for w in words:
				  if w not in stop_words:
					  filtered_tweet.append(w)
			  if 'accident' in filtered_tweet or 'accidents' in filtered_tweet:
				  for i in filtered_tweet:
					if spellchecker(i) != "~":
						tweetduparray.append(spellchecker(i))
					else:
						tweetduparray.append(i)
				  str = ' '.join(tweetduparray)
				  print str
				  classfunc(str,self.ber_obj,self.classifier)
				  print "Tweet classified..."
							
			  del filtered_tweet[:]
			  del tweetduparray[:]
			  del words[:]
			  str = None
			  return True

	def on_error(self, status):
		print(status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(locations=[72,18,73,20],languages = ["en"], stall_warnings = True)




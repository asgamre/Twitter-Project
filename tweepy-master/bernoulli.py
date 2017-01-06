#bernoulli.py

import nltk
from collections import defaultdict
from nltk.trainedobj import *
import math

class BernoulliNBClassifier:

	#word_list is dictionary.
	def __init__(self,word_list):
		print "BernoulliNBClassifier object initialized."
		self.word_list=word_list
	
	def CountDocsInClass(self,training_set,c):
		count=0
		for i in range(0,len(training_set)):
			if training_set[i][1]==c:
				count+=1
				
		return count		
	
	def CountDocsInClassContainingTerm(self,training_set,c,t):
		count=0
		mod_t="contains("+t+")"
		# print "mod_t "+mod_t
		
		for i in range(0,len(training_set)):
			words = training_set[i][0].keys()
			# print words
			classvar = training_set[i][1]
			#value = training_set[i][0].values()
			for w in range(0,len(words)):
				# print training_set[i][0].get(words[w])
				if classvar == c and words[w] == mod_t and training_set[i][0].get(words[w]) == True:
					count+=1
					break
					
		return count
	
	def maximum(self,score):
		if score["situational"] > score["non-situational"]:
			return "situational"
		return "non-situational"
	
	def train(self,list_class,training_set):
		prior={}
		# tweet="theres thing accident"
		# Vd=tweet.split(" ")
		condprob=defaultdict(dict)
		V=self.word_list
		# print V
		N=len(training_set)
		# print N
		for c in list_class:
			# print "train:"
			# print c
			Nc=self.CountDocsInClass(training_set,c)
			prior[c]=float(Nc)/N
			# print "prior:"
			# print prior[c]
			# print "\n"
			for t in V:
				Nct=self.CountDocsInClassContainingTerm(training_set,c,t)	#error point
				# print "Nct:"
				# print Nct
				# print "\n"
				condprob[t][c]=float((Nct+1))/(Nc+2)
				# if t in Vd:
					# print "condprob["+t+"]["+c+"]"
					# print condprob[t][c]
					# print "\n"
		return TrainedObject(V,prior,condprob)

	def classify(self,list_class,trained_object,test_doc):
		score={}
		print "entering classify..."
		Vd=test_doc.split(" ")
		for c in list_class:
			#print c
			score[c]=(trained_object.prior[c])		#math.log
			for t in trained_object.word_list:				#V
				if t in Vd:			#corrected it!
					# print "pos"
					# print trained_object.condprob[t][c]
					# print "\n"
					score[c] += (trained_object.condprob[t][c])		#math.log
					#print score[c]
				else:
					# print trained_object.condprob[t][c]
					# print "-neg\n"
					score[c] += (1-trained_object.condprob[t][c])	#math.log
			
			
		# print "positive:"	
		# print score["situational"]
		# print "\n"
		# print "negative:"
		# print score["non-situational"]
					
		return 	self.maximum(score)

	def classify_many(self,list_class,trained_object,test_dataset):
		return [self.classify(list_class,trained_object,tds) for tds in test_dataset]
		
	def accuracy(self,list_class,trained_object,test_dataset):
		results = self.classify_many(list_class,trained_object,[tds for (tds, l) in test_dataset])
		correct = [c == r for ((tds, c), r) in zip(test_dataset, results)]
		print correct
		if correct:
			return float(sum(correct)) / len(correct)
		else:
			return 0
		
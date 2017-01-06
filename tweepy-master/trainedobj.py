#trainedobj.py

class TrainedObject:
	
	def __init__(self,word_list, prior, condprob):
		print "TrainedObject initialized."
		self.word_list=word_list
		self.prior=prior
		self.condprob=condprob
		
		
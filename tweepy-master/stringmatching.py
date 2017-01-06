import sys

def spellchecker(location):

	places = [
			['andheri'] ,
			['borivali', 'bandra', 'bkc'],
			[],
			['dadar'],
			[],
			[],
			[],
			[],
			[],
			['jogeshwari', 'jvlr'],
                        [],
                        [],
                        [],
                        [],
                        [],
                        [],
                        [],
                        [],
                        [],
                        [],
                        [],
                        ['vashi','vikhroli'],
                        ['weh'],
                        [],
                        [],
                        []
                        
	]
		
	inputpara = location
	c = list(inputpara)
	index  = ord(c[0])-97 
	for i,val in enumerate(places[index]):
		#temp = list(places[index][i])
		#temp = list(places[index][val])
		temp = list(places[index][i])
			# print temp
		k=0
		count=0
		j=0
			# print len(temp)
		while ( k < len(c) and j < len(temp)):
			if( temp[j] == c[k]):
				count = count+1
				k = k+1
				j = j+1
				#print "if"
			else:
				j = j+1
				#print "else"

		
		if (count==len(c)):
			return places[index][i]
			

	return "~"



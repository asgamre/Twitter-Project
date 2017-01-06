# accident.py
# Twitter sentiment analysis using Python and NLTK
from datetime import datetime	
import nltk
from nltk.bernoulli import *
import mysql.connector
from mysql.connector import errorcode
import time


localtime = time.localtime(time.time())
todaysyear = localtime.tm_year
todaysmonth = localtime.tm_mon
todaysday = localtime.tm_mday
todayshour = localtime.tm_hour
todaysmin = localtime.tm_min
todayssec = localtime.tm_sec

#print tweets
# print to see the result

# test_tweets = [
	# (['#jogeshwari', '#accident'], 'situational'),
	# (['#andheri', '#accident'], 'situational'),
	# (['cat', '#accident'], 'non-situational'),
	# (['goat', 'girl', 'accident'], 'non-situational'),
	# (['#Vikhroli', '#accident'], 'situational')]

# print test_tweets

# The list of word features need to be extracted from the tweets. It is a list with every distinct words
# ordered by frequency of appearance. We use the follow ing function to get the list plus the tw o helper
# functions.
word_features = []
tweets = []
#ber_obj = []
#classifier = None
def get_words_in_tweets(tweets):
	all_words = []
	for (words, sentiment) in tweets:
		all_words.extend(words)
	return all_words
def get_word_features(wordlist):
	wordlist = nltk.FreqDist(wordlist)
	word_features = wordlist.keys()
	#print word_features
	return word_features
# what does word_features do?

# print word_features


# To create a classifier, we need to decide what features are relevant. To do that, we first need a
# feature extractor. The one we are going to use returns a dictionary indicating what words are
# contained in the input passed. Here, the input is the tweet. We use the word features list defined
# above along with the input to create the dictionary.

def extract_features(document):
	document_words = set(document)
	features = {}
	word_features = get_word_features(get_words_in_tweets(tweets))
	for word in word_features:
		features['contains(%s)' % word] = (word in document_words)
	return features
def trainfunc():
	pos_tweets = [('4am brake screech n crash woke me 2autos n scorpio. scorpio humanity tuk ppl 2 hsptl bt 1 atdrvr died accident jogeshwari #unhappymorning', 'situational'),
	('jeeturaaj mirchi983fm mirchimumbai heavy traffic jogeshwari wexp 4 bikers 1homeless man dead accident happened damn', 'situational'),
	('major accident andheri link road casualties reported yet sad', 'situational'),
	('fire andheri accident average saturday night', 'situational'),
	('andheri kurla road airport metro station par huwa accident', 'situational'),
	('fire accident andheri chawl slum area due cylinder blast travel commute likely disrupted', 'situational'),
	('fire accident andheri highrise 1 dead premises safe consult securityindia safety audit', 'situational'),
	('accident andheri last night', 'situational'),
	('called indian turtle accident mumbai andheri news', 'situational'),
	('accident train derails andheri station mumbai casualties injured', 'situational'),
	('last week witnessed accident andheri flyoverrushed bikers aid bad shapeleft leg caught bike tyre', 'situational'),
	('accident andheri flyover localpressco', 'situational'),
	('trafflinemum harbour line andheri running letsomething might happen accident', 'situational'),
	('insane accident andheri east mumbai bus rams shops damaging badly one hurt crash news', 'situational'),
	('best bus overturned andheri flyover accident traffic mumbai', 'situational'),
	('woman killed weekend car crash borivali caraccident majoraccident vehiclecrash accident', 'situational'),
	('borivali main road congested due car accident hopeless traffic', 'situational'),
	('borivali railway accident', 'situational'),
	('borivali western express highway par huwa accident', 'situational'),
	('train accident borivali railway station 2dae eve human amputated half mumbai safe travel', 'situational'),
	('bandra accident mumbai lilmississues sharinbhatti 3 people dead 36 cars motorbike near cbtl nothing tv', 'situational'),
	('lack fire safety precautions routine audits leads accident rbi building bandra mumbai', 'situational'),
	('accident bandra', 'situational'),
	('carterroad bandra midnight drunkdriving accident mumbaimirror mumbaimerijaan mumbai', 'situational'),
	('fire bandra accident weh average saturday night', 'situational'),
	('end road scene gruesome accident bandra mumbai canon 50mm nightcrawling', 'situational'),
	('4am brake screech n crash woke 2autos n scorpio scorpio humanity tuk ppl 2 hsptl bt 1 atdrvr died accident bandra unhappymorning', 'situational'),
	('blood needed lilavati hosp bandra revert back asap call 919454125733 shashwat mumbai urgent blooddonation accident', 'situational'),
	('roadaccident accident mumbai hitandrun hitandrunaccident bandra', 'situational'),
	('2days highlight accident western express highway near bandra hyundai santro kicks bmw x6s butt highway accident bmwvshyundai', 'situational'),
	('say fire bandra political game towers come soon casualty reported bandrafire accident', 'situational'),
	('week accident doubledecker best bus outside bkc policestation crushed two bike riders death scary', 'situational'),
	('soon accident prev sun bkc car 1 stopped red lights best bus 8851 broke signals traffic mumbai', 'situational'),
	('bkc best bus accident costing lives twowe lose little one reckless driving mumbai', 'situational'),
	('dont take lbt flyover u coming vashi bkc bad accident mumbai', 'situational'),
	('major fire bkc fireatbkc accident disaster', 'situational'),
	('shameful rather incencitive part citizens r v really human bkc accident victims could hav save', 'situational'),
	('fire accident dadar result major loss property goods casualties reported', 'situational'),
	('fire personal working get driver accident dadar smartmumbaikar trafflinemum', 'situational'),
	('accident dadar', 'situational'),
	('accident near plaza dadar mumbai caused lot traffic jam idiots plaza cinema dadar', 'situational'),
	('dadar today eyewitness incident woman nd man wer sitting inside bt luckily harm thm accident', 'situational'),
	('accident dadar station person seems either injured dead ppl r shouting gaya ki bacha fucking assholes', 'situational'),
	('need break accident news another accident jogeshwari link road', 'situational'),
	('accident goregoan jogeshwari railway track', 'situational'),
	('jeeturaaj mirchi983fm mirchimumbai heavy traffic jogeshwari wexp 4 bikers 1homeless man dead accident happened damn', 'situational'),
	('inverted truck jogeshwari flyover accident trafficupdate mumbai', 'situational'),
	('accident jogeshwari durganagar m safe', 'situational'),
	('breaking news dumpar ne jogeshwarivikroli link road par 6 vehicles ko udaya 2 logon ki ghatna sthal par hi mout accident', 'situational'),
	('stuck jus b4 jogeshwari station last 20 mins mumbailocal accident', 'situational'),
	('pretty bad accident jogeshwari south bound traffic western express highway hope one critical', 'situational'),
	('dont take lbt flyover u coming vashi youll late accident mumbai', 'situational'),
	('two cars involved brutal accident hill road vashi killerroads', 'situational'),
	('heavy traffic vashi bridge due accident mumbai ridlrmum trafflinemum', 'situational'),
	('bmw 160 kmph jumped divider smashed accident palmbeach vashi navimumbai', 'situational'),
	('accident vashi bridge', 'situational'),
	('truck loaded beer met accident near apmc market vashiyou never see', 'situational'),
	('another palmbeachroad accident vashi', 'situational'),
	('accident palm beach marg vashi navimumbai found', 'situational'),
	('3 back back 4carinline collisions vashi bridge navi mumbai accident hubbrz hubbrz', 'situational'),
	('3 bikes wagonr burnt completely front mango store vashi accident', 'situational'),
	('vikhrolis bridge doom multiple accident since last two months mumbai', 'situational'),
	('scorpio crashed divider near vikhroli railway station many injured accident', 'situational'),
	('trafflinemum accident gandhinagar vikhrolighatkopar road bike hit suv police sight nothin major seems', 'situational'),
	('accident 259 eastern express highway kannamwar nagar ii vikhroli east mumbai maharashtra 400083 india description 3 cars pile', 'situational'),
	('major accident involving 10 vehicles poonam nagar jvlr many casualties avoid road jvlr', 'situational'),
	('jvlr worst accident traffic late', 'situational'),
	('trafflinemum jvlr flyover weh n b slow moving accident opp nesco', 'situational'),
	('smartmumbaikar trafflinemum santro head collision loaded rickshaw eeh near jvlr junction accident cops spot traffucked', 'situational'),
	('accident jvlr westernexpress junction avoid traffic mumbai', 'situational'),
	('jvlr accident mumbai cc wearemumbai traffline', 'situational'),
	('mumbaiaccident jvlr accident avoid jvlr mumbaikars', 'situational'),
	('ok people playing hide n seek cars check pile jvlr accident', 'situational'),
	('heard abt big pile jvlr ursisurs accident please avoid jvlr', 'situational'),
	('accident weh', 'situational'),
	('mad traffic weh mumbai traffic accident morning mumairport', 'situational'),
	('fatal accident weh last night killed biker injured pillion rider mumbaimata trafflinemum', 'situational'),
	('accident western express highway', 'situational'),
	('mumbai bad accident western express highway near santacruz past airport towards bandra traffic going bad car upturned', 'situational'),
	('horrible accident westernexpress highway mumbai today 3 pm photograph mousumiroy', 'situational'),
	('2days highlight accident western express highway near bandra hyundai santro kicks bmw x6s butt highway accident bmwvshyundai', 'situational'),
	('accident aarey flyover western express highway mad traffic two rickshaw squeezed half trucks', 'situational'),
	('accident updatean accident 2 vehicles santacruz western express highway traffic towards andheri slow', 'situational'),
	('pretty bad accident jogeshwari south bound traffic western express highway hope one critical', 'situational'),
	('two parel residents killed fatal accident dadar', 'situational'),
	('two vehicles dadar near plazacinema traffic towards dadar hanuman temple affected mumbai accident', 'situational'),
	('panic situation near dadar sivajipark bus cars accident mumbai bealert', 'situational'),
	('saw horrific accident dadar station n collective effect everyone platform save lifehumanity dead', 'situational'),
	('travellers borivali virar thane doomed right standstill traffic due accident ghodbunderroad avoid gbroad', 'situational'),
	('accident one dead borivali express highway', 'situational'),
	('trafflinemum accident update 1830 hrs accident easternexpresshighway near vikhroli police chowky towards ghatkopar', 'situational'),
	('accident eastern express highway near godrej vikhroli major traffic jam', 'situational'),
	('accident involving vw vento vikhroli flyover south bound eeh traffic building ridlrmum', 'situational'),
	('bike jumped accident prone speed breakerrider hurt kailash business park powai vikhroli link rd pls break speed breaker mcgmbmc', 'situational'),
	('accident vikhroli flyover traffic slow trafflinemum', 'situational'),
	('trafflinemum 1st day oct starts late mark vikhroli accident slow moving traffic', 'situational'),
	('trafflinemum accident took place near dadar flyover take flyovers youre going towards vikhroli', 'situational'),
	('trafflinemum huge traffic eeh vikhroli ghatkopar going towards ghatkopar due accident', 'situational'),
	('trafflinemum smartmumbaikar smooth sclrsmall accident near vikhroli eeh led traffic build', 'situational'),
	('accident four vehicles vikhrolieastern express highway near godrej junction traffic towards bhandup slow', 'situational'),
	('accident car dumper kanjur marg near gandhi nagar junction traffic towards vikhroli is slow', 'situational'),
	('horror story mumbai vikhroli flyover accident', 'situational')]
	
	neg_tweets = [('Do you goat know what to do after a car accident Helpful tips keep safe', 'non-situational'),
			('know car accident helpful tips keep safe', 'non-situational'),
			('goat kicks girl goat girl girls kick tragedy accident troll fail lol lmao rofl sheep india', 'non-situational'),
			('ziuby pune india hongkong productivity accident', 'non-situational'),
			('look cat today accident cats lovethem', 'non-situational'),
			('wishing brendanrogers6 elynn99 speedy recoveries last nights battle brendan required 14 stitches accident', 'non-situational'),
			('wood coal stoves fireplaces chimneys inspected annually prevent accident safetytip', 'non-situational'),
			('smart car smart selfstopping car accident caraccident drivecarefully notexting drivesafely cars', 'non-situational'),
			('robby gordon withdraws 2016 dakar stupid accident', 'non-situational'),
			('slow hard accident', 'non-situational'),
			('norwegian union demands involved rig accident investigation', 'non-situational'),
			('google car first accident', 'non-situational'),
			('theres wall nearby theres 100 im gon na hit head accident prone', 'non-situational'),
			('went area like stepped wasps nest 200 wasps went pants accident prone mylife', 'non-situational'),
			('theres thing accident', 'non-situational'),
			('shocking aldenrichards narrowly escapes car accident', 'non-situational'),
			('song paranoid forever make think catastrophe drive pcb spring break freshman year accident fivegirls', 'non-situational'),
			('traffic accident information via propertycasualty360 stl', 'non-situational'),
			('road safety smartphone help auto accident', 'non-situational'),
			('worker dies falling 53 storeys los angeles building site heightsafety ppe accident construction', 'non-situational'),
			('incredible new discovery designed accident', 'non-situational'),
			('whoah many police ambulance fire engines banstead crossroads banstead accident', 'non-situational'),
			('25 inventions werent meant happen via list25 accident', 'non-situational'),
			('crash accident luck scoop incredible photos accident made news today', 'non-situational'),
			('everything changed accident newlife newme', 'non-situational'),
			('head went lunch realphoto talkinghead accident mysterious creepy invisible', 'non-situational'),
			('man breaking news man beheaded daughter washing accident dontloseyourhead daughterviolence accident', 'non-situational'),
			('thanks heavens okay except material lost black accident thanks friend god', 'non-situational'),
			('writes nice messages make happy badleg love accident pain inpain', 'non-situational'),
			('read workers labor law claim fails since conduct sole cause accident read workers labor law claim fails since conduct sole cause accident', 'non-situational'),
			('discuss accident one senior lawyers free afterhours 4162078200', 'non-situational'),
			('roadrunner coyotes artist unknown streetart art funny car accident', 'non-situational'),
			('note self always file police report get accident parties cant change story afterwards nohonesty', 'non-situational'),
			('young family know important get life back together accident', 'non-situational'),
			('young armenian man involved traffic accident comes coma month', 'non-situational'),
			('protected regardless whether vehicle cause accident', 'non-situational'),
			('listen loud victim neglect driver penske creamed us crosswalk regards accident love life say penske say', 'non-situational'),
			('slipandfall accident lawyer explains injury resulting fall ice snow buffalo', 'non-situational'),
			('travelling europe car ski trip holiday heres event road traffic accident', 'non-situational'),
			('59 million dollars verdicts settlements hughey law firm handles wrongfuldeath accident', 'non-situational'),
			('googles driverless car crashes bus roadsafety driving accident', 'non-situational'),
			('nj state trooper dies hit accident scene', 'non-situational'),
			('big time traffic accident', 'non-situational'),
			('breakingnews thoughts hurt loved ones accident derailment', 'non-situational'),
			('shoutout mom letting know surprise accident', 'non-situational'),
			('liya little accident gymnastics gymnastic gymnast funny gymnasts love fun', 'non-situational'),
			('hurt accident get insurancecoverage call office 302 7771000', 'non-situational'),
			('naked woman dancing big rig holds houston traffic uncategorized accident', 'non-situational'),
			('bmeckie haunting sound every time hear metal metal crunching glass get chill spine drivesafe accident', 'non-situational'),
			('accident toyota camry everyone appeared okay country style chicken waffles', 'non-situational'),
			('first ever google car crash dirty little secret read car accident law', 'non-situational'),
			('gasolinerainbow crazy accident witnessed tweetersteele gasoline rainbow', 'non-situational'),
			('according early reports moving rifle closet another item case shifted hit trigger accident', 'non-situational'),
			('pedestrian injured every 7 minutes us pedestrian accident', 'non-situational'),
			('jay williams motorcycle accident threw away everything', 'non-situational'),
			('suffered accident work call us 0800 731 7555 find make claim compensation', 'non-situational'),
			('eight year old girl dies suffocating balloon kidspotsocial tragic accident', 'non-situational'),
			('make claim even accident caused uninsured driver help contact us', 'non-situational'),
			('smriti irani gets right position lies accident', 'non-situational'),
			('shocking aldenrichards narrowly escapes car accident', 'non-situational'),
			('accident relief rarely available time rather blaming hrd ministers cavalcade need ask rapid accident relief teams', 'non-situational'),
			('bad things happen good people car accident talk senior lawyer 4162078199', 'non-situational'),
			('wait police accident accident crashing', 'non-situational'),
			('spotted accident thanks god everyone safe minor injuries rain slipperyroad', 'non-situational'),
			('dont meet people accident meant cross path reason', 'non-situational'),
			('bathroom floor tiles experienced splash luxurious serum bummed accident periconemd', 'non-situational'),
			('people get accident scene first thing check steal', 'non-situational'),
			('search launched man missing road crash cars crash appeal missing roads dundee fife accident', 'non-situational'),
			('retro follow old oldcar vintage accident car cigarette like4likes followme follow4follow beaverx', 'non-situational'),
			('accident situation someone hurt something damaged without anyone intending happen', 'non-situational'),
			('omg happen accidentally ended knit stitch accident knit', 'non-situational'),
			('knit going like tweet lol accident', 'non-situational'),
			('ambulance fire ambulance fire accident beware', 'non-situational'),
			('one accident small tip avoid accident follow rules', 'non-situational'),
			('ppl cant drive rain traffic accident', 'non-situational'),
			('fall bike cool kids itthey tell promise falling accident', 'non-situational'),
			('someone said words wait work almost started singing accident closeone', 'non-situational'),
			('need help motorcycle accident learn', 'non-situational'),
			('accidents happen shit happensaccident marker explode red shit draw color plop sketch', 'non-situational'),
			('hope youre enjoying weekend get accident take photos gather personal information dont admit fault', 'non-situational'),
			('appears one wheelchairtravelers may accident airportsarefunny', 'non-situational'),
			('new accident injury dhs module available', 'non-situational'),
			('smriti irani oh people dont get serious accident', 'non-situational'),
			('met accident first thing comes mind insured', 'non-situational'),
			('negligence involved dog driver truck accident', 'non-situational'),
			('thankyou lord unending grace life saved protected accident', 'non-situational'),
			('prevent form accident heavyvehicles allahrehamkare', 'non-situational'),
			('never ever trust wheels accident', 'non-situational'),
			('cancersurvivor survived drunkdriving accident changedmylife kid myhero', 'non-situational'),
			('wearing helmet makes feel safer safer accident pollution distraction thankyou hydtraffic 4 enforcing helmetrule', 'non-situational'),
			('soooooo close cars trucks tight close accident alley interesting photooftheday', 'non-situational'),
			('buddy lost tip dumbass finger tip accident dabstache dabstache stachearmy', 'non-situational'),
			('peter liang political scapegoat taking fall white supremacy peterliang accident', 'non-situational'),
			('cant get high today accident', 'non-situational'),
			('ur tweet cryin accident skyeoakesayy', 'non-situational'),
			('werent accident werent mass produced arent assembly line', 'non-situational'),
			('injured cycling accident team help get help deserve 4012260097', 'non-situational'),
			('suffer chronic back pain result car accident accident injury lawyer', 'non-situational'),
			('someone didnt start day well work snow accident prius', 'non-situational'),
			('one seemed think bad idea erecting building covered sloped windows reflecting sun light eyes motorists accident', 'non-situational'),
			('accident photo studio epicfail rofl', 'non-situational')]
	
	#print extract_features
	
	#tweets = []	added as a global variable
	for (words, sentiment) in pos_tweets + neg_tweets:
		words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
		tweets.append((words_filtered, sentiment))
		
	
	#print tweets
	word_features = get_word_features(get_words_in_tweets(tweets))
	#print word_features
	
	training_set = nltk.classify.util.apply_features(extract_features, tweets)
	#print training_set
	# be careful here, it should be nltk.classify.util.apply_features rather than nltk.classify.apply_features
	# apply the features to our classifier using the method apply_features.
	# We pass the feature extractor along with the tweets list defined above.

	# The variable training_set contains the labeled feature sets. It is a list of tuples which each tuple
	# containing the feature dictionary and the sentiment string for each tweet. The sentiment string is 
	# also called label.

	#-------------------------------------------NO CHANGE IN ABOVE CODE------------------------------------------------#

	list_class=["situational","non-situational"]
	#classifier = nltk.NaiveBayesClassifier.train(training_set)
	ber_obj=BernoulliNBClassifier(word_features)
	classifier = ber_obj.train(list_class, training_set)
	print "Classifier Done!"
	#print classifier
	# look inside the classifier train method in the source code of the NLTK library
	return (ber_obj,classifier)

def classfunc(tweet,ber_obj,classifier):
	#print "This is the tweet in class: " + tweet
	#tweet = "andheri cat bat sandra"
	#print "in classfunc"
	#print ber_obj.word_list
	list_class=["situational","non-situational"]
	classlabel = ber_obj.classify(list_class, classifier, tweet)
	tweetwords = tweet.split(" ")
	print classlabel
	if classlabel == "situational":
		cnx = mysql.connector.connect(user='root', password='rambo',
									  host='localhost',
									  database='beproject',
									  charset = 'utf8')
		cursor=cnx.cursor()
		#place = 'goregaon'
		#cursor.execute("INSERT INTO count (AreaName, counter, Timestamp) VALUES (%s,%s,%s)",(place, 5, time.time()))
		cursor.execute("Select AreaName from location")
		data = cursor.fetchall()
		locations = []
		# ts = '2013-01-12 15:27:43'
		# f = '%Y-%m-%d %H:%M:%S'
		for row in data:
			locations.append(row[0])
		# print locations	
		# print tweetwords
		for w in tweetwords:
			for l in locations:
				if w == l:
					
					cursor.execute("INSERT INTO classifiedtweet (Tweet, location) VALUES (%s,%s)",(tweet, l))
					cnx.commit()
					print "Insertion complete.."					
					
					cursor.execute("Select Timestamp from count where AreaName = '%s' " % (l))
					timestamp = cursor.fetchone()
					strtimes=''.join(map(str, timestamp))
					
					strarray = strtimes.split(' ')

					date = strarray[0].split('-')

					year = date[0]
					month = date[1]
					day = date[2]

					time = strarray[1].split(':')
					hour = time[0]
					minutes = time[1]
					secs = time[2]

					flag=0
					if (str(todaysyear) == str(year)):
						
						if (todaysmonth == int(month)):
							
							if(todaysday > int(day)):
								
								flag =1
							else:
								
								flag = -1
						else:
							flag =1
					else:
						flag=1

					if(flag==1):
					   cursor.execute("Update count SET counter=counter+1 where AreaName = '%s' " % (l))
					   cnx.commit()
				#else:
				   #print "Non-Situational"
					
		cursor.close()
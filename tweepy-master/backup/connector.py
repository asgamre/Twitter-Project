from datetime import datetime	
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
import pickle
# ckey="rWwXVqiCOYFxCUMIpcgJ2WIm2"
# csecret="eHwyTGNvuSCtUkUHf68o23PuVCECxKckYLA5E2k1BrNaqLMxKP"
# atoken="1926861750-Wxf4jWK2opPu5nNigottA229f5KeXoLPBW4jXzH"
# asecret="OdvnAvPBqu8mrRGy7mKrtvaft1boGWznIDkhiAi0yE9CF"
ckey="XflayFhqiT3CpTTUy1HlAYKgT"
csecret="nCQnXwgNFR1hCLJ0woc6mDW94Z1O2X9AwOY0yerwrKcHEhj6Zo"
atoken="116456043-BhynBGhHhNhOvGPs1LhzRNYZSsVHo1LhlM6Lzj2y"
asecret="NZBtZbd2isPfSqkB4nFNteJKkFzigW5tZExMoDk6cRaRt"
nltk.data.load('tokenizers/punkt/english.pickle')
stop_words = set(stopwords.words("english"))
filtered_tweet = []
# hashtags = []
tweetduparray = []
words = []

class listener(StreamListener):
		
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
		all_data = json.loads(data)
		list_class=["situational","non-situational"]
		if 'text' in all_data:
				  tweet = all_data["text"].encode('utf-8').lower()	
				  tweet = ''.join([x for x in tweet if ord(x) < 128])
				  exclude = set('!"$%&\'()*+,-./:;<=>?@[\]^_`{|}~')
				  tweet = ''.join(ch for ch in tweet if ch not in exclude)
				  tweet = tweet.replace("#","")	
				  result = re.sub(r"http\S+", "", tweet)
				  words = word_tokenize(result)
				  for w in words:
					  if w not in stop_words:
						  filtered_tweet.append(w)
				  if 'accident' in filtered_tweet:
					  for i in filtered_tweet:
						if spellchecker(i) != "~":
							tweetduparray.append(spellchecker(i))
						else:
							tweetduparray.append(i)
					  str = ' '.join(tweetduparray)
					  classfunc(str,self.ber_obj,self.classifier)
					  print str
					  print "Tweet classified..."
					  test_dataset =  [('major accident bkc link road casualties reported yet sad', 'non-situational'),
								 ('fire  bkc and then accident just average saturday night', 'situational'),
								 ('bkc kurla road airport metro station par huwa accident', 'situational'),
								 ('fire accident  bkc chawl slum area due  cylinder blast travel commute likely   disrupted', 'situational'), 
								 ('fire accident  bkc highrise dead  your premises safe consult security_india for safety audit', 'situational'),
								 ('accident  bkc last night ', 'situational'),
								 ('now that  called  indian turtle accident mumbai bkc news', 'situational'),
								 ('accident train derails  bkc station mumbai   casualties only few injured', 'situational'), 
								 ('last week witnessed  accident  bkc flyoverrushed  the bikers aid  was  bad shapeleft leg caught under the bike tyre', 'situational'),
								 ('accident  bkc flyover ', 'situational'),
								 ('woman killed  weekend car crash bandra caraccident majoraccident vehiclecrash', 'non-situational'),
								 ('bandra main road congested due  car accident hopeless traffic', 'non-situational'),
								 ('bandra railway accident ', 'non-situational'),
								 ('bandra western express highway par huwa accident ', 'non-situational'),
								 ('train accident  bandra railway station 2dae eve  human amputated into half  mumbai safe travel', 'situational'),
								 ('trafflinemum harbour line from bandra running letsomething might happenaccident', 'non-situational'),
								 ('insane accident  bandra east  mumbai bus rams into shops damaging  badly  one hurt crash news', 'situational'),
								 ('best bus overturned  bandra flyover accident traffic mumbai ', 'non-situational'),
								 ('borivali accident mumbai lilmississues sharinbhatti 3 people dead 3/6 cars motorbike near cbtl nothing  tv :(', 'situational'),
								 ('lack  fire safety precautions and routine audits leads  accident  rbi building  borivali mumbai', 'situational'),
								 ('accident  borivali', 'situational'), 
								 ('carterroad borivali midnight drunkdriving accident mumbaimirror mumbaimerijaan mumbai', 'situational'),
								 ('fire  borivali then  accident  the weh just  average saturday night', 'non-situational'),
								 ('end  the road scene   gruesome accident  borivali mumbai canon 50mm nightcrawling ', 'situational'),
								 ('4am brake screech  crash woke  2autos  scorpio scorpio humanity tuk ppl 2 hsptl bt 1 atdrvr died accident borivali unhappymorning', 'situational'),
								 (' blood needed  lilavati hosp borivali revert back asap call   shashwat mumbai urgent blooddonation accident', 'situational'),
								 ('roadaccident accident mumbai hitandrun hitandrunaccident borivali', 'non-situational'),
								 ('2days highlight accident  the western express highway near borivali  hyundai santro kicks  bmw x6\'s butt highway accident bmwvshyundai', 'situational'),
								 (' has been  week  accidents  doubledecker best bus outside andheri policestation crushed two bike riders  death scary!', 'situational'),
								 ('soon after accident  prev sun andheri  car was the only stopped  red lights best bus broke all the signals traffic mumbai', 'situational'),
								 ('after the andheri best bus accident costing lives  twowe lose  little one  reckless driving mumbai', 'situational'),
								 ('dont take lbt flyover   coming from vashi  andheri bad accident mumbai', 'situational'),
								 ('major fire  andheri fireatandheri accident disaster', 'situational'),
								 ('shameful  rather incencitive  our part  citizens r v really human?? andheri accident victims could hav been save ', 'situational'),
								 ('fire accidents  jvlr result  major loss  property and goods  casualties reported', 'non-situational'),
								 ('fire personal working  get the driver out accident jvlr smart_mumbaikar trafflinemum', 'situational'),
								 ('accident  jvlr ', 'situational'),
								 ('accident near plaza jvlr mumbai caused lot  traffic jam idiots  plaza cinema jvlr ', 'non-situational'),
								 (' jvlr today  eyewitness  the incident  woman nd man wer sitting inside bt luckily  harm  thm accident', 'situational'),
								 ('accident  jvlr station  person seems   either injured  dead and ppl r shouting gaya ki bacha fucking assholes!', 'situational'),
								 ('major accident involving over 10 vehicles  poonam nagar dadar many casualties avoid road dadardadar', 'situational'),
								 ('dadar   its worst again accident traffic late', 'non-situational'),
								 ('trafflinemum dadar flyover weh  slow moving accident opp nesco', 'non-situational'),
								 ('smart_mumbaikar trafflinemum eeh accident update traffic slow towards sion towards dadar normal traffic movement', 'situational'),
								 ('smart_mumbaikar trafflinemum santro head  collision with loaded rickshaw  eeh near dadar junction accident cops  spot traffucked', 'situational'),
								 ('accident dadar westernexpress junction avoid traffic mumbai', 'situational'),
								 ('image dadar accident mumbai wearemumbai traffline', 'situational'),
								 ('mumbai_accident dadar accident avoid dadar all mumbaikars', 'situational'), 
								 ('ok people are playing hide  seek under their cars check out the pile up  dadar accident', 'situational'),
								 ('heard abt  big pile up  dadar through ursisurs accident please avoid dadar', 'situational'),
								 ('accident  goregaon weh railway track  ', 'situational'),
								 ('jeeturaaj mirchi983fm mirchimumbai heavy traffic  weh wexp 4 bikers down 1homeless man dead accident happened damn!!!', 'situational'),
								 ('inverted truck  weh flyover accident trafficupdate mumbai', 'situational'),
								 (' accident  weh durganagar  m safe now', 'situational'),
								 ('breaking news :- dumpar weh-vikroli link road par vehicles udaya logon ghatna sthal par mout accident', 'situational'),
								 ('stuck jus weh station for last mins mumbailocal accident', 'non-situational'),
								 ('pretty bad accident  weh  south bound traffic  western express highway  hope  one critical', 'situational'),
								 ('accident  jogeshwari ', 'non-situational'),
								 ('mad traffic jogeshwari mumbai traffic accident morning mumairport ', 'non-situational'),
								 ('trafflinemum flyover jogeshwari  / b slow moving accident opp nesco', 'non-situational'),
								 ('fatal accident  jogeshwari last night killed biker and injured pillion rider mumbai_mata trafflinemum', 'situational'),
								 ('accident  western express highway ', 'non-situational'),
								 ('mumbai bad accident western express highway near santacruz past airport towards borivali traffic going   bad  while car upturned', 'situational'),
								 ('horrible accident  western-express highway mumbai today photograph mousumiroy', 'situational'),
								 ('2days highlight accident  the western express highway near borivali  hyundai santro kicks  bmw x6s butt highway accident bmwvshyundai', 'situational'),
								 ('accident  aarey flyover  western express highway mad traffic two rickshaw squeezed  half by trucks', 'situational'),
								 ('accident updatean accident between vehicles  santacruz western express highway traffic towards andheri  slow', 'situational'),
								 ('pretty bad accident  jogeshwari  south bound traffic  western express highway  hope  one critical', 'situational'),
								 ('this just  vashis bridge  doom multiple accidents since the last two months mumbai ', 'non-situational'),
								 ('scorpio crashed into the divider near vashi railway station many injured  the accident', 'situational'),
								 ('trafflinemum accident  gandhinagar  vashi-ghatkopar road bike hit by suv police  sight nothin major  seems', 'situational'),
								 ('accident  eastern express highway kannamwar nagar ii vashi east mumbai maharashtra  india description cars pile up', 'situational'),
								 ('dont take lbt flyover   coming from vikhroli youll  late accident mumbai', 'situational'),
								 ('two cars involved   brutal accident  hill road vikhroli killerroads', 'situational'),
								 ('heavy traffic  vikhroli bridge due  accident  mumbai ridlrmum trafflinemum', 'situational'),
								 ('bmw  kmph jumped over the divider and smashed accident palmbeach vikhroli navimumbai', 'situational'),
								 ('accident  vikhroli bridge ', 'situational'),
								 (' truck loaded with beer met  accident near apmc market vikhroliyou will never see ', 'situational'),
								 ('another palmbeachroad accident  vikhroli ', 'situational'),
								 ('accident  palm beach marg vikhroli navimumbai found  road', 'situational'), 
								 ('back  back 4-car--line collisions  vikhroli bridge navi mumbai accident hubbrz hubbrz', 'situational'),
								 ('bikes and  wagonr burnt completely  front  mango store vikhroli accident', 'situational'), ('realphoto talkinghead accident mysterious creepy invisible', 'non-situational'),
								 ('incredible new discovery designed  accident', 'non-situational'),
								 ('slipandfall accident lawyer explains  injury resulting equivalent  fall  ice  snow  buffalo ', 'non-situational'),
								 ('slipandfall accident lawyer explains  injury resulting equivalent  fall  ice  snow  buffalo', 'non-situational'),
								 ('discuss your accident   with one  our senior lawyers free afterhour', 'non-situational'),
								 ('by pune india hongkong productivity  accident', 'non-situational'),
								 ('look what  dog did today accident cats lovethem', 'non-situational'),
								 ('wishing ronspeedy recoveries equivalent last nights battle brendan required 14 stitches accident ', 'non-situational'),
								 ('have wood  coal lpg stoves fireplaces chimneys inspected annually  prevent  accident safetytip', 'non-situational'),
								 ('self-stopping car accident caraccident drivecarefully notexting drivesafely cars ', 'non-situational'),
								 ('ronshah withdraws equivalent dakar after stupid accident', 'situational'),
								 ('buckle down its not that hard accident ', 'non-situational'),
								 ('ronunion demands   involved  rig accident investigation ', 'non-situational'), 
								 ('the roncar had its first accident ', 'situational'),
								 (' theres  wall nearby theres  im gonna hit  head   accident prone', 'non-situational'),
								 ('went into  area like that stepped   wasps nest wasps went  pants accident prone mylife  rules', 'non-situational'),
								 ('theres  such thing   ronaccident.', 'non-situational'),
								 ('shocking ron narrowly escapes  car accident', 'situational'),
								 ('the song ronparanoid will forever make  think  our catastrophe   drive down  pcb for spring break freshman year accident fivegirls', 'non-situational'),
								 ('traffic accident information via propertycasualty360 ', 'non-situational'),
								 ('road safety how your smartness can help   auto accident ', 'situational'),
								 ('worker dies after falling storeys  los angeles building site heightsafety ppe accident construction ', 'non-situational'),
								 ('goat kicks  ronronis  girl goat girl girls kick tragedy accident troll fail lol lmao rofl sheep india', 'non-situational'),
								 ('whoah many police ambulance fire  banstead crossroads banstead accident', 'situational'),
								 ('these inventions werent meant  happen via list25 accident', 'non-situational'),
								 ('crash accident scoop incredible  photos  this accident made  news today', 'situational'),
								 ('when everything changed accident newme', 'non-situational'),
								 ('only  head went  lunch realphoto accident mysterious creepy invisible', 'non-situational'),
								 ('man down breaking news beheaded by daughter  washing accident dontloseyourhead daughterviolence accident', 'non-situational'),
								 ('thanks heavens all  except material lost black  accident thanks friend god', 'non-situational'),
								 (' writes nice messages make  happy badleg love accident pain inpain', 'non-situational'),
								 ('read workers labor  claim fails since his conduct was sole cause  accident read workers labor law claim fails since his conduct was sole cause  accident', 'non-situational'),
								 ('roadrunner coyotes after you artist unknown   streetart art funny car accident', 'non-situational'),
								 ('note  self file  police report  you get   accident   other parties cant change their story afterwards nohonesty', 'non-situational'),
								 ('have  family too know how important  get your life back together after  accident ', 'non-situational'),
								 ('young armenian involved  traffic accident comes out  coma after  month ', 'non-situational'),
								 ('are protected regardless  whether  not you  your vehicle were cause accident ', 'non-situational'),
								 ('listen  loud victim neglect driver  crosswalk  regards for accident love for life they ', 'non-situational'), 
								 ('travelling  europe and asia by car for  ski trip  holiday heres what event   road traffic accident ', 'non-situational'),
								 ('over million dollars  verdicts and settlements* hughey law firm handles wrongfuldeath accident ', 'non-situational'),
								 ('googles driverless car crashes  bus   roadsafety driving accident', 'non-situational'),
								 ('state trooper dies after being hit  accident scene', 'non-situational'), 
								 ('big time traffic killing accident', 'non-situational'),
								 ('breakingnews  thoughts are with  hurt and their loved ones accident derailment', 'non-situational'),
								 ('shoutout  mom for letting  know  was  surprise hell yeagh accident', 'non-situational'),
								 ('liya had  little accident gymnastics gymnastic gymnasts love fun', 'non-situational'),
								 ('hurt   accident can  get insurancecoverage fcall our office ', 'non-situational'), 
								 ('woman dancing  big rig holds up houston traffic  uncategorized accident', 'non-situational'),
								('bmeckie its  haunting sound every time  hear metal  metal with crunching glass  get  chill down spine drivesafe accident', 'non-situational'),
								('accident camry everyone appeared   okay  country style chicken and waffles ', 'non-situational'),
								('the first google car crash has  dirty little secret read more   car accident law', 'non-situational'),
								('gasolinerainbow equivalent that crazy accident you witnessed tweetersteele gasoline rainbow ', 'non-situational'),
								('according  early reports she had been moving  rifle  her closet when another item  its case shifted and hit  trigger accident', 'non-situational'),
								('pedestrian  injured every minutes  pedestrian accident', 'non-situational'),
								('jay williams  motorcycle accident  threw away everything ', 'non-situational'),
								('have you suffered  accident  work why not call    find out  you can make  claim for compensation', 'non-situational'),
								('eight year old girl dies after suffocating  balloon  kidspotsocial tragic accident', 'non-situational'),
								('you can make  claim even  your accident was caused by  uninsured driver    can help you contact  now', 'non-situational'),
								('smriti irani gets herself  just  right position when she lies accident ', 'situational'),
								('shocking aldenrichards narrowly escapes  car accident', 'non-situational'),
								('accident relief  rarely available  time rather than blaming hrd ministers cavalcade  need  ask for rapid accident relief teams', 'non-situational'),
								('bad things can happen  good people been   car accident talk   senior lawyer now ', 'non-situational'),
								('wait for police after accident accident crashing', 'non-situational'),
								('spotted accident thanks god everyone  safe minor rain slipperyroad', 'situational'),
								(' dont meet people by accident they are meant  our path for  reason', 'non-situational'),
								(' bathroom floor tiles just exp  splash  luxurious serum bummed accident periconemd', 'non-situational'),
								('when people get   accident scene  first thing they   check what they can steal', 'situational'),
								('search launched for man missing after road crash ://fwto/2rvflqk  cars crash appeal missing roads dundee fife accident', 'non-situational'),
								('retro follow old oldcar vintage accident car cigarette like4likes followme follow4follow by beaver_x', 'non-situational'),
								('accident situation  which someone  hurt  something  damaged without anyone intending   happen', 'non-situational'),
								('tweet has  cryin accident ', 'non-situational'),
								('you werent  accident you werent mass produced you arent  assembly line you were', 'non-situational'),
								('you have injured   cycling accident our team can help you get  help you deserve ', 'non-situational'),
								(' you suffer equivalent chronic back pain   result   car accident accident injury lawyer', 'non-situational'),
								('someone didnt start  day off well work snow accident prius', 'non-situational'),
								(' one seemed  think bad idea before erecting building covered  sloped windows reflecting sun light into  eyes  motorists accident', 'non-situational'),
								('hi hello accient.', 'non-situational'),
								('omg how did that happen accidentally ended up   knit and stitch!! accident knit ', 'non-situational'),
								('how am  going  like  own tweet lol accident', 'non-situational'),
								('ambulance  fire ambulance fire accident beware', 'situational'), 
								('one more accident  small tip  avoid accident follow rules', 'non-situational'),
								('ppl just cant drive   rain traffic accident ', 'non-situational'),
								('someone said  words she can wait    work and  almost started singing accident closeone', 'non-situational'),
								('need help with  motorcycle accident learn more here ', 'non-situational'),
								('accidents happen shit happens!!accident marker explode red shit draw color plop sketch ', 'non-situational'),
								('some negligence involved dog driver truck accident', 'non-situational'),
								('thankyou lord for your unending grace all through  life saved protected accident', 'non-situational'),
								('how you can prevent form the accident with heavyvehicles allahrehamkare ', 'situational'),
								('never ever trust  wheels accident', 'situational'),
								('she   cancersurvivor and  survived  drunkdriving accident that changedmylife this kid  myhero', 'non-situational'),
								('now wearing helmet makes  feel safer safer equivalent accident pollution distraction thank-you hydtraffic 4 enforcing helmetrule', 'non-situational'),
								('soooooo close cars trucks tight close accident alley interesting photooftheday ', 'situational'),
								(' buddy lost his tip dumbass finger tip accident dab_stache dabstache stachearmy', 'non-situational'),
								('peter liang   political scapegoat   taking  fall for white supremacy peterliang accident', 'non-situational'),
								('some cant get high today accident', 'non-situational'),
								('fall off your bike all  cool kids  they tell  promise falling accident ', 'non-situational'),
								('hope that youre enjoying your weekend  you get into  accident take photos gather personal information and dont admit fault', 'non-situational'),
								('appears one   wheelchairtravelers may have had  accident airportsarefunny', 'non-situational'),
								('new accident  injury dhs module now available', 'non-situational'),
								('need  break from all the accident news another accident  weh link road', 'non-situational'),
								('smriti irani people dont get  serious accident', 'non-situational'),
								('indian navy personnel died mumbai submarine blasts confirms defense minister globalannal accidents news','non-situational'),
								('heard terrible accident bandra near amarsons morning bandra traffic accident','non-situational')]
					  print "accuracy:"
					  print self.ber_obj.accuracy(list_class,self.classifier,test_dataset)				
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

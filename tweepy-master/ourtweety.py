from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener


#consumer key, consumer secret, access token, access secret.
ckey="rWwXVqiCOYFxCUMIpcgJ2WIm2"
csecret="eHwyTGNvuSCtUkUHf68o23PuVCECxKckYLA5E2k1BrNaqLMxKP"
atoken="1926861750-Wxf4jWK2opPu5nNigottA229f5KeXoLPBW4jXzH"
asecret="OdvnAvPBqu8mrRGy7mKrtvaft1boGWznIDkhiAi0yE9CF"

class listener(StreamListener):

    def on_data(self, data):
        print(data)
        return(True)

    def on_error(self, status):
        print status

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["accident"])


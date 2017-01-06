def FindHashTags(tweet):
    """
    This function takes the twittersearch output tweet,
    cleans up the text and the format, and returns
    the set of all hashtags in the tweet
    """
    # First get the tweet text
    #tweettxt = tweet['text'].encode('ascii','ignore')
    # People sometimes stack hashtags with no spacing
    # Add spacing before the hashtag symbol
    #tweettxt = tweettxt.replace('#',' #')
    # Clean all punctuation which sometimes 
    # gets cluttered in with the tag
    #for punct in '.!",;:%<>/~`()[]{}?':
    #    tweettxt = tweettxt.replace(punct,'')
    # Split the tweet string into a list of words,
    # some of which will be hashtagged
    # print tweettxt
    tweet = tweet.split()
    # Initiatie list of hashtags
    hashtags = []
    # Loop over the words in the tweet
    for word in tweet:
        # Find words beginning with hashtag
        if word[0]=='#':
            # Lower-case the word
            hashtag = word.lower()
            # Correct for possisives
            hashtag= hashtag.split('\'')[0]         
            # Get rid of the hashtag symbol
            hashtag = hashtag.replace('#','')
            # Make sure there is text left, append to list
            if len(hashtag)>0:
                hashtags.append(hashtag)
    # return clean list of hashtags
    return hashtags

import os
import tweepy as tw
import re
import itertools
import collections
import nltk
from nltk.corpus import stopwords

ACCESS_TOKEN = "1260596484770324480-Y9GAVM0KR7pdctblMhodqJRLcMWV9B"
ACCESS_TOKEN_SECRET = "00GbBIAHRVsjBJP5Fm1xPhCPhvzsa3YskINtJqiCAD75m"
CONSUMER_KEY = "4GjnyVYKsWwECqGuheqCeqMXi"
CONSUMER_SECRET = "44hc9jh2QvSTEZgPPecG5r5VCvDPnQbkaI2nIZBqGCi01JmI2P"

auth = tw.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tw.API(auth, wait_on_rate_limit=True)

search_words = ["coronavirus", "liberty", "autonomy", "freedom"]
date_since = "2020-05-01"


def remove_url(txt):

    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())


tweets = tw.Cursor(api.search,
                   q=search_words ,
                   lang="en",
                   since=date_since,
                   ).items(100)


# list of lists, where each list contains a tweet
all_tweets = [tweet.text for tweet in tweets]

# list of tweets minus urls
all_tweets_no_urls = [remove_url(tweet) for tweet in all_tweets]

# list of lists containing lowercase words in tweet
words_in_tweet = [tweet.lower().split() for tweet in all_tweets_no_urls]

# flattened list containing all words from all tweets
all_words_no_urls = list(itertools.chain(*words_in_tweet))

# counts frequency of each word in all words from tweets
counts_no_urls = collections.Counter(all_words_no_urls)

# creates a list of stop words
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
list(stop_words)

# creates a list of words from tweets without stopwords
all_words_nsw = []
for word in all_words_no_urls:
    if word not in stop_words:
        all_words_nsw.append(word)

# counts frequency of non-stopwords
counts_nsw = collections.Counter(all_words_nsw)
print(counts_nsw.most_common(50))








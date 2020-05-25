import tweepy
import requests
import nltk
from nltk.corpus import stopwords
import json
import re
import pandas as pd
import os

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')

# Fetced the following access token like so.
# curl -u f'{CONSUMER_KEY}:{CONSUMER_SECRET}' --data 'grant_type=client_credentials' 'https://api.twitter.com/oauth2/token'
BEARER__ACCESS_TOKEN=os.environ.get('BEARER__ACCESS_TOKEN')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True)
places = api.geo_search(query="USA",granularity="country")
place_id = places[0].id

# Ignored words, as these occur quite frequently and I am not interested in these
ignoredWords = ['covid19', 'coronavirus', 'covid', 'corona', 'virus', 'i', 'we', 'us', 'get', 'this', 'amp']

# creates a list of stop words, to enhance ignoredWords
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
list(stop_words)

# Should a URL be present in the string, remove it.
def remove_url(txt):
    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())

def printTopWords(wordCountDict):
    s = pd.Series(wordCountDict)
    print(s.nlargest(200))

#Doctionary to keep the word counts
wordCount = {}

dataPayload = {"query": "(corona OR covid OR coronavirus or covid19) place_country:US lang:en",
        "maxResults": "100",
        "fromDate":"202004250000",
        "toDate":"202005062359"}

hasNext = True
while(hasNext):
    r = requests.post('https://api.twitter.com/1.1/tweets/search/30day/prod.json',
                     headers = {"authorization": f"Bearer {BEARER__ACCESS_TOKEN}",
                              "content-type": "application/json"},
                      data = json.dumps(dataPayload))

    # If there is more data to be returned, a 'next' field is returned.
    # See https://developer.twitter.com/en/docs/tweets/search/api-reference/premium-search#pagination
    if ('next' in json.loads(r.text)):
        dataPayload['next'] = json.loads(r.text)['next']
        hasNext = True
    else:
        hasNext = False
    try:
        print(json.loads(r.text))
        results = json.loads(r.text)['results']
        for tweet in results:
            words = []
            if 'extended_tweet' in tweet:
                text = remove_url(tweet['extended_tweet']['full_text'])
            else:
                text = remove_url(tweet['text'])

            print(f"Processing: {text}")
            for word in text.split():
                if word not in stop_words:
                    if word.lower() in ignoredWords:
                        continue
                    # print(f"Interested in:{word}")
                    if word in wordCount:
                        count = wordCount[word]
                        count = count + 1
                        wordCount[word] = count;
                    else:
                        wordCount[word] = 1

    except Exception as e:
        print (f"Caught Exception: {e}")


printTopWords(wordCount)

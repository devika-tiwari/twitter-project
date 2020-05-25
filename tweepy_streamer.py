import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import Cursor
from tweepy import API
import json

import twitter_credentials


class TwitterStreamer:

    # Streams and processes live tweets

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        listener = StdOutListener(fetched_tweets_filename)
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)

        stream = Stream(auth, listener)

        stream.filter(track=hash_tag_list)


class StdOutListener(StreamListener):
    # prints received tweets

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            print(type(data))
            with open(self.fetched_tweets_filename, 'a') as tf:
                jsonObj = json.loads(data)
                if jsonObj['user']['location'] is None:
                    return True
                if (("US" in jsonObj['user']['location']) | ("USA" in jsonObj['user']['location']) | ("US" in jsonObj['user']['location'])):
                    tf.write(f"{jsonObj['text']} LOCATION:{jsonObj['user']['location']}\n")
            return True
        except BaseException as e:
            print("Error on data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)


if __name__ == "__main__":

    hash_tag_list = ['coronavirus', 'covid', 'liberty', 'freedom,' 'rights']
    fetched_tweets_filename = "tweets.json"

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)

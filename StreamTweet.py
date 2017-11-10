
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 10:48:50 2017

@author: darsh
"""

import tweepy
import time
import math
from Tweet import Tweet
from SaveTweets import SaveTweets
from AuthenticateTwitter import AuthenticateTwitter
#import subprocess


class TwitterStreamListener(tweepy.StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    def __init__(self):
        self.count = 0
        self.siesta = 0
        self.nightnight = 0
        super(TwitterStreamListener, self).__init__()

    def on_status(self, status):
        self.count = self.count + 1
        print("Tweets downloaded till now : "+ str(self.count))
        if(self.count<=10000):
            saveTweets.write_into_json(status._json)
            tweet_data.reset_tweet_data()
            saveTweets.get_tweet(status,tweet_data)
            saveTweets.get_user_informations(status,tweet_data)
            saveTweets.write_into_csv(tweet_data)
            return True
        else:
            saveTweets.csvFile.close()
            saveTweets.jsonFile.close()
            self.count = 0
            return False

    # Twitter error list : https://dev.twitter.com/overview/api/response-codes
    
    def on_error(self, status_code):
        if status_code == 403:
            print("The request is understood, but it has been refused or access is not allowed. Limit is maybe reached")
            return False
        elif status_code == 420:
            sleepy = 60 * math.pow(2, self.siesta)
            print (time.strftime("%Y%m%d_%H%M%S"))
            print ("A reconnection attempt will occur in " + str(sleepy/60) + " minutes.")
            print ('''
            *******************************************************************
            From Twitter Streaming API Documentation
            420: Rate Limited
            The client has connected too frequently. For example, an 
            endpoint returns this status if:
            - A client makes too many login attempts in a short period 
              of time.
            - Too many copies of an application attempt to authenticate 
              with the same credentials.
            *******************************************************************
            ''')
            time.sleep(sleepy)
            self.siesta += 1
        else:
            sleepy = 5 * math.pow(2, self.nightnight)
            print (time.strftime("%Y%m%d_%H%M%S"))
            print ("A reconnection attempt will occur in " + \
            str(sleepy) + " seconds.")
            time.sleep(sleepy)
            self.nightnight += 1
        return True

if __name__ == '__main__':

    # Get access and key from another class
    authenticateTwitter = AuthenticateTwitter()
    auth = authenticateTwitter.getAuthObject()
    tweet_data = Tweet()
    batchNo = 1
    saveTweets = SaveTweets(batchNo)
    
    #How long do you want to stream tweets (in seconds)
    #runtime = 60 #this means one minute
    #track=['newyork']
    #-74,40,-73,41 - NY
    #-74.2591,40.4774,-73.7002,40.9176
    #-128.14,29.99,-69.87,48.78 - USA

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=10, retry_delay=5, retry_errors=set([401, 404, 500, 503]))
    streamListener = TwitterStreamListener()         
    myStream = tweepy.Stream(auth=api.auth, listener=streamListener)
    
    while True:
        try:
            myStream.filter(track=['#nurse'],locations=[-74,40,-73,41],languages=['en'],encoding='utf-8')
            saveTweets.batchNo += 1
            saveTweets.csvFile.close()
            saveTweets.jsonFile.close()
            saveTweets.update_object()
        except Exception as e:
            print (e)
            continue
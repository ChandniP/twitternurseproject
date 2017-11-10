# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 09:45:20 2017

@author: darsh
"""
import tweepy

class AuthenticateTwitter():
    
    def __init__(self):
        # Go to http://apps.twitter.com and create an app.
        # The consumer key and secret will be generated for you after
        self.consumer_key ="Kqbrr21dQ8QiCwgtemvcECU1Q"
        self.consumer_secret="IaZKhy4sZkBwO365PLmqDrYAirAT51UtbnnIhXLcpbDI38nB5V"

        # After the step above, you will be redirected to your app's page.
        # Create an access token under the the "Your access token" section
        self.access_token="764997225487462400-n4dk3G0x6WkaK3sTDxHv3OiyznTX5Io"
        self.access_token_secret="1lMgqE3dzk06b87GcgKJySbVptmGZRD0H0suU7ZJiaL33"
        
    def getconsumer_key(self):
        return self.consumer_key
        
    def getconsumer_secret(self):
        return self.consumer_secret
    
    def getaccess_token(self):
        return self.access_token

    def getaccess_token_secret(self):
        return self.access_token_secret
    
    def getAuthObject(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.secure = True
        auth.set_access_token(self.access_token, self.access_token_secret)
        return auth
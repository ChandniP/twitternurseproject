# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 21:54:28 2017

@author: darsh
"""

class Tweet:
    
    def __init__(self):
        self.tweet_id=None
        self.message=None
        self.created_at=None
        self.coordinates=None
        self.language=None
        self.place_id=None
        self.place_type=None
        self.place_name=None
        self.place_full_name=None
        self.country_code=None
        self.place_bounding_box_coordinates=None
        self.place_url=None
        self.media_url=None
        self.media_type=None
        self.user_id=None
        self.user_name=None
        self.user_geo_enabled=None
    
    def reset_tweet_data(self):
        self.tweet_id=None
        self.message=None
        self.created_at=None
        self.coordinates=None
        self.language=None
        self.place_id=None
        self.place_type=None
        self.place_name=None
        self.place_full_name=None
        self.country_code=None
        self.place_bounding_box_coordinates=None
        self.place_url=None
        self.media_url=None
        self.media_type=None
        self.user_id=None
        self.user_name=None
        self.user_geo_enabled=None
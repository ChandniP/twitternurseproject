# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 10:53:36 2017

@author: darsh
"""

import wget
import csv
import json
from urllib.parse  import urlparse
from os.path import splitext, basename
import os
import errno

class SaveTweets():
    def __init__(self,batchNo):
        self.batchNo = batchNo
        self.csvFolderPath = str("/home/centos/Twitter_Streaming/dump/")+str(self.batchNo)+str("/")
        #print(self.csvFolderPath)
        self.make_dir(self.csvFolderPath)
        self.csvFileName = str("streamTweets_") + str(self.batchNo) + str(".csv")
        self.csvFile = open(self.csvFolderPath+self.csvFileName,'w',newline="", encoding="utf-8")
        self.csvWriter = csv.writer(self.csvFile)
        self.csvWriter.writerow(["Tweet_Id","Message","Created_At", "Coordinates","Language","Source" ,"Place_Id","Place_Type" ,"Place_Name", "Place_Full_Name", 
                        "Place_Country_Code", "Place_Coordinates","Place_Url","Media_URL","Media_Type","User_ID","User_Name","User_Screen_Name","User_Geo_Enabled"])
    
        self.jsonFolderPath = str("/home/centos/Twitter_Streaming/dump/")+str(self.batchNo)+str("/")
        #print(self.jsonFolderPath)
        self.jsonFileName = str("streamTweets_") + str(self.batchNo) + str(".json")
        self.jsonFile = open(self.jsonFolderPath+self.jsonFileName, 'w',encoding="utf8")
        
        self.imageFolderPath = str("/home/centos/Twitter_Streaming/dump/") + str(self.batchNo) + str("/") + str("images_") + str(self.batchNo) + str("/")
        self.videoFolderPath = str("/home/centos/Twitter_Streaming/dump/") + str(self.batchNo) + str("/") + str("videos_") + str(self.batchNo) + str("/")
        self.make_dir(self.imageFolderPath)
        self.make_dir(self.videoFolderPath)
    
    def update_object(self):
        self.csvFolderPath = str("/home/centos/Twitter_Streaming/dump/")+str(self.batchNo)+str("/")
        #print(self.csvFolderPath)
        self.make_dir(self.csvFolderPath)
        self.csvFileName = str("streamTweets_") + str(self.batchNo) + str(".csv")
        self.csvFile = open(self.csvFolderPath+self.csvFileName,'w',newline="", encoding="utf-8")
        self.csvWriter = csv.writer(self.csvFile)
        self.csvWriter.writerow(["Tweet_Id","Message","Created_At", "Coordinates","Language","Source" ,"Place_Id","Place_Type" ,"Place_Name", "Place_Full_Name", 
                        "Place_Country_Code", "Place_Coordinates","Place_Url","Media_URL","Media_Type","User_ID","User_Name","User_Screen_Name","User_Geo_Enabled"])
    
        self.jsonFolderPath = str("/home/centos/Twitter_Streaming/dump/")+str(self.batchNo)+str("/")
        #print(self.jsonFolderPath)
        self.jsonFileName = str("streamTweets_") + str(self.batchNo) + str(".json")
        self.jsonFile = open(self.jsonFolderPath+self.jsonFileName, 'w',encoding="utf8")
        
        self.imageFolderPath = str("/home/centos/Twitter_Streaming/dump/") + str(self.batchNo) + str("/") + str("images_") + str(self.batchNo) + str("/")
        self.videoFolderPath = str("/home/centos/Twitter_Streaming/dump/") + str(self.batchNo) + str("/") + str("videos_") + str(self.batchNo) + str("/")
        self.make_dir(self.imageFolderPath)
        self.make_dir(self.videoFolderPath)
    
    def get_jsonFile(self):
        return self.jsonFile
    
    def get_csvFile(self):
        return self.csvWriter
    
    def close_csvFile(self):
        self.csvFile.close()
    
    def close_jsonFile(self):
        self.jsonFile.close()
    
    def download_pictures(self,url,image_name):
        wget.download(url,out=str('./images/')+image_name)
    

    def download_videos(self,url,video_name):
        wget.download(url,out=str('./videos/')+video_name)


    def write_into_csv(self,tweet_data):
    
        self.csvWriter.writerow([tweet_data.tweet_id, tweet_data.message, tweet_data.created_at,tweet_data.coordinates,tweet_data.language,tweet_data.source,
                        tweet_data.place_id,tweet_data.place_type,tweet_data.place_name,tweet_data.place_full_name,tweet_data.country_code,
                        tweet_data.place_bounding_box_coordinates,tweet_data.place_url,tweet_data.media_url,tweet_data.media_type,
                        tweet_data.user_id,tweet_data.user_name,tweet_data.user_screen_name,tweet_data.user_geo_enabled])
        
    def write_into_json(self,json_data):
        json.dump(json_data,self.jsonFile,sort_keys = True,indent = 4)
    
    def get_tweet(self,tweet,tweet_data):
        tweet_data.tweet_id = tweet.id_str
        tweet_data.message = tweet.text
        tweet_data.created_at = tweet.created_at
        tweet_data.coordinates = tweet.coordinates
        tweet_data.language = tweet.lang
        tweet_data.source = tweet.source
        try:
            if hasattr(tweet, 'place'):
                tweet_data.place_id = tweet.place.id
                tweet_data.place_type = tweet.place.place_type
                tweet_data.place_name = tweet.place.name
                tweet_data.place_full_name = tweet.place.full_name
                tweet_data.country_code = tweet.place.country_code
                tweet_data.place_bounding_box_coordinates = tweet.place.bounding_box.coordinates
                tweet_data.place_url = tweet.place.url
        except:
            pass
    
        try:
            if (tweet.entities['media'][0]['type']=='photo'):
                tweet_data.media_url = tweet.extended_entities['media']
                links = []
                number = 0
                for link in tweet_data.media_url:
                    try:
                        number = number + 1
                        links.append(link['media_url'])
                        picture_url = str(link['media_url'])
                        disassembled = urlparse(picture_url)
                        filename, file_ext = splitext(basename(disassembled.path))
                        image_name = str(tweet_data.tweet_id)+'_'+str(number)+str(file_ext)
                        #proc = subprocess.Popen(['python', 'importPictures.py',str(picture_url),str(image_name)])
                        wget.download(picture_url,out=str(self.imageFolderPath)+image_name)
                    except:
                        continue
                tweet_data.media_url = links
                tweet_data.media_type = tweet.extended_entities['media'][0]['type']
        except:
            pass
    
        try:
            if (tweet.extended_entities['media'][0]['type']=='video' or tweet.extended_entities['media'][0]['type']=='animated_gif'):
                tweet_data.media_url = tweet.extended_entities['media'][0]['video_info']['variants']
                for item in tweet_data.media_url:
                    try:
                        if (item['bitrate']):
                            None
                    except KeyError:
                        tweet_data.media_url.remove(item)
                        continue
                maxBitRateItem = max(tweet_data.media_url, key=lambda x:x['bitrate'])
                tweet_data.media_url = maxBitRateItem['url']
                video_url = str(tweet_data.media_url)
                disassembled = urlparse(video_url)
                v_filename, v_file_ext = splitext(basename(disassembled.path))
                video_name = str(tweet_data.tweet_id)+str(v_file_ext)
                #proc = subprocess.Popen(['python', 'importVideos.py',str(video_url),str(video_name)])
                wget.download(video_url,out=str(self.videoFolderPath)+video_name)
                tweet_data.media_type = tweet.extended_entities['media'][0]['type']
        except:
            pass

    def get_user_informations(self,tweet,tweet_data):
        tweet_data.user_id = tweet.user.id
        tweet_data.user_name = tweet.user.name
        tweet_data.user_screen_name = tweet.user.screen_name
        tweet_data.user_geo_enabled = tweet.user.geo_enabled
        
    def make_dir(self,path):
        try:
            os.makedirs(path, exist_ok=True)  # Python>3.2
        except TypeError:
            try:
                os.makedirs(path)
            except OSError as exc: # Python >2.5
                if exc.errno == errno.EEXIST and os.path.isdir(path):
                    pass
                else: raise
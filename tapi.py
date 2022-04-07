import tweepy
import random
import json
import os

#import dotenv to access discord token
from dotenv import load_dotenv

load_dotenv()
BEARER_TOKEN = os.getenv('BEARER_TOKEN')
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_SECRET = os.getenv('ACCESS_SECRET')

#Activate client using given keys and tokens
def getClient():
   client = tweepy.Client(bearer_token=BEARER_TOKEN,
                           consumer_key=CONSUMER_KEY,
                           consumer_secret=CONSUMER_SECRET,
                           access_token=ACCESS_TOKEN,
                           access_token_secret=ACCESS_SECRET)
   
   return client


#Searches for given user name's most recent 5 tweets and returns them as a dictionary
def searchTweets(user_field):
   #Activate client
   client = getClient()
   #Get user from user name
   user = client.get_user(username=user_field, user_fields='profile_image_url')
   #Search for last 5 tweets
   tweets = client.get_users_tweets(id=user.data.id, max_results=5, media_fields=['url', 'preview_image_url'], expansions='attachments.media_keys')
   
   #Get data from tweets
   tweet_data = tweets.data

   #Create list for tweets
   results = []

   #Check for media in tweet list
   if any('media' in keys for keys in tweets.includes):
      media = {m['media_key']: m for m in tweets.includes['media']}

   #Cycle through each tweet and collect tweet id, text, and url for preview image
   if not tweet_data is None and len(tweet_data) > 0:
      for tweet in tweet_data:
         obj = {}
         #Check if there is any media in the tweet
         if any('media' in keys for keys in tweets.includes):
            if any('attachments' in keys for keys in tweet.data):
               attachments = tweet.data['attachments']
               media_keys = attachments['media_keys']
               #If media key is a preview image url, that means it is for a video. If it is just a url, then it is for a picture
               if media[media_keys[0]].preview_image_url:
                  obj['url'] = media[media_keys[0]].preview_image_url
               if media[media_keys[0]].url:
                  obj['url'] = media[media_keys[0]].url
         obj['id'] = tweet.id
         obj['text'] = tweet.text
         obj['len'] = len(tweets.includes)
         obj['pp'] = user.data.profile_image_url
         obj['name'] = user_field
         #obj['url'] = tweet.url
         results.append(obj)
   else:
      return ''
   
   return results

#!/usr/bin/env python

'''

This is my attempt at just some barebones coding for get_comments, which I 
can easily translate into the api.py format. 

The major issues include:

1. Search will only grab the last 1500 replies, or those from the last 7 days, 
   whichever comes first. So realistically, we won't be able to get replies 
   on statuses made >7 days ago. 
2. Rate limits suck. 

For now I just have the code spit out the resulting replies as a sanity check.
In the final code, they'll be sent to map_posts()

'''

import tweepy
from config import twitter_config

auth = tweepy.OAuthHandler(twitter_config.CONSUMER_KEY, twitter_config.CONSUMER_SECRET)
auth.set_access_token(twitter_config.ACCESS_TOKEN, twitter_config.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

'''
realDonaldTrump Jan20 status
crashes on rate limits
also likely would not work because it's >7 days old
'''
#tweet_id = 822502135233384448

# D4D status from Jan31 -- works!
tweet_id = 826646197670641664

status = api.get_status(tweet_id)

name = status.user.screen_name

for item in tweepy.Cursor(api.search, q='@'+name, since_id=tweet_id).items():
    if item.in_reply_to_status_id==tweet_id:
    	print item.text

from __future__ import print_function

import dataset
import twitter
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException 
from selenium.common.exceptions import StaleElementReferenceException

from collect_social.twitter.utils import get_api
import datetime

def chunker(seq, size):
    """
    Taken from:
    http://stackoverflow.com/questions/434287/what-is-the-most-pythonic-way-to-iterate-over-a-list-in-chunks
    """
    return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))

def increment_day(date, i):
    """Increment day object by i days.
    
    Taken from:
    https://github.com/alejandrox1/tweet_authorship/blob/master/Notebook_helperfunctions.py

    Params
    -------
    date : datetime-obj
    i : int
    
    Returns
    -------
    {datetime-obj} next day.
    """
    return date + datetime.timedelta(days=i)

def twitter_url(screen_name, no_rt, start, end):
    """Form url to access tweets via Twitter's search page.

    Taken from: 
    https://github.com/alejandrox1/tweet_authorship/blob/master/Notebook_helperfunctions.py    

    Params
    -------
    screen_name : str
    no_rt : bool
    start : datetime-onj
    end : datetime-obj
    
    Returns
    -------
    {string} search url for twitter
    """
    url1 = 'https://twitter.com/search?f=tweets&q=from%3A'
    url2 = screen_name + '%20since%3A' + start.strftime('%Y-%m-%d') 
    url3 = ''
    if no_rt:
        url3 = '%20until%3A' + end.strftime('%Y-%m-%d') + '%20&src=typd'
    else:
        url3 = '%20until%3A' + end.strftime('%Y-%m-%d') + \
                '%20include%3Aretweets&src=typd'
    
    return url1 + url2 + url3

def get_all_user_tweets(screen_name, start, end, tweet_lim=-1, no_rt=False):
    """
    Adapted from: 
    https://github.com/alejandrox1/tweet_authorship/blob/master/Notebook_helperfunctions.py

    Params
    ------
    screen_name : str
    start : datetime-obj
    end : datetime-obj
    no_rt : bool
    tweet_lim : int {default none / -1}
    
    returns
    -------
    {int} total number of tweet ids obtained
    """
    # Selenium params
    delay = 1  # time to wait on each page load before reading the page
    driver = webdriver.Chrome() 
    
    all_ids = []
    ids_total = 0
    for day in range((end - start).days + 1):
        # Get Twitter search url
        startDate = increment_day(start, 0)
        endDate = increment_day(start, 1)
        url = twitter_url(screen_name, no_rt, startDate, endDate)

        driver.get(url)
        time.sleep(delay)
	
        try:
            found_tweets = \
            driver.find_elements_by_css_selector('li.js-stream-item')
            increment = 10

            # Scroll through the Twitter search page
            while len(found_tweets) >= increment:
                # scroll down for more results
                driver.execute_script(
                    'window.scrollTo(0, document.body.scrollHeight);'
                )
                time.sleep(delay)
                # select tweets
                found_tweets = driver.find_elements_by_css_selector(
                    'li.js-stream-item'
                )
                increment += 10

            # Get the IDs for all Tweets
            for tweet in found_tweets:
            	try:
                	# get tweet id
                        tweet_id = tweet.find_element_by_css_selector(
                            '.time a.tweet-timestamp'
                        ).get_attribute('href').split('/')[-1]
                        all_ids.append(tweet_id)
                        ids_total += 1
                        # break if tweet_lim has been reached                           
                        if ids_total == tweet_lim:                                   
                            return ids_total

                except StaleElementReferenceException as e:
                	print('lost element reference', tweet)
        
        except NoSuchElementException:
            print('no tweets on this day')

        start = increment_day(start, 1)
    
    # Close selenium driver
    driver.close()
    print('{} tweets found total'.format(ids_total))
    return all_ids

def upsert_tweets(db,tweets):
    if not tweets:
        return None

    tweet_table = db['tweet']
    media_table = db['media']
    mention_table = db['mention']
    url_table = db['url']
    hashtag_table = db['hashtag']

    for tweet in tweets:
        for user_mention in tweet.user_mentions:
            um_data = {
                'user_id': tweet.user.id,
                'user_sceen_name': tweet.user.screen_name,
                'tweet_id': tweet.id,
                'mentioned_user_id': user_mention.id,
                'mentioned_userr_screen_name': user_mention.screen_name,
                'mentioned_tweet_id': None,
                'mention_type': 'mention'
            }

            if tweet.retweeted_status is not None and \
                tweet.retweeted_status.user.screen_name == user_mention.screen_name:
                um_data['mention_type'] = 'retweet'
                um_data['mentioned_tweet_id'] =  tweet.retweeted_status.id

            if tweet.in_reply_to_screen_name == user_mention.screen_name:
                um_data['mention_type'] = 'reply'
                um_data['mentioned_tweet_id'] =  tweet.in_reply_to_status_id

            mention_table.upsert(um_data, ['tweet_id','user_id','mentioned_user_id'])

        if tweet.media:
            for media in tweet.media:
                m_data = {
                    'user_id': tweet.user.id,
                    'user_sceen_name': tweet.user.screen_name,
                    'tweet_id': tweet.id,
                    'media_type': media.type,
                    'url': media.media_url 
                }
                media_table.upsert(m_data, ['tweet_id','user_id','url'])

        
        if tweet.hashtags:
            for hashtag in tweet.hashtags:
                h_data = {
                    'user_id': tweet.user.id,
                    'user_sceen_name': tweet.user.screen_name,
                    'tweet_id': tweet.id,
                    'text': hashtag.text,
                }
                hashtag_table.upsert(h_data, ['tweet_id','user_id','text'])


        if tweet.urls:
            for url in tweet.urls:
                u_data = {
                    'user_id': tweet.user.id,
                    'user_sceen_name': tweet.user.screen_name,
                    'tweet_id': tweet.id,
                    'url': url.expanded_url,
                }
                url_table.upsert(u_data, ['tweet_id','user_id','url'])


        tweet_type = 'tweet'
        referenced_tweet_id = None
        if tweet.retweeted_status is not None:
            tweet_type = 'retweet'
            referenced_tweet_id = tweet.retweeted_status.id
        elif tweet.in_reply_to_status_id is not None:
            tweet_type = 'reply'
            referenced_tweet_id = tweet.in_reply_to_status_id 


        t_data = {
            'tweet_id':tweet.id,
            'user_id': tweet.user.id,
            'user_sceen_name': tweet.user.screen_name,
            'tweet_type': tweet_type,
            'referenced_tweet_id': referenced_tweet_id
        }

        if tweet.geo is not None and 'coordinates' in tweet.geo:
            t_data['latitude'] = tweet.geo['coordinates'][0]
            t_data['longitude'] = tweet.geo['coordinates'][1]

        tweet_props = [
            'created_at',
            'favorite_count',
            'favorited',
            'lang',
            'retweet_count',
            'retweeted',
            'source',
            'text'
        ]

        for key in tweet_props:
            t_data[key] = getattr(tweet,key)

        tweet_table.upsert(t_data, ['tweet_id'])      


def run(consumer_key, consumer_secret, access_key, access_secret, 
        connection_string, user_id=None, all_tweets=True):

    db = dataset.connect(connection_string)
    api = get_api(consumer_key, consumer_secret, access_key, access_secret)
    user_table = db['user']

    if not user_id:
        users = user_table.find(tweets_collected=0)
        user_ids = [u['screen_name'] for u in users]
    else:
        user_ids = []

    remaining = len(user_ids)
    for user_id in user_ids:
	print(str(remaining) + ' users to go')
	print(user_id)

        if all_tweets:
            start = datetime.datetime(2016, 1, 1)  
	    end = datetime.datetime.today()
	    
	    tweet_ids = get_all_user_tweets(user_id, start, end)
  	    
	    tweet_groups = chunker(tweet_ids,100)

    	    for group in tweet_groups:
        	temptweets = api.StatusesLookup(group, include_entities=True)
        	upsert_tweets(db,temptweets)

        remaining -= 1

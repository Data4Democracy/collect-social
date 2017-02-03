import tweepy
import dataset
from tweet_model import map_tweet

# unicode mgmt
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# auth & api handlers
def get_api(consumer_key,consumer_secret,access_token,access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)


def setup_tables(db):
    tweet_table = db['tweet']
    tweet_table.create_index(['id_str'])
    tweet_table.create_index(['user_id'])


def setup_db(connection_string):
    db = dataset.connect(connection_string)
    setup_tables(db)
    return db


def upsert_tweets(tweets,db,topics):
    if not tweets:
        return None

    tweet_table = db['tweet']
    
    for tweet in tweets:
        if (not tweet.retweeted) and ('RT @' not in tweet.text):
            tweet_table.upsert(map_tweet(tweet,topics), ["id_str"])        


def run(consumer_key,consumer_secret,access_token,access_token_secret,connection_string,topics,count=100):
    api = get_api(consumer_key,consumer_secret,access_token,access_token_secret)
    search = api.search(q=topics, count=count)
    db = setup_db(connection_string)

    upsert_tweets(search,db,topics)
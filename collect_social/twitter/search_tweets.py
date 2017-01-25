import tweepy
import dataset

# unicode mgmt
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# auth & api handlers
auth = tweepy.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# load topics & build a search
topics = ["alted"]
search = api.search(q=topics, count=100)

def setup_db(connection_string):
    db = sqlite_connect(connection_string)
    setup_sqlite(db)
    return db

def sqlite_connect(connection_string):
    return dataset.connect(connection_string)

def setup_sqlite(db):
    tweet_table = db['tweet']
    media_table = db['media']
    mention_table = db['mention']
    url_table = db['url']
    hashtag_table = db['hashtag']
    user_table = db['user']

    tweet_table.create_index(['tweet_id'])
    media_table.create_index(['tweet_id'])
    mention_table.create_index(['tweet_id'])
    url_table.create_index(['tweet_id'])
    hashtag_table.create_index(['tweet_id'])

    tweet_table.create_index(['user_id'])
    media_table.create_index(['user_id'])
    mention_table.create_index(['user_id'])
    mention_table.create_index(['mentioned_user_id'])
    url_table.create_index(['user_id'])
    hashtag_table.create_index(['user_id'])
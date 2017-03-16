import pytest
import vcr
from collect_social.twitter import utils
from collect_social.twitter import get_tweets


@pytest.fixture
def db():
    """Creates a temporary database in memory"""
    return utils.setup_db('sqlite://')


@pytest.fixture
def api():
    consumer_key = 'fake'
    consumer_secret = 'key'

    access_key = 'and'
    access_secret = 'secret'
    auth_args = [consumer_key, consumer_secret,
                 access_key, access_secret]

    twitter_api = utils.get_api(*auth_args)

    return twitter_api

# TODO whole section is bad/figure out better way
@pytest.fixture
def tweets(api):
    with vcr.use_cassette('./fixtures/test_twitter_get_tweets.yaml', record_mode='none'):
        tweet_list = get_tweets.get_tweets(api, 461594173)
        return tweet_list

@pytest.fixture
def tweet_with_hashtag(tweets):
    for tweet in tweets:
        if tweet.id == 827545241188184065:
            return tweet


@pytest.fixture
def tweet_with_media(tweets):
    for tweet in tweets:
        if tweet.id == 825481027955126272:
            return tweet


@pytest.fixture
def tweet_with_media(tweets):
    for tweet in tweets:
        if tweet.id == 825481027955126272:
            return tweet


@pytest.fixture
def tweet_with_url(tweets):
    for tweet in tweets:
        if tweet.id == 828377877443903488:
            return tweet


@pytest.fixture
def tweet_with_mention(tweets):
    for tweet in tweets:
        if tweet.id == 840186107186802688:
            return tweet

def test_setup_db_tables(db):
    for table in ['user', 'tweet', 'media', 'mention', 'url', 'hashtag']:
        assert table in db


def test_insert_if_missing_new_record(db):
    utils.insert_if_missing(db, ['1', '3', '5'])
    assert db['user'].count() == 3


def test_insert_if_missing_existing_record(db):
    user = dict(user_id=10)
    db['user'].insert(user)

    utils.insert_if_missing(db, ['10'])

    assert db['user'].count() == 1


def test_get_api():
    consumer_key = 'key'
    consumer_secret = 'secret'
    access_key = 'a_key'
    access_secret = 'access_secret'

    test_api = utils.get_api(
        consumer_key, consumer_secret, access_key, access_secret)

    assert test_api._consumer_key == 'key'


def test_set_tweets_gathered(db):
    db['user'].insert(dict(user_id=5, tweets_collected=0))
    result = get_tweets.set_tweets_collected(db, user_id=5)
    assert result == 1


def test_set_tweets_gathered_not_found(db):
    result = get_tweets.set_tweets_collected(db, user_id=113)
    assert result == 0


def test_upsert_tweets(db, tweets):
    get_tweets.upsert_tweets(db, tweets)
    assert db['tweet'].count() == 29


def test_map_hashtag(db, tweet_with_hashtag):
    get_tweets.map_hashtag(db, tweet_with_hashtag)
    record = db['hashtag'].find_one(id=1)

    assert db['hashtag'].count() == 2
    for field  in ['user_id', 'user_sceen_name', 'tweet_id', 'text']:
        assert field in record.keys()


def test_map_media(db, tweet_with_media):
    get_tweets.map_media(db, tweet_with_media)
    record = db['media'].find_one(id=1)

    assert db['media'].count() == 1
    assert record['url'] == 'http://pbs.twimg.com/media/C3Syh9sWIAEd5eL.png'


def test_map_url(db, tweet_with_url):
    get_tweets.map_url(db, tweet_with_url)
    record = db['url'].find_one(id=1)

    assert db['url'].count() == 1
    assert record['url'] == 'http://newknowledge.io/'
    assert len(record) == 5


def test_map_mentions(db, tweet_with_mention):
    get_tweets.map_user_mention(db, tweet_with_mention)
    record = db['mention'].find_one(id=1)

    assert db['mention'].count() == 2
    assert record['mentioned_user_screen_name'] == 'GOLDIE_ice'
    assert len(record) == 8
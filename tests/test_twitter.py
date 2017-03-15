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


@pytest.fixture
def tweets(api):
    with vcr.use_cassette('./fixtures/test_twitter_get_tweets.yaml', record_mode='none'):
        tweet_list = get_tweets.get_tweets(api, 461594173)
        return tweet_list


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

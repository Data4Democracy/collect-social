import pytest
from collect_social.twitter import search_tweets

# Mock tweepy Status Object
class Status:
    def __init__(self,**entries):
        self.__dict__.update(entries)

class User:
    def __init__(self,**entries):
        self.__dict__.update(entries)


@pytest.fixture
def tmp_db_str(tmpdir):
    ''' Creates a temporary database connection string.'''
    return 'sqlite:///{}'.format(tmpdir.join('test.sqlite').strpath)

@pytest.fixture
def db(tmp_db_str):
    ''' Creates a temporary database.'''
    return search_tweets.setup_db(tmp_db_str)

@pytest.fixture
def tweet_status():
    ''' Creates a test tweepy status '''
    tweet_dict = {
        'created_at': '2017-01-30 03:03:01.000000',
        'id_str': '825775143846871041',
        'retweeted': False,
        'retweet_count': 5,
        'text': 'Check out Collect Social, a tool for grabbing posts and comments from Facebook, along with Twitter search data.'
    }

    user_dict = {
        'created_at': '2009-05-18 21:48:17.000000',
        'description': 'Collaborating on data projects to build a stronger society.',
        'followers_count': 500,
	    'friends_count': 1000,
        'id_str': '40977446',
        'location': 'Washington DC',
        'screen_name': 'data4democracy'
    }

    tweet = Status(**tweet_dict)
    tweet.user = (User(**user_dict))
    return tweet

def test_setup_db_tables(db):
    for table in ['tweet']:
        assert table in db

def test_upsert_tweet(db, tweet_status):
    search_tweets.upsert_tweets([tweet_status], db, topics=['data4democracy'])
    assert db['tweet'].find_one(id_str=tweet_status.id_str)['name'] == tweet_status.user.screen_name

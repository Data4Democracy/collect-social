import pytest
from collect_social.twitter.api import map_post, map_user, map_followers


class User:
    def __init__(self, **entries):
        self.__dict__.update(entries)

class Status:
    def __init__(self, **entries):
        self.__dict__.update(entries)

@pytest.fixture
def twitter_user():
    user_dict = {
        'created_at': '2009-05-18 21:48:17.000000',
        'description': 'Collaborating on data projects to build a stronger society.',
        'followers_count': 500,
        'friends_count': 1000,
        'statuses_count': 3,
        'id_str': '40977446',
        'location': 'Washington DC',
        'time_zone': 'UTC',
        'lang': 'en',
        'screen_name': 'data4democracy',
        'name': 'Data For Democracy',
        'verified': False,
        'favourites_count': 0

    }

    user = (User(**user_dict))
    return user

def twitter_status():
    status_dict = {
        'id_str': '40977446',
        'user_id': '78910',
        'text': 'Hello I am a tweet',
        'created_at': '2009-05-18 21:48:17.000000',
        'retweet_count': 5,
        'favorite_count': 50,
    }

    user_dict = {
        'created_at': '2009-05-18 21:48:17.000000',
        'description': 'Collaborating on data projects to build a stronger society.',
        'followers_count': 500,
        'friends_count': 1000,
        'statuses_count': 3,
        'id_str': '40977446',
        'location': 'Washington DC',
        'time_zone': 'UTC',
        'lang': 'en',
        'screen_name': 'data4democracy',
        'name': 'Data For Democracy',
        'verified': False,
        'favourites_count': 0

    }

    
    status = (Status(**status_dict))
    status.user = (User(**user_dict))
    return status

def test_map_post():
    assert map_post(twitter_status())

def test_map_user():
    assert map_user(twitter_user())

def test_map_followers():
    assert map_followers([twitter_user()])

def test_map_users():
    assert map_users([twitter_user()])


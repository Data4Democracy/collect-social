import pytest
from collect_social.twitter.api import map_user, map_users, map_post, map_place, map_posts


class User:
    def __init__(self, **entries):
        self.__dict__.update(entries)


class Status:
    def __init__(self,**entries):
        self.__dict__.update(entries)


class Place:
    def __init__(self,**entries):
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


@pytest.fixture
def tweet_post():
    tweet_dict = {
        'user': twitter_user(),
        'created_at': '2017-01-30 03:03:01.000000',
        'id_str': '825775143846871041',
        'retweeted': False,
        'retweet_count': 5,
        'favorite_count': 5,
        'lang': 'en',
        'coordinates': None,
        'entities': {
            'hashtags': [
                {'text': 'data4democracy'}
            ],
            'user_mentions': [
                {
                    'screen_name': 'realDonaldTrump'
                },
                {
                    'screen_name': 'BarackObama'
                }
            ],
            'urls': [
                {'expanded_url': 'http://www.datafordemocracy.org'}
            ]
        },
        'in_reply_to_screen_name': None,
        'in_reply_to_status_id_str': None,
        'place': None,
        'text': 'Check out Collect Social, a tool for grabbing posts and comments from Facebook, along with Twitter search data.'
    }

    tweet = Status(**tweet_dict)
    return tweet


@pytest.fixture
def twitter_place():
    place_dict = {
        'id': '7238f93a3e899af6',
        'attributes': {
            'street_address': '795 Folsom St',
            '623:id': '210176',
            'twitter': 'twitter'
        },
        'country': 'USA',
        'country_code': 'US',
        'full_name': 'Whereverville, CA',
        'name': 'Whereverville',
        'place_type': 'city',
        'url': 'https://api.twitter.com/1.1/geo/id/7238f93a3e899af6.json'
    }

    place = (Place(**place_dict))
    return place


def test_map_user():
    assert map_user(twitter_user())


def test_map_users():
    assert map_users([twitter_user()])


def test_map_post():
    assert map_post(tweet_post())


def test_map_posts():
    assert map_posts([tweet_post()])


def test_map_place():
    assert map_place(twitter_place())

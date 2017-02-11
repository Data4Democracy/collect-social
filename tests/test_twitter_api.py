import pytest
import datetime
from collect_social.twitter.api import (map_post, map_user, map_users, map_reactions,
        map_reactions_native, check_original_content)


class User:
    def __init__(self, **entries):
        self.__dict__.update(entries)


class Status:
    def __init__(self, **entries):
        self.__dict__.update(entries)


class Tweet:
    def __init__(self, **entries):
        self.__dict__.update(entries)


@pytest.fixture
def twitter_user():
    user_dict = {
        'created_at': datetime.datetime(2017, 1, 1),
        'description': 'Collaborating on data projects to build a stronger society.',
        'profile_image_url': 'http://example.com/file.jpeg',
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
        'favourites_count': 4

    }

    user = (User(**user_dict))
    return user


def twitter_status():
    # TODO need to mock actual twitter status??
    status_dict = {
        'id_str': '40977446',
        'user_id': '78910',
        'text': 'Hello I am a tweet',
        'created_at': '2009-05-18 21:48:17.000000',
        'retweet_count': 5,
        'favorite_count': 50,
        'in_reply_to_user_id': 1337
    }

    user_dict = {
        'created_at': datetime.datetime(2017, 1, 1),
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

@pytest.mark.skip(reason="Working on model for post")
def test_map_post():
    # assert map_post(twitter_status())
    # TODO work on tests for new model
    pass


def test_map_user_base_case():
    user = map_user(twitter_user())
    assert user['user_created'] == '2017-01-01T00:00:00'
    assert user['engagement'] == 7


def test_map_users_base_case():
    users = map_users([twitter_user()])
    assert type(users) == list
    assert users[0]['user_created'] == '2017-01-01T00:00:00'
    assert users[0]['engagement'] == 7


def test_map_reactions():
    reactions = map_reactions(twitter_status())
    assert reactions['pos_sentiment'] == 55


def test_map_reactions_platform_native():
    reactions = map_reactions_native(twitter_status())
    assert reactions['platform'] == 'twitter'


def test_check_original_content_reply():
    original_content = check_original_content(twitter_status())
    assert original_content == ('reply', 1337, None)


@pytest.mark.skip(reason="Solve issue with all tweets having attribute in_reply_to_user_id")
def test_check_original_content_quote():
    pass

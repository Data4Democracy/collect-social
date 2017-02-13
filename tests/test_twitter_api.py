import datetime
import pytest
import vcr
import tweepy
from collect_social.twitter import api


@pytest.fixture
def create_user_response():
    with vcr.use_cassette('tests/fixtures/user_test.yaml'):
        user = api.Twitter().get_user('bstarling_')
    return user


@pytest.fixture
def create_post_response():
    with vcr.use_cassette('tests/fixtures/post_test.yaml'):
        post = api.Twitter().get_post(830798975171174404)
    return post


@pytest.fixture
def create_posts_response():
    with vcr.use_cassette('tests/fixtures/posts_test.yaml'):
        post = api.Twitter().get_posts(461594173)
    return post


@pytest.fixture
def create_reaction_response():
    with vcr.use_cassette('tests/fixtures/post_test.yaml'):
        post = api.Twitter().get_reaction(830798975171174404)
    return post


@pytest.fixture
def create_users_response():
    with vcr.use_cassette('tests/fixtures/users_test.yaml'):
        users = api.Twitter().get_users(['bstarling_', 'hadoopjax', 'X1alejandro3x'])
    return users


@pytest.fixture
def create_following_response():
    with vcr.use_cassette('tests/fixtures/following_test.yaml'):
        following = api.Twitter().get_following('bstarling_')
    return following


@pytest.fixture
def create_followers_response():
    with vcr.use_cassette('tests/fixtures/followers_test.yaml'):
        followers = api.Twitter().get_followers('bstarling_')
    return followers


@pytest.fixture
def create_stream():
    with vcr.use_cassette('tests/fixtures/stream_football_test.yaml'):
        stream = api.Twitter().start_stream(topics=['football'])
    return stream


def test_get_user_base_case():
    user = create_user_response()
    assert user.screen_name == 'bstarling_'
    assert user.created_at == datetime.datetime(2012, 1, 11, 23, 54, 28)


def test_get_post_base_case():
    post = create_post_response()
    assert post.id == 830798975171174404
    assert post.created_at == datetime.datetime(2017, 2, 12, 15, 21, 25)


def test_get_reaction_base_case():
    reaction = create_reaction_response()
    assert reaction == {'favorite_count': 207, 'retweet_count': 129}


def test_get_users_base_case():
    users = create_users_response()
    assert len(users) == 3
    assert users[2].screen_name == 'X1alejandro3x'


def test_get_following_base_case():
    following = create_following_response()
    assert len(following) == 286
    assert type(following[0]) == tweepy.models.User


def test_get_followers_base_case():
    followers = create_followers_response()
    assert len(followers) == 41


def test_get_followers_returns_list_of_tweepy_user():
    followers = create_followers_response()
    assert type(followers) == list
    assert type(followers[0]) == tweepy.models.User


def test_get_posts_base_case():
    posts = create_posts_response()
    assert len(posts) == 216

import datetime
import pytest
import vcr
from collect_social.twitter import api


@pytest.fixture
def create_user_response():
    with vcr.use_cassette('tests/fixtures/usertest.yaml'):
        user = api.Twitter().get_user('bstarling_')
    return user


def test_user_base_case():
    user = create_user_response()
    assert user.screen_name == 'bstarling_'
    assert user.created_at == datetime.datetime(2012, 1, 11, 23, 54, 28)

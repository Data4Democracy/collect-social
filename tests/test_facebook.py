import pytest
from collect_social.facebook import utils
from collect_social.facebook import get_comments

@pytest.fixture
def db():
    """Creates a temporary database in memory"""
    return utils.setup_db('sqlite://')


def test_setup_db_tables(db):
    for table in ['page', 'user', 'post', 'comment', 'interaction']:
        assert table in db


def test_update_user_insert(db):
    user_data = dict(id=451, name='Ray Bradbury')
    utils.update_user(db, user_data)
    assert db['user'].find_one(user_id=user_data['id'])[
        'name'] == user_data['name']


def test_update_user_no_duplicates(db):
    user_data = dict(id=314, name='Pi')
    utils.update_user(db, user_data)
    utils.update_user(db, user_data)
    assert db['user'].count() == 1


def test_update_comment(db):
    post_id = 10
    comment_data = {
        'id': 24,
        'from': {'id': 8, 'name': 'John Doe'}
    }

    get_comments.update_comment(db, comment_data, post_id)
    comment = db['comment'].find_one(comment_id=comment_data['id'])

    assert comment['comment_id'] == comment_data['id']
    assert comment['post_id'] == post_id
    assert comment['author_id'] == comment_data['from']['id']

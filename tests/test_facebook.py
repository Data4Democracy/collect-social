import pytest
from collect_social.facebook import utils

# @pytest.fixture
# def tmp_db_str(tmpdir):
#     ''' Creates a temporary database connection string.'''
#     return 'sqlite:///{}'.format(tmpdir.join('test.sqlite').strpath)

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
    assert db['user'].find_one(user_id=user_data['id'])['name'] == user_data['name']

def test_update_user_no_duplicates(db):
    user_data = dict(id=314, name='Pi')
    utils.update_user(db, user_data)
    utils.update_user(db, user_data)
    assert db['user'].count() == 1

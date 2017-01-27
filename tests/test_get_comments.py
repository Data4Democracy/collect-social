import pytest
from collect_social.facebook import utils
from collect_social.facebook import get_comments


@pytest.fixture
def tmp_db_str(tmpdir):
    # Creates a temporary database connection string.
    return 'sqlite:///{}'.format(tmpdir.join('test.sqlite').strpath)


@pytest.fixture
def db(tmp_db_str):
    # Creates a temporary database.
    return utils.setup_db(tmp_db_str)


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

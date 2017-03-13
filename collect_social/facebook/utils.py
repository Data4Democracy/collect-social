import facepy
import dataset


def update_user(db,user_data):
    users = db['user']
    user = users.find_one(user_id=user_data['id'])

    if not user:
        data = {
            'user_id': user_data['id'],
            'name': user_data['name']
        }
        users.insert(data, ensure=True) 


def setup_db(connection_string):
    db = dataset.connect(connection_string)

    pages = db['page']
    users = db['user']
    posts = db['post']
    comments = db['comment']
    interactions = db['interaction']

    users.create_index(['user_id'])
    posts.create_index(['post_id'])
    comments.create_index(['comment_id'])
    comments.create_index(['post_id'])
    interactions.create_index(['comment_id'])
    interactions.create_index(['post_id'])
    interactions.create_index(['user_id']) 

    return db


def get_api(app_id,app_secret):
    auth_token = facepy.utils.get_application_access_token(app_id, app_secret, api_version='2.6')
    graph = facepy.GraphAPI(auth_token)

    return graph
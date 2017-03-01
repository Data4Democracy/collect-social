from __future__ import print_function
from datetime import datetime
from collect_social.facebook.utils import get_api, setup_db, update_user

import time


def update_post(db,post_data,page_id):
    posts = db['post']
    post = posts.find_one(post_id=post_data['id'])
        
    if not post:
        fields = [
                    'caption',
                    'created_time',
                    'description',
                    'message',
                    'permalink_url',
                    'picture',
                    'link',
                    'type',
                    'story',
                    'status_type'
                ]

        data = {
            'post_id': post_data['id'],
            'page_id': page_id
        }

        author_id = None
        if 'admin_creator' in post_data and 'id' in post_data['admin_creator']:
            data['author_id'] = post_data['admin_creator']['id']
            author_id = data['author_id']
            update_user(db,post_data['admin_creator'])

        if 'from' in post_data and 'id' in post_data['from']:
            data['author_id'] = post_data['from']['id']
            author_id = data['author_id']
            update_user(db,post_data['from'])

        if 'name' in post_data and post_data['name']:
            data['link_name'] = post_data['name']

        if 'to' in post_data:
            for user in post_data['to']:
                update_user(db,user)

        for f in fields:
            if f in post_data:
                data[f] = post_data[f]


        posts.insert(data, ensure=True)  


def get_posts(graph,db,page_id):
    limit = 20

    kwargs = {
        'path': '/'+str(page_id)+'/posts',
        'limit': limit,
        'page': True
    }

    post_data_pages = graph.get(**kwargs)
    for post_data in post_data_pages:
        posts_data = post_data['data']

        for post in posts_data:
            update_post(db,post,page_id)

        print('Updated 100 posts')


def run(app_id,app_secret,connection_string,page_ids):
    db = setup_db(connection_string)
    graph = get_api(app_id,app_secret)

    for page_id in page_ids:
        get_posts(graph,db,page_id)
